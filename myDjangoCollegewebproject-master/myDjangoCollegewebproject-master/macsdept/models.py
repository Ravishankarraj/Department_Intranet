from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class NoticeText(models.Model):
    subject = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateField()
    pdf = models.FileField(upload_to='notice/pdfs')
    isStaff = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)
    isTeacher = models.BooleanField(default=False)
    isAll = models.BooleanField(default=False)
    isResearcher = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    isStaff = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)
    isTeacher = models.BooleanField(default=False)
    isResearcher = models.BooleanField(default=False)


class LeaveApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isCasual = models.BooleanField(default=False)
    isEarned = models.BooleanField(default=False)
    isCommuted = models.BooleanField(default=False)
    isCompensatory = models.BooleanField(default=False)
    requestDate = models.DateField()
    firstDate = models.DateField()
    lastDate = models.DateField()
    isApprove = models.BooleanField(default=False)
    reason = models.TextField()


class LeaveStatus(models.Model):
    leave = models.ForeignKey(LeaveApplication, on_delete=models.CASCADE)
    approveDate = models.DateField()
