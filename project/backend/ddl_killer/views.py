from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import User
from .models import Course
from .models import UserCourse
from .models import Task
from .models import UserTask

def create_user(request): #用户注册
    response={}
    data = json.loads(request.body.decode())
    user = User.objects.filter(uid=data["uid"])
    if user.exists():
        response["msg"]="The user already exists."
    else:
        User.objects.create(uid = data["uid"], name = data["name"], password = data["password"], email = data["email"])
        response["msg"]="Success."
    return JsonResponse(response)

def show_user(request): #展示用户信息
    response = {}
    data = json.loads(request.body.decode())
    user = User.objects.get(data["uid"])
    response["uid"] = user.uid
    response["name"] = user.name
    response["email"] = user.email
    return JsonResponse(response)

def create_courses(request): #管理员创建新课程
    response={}
    data = json.loads(request.body.decode())
    course = Course.objects.filter(cid=data["cid"])
    if course.exists():
        response["msg"]="The course_id already exists."
    else:
        Course.objects.create(cid = data["cid"], name = data["name"])
        response["msg"]="Success."
    return JsonResponse(response)

def show_all_courses(request): #查看所有课程列表(管理员维护以及用户选课)
    response = {}
    courses = Course.objects.all()
    for c in courses:
        response["data"] += [{
            "cid": c.cid,
            "course_name": c.name
        }]
    return JsonResponse(response)
    
def add_courses(request): #用户添加自己所选课程
    data = json.loads(request.body.decode())
    usercourse = UserCourse.objects.filter(cid=data["cid"])
    if usercourse.exists():
        response["msg"]="The course has already been chosen."
    else:
        UserCourse.objects.create(user = data["uid"], course = data["cid"])
        response["msg"]="Success."
    return JsonResponse(response)
    

def show_user_courses(request): #用户查看自己所选课程
    response = {}
    data = json.loads(request.body.decode())
    usercourse = UserCourse.objects.filter(user=data["uid"])
    for c in usercourse:
        course = Course.objects.get(cid=c.course)
        response["data"] += [{
            "cid": course.cid,
            "course_name": course.name,
            "is_admin": c.is_admin
        }]  
    return JsonResponse(response)


def add_task(request): #添加task，传入的json有receiver一项列表存储接收者的学号,uid记录发布者(有修改权)
    response={}
    data = json.loads(request.body.decode())
    task = Task.objects.filter(tid=data["tid"])
    if task.exists():
        response["msg"]="The task already exists."
    else:
        Task.objects.create(tid=data["tid"],title=data["title"],course=data["course"],content=data["content"],category=data["category"],urls=data["urls"],ddl_time=data["ddl_time"],notification_time=data["notification_time"],notification_content=data["notification_content"])
        response["msg"]="Success."
        UserTask.objects.create(user=data["uid"],task=data["tid"],is_admin=True) #发布者有修改权
        for id in data["receiver"]:
            UserTask.objects.create(user=id,task=data["tid"])
    return JsonResponse(response)


def show_user_task(request): #用户查看自己的所有任务及ddl
    response = {}
    data = json.loads(request.body.decode())
    usertask = UserTask.objects.filter(user=data["uid"])
    for t in usertask:
        task = Task.objects.get(tid=t.task)
        response["data"] += [{
            "tid": task.tid,
            "title": task.title,
            "course": task.course,
            "content": task.content,
            "category": task.category,
            "urls": task.urls,
            "ddl_time": task.ddl_time,
            "notification_time": task.notification_time,
            "notification_content": task.notification_content
            "is_admin:": t.is_admin
        }]  
    return JsonResponse(response)
    
    
def appoint_course_admin(request): #授予普通用户某门课程的管理权
    response={}
    data = json.loads(request.body.decode())
    usercourse = UserCourse.objects.filter(user=data["uid"],course=data["cid"])
    if usercourse.is_admin:
        response["msg"]="The user has already been the course_administor."
    else:
        usercourse.update(is_admin=True)
        response["msg"]="Success."
    return JsonResponse(response)
    



