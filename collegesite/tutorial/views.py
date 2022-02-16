from django.shortcuts import render, get_list_or_404, redirect, HttpResponse, get_object_or_404
from tutorial.models import *
from oes.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tutorial.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
import json
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from django.core.mail import send_mail
import math, random
from django.views.generic.edit import CreateView


# Create your views here.

def index(request):
	j = Subject.objects.filter()[:6]
	context = {'j': j}
	return render(request,'tutorial/index.html',context)

#@login_required(login_url='/')
def tutorial(request):
	j = Subject.objects.filter()
	context = {'j':j}
	return render(request,'tutorial/tutorial.html',context)

def detail(request,pk):
	form = ReplyForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			rep = form.cleaned_data['reply']
			id = request.POST.get('mid')
			cmt = Comment.objects.get(id=id)
			rep = Reply.objects.create(comment=cmt, user=User.objects.get(id=request.user.id), reply=rep)
			rep.save()
	j = Material.objects.filter(topic = pk)
	for i in j:
		q = i.pk

	comments = Comment.objects.all()
	replies = Reply.objects.all()
	count = Comment.objects.filter(post=pk).count()
	paginator = Paginator(j, 1)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	blogs = dict()
	try:
		blogs = paginator.get_page(page)
	except(EmptyPage, InvalidPage):
		blogs = paginator.get_page(page)

	page_number = request.GET.get('page')
	page_range = paginator.page_range
	page_obj = paginator.get_page(page_number)
	context = {'j':j,'comments':comments,'count':count,'replies':replies,'blogs': blogs,'page_obj':page_obj,'form':form}
	return render(request,'tutorial/detail.html',context)


def loginpage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
			else:
				return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"message": "invalid"}), content_type="application/json")
	return HttpResponse(json.dumps({"message": "denied"}), content_type="application/json")

def otp():
	global OTP
	OTP = random.randint(1000, 9999)
	return OTP

def register(request):
	if request.method == 'GET':
		global otp1
		otp1 = otp()
		email = request.GET.get('email')
		# Declare a digits variable
		# which stores all digits
		# length of password can be chaged
		# by changing value in range

		mail = send_mail(
			'Email Confirmation Message..',
			'Your OTP for Email Verification is ' + str(otp1),
			'admin@admin.com',
			[email],
			fail_silently=False,
		)

	if request.method == 'POST':
		username = request.POST.get('username')
		name = request.POST.get('name')
		email = request.POST.get('email')
		otp2 = request.POST.get('otp')
		computer_code = request.POST.get('computer_code')
		course = request.POST.get('course')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		data = {'username':username,'name':name,'email':email,'computer_code':computer_code,'course':course,'password1':password1,'password2':password2}
		form = CreateUserForm(data=data)

		if not otp1 == int(otp2):
			return HttpResponse(json.dumps({"message": "Denied"}), content_type="application/json")

		if form.is_valid():
			user = form.save(commit=False)
			computer_code = form.cleaned_data.get('computer_code')
			course = form.cleaned_data.get('course')
			name = form.cleaned_data.get('name')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')

			user.is_active = True
			user.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			Student_Model(user=User.objects.filter(username=username).first(), computer_code=computer_code,course=course, name=name).save()

			return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"message": form.errors}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"message": "Denied"}),content_type="application/json")


def logout_request(request):
	logout(request)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def like(request):
	if request.is_ajax():
		i = request.GET.get('i')
		p = Material.objects.get(pk = i)
		p.likes += 1
		p.save()
		data = {'i':p.likes}
		return JsonResponse(data)

def comment(request):
	if request.method == 'POST':
		comment = request.POST.get('comment')
		id = request.POST.get('id')
		print(comment,id)
		user = User.objects.get(id=request.user.id)
		cmt = Comment.objects.create(post = Material.objects.get(pk=id),user = user,comment=comment)
		cmt.save()
		return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"message": "Denied"}),content_type="application/json")

def reply(request):
	if request.method == 'POST':
		reply = request.POST.get('reply')
		id = request.POST.get('id')
		print(id,reply)
		cmt = Comment.objects.get(id=id)
		rep = Reply.objects.create(comment=cmt,user = User.objects.get(id=request.user.id), reply=reply)
		rep.save()
		return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"message": form.errors}), content_type="application/json")

@login_required(login_url='/')
def profile(request):
	context = {}
	check = Student_Model.objects.filter(user=request.user.id)
	if len(check) > 0:
		data = Student_Model.objects.get(user=request.user.id)
		context["data"] = data
	if request.method == "POST":
		username = request.POST["username"]
		name = request.POST["name"]
		email = request.POST["email"]
		computer_code = request.POST["computer_code"]
		course = request.POST["course"]
		enrollment_no = request.POST["enrollment_no"]

		usr = User.objects.get(id=request.user.id)
		usr.username = username
		usr.email = email
		usr.save()

		data.name = name
		data.computer_code = computer_code
		data.course = course
		data.enrollment_no = enrollment_no

		if "image" in request.FILES:
			img = request.FILES["image"]
			data.image = img
			data.save()

		context["status"] = "Changes Saved Successfully !"
	return render(request,'profile.html',context)
'''
	if request.method == "POST":
		u_form = UserUpdate(request.POST,instance=request.user)
		p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.student_model)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
	else:
		u_form = UserUpdate(instance = request.user)
		p_form = ProfileUpdate(instance = request.user.student_model)'''
	#return render(request,'profile.html',{'u_form':u_form,'p_form':p_form})

#Faculty Login
def login_faculty(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get("password")
		print(username,password)
		dbuser = Faculty.objects.filter(username=username, password=password)
		print(dbuser)
		if not dbuser:
			return HttpResponse('Login failed')
		else:
			request.session['name'] = username
			#request.session.get_expiry_age()
			instance = get_object_or_404(Faculty, username=username)
			return HttpResponse(json.dumps({"message": "Success","instance":username}), content_type="application/json")
