from sqlalchemy import Column, String, SmallInteger, Integer, orm, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from apps.exception.error_code import AuthFailed
from apps.models.base import Base


class User(Base):
    """
    用户表
    """
    account = Column(String(50), nullable=False, comment='邮箱类型账号')
    _password = Column("password", String(150), nullable=False, comment='密码')
    nickname = Column(String(20), nullable=False, comment='昵称')
    telephone_number = Column(String(11), nullable=False, comment="手机号码")
    desc = Column(String(100), comment='描述')
    enable = Column(SmallInteger, default=1, comment="是否启用,0:未启用,1: 启用")
    last_login = Column(Integer, comment="最后登录时间")
    role_id = Column(Integer, ForeignKey('role.id'), comment='角色ID')
    role = relationship('Role', backref='users')

    @orm.reconstructor
    def __init__(self):
        super().__init__()
        self.fields = [
            "id",
            "account",
            "nickname",
            "desc",
            "enable",
            "telephone_number",
        ]

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    @staticmethod
    def verity(account, password):
        user = User.query.filter_by(account=account).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        elif user.enable == 0:
            raise AuthFailed(msg='账户未启动，请联系管理员')
        return {'uid': user.id}


class Role(Base):
    """
    角色表
    """
    name = Column(String(50), nullable=False, comment='名称')
    desc = Column(String(100), nullable=False, comment='描述')

    @orm.reconstructor
    def __init__(self):
        super().__init__()
        self.fields = [
            "id",
            "name",
            "desc",
        ]


class MenuPermission(Base):
    """
    菜单权限表
    """
    name = Column(String(50), nullable=False, comment='名称')
    mark = Column(String(50), nullable=False, comment='标识')
    desc = Column(String(100), nullable=False, comment='描述')

    @orm.reconstructor
    def __init__(self):
        super().__init__()
        self.fields = [
            "id",
            "name",
            "mark",
            "desc",
        ]


class FunctionalPermission(Base):
    """
    功能权限表
    """
    name = Column(String(50), nullable=False, comment='名称')
    mark = Column(String(50), nullable=False, comment='标识')
    desc = Column(String(100), nullable=False, comment='描述')
    menu_permission_id = Column(Integer, ForeignKey('menu_permission.id'), comment='菜单权限ID')
    menu_permission = relationship('MenuPermission', backref='functional_permission')

    @orm.reconstructor
    def __init__(self):
        super().__init__()
        self.fields = [
            "id",
            "name",
            "mark",
            "desc",
        ]


class RoleToPermission(Base):
    """角色权限表"""
    role_id = Column(Integer, ForeignKey('roles.id'), comment='角色ID')
    permission_list = Column(String(200), comment='权限ID列表')

    @orm.reconstructor
    def __init__(self):
        super().__init__()
        self.fields = [
            "id",
            "role_id",
            "permission_list"
        ]
