from django.shortcuts import render, get_list_or_404, redirect, HttpResponse, get_object_or_404
from oes.models import *
from tutorial.models import *
from oes.forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
import datetime
from django.core.paginator import Paginator
import json
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def index(request):
	exam_count = Exam_detail.objects.all().count()
	user_reg_count = User.objects.all().count()
	result_count = Result.objects.all().count()
	fac_count = Faculty.objects.all().count()
	labels = []
	data = []
	# queryset = Result.objects.filter(reg_id = Registration.objects.filter(user_id = request.user.id))
	# For Bar Chart
	queryset = Result.objects.filter(user_id=User.objects.get(pk=int(request.user.id)))
	for i in queryset:
		labels.append(str(i.exam_id.exam_name))
		data.append(i.total_marks)
	# For Pie Chart
	labels1 = []
	data1 = []
	a = Student_Model.objects.all()
	a1 = Course.objects.all()
	for i in a1:
		labels1.append(i.course_name)
	for i in a1:
		c = 0
		for j in a:
			if i.course_name == j.course:
				c = c + 1
		data1.append(c)
	context = {'exam_count':exam_count,'user_reg_count':user_reg_count,'result_count':result_count,'fac_count':fac_count,'data':data,'labels':labels,'data1':data1,'labels1':labels1}
	return render(request,'oes/student_dashboard.html',context)

@login_required(login_url='/')
def examinations(request):
	Final = dict()
	if(request.method == "POST" and request.POST.get('exam_id', False) != False):
		exam_id = request.POST.get('exam_id')
		id = request.user.id
		attem_left = int(Exam_detail.objects.get(id=exam_id).attempts_allowed) - Registration.objects.filter(user_id=id, exam_id=exam_id).count()
		if (attem_left !=0):
			temp = Registration()
			temp.user_id = User.objects.get(id=id)
			temp.exam_id = Exam_detail.objects.get(id = exam_id)
			temp.attempt_no = Registration.objects.filter(user_id=temp.user_id, exam_id=temp.exam_id).count() + 1
			temp.save()
			Final["message"] = "Applied for registration successfully!!"
	exams = []
	for i in Exam_detail.objects.filter(status="0").all():
		tmpdct = dict()
		tmpdct["id"] = i.id
		tmpdct["exam_name"] = i.exam_name
		tmpdct["description"] = i.description
		tmpdct["course_name"] = i.course_id.course_name
		tmpdct["year"] = i.year
		user_id = request.user.id
		exam_id = i
		tmpdct["attempts_left"] = int(i.attempts_allowed) - Registration.objects.filter(user_id=user_id,
																						exam_id=exam_id).count()
		exams.append(tmpdct)
	Final["exams"] = exams
	return render(request, 'oes/examinations.html', Final)
	#e = Exam_detail.objects.all()
	#return render(request,'oes/examinations.html',{'exams':e})

@login_required(login_url='/')
def approved_exams(request):
	Final = []
	for i in Registration.objects.filter(user_id=User.objects.get(pk=int(request.user.id)), registered=1):
		exams = dict()
		exams["registration_id"] = i.id
		exams["exam_id"] = i.exam_id.id
		exams["exam_name"] = i.exam_id.exam_name
		#exams["exam_status"] = i.exam_id.status
		exams["start_time"] = i.exam_id.start_time
		exams["end_time"] = i.exam_id.end_time
		exams["course_name"] = i.exam_id.course_id.course_name
		exams["description"] = i.exam_id.description
		exams["attempt_no"] = i.attempt_no
		exams["no_of_questions"] = i.exam_id.no_of_questions
		exams["pass_percentage"] = i.exam_id.pass_percentage
		start_time = i.exam_id.start_time
		end_time = i.exam_id.end_time
		if (start_time <= timezone.now() and end_time >= timezone.now() and i.answered == 0 and i.registered == 1):
			exams["attemptable"] = 1
		else:
			exams["attemptable"] = 0
		Final.append(exams)
	return render(request, 'oes/approved_exams.html',{"exams": Final, "current_time": datetime.datetime.now()})

@login_required(login_url='/')
def instructions(request,pk):
	c = Registration.objects.filter(pk=pk)
	d = Registration.objects.get(pk=pk)
	if d.answered == 0:
		return render(request,"oes/instructions.html",{'c':c})
	else:
		return render(request,"oes/student_dashboard.html")

@login_required(login_url='/')
def questions(request,pk,pk1):
	q = Exam_detail.objects.filter(pk=pk)
	w = Registration.objects.filter(pk=pk1)
	for i in w:
		a = i.answered
	if a == 0:
		for i in Exam_detail.objects.filter(pk=pk):
			exams = dict()
			#exams["exam_status"] = i.exam_id.status
			exams["exam_id"] = i.id
			exams["start_time"] = i.start_time
			exams["end_time"] = i.end_time
			exams["no_of_questions"] = i.no_of_questions
			exams["pass_percentage"] = i.pass_percentage
			#start_time = i.start_time
			end_time = i.end_time

		x = end_time-timezone.now()
		time_diff = x.total_seconds()
		p = Exam_detail.objects.get(pk=pk)
		j = Question_bank.objects.filter(exam_id=p)
		my_model = Question_bank.objects.filter(exam_id=p)
		paginatorr = Paginator(my_model, 1)
		que_count = paginatorr.count
		page_range = paginatorr.page_range
		context = {'j': j,'q':q, 'w':w, 'time':time_diff, 'page_range': page_range}
		return render(request, 'oes/questions.html', context)
	else:
		return render(request, 'oes/student_dashboard.html')

@login_required(login_url='/')
def res(request):
	if request.method == "POST":
		optedOptions = request.POST.getlist('optedOptions[]')
		exam_id = request.POST.get('exam_id')
		reg_id = request.POST.get('reg_id')
		attempted = request.POST.get('att')
		w = Registration.objects.get(pk=reg_id)
		if w.answered == 0:
			w.answered = 1
			w.save()
			q_id = Question_bank.objects.filter(exam_id=exam_id)
			ans = list()
			mk = list()
			for i in q_id:
				ans.append(i.answer)
				mk.append(i.marks)
			tot_marks = 0
			c = 0
			right_ans = 0
			count = 0 #null or unattempted
			wrong = 0
			for x, y in zip(optedOptions, ans):
				if x == y:
					tot_marks = tot_marks + mk[c]
					right_ans = right_ans + 1
				elif x == "":
					count = count + 1
				else:
					wrong = wrong + 1
				c = c + 1
			w = wrong * (.25)
			tot_marks = tot_marks - w
			#print(tot_marks)
			p = Result.objects.create(user_id=User.objects.get(pk=int(request.user.id)),reg_id_id=reg_id,exam_id_id=exam_id)
			#p = reg_id
			#p.exam_id = exam_id
			p.no_ques_attempt = int(attempted)
			p.no_ques_unattempt = count
			p.no_ques_right = right_ans
			p.no_ques_wrong = wrong
			p.total_marks = tot_marks
			p.save()
			print(p.total_marks)
			#p.exam_id = exam_id
		return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")

@login_required(login_url='/')
def result(request,pk,pk1):
	context = Result.objects.filter(reg_id=pk,exam_id=pk1)
	ques = Question_bank.objects.filter(exam_id=pk1)
	return render(request,'oes/result.html',{'context':context,'ques':ques})

@login_required(login_url='/')
def result_analysis(request):
	labels = []
	data = []
	#queryset = Result.objects.filter(reg_id = Registration.objects.filter(user_id = request.user.id))
	queryset = Result.objects.filter(user_id =User.objects.get(pk=int(request.user.id)))
	Final = []
	for i in queryset:
		labels.append(str(i.created.date()))
		data.append(i.total_marks)
	for i in Result.objects.filter(user_id=User.objects.get(pk=int(request.user.id))):
		res = dict()
		print("Hello")
		res["exam_name"] = i.exam_id.exam_name
		res["course_name"] = i.exam_id.course_id.course_name
		res["semester"] = i.exam_id.semester
		res["year"] = i.exam_id.year
		res["attempt_no"] = i.reg_id.attempt_no
		res["no_of_questions"] = i.exam_id.no_of_questions
		res["marks_obtained"] = i.total_marks
		res["pass_percentage"] = i.exam_id.pass_percentage
		res["attempted"] = i.no_ques_attempt
		res["right_answers"] = i.no_ques_right
		res["wrong_answers"] = i.no_ques_wrong
		Final.append(res)
	labels = []
	data = []
	# queryset = Result.objects.filter(reg_id = Registration.objects.filter(user_id = request.user.id))
	# For Bar Chart
	queryset = Result.objects.filter(user_id=User.objects.get(pk=int(request.user.id)))
	for i in queryset:
		labels.append(str(i.exam_id.exam_name))
		data.append(i.total_marks)
	# For Pie Chart
	labels1 = []
	data1 = []
	a = Student_Model.objects.all()
	a1 = Course.objects.all()
	for i in a1:
		labels1.append(i.course_name)
	for i in a1:
		c = 0
		for j in a:
			if i.course_name == j.course:
				c = c + 1
		data1.append(c)
	return render(request, 'oes/result_analysis.html',{'labels': labels,'data': data,'res':Final,'data1':data1,'labels1':labels1})

@login_required(login_url='/')
def user_registration(request):
	labels = []
	data = []
	queryset = User.objects.all()
	count = 0
	for i in queryset:
		labels.append(str(i.date_joined.date()))
		for j in queryset:
			if j.date_joined.date() == i.date_joined.date():
				count = count + 1
		data.append(count)
		count = 0
	from django.db.models import Count
	a = User.objects.all().extra({'date_created' : "date(date_joined)"}).values('date_created').annotate(created_count=Count('id'))
	for k in a:
		print(a)

	return render(request,'oes/stu_dash_user_registration.html',{'data':data,'labels':labels})

def faculty_dashboard(request):
	if 'name' in request.session:
		exam_count = Exam_detail.objects.all().count()
		user_reg_count = Registration.objects.filter(registered = 0).count()
		user_count = User.objects.all().count()
		fac_count = Faculty.objects.all().count()
		result_count = Result.objects.all().count()
		#----------------Chart area------------------------------------------------------
		labels = []
		data = []
		# queryset = Result.objects.filter(reg_id = Registration.objects.filter(user_id = request.user.id))
		# For Bar Chart
		queryset = Result.objects.all()
		queryset1 = Exam_detail.objects.all()
		for i in queryset1:
			labels.append(i.exam_name)
		for i in queryset1:
			c = 0
			for j in queryset:
				if i.exam_name == j.exam_id.exam_name:
					c = c + 1
			data.append(c)
		# For Pie Chart
		labels1 = []
		data1 = []
		a = Student_Model.objects.all()
		a1 = Course.objects.all()
		for i in a1:
			labels1.append(i.course_name)
		for i in a1:
			c = 0
			for j in a:
				if i.course_name == j.course:
					c = c + 1
			data1.append(c)
		context = {'labels': labels, 'data': data, 'labels1': labels1, 'data1': data1}
		#-----------------------------------------------------------------------------------
		context = {'exam_count': exam_count, 'user_reg_count': user_reg_count,'user_count': user_count,'fac_count': fac_count, 'result_count': result_count,'labels': labels, 'data': data, 'labels1': labels1, 'data1': data1}
		return render(request,'oes/faculty_dashboard.html',context)
	else:
		return redirect('/')

def fac_logout(request):
	if 'name' in request.session:
		del request.session['name']
		return redirect('/')
	else:
		return redirect('/')

def progress(request):
	if 'name' in request.session:
		labels = []
		data = []
		# queryset = Result.objects.filter(reg_id = Registration.objects.filter(user_id = request.user.id))
		# For Bar Chart
		queryset = Result.objects.all()
		queryset1 = Exam_detail.objects.all()
		for i in queryset1:
			labels.append(i.exam_name)
		for i in queryset1:
			c = 0
			for j in queryset:
				if i.exam_name == j.exam_id.exam_name:
					c = c + 1
			data.append(c)
		#For Pie Chart
		labels1 = []
		data1 = []
		a = Student_Model.objects.all()
		a1 = Course.objects.all()
		for i in a1:
			labels1.append(i.course_name)
		for i in a1:
			c = 0
			for j in a:
				if i.course_name == j.course:
					c = c + 1
			data1.append(c)
		context = {'labels': labels, 'data': data, 'labels1':labels1,'data1':data1}
		return render(request, 'oes/progress.html', context)
	else:
		return redirect('/')

def fac_exam_registration(request):
	if 'name' in request.session:
		message = ""
		reg = Registration.objects.all().order_by('-registered_time')
		reg_count = Registration.objects.filter(registered = 0).count()
		if(request.method == "POST" and request.POST.get('exam_id', False) != False and request.POST.get('reg_id', False) != False):
			id = request.POST.get('reg_id')
			exam_id = request.POST.get('exam_id')
			a = Registration.objects.get(id=id, exam_id=exam_id)
			a.registered = 1
			a.save()
			message = "Approved !"
		return render(request,'oes/fac_exam_registration.html',{'reg':reg,'reg_count':reg_count,'message':message})
	else:
		return redirect('/')


def fac_examinations(request):
	if 'name' in request.session:
		exams = Exam_detail.objects.all().order_by('-modified')
		exam_count = Exam_detail.objects.all().count()
		if (request.method == "POST" and request.POST.get('exam_id', False) != False and request.POST.get('reg_id',False) != False):
			id = request.POST.get('reg_id')
			exam_id = request.POST.get('exam_id')
			a = Registration.objects.get(id=id, exam_id=exam_id)
			a.registered = 1
			a.save()
		return render(request,'oes/fac_examinations.html',{'exams':exams,'exam_count':exam_count})
	else:
		return redirect('/')

class Ex_view(CreateView):
	model = Exam_detail
	template_name = 'oes/create.html'
	fields = ['exam_name','description','no_of_questions','attempts_allowed','pass_percentage','start_time','end_time','course_id','semester','year']
	success_url = '/oes/fac_examinations/'

class Ex_update_view(UpdateView):
	model = Exam_detail
	template_name = 'oes/update.html'
	fields = ['exam_name','description','no_of_questions','attempts_allowed','pass_percentage','start_time','end_time','course_id','semester','year']
	success_url = '/oes/fac_examinations/'

class Ex_delete_view(DeleteView):
	model = Exam_detail
	success_url = '/oes/fac_examinations/'