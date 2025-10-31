from django.urls import path
from OTS.views import *

urlpatterns = [
    path("",welcome,name="welcome"),
    path("new-candidate/",candidateRegistrationForm,name="registrationForm"),
    path("store-candidate/",candidateRegistration,name="storeCandidate"),
    path("login/",loginView,name="login"),
    path("home/",candidateHome, name="home"),
    path("test-paper/",testPaper, name="testPaper"),
    path("calculate-result/",calculateTestResult, name="calculateResult"),
    path("test-history/",testResultHistory, name="testHistory"),
    path("result/",showTestResult, name="testResult"),
    path("logout/",logoutView, name="logout"),
]