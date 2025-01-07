from app.extensions.init_sqlalchemy import ma


class MenuSchema(ma.Schema):
    id = ma.Integer(dump_only=True, attribute='id')
    menuName = ma.Str(requests=True, attribute='menu_name')
    menuType = ma.Str(requests=True, attribute='menu_type')
    parentId = ma.Integer(requests=True, attribute='parent_id')
    permitName = ma.Str(requests=True, attribute='permit_name')
    remark = ma.Str(attribute='remark')
    routerKey = ma.Str(requests=True, attribute='router_key')
    routerName = ma.Str(requests=True, attribute='router_name')
    routerPath = ma.Str(requests=True, attribute='router_path')
    status = ma.Integer(requests=True, attribute='status')
    icon = ma.Str(requests=True, attribute='icon')
    iconType = ma.Str(requests=True, attribute='icon_type')
    component = ma.Str(requests=True, attribute='component')
    order = ma.Integer(requests=True, attribute='order')
    ctime = ma.DateTime(attribute='ctime')
    mtime = ma.DateTime(attribute='mtime')

    class Meta:
        fields = (
            'id', 'menuName', 'menuType', 'parentId', 'permitName', 'remark', 'routerKey', 'routerName', 'routerPath',
            'status', 'icon', 'iconType', 'component', 'order', 'ctime', 'mtime')


class ButtonSchema(ma.Schema):
    id = ma.Integer(dump_only=True, attribute='id')
    title = ma.Str(attribute='menu_name')
    code = ma.Str(attribute='permit_name')
    routeName = ma.Str(attribute='router_key')
