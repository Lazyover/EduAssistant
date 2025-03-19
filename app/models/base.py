from playhouse.postgres_ext import PostgresqlExtDatabase, Model
from peewee import *
import datetime

# 创建数据库实例
db = PostgresqlExtDatabase(None)

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    
    class Meta:
        database = db
