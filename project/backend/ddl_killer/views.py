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


def show_user(request, uid): #展示用户信息
    response = {}
    user = User.objects.get(uid=uid)
    print(uid)
    response["uid"] = user.uid
    response["name"] = user.name
    response["email"] = user.email
    return JsonResponse(response)
    
    
def add_courses(request): #从课程中心获取用户所选课程并同步作业，url未完成
    response = {}
    data = json.loads(request.body.decode())
    for d in data["courses"]:
        course = Course.objects.filter(name=d["course_name"],teacher=d["course_teacher"])
        if course.exists():
            course_id=course.cid
        else:
            Course.objects.create(name=d["course_name"],teacher=d["course_teacher"])
            new_course=Course.objects.get(name=d["course_name"],teacher=d["course_teacher"])
            course_id=new_course.cid
            for a in d["assignments"]:
                Task.objects.create(title=a["title"],course=new_course,content=a["content"],category="homework",urls=a["urls"],ddl_time=a["ddl_time"],notification_time=a["notification_time"],notification_content=a["notification_content"],notification_alert=a["notification_alert"])
        usercourse = UserCourse.objects.filter(user__uid=data["uid"],course__cid=course_id)
        if not usercourse.exists():
            user_obj=User.objects.get(uid=data["uid"])
            course_obj=Course.objects.get(cid=course_id)
            UserCourse.objects.create(user = user_obj, course = course_obj)
            for a in d["assignments"]:
                task_obj = Task.objects.get(title=a["title"],course__cid=course_id,content=a["content"],category="homework",urls=a["urls"],ddl_time=a["ddl_time"],notification_time=a["notification_time"],notification_content=a["notification_content"],notification_alert=a["notification_alert"])
                UserTask.objects.create(user = user_obj, task = task_obj)
    return JsonResponse(response)
    

def show_user_courses(request, uid): #用户查看自己所选课程
    response = {}
    response["data"]=[]
    usercourse = UserCourse.objects.filter(user__uid=uid)
    for c in usercourse:
        course = Course.objects.get(cid=c.course.cid)
        response["data"] += [{
            "cid": course.cid,
            "course_name": course.name,
            "course_teacher": course.teacher,
            "is_admin": c.is_admin
        }]  
    return JsonResponse(response)


def admin_add_task(request, cid): #课程管理员为选择了所有课的人添加task，participant由数据表关联得到，不需前端传入
    response={}
    data = json.loads(request.body.decode())
    usercourse = UserCourse.objects.filter(user__uid=data["uid"],course__cid=cid)
    if usercourse.is_admin:
        course_obj = Course.objects.get(cid=cid)
        Task.objects.create(title=data["title"],course=course_obj,content=data["content"],category=data["category"],urls=data["urls"],ddl_time=data["ddl_time"],notification_time=data["notification_time"],notification_content=data["notification_content"],notification_alert=data["notification_alert"])
        task_obj = Task.objects.get(title=data["title"],course__cid=cid,content=data["content"],category=data["category"],urls=data["urls"],ddl_time=data["ddl_time"],notification_time=data["notification_time"],notification_content=data["notification_content"],notification_alert=data["notification_alert"])
        response["msg"]="Success."
        participants=UserCourse.objects.filter(course__cid=cid) 
        for p in participants:
            user_obj=User.objects.get(uid=p.user.uid)
            UserTask.objects.create(user=user_obj,task=task_obj)
        UserTask.objects.filter(user__uid=data["uid"],task__tid=task_obj.tid).update(is_admin=True) #发布者有修改此task的权利
    else:
        response["msg"]="The user is not admin."
    return JsonResponse(response)


def add_task(request, uid): #用户个人添加task(需要选择或输入participant)，传入的json有participant一项列表存储接收者的学号,uid记录发布者(有修改权)
    response={}                   #没有course_id项也不需要修改course_id项
    data = json.loads(request.body.decode())
    task = Task.objects.filter(tid=data["tid"])
    if task.exists(): #若此项task已存在则视为修改此task的属性信息
        #验证修改权限
        if UserTask.objects.filter(user__uid=uid,task__tid=data["tid"],is_admin=True).exists():
            task.update(title=data["title"])
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
    else: #不存在就创建新的task(传入的tid为空)
        Task.objects.create(title=data["title"],content=data["content"],category=data["category"],urls=data["urls"],ddl_time=data["ddl_time"],notification_time=data["notification_time"],notification_content=data["notification_content"],notification_alert=data["notification_alert"])
        task_obj = Task.objects.get(title=data["title"],content=data["content"],category=data["category"],urls=data["urls"],ddl_time=data["ddl_time"],notification_time=data["notification_time"],notification_content=data["notification_content"],notification_alert=data["notification_alert"])
        response["msg"]="Create success."
        user_obj=User.objects.get(uid=uid)
        UserTask.objects.create(user=user_obj,task=task_obj,is_admin=True) #发布者有修改权
        for id in data["participant"]:
            user_obj=User.objects.get(uid=id)
            UserTask.objects.create(user=user_obj,task=task_obj)
    return JsonResponse(response)


def show_user_tasks(request, uid): #用户查看自己的所有任务及ddl
    response = {}
    response['data'] = []
    usertask = UserTask.objects.filter(user__uid=uid)
    if usertask.exists():
        for t in usertask:
            if t.task.course is None:
                response["data"] += [{
                    "tid": t.task.tid,
                    "title": t.task.title,
                    "course": t.task.course,
                    "content": t.task.content,
                    "platform": t.task.platform,
                    "category": t.task.category,
                    "urls": t.task.urls,
                    "ddl_time": t.task.ddl_time,
                    "notification_time": t.task.notification_time,
                    "notification_content": t.task.notification_content,
                    "notification_alert": t.task.notification_alert,
                    "is_admin:": t.is_admin,
                    "is_finished": t.is_finished
                }]   
            else:
                response["data"] += [{
                    "tid": t.task.tid,
                    "title": t.task.title,
                    "course": t.task.course.name,
                    "content": t.task.content,
                    "platform": t.task.platform,
                    "category": t.task.category,
                    "urls": t.task.urls,
                    "ddl_time": t.task.ddl_time,
                    "notification_time": t.task.notification_time,
                    "notification_content": t.task.notification_content,
                    "notification_alert": t.task.notification_alert,
                    "is_admin:": t.is_admin,
                    "is_finished": t.is_finished
                }]   
    else:
        response["msg"]="No tasks."
    return JsonResponse(response)
    
    
def show_course_tasks(request, uid, cid): #用户uid,相应课程cid
    response={}
    response['data'] =[]
    tasks = Task.objects.filter(course__isnull=False)
    print(tasks)
    for t in tasks:
        if t.course.cid==cid:
            usertask = UserTask.objects.filter(user__uid=uid,task__tid=t.tid)
            for ut in usertask:
                response["data"] += [{
                    "tid": t.tid,
                    "title": t.title,
                    "course": t.course.name,
                    "content": t.content,
                    "platform": t.platform,
                    "category": t.category,
                    "urls": t.urls,
                    "ddl_time": t.ddl_time,
                    "notification_time": t.notification_time,
                    "notification_content": t.notification_content,
                    "notification_alert": t.notification_alert,
                    "is_admin:": ut.is_admin,
                    "is_finished": ut.is_finished
                }]       
    return JsonResponse(response)
    
def appoint_course_admin(request, cid, uid): #授予普通用户某门课程的管理权
    response={}
    usercourse = UserCourse.objects.filter(user__uid=uid,course__cid=cid)
    if usercourse.exists():
        if usercourse[0].is_admin:
            response["msg"]="The user has already been the course_administor."
        else:
            usercourse.update(is_admin=True)
            tasks = Task.objects.filter(course__isnull=False)
            for t in tasks:
                if t.course.cid==cid and UserTask.objects.filter(user__uid=uid,task__tid=t.tid).exists():
                    UserTask.objects.filter(user__uid=uid,task__tid=t.tid).update(is_admin=True)
            response["msg"]="Success."
    else:
        response["msg"]="The user did not select the course."
    return JsonResponse(response)
  
  
def finish_task(request, uid, tid):
    response={}
    usertask = UserTask.objects.filter(user__uid=uid,task__tid=tid)
    if usertask.exists():
        usertask.update(is_finished=True)
        response["msg"]="Success."
    else:
        response["msg"]="The task of the user is not found."
    return JsonResponse(response)

    

