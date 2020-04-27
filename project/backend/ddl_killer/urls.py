"""django_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/users/<int:student_id>/verify', views.user_verify),
    path('api/users/email/verify', views.send_verify_email),
    path('api/users/email/verify/<int:uid>/<int:verification_code>', views.verify_email),
    path('api/course/<int:course_id>/ddls', views.get_course_ddls),
    path('api/user/<int:uid>/ddls', views.get_user_ddls),
    path('api/ddls', views.get_all_ddls),
    path('api/user/<int:uid>/task/<int:tid>', views.get_user_tasks),
    path('api/user/<int:uid>/courses', views.get_user_tasks),
    path('api/tasks', views.get_all_tasks),
    path('api/course/quit', views.quit_course),
    path('api/course/apply', views.apply_course),
    path('api/task/<int:tid>/alert', views.set_alert),
    path('api/course/<int:cid>/appoint', views.appoint_course_leader),
    path('api/user/apply', views.user_apply),
    path('api/user/<int:uid>/info', views.get_user_info),
    path('api/user/<int:uid>/modify', views.modify_user_info),



    path('admin/', admin.site.urls),

]
