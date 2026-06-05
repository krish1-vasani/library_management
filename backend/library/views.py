from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from django.core.mail import send_mail
from django.conf import settings


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/index.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/studentclick.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/adminclick.html')


def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
            my_student_group, _ = Group.objects.get_or_create(name='STUDENT')
            my_student_group.user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'library/studentsignup.html', context=mydict)


def is_admin(user):
    return user.is_superuser or user.is_staff


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')
    elif is_student(request.user):
        return render(request, 'library/studentafterlogin.html')
    return redirect('/')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'library/bookadded.html')
    return render(request, 'library/addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books = models.Book.objects.all()
    return render(request, 'library/viewbook.html', {'books': books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook(
                enrollment=request.POST.get('enrollment2'),
                isbn=request.POST.get('isbn2')
            )
            obj.save()
            return render(request, 'library/bookissued.html')
    return render(request, 'library/issuebook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []
    for ib in issuedbooks:
        issdate = ib.issuedate.strftime('%d-%m-%Y')
        expdate = ib.expirydate.strftime('%d-%m-%Y')
        days_held = (date.today() - ib.issuedate).days
        fine = max(0, (days_held - 15) * 10)

        books = list(models.Book.objects.filter(isbn=ib.isbn))
        students = list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        for i, book in enumerate(books):
            if i < len(students):
                t = (students[i].get_name, students[i].enrollment,
                     book.name, book.author, issdate, expdate, fine, ib.status)
                li.append(t)

    return render(request, 'library/viewissuedbook.html', {'li': li})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'library/viewstudent.html', {'students': students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id)
    if not student.exists():
        return redirect('/')
    issuedbook = models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1, li2 = [], []
    for ib in issuedbook:
        books = models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            li1.append((request.user, student[0].enrollment, student[0].branch, book.name, book.author))
        issdate = ib.issuedate.strftime('%d-%m-%Y')
        expdate = ib.expirydate.strftime('%d-%m-%Y')
        days_held = (date.today() - ib.issuedate).days
        fine = max(0, (days_held - 15) * 10)
        li2.append((issdate, expdate, fine, ib.status, ib.id))

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})


def returnbook(request, id):
    issued_book = models.IssuedBook.objects.get(pk=id)
    issued_book.status = 'Returned'
    issued_book.save()
    return redirect('viewissuedbookbystudent')


def aboutus_view(request):
    return render(request, 'library/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(
                f'{name} || {email}',
                message,
                settings.EMAIL_HOST_USER,
                ['admin@yourdomain.com'],
                fail_silently=False
            )
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form': sub})
