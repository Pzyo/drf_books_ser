from django.db import models
import datetime


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)

    # 创建时间
    # 方式1
    # auto_now_add=True 只记录创建, 自动插入当前时间用于创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 方式2
    # create_time = models.DateTimeField(default=datetime.datetime.now)

    # auto_now=True, 只要更新就会自动更新时间
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 单个字段, 有索引, 有唯一
        # 多个字段, 有联合索引, 有联合唯一
        # index_together = []
        # unique_together = []

        abstract=True  # 抽象表, 不在数据库中建立表


class Book(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 一对多的关系一旦确定, 关联字段写在多的一方
    # to_field默认不写, 关联到Publish的主键
    # db_constraint=False 逻辑上的关联, 实际上没有外键联系, 增删不会受外键影响, 但是orm查询不影响
    publish = models.ForeignKey(to='Publish', on_delete=models.DO_NOTHING, db_constraint=False)

    # 多对多, 跟作者, 关联字段写在查询次数多的一方
    authors = models.ManyToManyField(to='Author', db_constraint=False)

    def __str__(self):
        return self.name

    @property
    def publish_name(self):
        return self.publish.name

    def author_list(self):
        author_list = self.authors.all()
        # ll = []
        # for author in author_list:
        #     ll.append({'name':author.name, 'sex':author.get_sex_display()})
        # return ll
        return [{'name':author.name, 'sex':author.get_sex_display()} for author in author_list]


class Publish(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Author(BaseModel):
    name = models.CharField(max_length=32)
    sex = models.IntegerField(choices=((1, '男'),(2, '女')))
    # 一对一, 写在查询频率高的
    # OneToOneField本质是ForeignKey + unique
    authordetail = models.OneToOneField(to='AuthorDetail', db_constraint=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AuthorDetail(BaseModel):
    mobile = models.CharField(max_length=11)


