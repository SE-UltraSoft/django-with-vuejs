from django.db import models
# django密码转换
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20, null=False, default='user')
    password = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    
    
    def save(self):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()

class Course(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, default='course')
    teacher =models.CharField(max_length=50, null=False, default='teacher')
   
   
class UserCourse(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    
    
class Task(models.Model):
    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    platform = models.CharField(max_length=20, null=True, blank=True)
    category = models.CharField(max_length=20)
    urls = models.CharField(max_length=200,null=True, blank=True)
    ddl_time = models.CharField(max_length=50,null=True)
    notification_time = models.CharField(max_length=50,null=True)
    notification_alert = models.BooleanField(default = True)
    create_time = models.CharField(max_length=50,null=True)
    
    
class UserTask(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)