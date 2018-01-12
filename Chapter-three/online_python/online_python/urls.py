from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from backend.views import CodeViewSet, RunCodeAPIView, home, js, css

router = DefaultRouter()
router.register(prefix='code', viewset=CodeViewSet, base_name='code')

API_V1 = [url(r'^run/$', RunCodeAPIView.as_view(), name='run')]

API_V1.extend(router.urls)

API_VERSIONS = [url(r'^v1/', include(API_V1))]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(API_VERSIONS)),
    url(r'^js/(?P<filename>.*\.js)$', js, name='js'),
    url(r'^css/(?P<filename>.*\.css)$', css, name='css'),
    url(r'^$', home, name='home')
]
