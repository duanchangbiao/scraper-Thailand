from app.extensions.init_sqlalchemy import ma


def model_to_dicts(schema: ma.Schema, data):
    """
    :param schema: schema类
    :param model: sqlalchemy查询结果
    :return: 返回单个查询结果
    """
    # 如果是分页器返回，需要传入model.items
    common_schema = schema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = common_schema.dump(data)  # 生成可序列化对象
    return output


def get_Pages(total: int = 0, pageSize: int = 10):
    """
    :param total: 总条数
    :param page: 当前页
    :param pageSize: 每页条数
    :return: 返回分页器
    """
    if total % pageSize == 0:
        total_pages = int(total / pageSize)
    else:
        total_pages = int(total / pageSize) + 1

    return total_pages
