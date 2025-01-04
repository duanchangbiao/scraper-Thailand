from flask import jsonify


def success_api(msg: str = "成功", data: dict = None, code: int = 200):
    """ 成功响应 默认值“成功” """
    return jsonify(success=True, msg=msg, data=data, code=code)


def fail_api(msg: str = "失败"):
    """ 失败响应 默认值“失败” """
    return jsonify(success=False, msg=msg)


def table_api(msg: str = "", data=None, size: int = None, code: str = 200, total: int = None, current: int = None):
    """ 动态表格渲染响应 """
    res = {
        'msg': msg,
        'code': code,
        'data': {
            "current": current,
            "total": total,
            "records": data,
            "size": size,
        },
    }
    return jsonify(res)
