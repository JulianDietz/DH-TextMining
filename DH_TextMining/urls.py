"""DH_TextMining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path

from DH_TextMining import settings
from TextMining import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.redirect_view),
    path('textMining/upload/', views.uploadFiles, name='upload'),
    path('textMining/uploadImprovedPaperAjax/', views.uploadImprovedPaper, name="improvedPaper"),
    path('textMining/completeUpload/', views.completeUpload, name='completeUpload'),
    path('textMining/readPaperView/', views.readJsonFilesView, name='readJsonFilesView'),
    path('textMining/processPaperView/', views.processPaperView, name='processPaperView'),
    path('textMining/corpusSelection/', views.corpusSelection, name='corpusSelection'),
    path('textMining/getSelectedPaper/', views.getSelectedPaper, name='getSelectedPaper'),
    path('textMining/results/', views.startAnalyse, name='startAnalyse'),
    path('textMining/info/', views.showInfo, name='info'),

    # ajax read .json files
    path('textMining/readPaper/', views.readJsonFiles, name='readJsonFiles'),
    path('textMining/processPaper/', views.processPaper, name='processPaper'),
    path('textMining/getCalculation/', views.calculateMetrik, name='calculateMetrik'),
    path('textMining/downloadCorpus/<str:Corpus>', views.downloadResults, name='downloadKorpus'),

    # test
    path('textMining/test/', views.testMethode, name='test'),
]
