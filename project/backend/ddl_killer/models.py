from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    
    
class Course(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    teacher =models.CharField(max_length=50)
   
   
class UserCourse(models.Model):
    user = models.ForeignKey(to='User',to_field='uid', on_delete=models.CASCADE)
    course = models.ForeignKey(to='Course',to_field='cid', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    
    
class Task(models.Model):
    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    course = models.ForeignKey(to='Course',to_field='cid', on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)
    platform = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    urls = models.CharField(max_length=200,null=True)
    ddl_time = models.DateTimeField(null=True)
    notification_time = models.DateTimeField(null=True)
    notification_content = models.TextField(null=True)
    notification_alert = models.BooleanField(default = True)
    
    
class UserTask(models.Model):
    user = models.ForeignKey(to='User',to_field='uid', on_delete=models.CASCADE)
    task = models.ForeignKey(to='Task',to_field='tid', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)