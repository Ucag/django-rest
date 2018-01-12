from rest_framework import serializers
from .models import Code

#创建序列化器
class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__' #序列化全部字段

#用于列表展示的序列化器
class CodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ('id', 'name')