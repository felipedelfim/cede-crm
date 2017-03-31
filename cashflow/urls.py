from django.conf.urls import url

from . import views

app_name = 'cashflow'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.transaction_new, name='transaction_new'),
    url(r'^(?P<pk>\d+)/edit/$', views.transaction_edit, name='transaction_edit'),
    url(r'^(?P<pk>\d+)/pay/$', views.transaction_pay, name='transaction_pay'),
    url(r'^(?P<pk>\d+)/remove/$', views.transaction_remove, name='transaction_remove'),
]
