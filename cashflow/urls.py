from django.conf.urls import url

from . import views

app_name = 'cashflow'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^new/$', views.transaction_new, name='new'),
    url(r'^(?P<pk>\d+)/edit/$', views.transaction_edit, name='edit'),
]
