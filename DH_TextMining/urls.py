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
    path('textMining/helloWorld/', views.helloWorld),
    path('textMining/upload/', views.uploadFiles, name='upload'),
    path('textMining/uploadImprovedPaperAjax/', views.uploadImprovedPaper, name="improvedPaper"),
    path('textMining/completeUpload/', views.completeUpload, name='completeUpload'),
    path('textMining/readPaperView/', views.readJsonFilesView , name='readJsonFilesView'),
    path('textMining/processPaperView/', views.processPaperView, name='processPaperView'),
    path('textMining/results/', views.results, name='results'),


    #ajax read .json files
    path('textMining/readPaper/', views.readJsonFiles , name='readJsonFiles'),
    path('textMining/processPaper/', views.processPaper , name='processPaper'),
    path('textMining/test/', views.testMethode, name='test'),
]

'''
    #path('textMining/<int:pk>/', views.changeCategory),

    path('textMining/calculateMetriken/', generalviews.calculateMetriken),

    path('textMining/calculateFreqWords/', generalviews.calculateFreqWords),

    path('textMining', generalviews.showStartPage, name='home'),
    path('textMining/vergleich/', generalviews.showVergleichPage, name='vergleich'),
    path('textMining/results/', generalviews.showResults, name='results'),


    path('textMining/results/download/', downloadviews.downloadResults, name='download'),
    #path('textMining/results/download/', downloadviews.downloadResults2, name='download2'),


    path('textMining/ajax/categorie', generalviews.ajaxCategorie, name='ajaxCateogrie'),
    path('textMining/ajax/categorie', generalviews.ajaxAuthor, name='ajaxAuthor'),

'''