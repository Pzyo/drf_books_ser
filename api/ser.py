
from rest_framework import serializers
from api import models


# 如果序列化的是数据库的表, 尽量使用ModelSerializer
class BookModelSerializer(serializers.ModelSerializer):
    # 方案1: (序列化可以, 反序列化有问题)
    # publish = serializers.CharField(source='publish.name')
    # 方案2
    # 在models表模型写方法

    class Meta:
        model = models.Book
        # fields = '__all__'
        # depth = 0
        fields = ('name', 'price', 'authors', 'author_list', 'publish', 'publish_name')
        extra_kwargs = {
            'publish': {'write_only': True},
            'publish_name': {'read_only': True},
            'authors': {'write_only': True},
            'author_list': {'read_only': True}
        }
