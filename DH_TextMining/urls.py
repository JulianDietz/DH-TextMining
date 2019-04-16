"""DH_TextMining URL Configuration
"""
from django.urls import path
from TextMining import views

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
]
