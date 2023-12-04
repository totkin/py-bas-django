from django.urls import re_path

from . import views
# from ..nomad import settings

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^managers/$', views.ManagerListView.as_view(), name='managers'),
    re_path(r'^manager/(?P<pk>\d+)$', views.ManagerDetailView.as_view(), name='manager-detail'),
    re_path(r'^departments/$', views.DepartmentListView.as_view(), name='departments'),
    re_path(r'^department/(?P<pk>\d+)$', views.DepartmentDetailView.as_view(), name='department-detail'),
    re_path(r'^titles/$', views.TitleListView.as_view(), name='titles'),
    re_path(r'^title/(?P<pk>\d+)$', views.TitleDetailView.as_view(), name='title-detail'),
    re_path(r'^manager/(?P<pk>[-\w]+)/renew/$', views.renew_Manager, name='renew-Manager'),
]

urlpatterns += [
    re_path(r'^subscriptions/$', views.SubscriptionListView.as_view(), name='subscriptions'),
    re_path(r'^subscription/(?P<pk>\d+)$', views.SubscriptionDetailView.as_view(), name='subscription-detail'),
    re_path(r'^subscription/create/$', views.SubscriptionCreate.as_view(), name='subscription_create'),
    re_path(r'^subscription/(?P<pk>\d+)/update/$', views.SubscriptionUpdate.as_view(), name='subscription_update'),
    re_path(r'^subscription/(?P<pk>\d+)/delete/$', views.SubscriptionDelete.as_view(), name='subscription_delete'),
]
