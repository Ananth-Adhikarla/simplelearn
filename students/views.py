from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.views.generic.edit import FormView
from braces.views import LoginRequiredMixin
from .forms import CourseEnrollForm

from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView

from django.contrib.auth.models import Group, User

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        login(self.request, user)
        return result

class InstructorRegistrationView(CreateView):
    template_name = 'students/instructor/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('manage_course_list')

    def form_valid(self, form):
        result = super(InstructorRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        g = Group.objects.get(name='Instructor')
        u = User.objects.get(username=user)
        g.user_set.add(user)
        u.first_name = cd['username']
        u.is_staff = True
        u.save()
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context

class PythonShellView(TemplateView):

    template_name = 'students/python_shell/pshell.html'
    def relative_url_view(request):
        return redirect(template_name)

class NodeJSView(TemplateView):

    template_name = 'students/node_shell/nodeshell.html'
    def relative_url_view(request):
        return redirect(template_name)

class PythonInterpreterView(TemplateView):

    template_name = 'students/python_interpreter/python_interpreter.html'
    def relative_url_view(request):
        return redirect(template_name)