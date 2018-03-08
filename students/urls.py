from django.conf.urls import url
from . import views


urlpatterns = [

	url(r'^register/$', views.StudentRegistrationView.as_view(), name='student_registration'),
	url(r'^registerinstructor/$', views.InstructorRegistrationView.as_view(), name='instructor_registration'),
	url(r'^enroll-course/$',views.StudentEnrollCourseView.as_view(),name='student_enroll_course'),
	url(r'^courses/$',views.StudentCourseListView.as_view(),name='student_course_list'),
	url(r'^course/(?P<pk>\d+)/$',views.StudentCourseDetailView.as_view(),name='student_course_detail'),
	url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$',views.StudentCourseDetailView.as_view(),name='student_course_detail_module'),
	url(r'^pshell/$',views.PythonShellView.as_view(),name='python_shell'),
	url(r'^njshell/$',views.NodeJSView.as_view(),name='nodejs_shell'),
	url(r'^pinterpreter/$',views.PythonInterpreterView.as_view(),name='python_interpreter'),
]