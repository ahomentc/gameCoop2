from django.conf.urls import url
from . import views

app_name = 'activity_feed'

urlpatterns = [
    url(r'^submitActivityClient',views.submitActivityClient,name='submitActivityClient'),
]

