from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from .models import student,CustomUser, EnrollCourse
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.
def homepage(request):
	return render(
			request,
			'main/home.html'
		)

def s_list(batch, dept):
        st_list=[]
        s = student.objects.filter(batch = batch, dept=dept).values('first_name', 'last_name')
        for st in s:
            st_list.append({"name" : st['first_name']+" "+ st['last_name'], "children":[]})

        return st_list



def graph(request):

    '''
    dept = student.objects.all().values('dept').distinct()
    dept_name = [item["dept"] for item in dept]

    dept_dict_list = [{ "name": "Department", "parent": "null" }]
    

    for d in dept_name:

        dept_dict_list.append(  { "name" : d, "parent" : "Department" } )
        t = EnrollCourse.objects.filter(dept=d).values('teacher').distinct()
        
        for teacher in t:
            teacher_name = teacher['teacher']
            dept_dict_list.append( { "name": teacher_name, "parent": d } )
            s = EnrollCourse.objects.filter(teacher = teacher_name).values('session').distinct()

            for session in s:
                session_year = session['session']
                dept_dict_list.append( { "name": session_year, "parent": teacher_name } )
                b = EnrollCourse.objects.filter(teacher = teacher_name, session = session_year).values('batch').distinct()

                for batch in b:
                    batch_year = batch['batch']+"batch"
                    dept_dict_list.append( { "name": batch_year, "parent": session_year } )

        '''
    dept = student.objects.all().values('dept').distinct()
    dept_name = [item["dept"] for item in dept]
    dept_teacher=[]
    dept_session=[]
    dept_batch=[]
    for d in dept_name:
        t = EnrollCourse.objects.filter(dept=d).values('teacher').distinct()
        for teacher in t:
            teacher_name = teacher['teacher']
            dept_teacher.append({d:teacher['teacher']})
            s = EnrollCourse.objects.filter(teacher = teacher_name).values('session').distinct()
            for session in s:
                session_year = session['session']
                dept_session.append({session['session']:{d:teacher['teacher']}})
                b = EnrollCourse.objects.filter(teacher = teacher_name, session = session_year).values('batch').distinct()
                for batch in b:
                    dept_batch.append({batch['batch']:{session['session']:{d:teacher['teacher']}}})


        
    


    dept_dict_list = []

    dept_dict_list = [{"name":"Department","children":
                            [{"name":d, "children": 
                                    [{"name":t[d],"children":
                                        [{"name":"session: "+list(s.keys())[0], "children":
                                            [ {"name":"batch: "+list(b.keys())[0] , "children":
                                                s_list(list(b.keys())[0], d)} for b in dept_batch for b_key, b_value in b.items() for key in b_value if key==list(s.keys())[0] for b1_key,b1_value in b_value.items() for n_key in b1_value if b1_value[n_key]==t[d] ]} for s in dept_session for s_key, s_value in s.items() for key in s_value if s_value[key]==t[d] ] }  for t in dept_teacher if list(t.keys())[0]==d ]} for d in dept_name]}]
    '''
  
    dept_dict_list = [{"name":"Department","children":
                            [{"name":d, "children": 
                                    [{"name":t[d],"children":
                                            [{"name":s['session'],"children":b['batch']} for s in dept_session if  for b in EnrollCourse.objects.filter(teacher = t['teacher'], session = s['session']).values('batch').distinct()] }  for t in dept_teacher if t.keys()==d ]} for d in dept]}]
    
    '''




    return render(
        request,
        "main/graph.html",
        {"dept_dict_list" : dept_dict_list[0]}
        
        )

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                dj_login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

@login_required
def cpanel(request):
	return render(
		request,
		"main/cpanel.html"
		)

@login_required
def add_student(request):

    if request.method == "POST":
        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('b_date') and request.POST.get('roll') and request.POST.get('dept') and request.POST.get('batch') :
            post=student()
            post.first_name= request.POST.get('first_name')
            post.last_name= request.POST.get('last_name')
            post.b_date= request.POST.get('b_date')
            post.roll= request.POST.get('roll')
            post.dept= request.POST.get('dept')
            post.batch= request.POST.get('batch')

            post.save()
            messages.info(request, f"Data inserted for { request.POST.get('first_name') }")
        else:
            messages.error(request, "Please Fill Up all the Fields")

            
    return render(
        request,
        "main/add_student.html"
        )
    

def view_students(request):

    return render(
        request,
        "main/view_students.html"
        )

def list_students(request):

    current = datetime.now().date()

    all_students = student.objects.all()
    if request.method == "POST":
        search_id = request.POST.get('search_id')
        

    filter_id = student.objects.filter(roll = search_id)
    age = int( (current - filter_id[0].b_date ).days  / 365.25)

    return render(
        request,
        "main/list_students.html",
        {'all_students': filter_id, 'age' : age}
        )


@login_required
def enroll_course(request):
   

    if request.method == "POST":
        dept = request.POST.get('dept')
        crs_teacher = request.POST.get('crs_teacher')
        batch = request.POST.get('batch')
        session = request.POST.get('session')
        if dept and crs_teacher and batch and session  :
            existence = EnrollCourse.objects.filter(dept = dept, session = session, batch = batch).count()
            if existence == 0:
                post=EnrollCourse()
                post.teacher= request.POST.get('crs_teacher')
                post.session= request.POST.get('session')
              
                post.dept= request.POST.get('dept')
                post.batch= request.POST.get('batch')

                post.save()
                messages.info(request, f"Data inserted for { request.POST.get('crs_teacher') }")
            else:
                messages.error(request, dept +" "+ batch + " batch is allready assigned in session " + session)
        else:
            messages.error(request, "Please Fill Up all the Fields")
    current_date = datetime.now().year
    return render(
        request,
        "main/enroll_course.html",
        {"current_date" : current_date}
        )



@login_required
def view_enrolled_course(request):
    uniq_dept =  EnrollCourse.objects.values('dept').distinct()
    return render(
        request,
        "main/view_enrolled_course.html",
        {"uniq_dept":uniq_dept}
        )


@login_required
def fetch_teacher(request):
    all_teachers = CustomUser.objects.all()

    if request.method == "POST":
        selectedDept = request.POST.get('selectedDept')
        

    filter_teacher = CustomUser.objects.filter(dept = selectedDept, userRole = 'teacher')

    return render(
        request,
        "main/fetch_teacher.html",
        {'all_teachers': filter_teacher}
        )

@login_required
def account(request):
    return render(request,'main/account.html',{'user':request.user})   


@login_required
def fetch_enrolled_teacher(request):

    if request.method == "POST":
        selectedDept = request.POST.get('selectedDept')
        

    filter_teacher = EnrollCourse.objects.filter(dept = selectedDept).values('teacher').distinct()

    return render(
        request,
        "main/fetch_enrolled_teacher.html",
        {'all_enrolled_teachers': filter_teacher}
        )

@login_required
def fetch_enrolled_session(request):

    if request.method == "POST":
        crs_teacher = request.POST.get('crs_teacher')
        

    filter_session = EnrollCourse.objects.filter(teacher = crs_teacher).values('session').distinct()

    return render(
        request,
        "main/fetch_enrolled_session.html",
        {'all_enrolled_session': filter_session}
        )

@login_required
def fetch_enrolled_batch(request):

    if request.method == "POST":
        crs_teacher = request.POST.get('crs_teacher')
        session = request.POST.get('session')
        

    filter_batch = EnrollCourse.objects.filter(teacher = crs_teacher, session = session).values('batch').distinct()

    return render(
        request,
        "main/fetch_enrolled_batch.html",
        {'all_enrolled_batch': filter_batch}
        )

@login_required
def view_enrolled_student(request):
    if request.method == "POST":
        selectedDept = request.POST.get('dept')
        selectedBatch = request.POST.get('batch')

        filter_student = student.objects.filter(batch = selectedBatch, dept = selectedDept)
        

    return render(request,
        'main/view_enrolled_student.html',
         {'all_enrolled_student': filter_student}
        )   

