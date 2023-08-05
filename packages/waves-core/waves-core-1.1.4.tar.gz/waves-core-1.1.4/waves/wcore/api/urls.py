from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include('waves.wcore.api.v1.urls', namespace='api_v1')),
    url(r'^', include('waves.wcore.api.v2.urls', namespace='api_v2')),
]
