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
    path(r'user/<int:uid>/course/<int:cid>/tasks', views.show_course_tasks),
    path(r'user/<int:uid>/tasks', views.show_user_tasks),
    path(r'user/<int:uid>/courses', views.show_user_courses),
    path(r'course/<int:cid>/tasks/new', views.admin_add_task),
    path(r'user/<int:uid>/tasks/new', views.add_task),
    path(r'course/new', views.add_courses),
    path(r'course/<int:cid>/user/<int:uid>/appoint', views.appoint_course_admin),
    path(r'user/apply', views.create_user),
    path(r'user/<int:uid>/info', views.show_user),
    path(r'user/<int:uid>/task/<int:tid>/finish', views.finish_task),

]
