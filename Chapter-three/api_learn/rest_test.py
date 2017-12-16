from django import setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','api_learn.settings')
setup()

from rest_framework import serializers

class TestSerilOne(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()


frontend_data = {
        'name':'ucag',
        'age':'ucag'
    }

# test = TestSerilOne(data=frontend_data)
# if not test.is_valid():
#     print(test.errors)

class TestSerilTwo(serializers.Serializer):
    name = serializers.CharField(max_length=20)


# from rest_learn.models import TestModel
# codes = TestModel.objects.all()
# test = TestSerilTwo(instance=codes,many=True)
# print(test.data)

from rest_learn.models import TestModel
class TestSerilThree(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['name','code','created_time','changed_time','id']
        read_only_fields = ['created_time','changed_time']

# code = TestModel.objects.get(name='ls')
# codes = TestModel.objects.all()

# 前端写入测试
# frontend_data = {
#     'name':'ModelSeril',
#     'code':"""print('frontend test')""",
#     'created_time':'2107-12-16'
# }
# test1 = TestSerilThree(data=frontend_data)
# if test1.is_valid():
#     print('Frontend test:',test1.validated_data)
# 后端传出测试：
# test2 = TestSerilThree(instance=code)
# print('Backend single instance test:',test2.data)
# test3 = TestSerilThree(instance=codes,many=True)
# print('Backend multiple instances test',test3.data)

class ProfileSerializer(serializers.Serializer):
    tel = serializers.CharField(max_length=15)
    height = serializers.IntegerField()

class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    qq = serializers.CharField(max_length=15)
    profile = ProfileSerializer()

# frontend_data = {
#     'name':'ucag',
#     'qq':'88888888',
#     'profile':{
#         'tel':'66666666666',
#         'height':'185'
#     }
# }

# test = UserSerializer(data=frontend_data)
# if test.is_valid():
#     print(test.validated_data)
class TEL(object):
    """电话号码对象"""
    def __init__(self, num=None):
        self.num = num
    def text(self, message):
        """发短信功能"""
        return self._send_message(message)
    def _send_message(self,message):
        """发短信"""
        print('Send {} to {}'.format(message[:10], self.num))
class TELField(serializers.Field):
    def to_representation(self, tel_obj):
        return tel_obj.num
    def to_internal_value(self, data):
        data = data.lstrip().rstrip().strip()
        if 8 <= len(data) <=11:
            return TEL(num=data)
        raise serializers.ValidationError('Invalid telephone number.')

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    tel = TELField()

# frontend_data = {
#     'name':'ucag',
#     'tel':'88888888'
# }
# test = ContactSerializer(data=frontend_data)
# if test.is_valid():
#     tel = test.validated_data['tel']
#     print('TEL',tel.num)
#     tel.text('这是一个骚字段')

from rest_framework.viewsets import ModelViewSet
class TestViewSet(ModelViewSet):
    queryset = TestModel.objects.all()

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'codes', TestViewSet)
urlpatterns = router.urls
print(urlpatterns)