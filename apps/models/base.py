import datetime
from contextlib import contextmanager
from sqlalchemy import Column, SmallInteger, Integer
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery

from apps.exception.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(SmallInteger, default=1, comment="状态码：0 未激活，1 已激活")
    create_time = Column(Integer, comment="创建时间，时间戳")
    update_time = Column(Integer, comment="更新时间，时间戳")

    def __init__(self):
        if self.create_time == "" or self.create_time is None:
            self.create_time = int(datetime.datetime.now().timestamp())
        if self.update_time == "" or self.update_time is None:
            self.update_time = int(datetime.datetime.now().timestamp())

    def keys(self):
        return self.fields

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_time_format(self):
        if not self.create_time:
            return None
        init_datetime = datetime.datetime.fromtimestamp(self.create_time)
        return init_datetime.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def update_time_format(self):
        if not self.update_time:
            return None
        init_datetime = datetime.datetime.fromtimestamp(self.update_time)
        return init_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def hide(self, *args):
        for key in args:
            self.fields.remove(key)
        return self

    def append(self, *args):
        for key in args:
            self.fields.append(key)
        return self
