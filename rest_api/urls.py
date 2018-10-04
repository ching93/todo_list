from django.conf.urls import url
from . import views

app_name = 'rest_api'


urlpatterns = [
	#url(r'^$', views.main, name='main'),
	url(r'login', views.rest_login, name='login'),
	url(r'logout', views.rest_logout, name='logout'),
	url(r'add_employee/',views.employee_list, name='employee_list'),
	url(r'todo_list/', views.todo_list, name='todo_list'),
	url(r'todo_detail/(?P<pk>\d+)',views.todo_detail, name='todo_detail'),
	url(r'org_list/', views.OrgList.as_view(), name='org_list'),
	url(r'org_detail/(?P<pk>\d+)',views.OrgDetail.as_view(), name='org_detail'),
	
]