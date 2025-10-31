from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from OTS.models import * 
from django.urls import reverse
import random

# Create your views here.

def welcome(request):
    template = loader.get_template("welcome.html")
    return HttpResponse(template.render())

def candidateRegistrationForm(request):
    res=render(request,"registrationForm.html")
    return res

def candidateRegistration(request):
    if request.method == "POST":
        username = request.POST['username']
        # check if username already exists
        if (len(Candidate.objects.filter(username=username))):
            userStatus = 1
        else:
            candidate = Candidate()
            candidate.username = username
            candidate.password = request.POST['password']
            candidate.name = request.POST['fullname']
            candidate.save()
            userStatus = 2
    else:
        userStatus = 3 #Request method not POST
    context = {
            'userStatus': userStatus
        }
    res = render(request, "registrationStatus.html", context)
    return res
 
def loginView(request):
    if request.method == "POST":    
        username = request.POST['username']
        password = request.POST['password']
        candidate = Candidate.objects.filter(username=username, password=password)
        if len(candidate) == 0:
            loginError = "Invalid Username or Password"
            res = render(request, "login.html", {'loginError': loginError})
        
        else:
            # Successful Login
            request.session['username'] = candidate[0].username
            request.session['name'] = candidate[0].name
            res = HttpResponseRedirect(reverse("home"))

    else:        
        res = render(request, "login.html")
    return res

def candidateHome(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect(reverse("login"))
    
    else:
        res = render(request, "home.html")
    
    return res

def testPaper(request):
    if 'name' not in request.session.keys():
        res =  HttpResponseRedirect(reverse("login"))

    # fetch all questions from database table

    n=int(request.GET['n'])
    question_pool = list(Question.objects.all())
    random.shuffle(question_pool)
    questions_list = question_pool[:n]
    context = {'questions': questions_list}
    res = render(request, "test_paper.html", context)
    return res

def calculateTestResult(request):
    if 'name' not in request.session.keys():
        return HttpResponseRedirect(reverse("login"))
    
    total_attempt=0
    right_answers=0
    wrong_answers=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question=Question.objects.get(qid=n)
        try:
            if question.ans==request.POST['q'+str(n)]:
                right_answers+=1
            else:
                wrong_answers+=1
            total_attempt+=1
        except:
            pass

    points=(right_answers-wrong_answers)/len(qid_list)*10
    #store result in Result Table
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username'])
    result.attempt=total_attempt
    result.right=right_answers
    result.wrong=wrong_answers 
    result.points=points
    result.save()

    #update candidate table
    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted+=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted
    candidate.save()

    request.session['test_attempted'] = candidate.test_attempted
    request.session['points'] = round(candidate.points, 2)

    
    return HttpResponseRedirect(reverse("testResult"))

def testResultHistory(request):
    if 'name' not in request.session.keys():
        return HttpResponseRedirect(reverse("login"))
      
    #fetch all results from Result Table for the logged in user
    candidate = Candidate.objects.filter(username=request.session['username'])
    results = Result.objects.filter(username_id=candidate[0].username)
    context = {'candidate': candidate[0], 'results': results}
    res = render(request, "test_history.html", context)
    return res

def showTestResult(request):
    if 'name' not in request.session.keys():
        return HttpResponseRedirect(reverse("login"))
      
    #fetch latest result from Result Table
    result = Result.objects.filter(resultid=Result.objects.latest('resultid').resultid, username_id=request.session['username'])
    context = {'result': result}
    res = render(request, "result.html", context)
    return res

def logoutView(request):
    request.session.flush() # saare session data delete kar dega
    return HttpResponseRedirect(reverse("login")) # logout ke baad login page par redirect


    # if 'name' in request.session.keys():
    #     del request.session['username']
    #     del request.session['name']
    # return HttpResponseRedirect(reverse("login"))
