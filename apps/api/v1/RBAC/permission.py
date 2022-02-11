from apps.libs.common.jsonify import jsonify
from apps.libs.common.red_print import Redprint
from apps.models.RBAC import MenuPermissions

api = Redprint('permission')


@api.route('/list')
def permission_list():
    menus = MenuPermissions.query.filter_by().all()
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
        functionals = menu.functional_permissions
        for functional in functionals:
            functional_dict = {
                'id': str(menu.id) + '-' + str(functional.id),
                'name': functional.name,
                'mark': functional.mark,
                'desc': functional.desc,
                'type': 'functional'
            }
            menu_dict['children'].append(functional_dict)
        result.append(menu_dict)
    return jsonify(result)
