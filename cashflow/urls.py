from django.conf.urls import url

from . import views

app_name = 'cashflow'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.transaction_new, name='transaction_new'),
    url(r'^(?P<pk>\d+)/edit/$', views.transaction_edit, name='transaction_edit'),
    url(r'^(?P<pk>\d+)/pay/$', views.transaction_pay, name='transaction_pay'),
    url(r'^(?P<pk>\d+)/remove/$', views.transaction_remove, name='transaction_remove'),
    url(r'^persons/$', views.PersonListView.as_view(), name='person_list'),
    url(r'^persons/new/$', views.person_new, name='person_new'),
    url(r'^persons/(?P<pk>\d+)/edit/$', views.person_edit, name='person_edit'),
    url(r'^items/(?P<pk>\d+)/value/$', views.item_get_value, name='item_get_value'),
    url(r'^reports/$', views.transaction_report, name='transaction_report'),

]
