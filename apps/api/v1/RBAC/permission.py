from apps.libs.common.jsonify import jsonify
from apps.libs.common.red_print import Redprint
from apps.models.RBAC import MenuPermission

api = Redprint('permission')


@api.route('/list')
def permission_list():
    menus = MenuPermission.query.filter_by().all()
    result = []
    for menu in menus:
        menu_dict = {
            'id': str(menu.id),
            'name': menu.name,
            'mark': menu.mark,
            'desc': menu.desc,
            'type': 'menu',
            'children': []
        }
        functional = menu.functional_permission
        for item in functional:
            functional_dict = {
                'id': str(menu.id) + '-' + str(item.id),
                'name': item.name,
                'mark': item.mark,
                'desc': item.desc,
                'type': 'functional'
            }
            menu_dict['children'].append(functional_dict)
        result.append(menu_dict)
    return jsonify(result)
