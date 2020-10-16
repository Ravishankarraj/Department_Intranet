from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.utils.datetime_safe import date
from .models import NoticeText
from .models import UserProfile
from .models import LeaveApplication


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid UserId or Password")
            return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


def postednotice(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            notices = NoticeText.objects.all()

        elif UserProfile.objects.filter(user_id=request.user.id, isStudent=True):
            notices = NoticeText.objects.filter(Q(isStudent=True) | Q(isAll=True))

        elif UserProfile.objects.filter(user_id=request.user.id, isTeacher=True):
            notices = NoticeText.objects.filter(Q(isTeacher=True) | Q(isAll=True))

        elif UserProfile.objects.filter(user_id=request.user.id, isStaff=True):
            notices = NoticeText.objects.filter(Q(isStaff=True) | Q(isAll=True))

        elif UserProfile.objects.filter(user_id=request.user.id, isResearcher=True):
            notices = NoticeText.objects.filter(Q(isResearcher=True) | Q(isAll=True))

        else:
            notices = None
        return render(request, 'noticeview.html', {'notices': notices})

    else:
        return render(request, 'index.html')


def pendingnotice(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            notices = NoticeText.objects.filter(isApproved=False)
            return render(request, 'pendingnotice.html', {'notices': notices})

    else:
        return render(request, 'index.html')


def index(request):
    return render(request, 'loginpage.html', {'name': 'index'})


def profile(request):
    if request.user.is_authenticated:
        notices = NoticeText.objects.all()
        posted_notices = 0
        pending_notices = 0
        leave_application = 0

        if request.user.is_superuser:
            designation = "Head of department"
            posted_notices = NoticeText.objects.filter(isApproved=True).count()
            pending_notices = NoticeText.objects.filter(isApproved=False).count()
            leave_application = LeaveApplication.objects.filter(isApprove=False).count()

        elif UserProfile.objects.filter(user_id=request.user.id, isStudent=True).count() > 0:
            designation = "Student"
            posted_notices = NoticeText.objects.filter((Q(isStudent=True) | Q(isAll=True)), isApproved=True).count()

        elif UserProfile.objects.filter(user_id=request.user.id, isTeacher=True).count() > 0:
            designation = "Teacher"
            posted_notices = NoticeText.objects.filter((Q(isTeacher=True) | Q(isAll=True)), isApproved=True).count()

        elif UserProfile.objects.filter(user_id=request.user.id, isResearcher=True).count() > 0:
            designation = "Researcher"
            posted_notices = NoticeText.objects.filter((Q(isResearcher=True) | Q(isAll=True)), isApproved=True).count()

        elif UserProfile.objects.filter(user_id=request.user.id, isStaff=True).count() > 0:
            designation = "Staff"
            posted_notices = NoticeText.objects.filter((Q(isStaff=True) | Q(isAll=True)), isApproved=True).count()

        else:
            designation = "Unknown"

        return render(request, 'profile.html',
                      {'notices': notices, 'username': request.user, 'pending_notices': pending_notices,
                       'posted_notices': posted_notices, 'leave_application': leave_application,
                       'designation': designation})

    else:
        return render(request, 'index.html')


def approve(request):
    notice_id = request.POST['noticeId']
    notice = NoticeText.objects.get(id=notice_id)
    notice.isApproved = True
    notice.save()
    return redirect('profile')


def delete(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            print("Inside super User")
            notice_id = request.POST['noticeId']
            notice = NoticeText.objects.filter(id=notice_id)
            notice.delete()
            return redirect('postednotice')
    return redirect('/')


def edit(request):
    if request.method == 'POST':
        print("Inside edit method post")
        notice_id = request.POST['noticeId']
        print(notice_id)
        notice = NoticeText.objects.filter(id=notice_id)
        print(notice)
        print(notice[0].subject)
        print(notice[0].pdf.url)
        # print(notice.subject)
        # print(notice.content)
        return render(request, 'postnotice.html', {'notice': notice})
    return redirect('/')


def postnotice(request):
    subject = request.POST['subject']
    content = request.POST['content']
    pdf = request.FILES['pdfFile']
    notice_id = request.POST['noticeId']
    student = staff = teacher = researcher = for_all = False
    if 'student' in request:
        student = True
    if 'staff' in request:
        staff = True
    if 'teacher' in request:
        teacher = True
    if 'researcher' in request:
        researcher = True
    if 'for_all' in request:
        for_all = True
    if notice_id == "":
        if request.user.is_superuser:
            notice = NoticeText.objects.create(subject=subject, content=content, date=date.today(), isApproved=True,
                                               isStudent=student, pdf=pdf)
        else:
            notice = NoticeText.objects.create(subject=subject, content=content, date=date.today(), pdf=pdf)
        notice.save();
    else:
        notice = NoticeText.objects.get(id=notice_id)
        print(notice)
        notice.subject = subject
        notice.content = content
        notice.pdf = pdf
        notice.isStudent = student
        notice.isAll = for_all
        notice.save()
    print('notice saved')
    return redirect('profile')


def new_notice(request):
    if request.user.is_authenticated:
        return render(request, 'postnotice.html')
    else:
        return redirect('/')


def leave_management(request):
    if request.method == 'POST':
        casual = earned = commuted = compensatory = False
        if 'casual' in request:
            casual = True
        if 'earned' in request:
            earned = True
        if 'commuted' in request:
            commuted = True
        if 'compensatory' in request:
            compensatory = True
        reason = request.POST['reason']
        start_date = request.POST['firstdate']
        last_date = request.POST['lastdate']

        leave_application = LeaveApplication.objects.create(isCasual=casual, isEarned=earned, isCommuted=commuted,
                                                            isCompensatory=compensatory, reason=reason,
                                                            firstDate=start_date, lastDate=last_date, isApprove=False,
                                                            user_id=request.user.id, requestDate=date.today())
        leave_application.save()
        return redirect('profile')
    elif request.user.is_superuser:
        leaves = LeaveApplication.objects.filter(isApprove=False)
        return render(request, 'leavemain.html', {'leaves': leaves})
    else:
        return render(request, 'leaveuser.html', {'totalLeave': 0})
