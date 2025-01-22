import time
from datetime import datetime

from croniter import croniter
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from web.common import curd
from web.extensions import db
from web.models.models import SysJobLog, SysJob
from web.route import scheduler
from web.schema.job_schema import SysJobSchema, SysJobLogSchema
from web.utils.response import  table_api

app_router = Blueprint('job', __name__, url_prefix='/job')


def after_task_log(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        run_ms = (time.time() - start_time) / 60
        from app import app
        with app.app_context():
            sysJobLog = SysJobLog()
            sysJobLog.job_name = args[0]['jobName']
            sysJobLog.job_group = args[0]['jobGroup']
            sysJobLog.invoke_target = args[0]['invokeTarget']
            sysJobLog.job_message = f"{args[0]['jobName']} 总共耗时：{run_ms}分钟"
            sysJobLog.status = '0' if result['code'] else '1'
            if not result['code']:
                sysJobLog.exception_info = result['msg']
            db.session.add(sysJobLog)
            db.session.commit()
        return result

    return wrapper


@after_task_log
def execute_task(job):
    try:
        target_module, target_function, args = get_target_function_and_args(job['invokeTarget'].strip())
        module = __import__('web.task.' + target_module, fromlist=[target_function])
        function = getattr(module, target_function)
        function(args) if len(args) > 0 else function()
        print(target_function, args, target_module)
        return {"code": True, "msg": "执行成功"}
    except Exception as e:
        print(f"执行任务 {job['jobId']} 时出错: {e}")
        return {"code": False, "msg": str(e)}


def createScheduleJob(job):
    job_id = f"{job['jobId']}_{job['jobName']}"
    specific_job = scheduler.get_job(job_id)
    print(specific_job)
    if specific_job:
        scheduler.remove_job(job_id)
    # misfirePolicy 计划执行错误策略（1立即执行 2执行一次 3放弃执行）
    if job['status'] == '0' and job['misfirePolicy'] == '1':
        add_job(job)
    elif job['misfirePolicy'] == '2':
        execute_task(job)


def add_job(job):
    scheduler.add_job(execute_task, 'cron', args=(job,), second=job['cronExpression'].split(' ')[0],
                      minute=job['cronExpression'].split(' ')[1], hour=job['cronExpression'].split(' ')[2],
                      day=job['cronExpression'].split(' ')[3].replace("?", "*"),
                      month=job['cronExpression'].split(' ')[4],
                      day_of_week=job['cronExpression'].split(' ')[5].replace("?", "*"),
                      id=f"{job['jobId']}_{job['jobName']}",
                      misfire_grace_time=30, replace_existing=(False if job['concurrent'] == '0' else True))


def get_target_function_and_args(function_path_str):
    args = []
    parts = []
    if function_path_str.find('(') > 0:
        function_part, args_part = function_path_str.split('(', 1)
        parts = function_part.split('.')
        args_list = args_part.rstrip(')').split(',')
        for arg in args_list:
            if arg.strip() == 'true':
                args.append(True)
            elif arg.strip() == 'false':
                args.append(False)
            else:
                args.append(eval(arg.strip().replace('L', '').replace('D', '')))
    else:
        parts = function_path_str.split('.')
    parts.append(args)
    return parts


def next_execution_time(cron_expression):
    base_time = datetime.now()
    cron = croniter(cron_expression, base_time)
    return cron.get_next(datetime)


def deleteScheduleJob(job):
    job_id = f"{job['jobId']}_{job['jobName']}"
    specific_job = scheduler.get_job(job_id)
    if specific_job:
        scheduler.remove_job(job_id)


@app_router.route('/list', methods=['GET'])
@jwt_required()
def sysjob_list():
    filters = []
    if request.args.get('jobName'):
        filters.append(SysJob.job_name.like('%' + request.args.get('jobName') + '%'))
    if request.args.get('jobGroup'):
        filters.append(SysJob.job_group == request.args.get('jobGroup'))
    if request.args.get('status'):
        filters.append(SysJob.status == request.args.get('status'))
    page = request.args.get('current', 1, type=int)
    size = request.args.get('size', 10, type=int)
    sysJob = SysJob.query.filter(*filters).order_by(SysJob.create_time).paginates(page=page, pageSize=size)
    count = sysJob.total
    data = curd.model_to_dicts(schema=SysJobSchema, data=sysJob.items)
    return table_api(data=data, total=count, current=page, size=size, msg="查询成功")


@app_router.route('/add', methods=['POST'])
@jwt_required()
def sysjob_add():
    sysjob = SysJob()
    if 'jobName' in request.json: sysjob.job_name = request.json['jobName']
    if 'jobGroup' in request.json: sysjob.job_group = request.json['jobGroup']
    if 'invokeTarget' in request.json: sysjob.invoke_target = request.json['invokeTarget']
    if 'cronExpression' in request.json: sysjob.cron_expression = request.json['cronExpression']
    if 'misfirePolicy' in request.json: sysjob.misfire_policy = request.json['misfirePolicy']
    if 'concurrent' in request.json: sysjob.concurrent = request.json['concurrent']
    if 'status' in request.json: sysjob.status = request.json['status']
    db.session.add(sysjob)
    db.session.commit()
    job_id = sysjob.job_id
    createScheduleJob(sysjob.to_json())
    return jsonify({'code': 200, 'msg': '操作成功'})


@app_router.route('/update', methods=['PUT'])
@jwt_required()
def sysjob_update():
    sysjob = SysJob.query.get(request.json['jobId'])
    if 'jobName' in request.json: sysjob.job_name = request.json['jobName']
    if 'jobGroup' in request.json: sysjob.job_group = request.json['jobGroup']
    if 'invokeTarget' in request.json: sysjob.invoke_target = request.json['invokeTarget']
    if 'cronExpression' in request.json: sysjob.cron_expression = request.json['cronExpression']
    if 'misfirePolicy' in request.json: sysjob.misfire_policy = request.json['misfirePolicy']
    if 'concurrent' in request.json: sysjob.concurrent = request.json['concurrent']
    if 'status' in request.json: sysjob.status = request.json['status']
    db.session.add(sysjob)
    createScheduleJob(sysjob.to_json())
    return jsonify({'code': 200, 'msg': '操作成功'})


@app_router.route('/run', methods=['get'])
@jwt_required()
def sysjob_run():
    sysjob = SysJob.query.get(request.args.get('jobId'))
    res = execute_task(sysjob.to_json())
    if res['code']:
        return jsonify({'code': 200, 'msg': '执行成功'})
    return jsonify({'code': 500, 'msg': f"执行任务 {request.json['jobId']} 时出错:{res['msg']}"})


@app_router.route('/delete/<string:ids>', methods=['DELETE'])
@jwt_required()
def sysjob_delete(ids):
    idList = ids.split(',')
    for id in idList:
        sysjob = SysJob.query.get(id)
        if sysjob:
            db.session.delete(sysjob)
            deleteScheduleJob(sysjob.to_json())

    return jsonify({'code': 200, 'msg': '操作成功'})


@app_router.route('/changeStatus', methods=['PUT'])
@jwt_required()
def sysjob_status_update():
    sysjob = SysJob.query.get(request.json['jobId'])
    if 'status' in request.json: sysjob.status = request.json['status']
    db.session.add(sysjob)
    createScheduleJob(sysjob.to_json())
    return jsonify({'code': 200, 'msg': '操作成功'})


@app_router.route('/getById/<string:id>', methods=['GET'])
@jwt_required()
def sysjob_getById(id):
    sysjob = SysJob.query.get(id)
    if sysjob:
        data = sysjob.to_json()
        try:
            data['nextValidTime'] = next_execution_time(sysjob.cron_expression.replace('?', '*'))
        except Exception as e:
            data['nextValidTime'] = ''
        return jsonify({'code': 200, 'msg': '操作成功', 'data': data})
    else:
        return jsonify({'code': 500, 'msg': 'error'})


@app_router.route('/jobLog/list', methods=['GET'])
@jwt_required()
def sysjobLog_list():
    filters = []
    if request.args.get('jobName'):
        filters.append(SysJobLog.job_name.like('%' + request.args.get('jobName') + '%'))
    if request.args.get('jobGroup'):
        filters.append(SysJobLog.job_group == request.args.get('jobGroup'))
    if request.args.get('status'):
        filters.append(SysJobLog.status == request.args.get('status'))
    if 'params[beginTime]' in request.args and 'params[endTime]' in request.args:
        filters.append(SysJobLog.create_time > request.args['params[beginTime]'])
        filters.append(SysJobLog.create_time < request.args['params[endTime]'])
    current = request.args.get('current', 1, type=int)
    size = request.args.get('size', 10, type=int)
    pagination = SysJobLog.query.filter(*filters).order_by(SysJobLog.create_time.desc()).paginates(page=current,
                                                                                                   pageSize=size)
    return table_api(data=curd.model_to_dicts(schema=SysJobLogSchema, data=pagination.items), total=pagination.total,
                     current=current, size=size)


@app_router.route('/jobLog/<string:ids>', methods=['DELETE'])
@jwt_required()
def sysjoblog_delete(ids):
    idList = ids.split(',')
    for id in idList:
        sysjoblog = SysJobLog.query.get(id)
        if sysjoblog:
            db.session.delete(sysjoblog)
    return jsonify({'code': 200, 'msg': '操作成功'})


@app_router.route('/jobLog/clean', methods=['DELETE'])
@jwt_required()
def sysjoblog_clean():
    return jsonify({'code': 500, 'msg': '不支持清空'})
