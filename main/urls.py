"""versity_enroll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("cpanel/", views.cpanel, name="cpanel"),
    path("add_student/", views.add_student, name="add_student"),
    path("view_students/", views.view_students, name="add_student"),
    path("list_students/", views.list_students, name="list_student"),
    path("enroll_course/", views.enroll_course, name="enroll_course"),
    path("view_enrolled_course/", views.view_enrolled_course, name="enroll_course"),
    path("fetch_teacher/", views.fetch_teacher, name="fetch_teacher"),
    path("account/",views.account,name="Show Profile"),
    path("fetch_enrolled_teacher/",views.fetch_enrolled_teacher,name="fetch_enrolled_teacher"),
    path("fetch_enrolled_session/",views.fetch_enrolled_session,name="fetch_enrolled_session"),
    path("fetch_enrolled_batch/",views.fetch_enrolled_batch,name="fetch_enrolled_batch"),
    path("view_enrolled_student/",views.view_enrolled_student,name="view_enrolled_student"),
    path("graph/",views.graph,name="graph"),


 ]