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


#def create_courses(request): #管理员创建新课程
#    response={}
#    data = json.loads(request.body.decode())
#    course = Course.objects.filter(cid=data["cid"])
#    if course.exists():
#        response["msg"]="The course_id already exists."
#    else:
#        Course.objects.create(cid = data["cid"], name = data["name"])
#        response["msg"]="Success."
#    return JsonResponse(response)


#def show_all_courses(request): #查看所有课程列表(管理员维护以及用户选课)
#    response = {}
#    courses = Course.objects.all()
#    for c in courses:
#        response["data"] += [{
#            "cid": c.cid,
#            "course_name": c.name
#        }]
#    return JsonResponse(response)
    
    
def add_courses(request): #从课程中心获取用户所选课程并同步作业
    response = {}
    data = json.loads(request.body.decode())
    for d in data["courses"]:
        course = Course.objects.filter(cid=d["cid"])
        if not course.exists():
            Course.objects.create(cid=d["cid"],name=d["course_name"],teacher=d["course_teacher"])
            for a in d["assignments"]:
                Task.objects.create(tid=a["tid"],title=a["title"],course=d["cid"],content=a["content"],category="homework",urls=a["urls"],ddl_time=a["ddl_time"],notification_time=a["notification_time"],notification_content=a["notification_content"],notification_alert=a["notification_alert"])
        usercourse = UserCourse.objects.filter(uid=data["uid"],cid=d["cid"])
        if not usercourse.exists():
            UserCourse.objects.create(user = data["uid"], course = d["cid"])
            for a in d["assignments"]:
                UserTask.objects.create(user = data["uid"], task = a["tid"])
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
            "course_teacher": course.teacher,
            "is_admin": c.is_admin
        }]  
    return JsonResponse(response)


def admin_add_task(request): #课程管理员为选择了所有课的人添加task，participant由数据表关联得到，不需前端传入
    response={}
    data = json.loads(request.body.decode())
    usercourse = UserCourse.objects.filter(user=data["uid"],course=data["cid"])
    if usercourse.is_admin:
        Task.objects.create(tid=data["tid"],title=data["title"],course=data["cid"],content=data["content"],category=data["category"],urls=data["urls"],ddl_time=data["ddl_time"],notification_time=data["notification_time"],notification_content=data["notification_content"],notification_alert=data["notification_alert"])
        response["msg"]="Success."
        participants=UserCourse.objects.filter(course=data["cid"]) 
        for p in participants:
            UserTask.objects.create(user=p.uid,task=data["tid"])
        UserTask.objects.filter(user=data["uid"],task=data["tid"]).update(is_admin=True) #发布者有修改此task的权利
    else:
        response["msg"]="The user is not admin."
    return JsonResponse(response)


def add_task(request): #用户个人添加task(需要选择或输入participant)，传入的json有participant一项列表存储接收者的学号,uid记录发布者(有修改权)
    response={}
    data = json.loads(request.body.decode())
    task = Task.objects.filter(tid=data["tid"])
    if task.exists(): #若此项task已存在则视为修改此task的属性信息
        #验证修改权限
        if UserTask.objects.filter(user=data["uid"],task=data["tid"],is_admin=True).exists():
            task.update(title=data["title"])
            task.update(course=data["course"])
            task.update(content=data["content"])
            task.update(platform=data["platform"])
            task.update(category=data["category"])
            task.update(urls=data["urls"])
            task.update(ddl_time=data["ddl_time"])
            task.update(notification_time=data["notification_time"])
            task.update(notification_content=data["notification_content"])
            task.update(notification_alert=data["notification_alert"])
            response["msg"]="Update success."
        else:
            response["msg"]="Cannot modify task."
    else: #不存在就创建新的task
        Task.objects.create(tid=data["tid"],title=data["title"],course=data["course"],content=data["content"],category=data["category"],urls=data["urls"],ddl_time=data["ddl_time"],notification_time=data["notification_time"],notification_content=data["notification_content"],notification_alert=data["notification_alert"])
        response["msg"]="Create success."
        UserTask.objects.create(user=data["uid"],task=data["tid"],is_admin=True) #发布者有修改权
        for id in data["participant"]:
            UserTask.objects.create(user=id,task=data["tid"])
    return JsonResponse(response)


def show_user_task(request): #用户查看自己的所有任务及ddl
    response = {}
    data = json.loads(request.body.decode())
    usertask = UserTask.objects.filter(user=data["uid"])
    if usertask.exists():
        for t in usertask:
            task = Task.objects.get(tid=t.task)
            response["data"] += [{
                "tid": task.tid,
                "title": task.title,
                "course": task.course,
                "content": task.content,
                "platform": task.platform,
                "category": task.category,
                "urls": task.urls,
                "ddl_time": task.ddl_time,
                "notification_time": task.notification_time,
                "notification_content": task.notification_content,
                "notification_alert": task.notification_alert,
                "is_admin:": t.is_admin,
                "is_finished": t.is_finished
            }]  
    else:
        response["msg"]="No tasks."
    return JsonResponse(response)
    
    
def appoint_course_admin(request): #授予普通用户某门课程的管理权
    response={}
    data = json.loads(request.body.decode())
    usercourse = UserCourse.objects.filter(user=data["uid"],course=data["cid"])
    taskid = UserTask.objects.filter(user=data["uid"])
    if usercourse.is_admin:
        response["msg"]="The user has already been the course_administor."
    else:
        usercourse.update(is_admin=True)
        for t in taskid: #与该门课有关的task权限也进行更改
            task = Task.objects.filter(tid=t.task)
            if task.exists() and task[0].course == data["cid"]:
               t.update(is_admin=True)
        response["msg"]="Success."
    return JsonResponse(response)
  
  
def finish_task(request):
    response={}
    data = json.loads(request.body.decode())
    usertask = UserTask.objects.filter(user=data["uid"],task=data["tid"])
    if usertask.exists():
        usercourse.update(is_finished=True)
        response["msg"]="Success."
    else:
        response["msg"]="The task of the user is not found."
    return JsonResponse(response)

    

