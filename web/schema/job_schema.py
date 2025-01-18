from marshmallow import fields

from web.extensions.init_sqlalchemy import ma


class SysJobSchema(ma.Schema):
    jobId = fields.Int(dump_only=True, attribute='job_id')
    jobName = fields.Str(required=True, attribute='job_name')
    jobGroup = fields.Str(required=True, attribute='job_group')
    jobStatus = fields.Str(required=True, attribute='status')
    invokeTarget = fields.Str(required=True, attribute='invoke_target')
    cronExpression = fields.Str(required=True, attribute='cron_expression')
    misfirePolicy = fields.Str(required=True, attribute='misfire_policy')
    createTime = fields.Str(required=True, attribute='create_time')
