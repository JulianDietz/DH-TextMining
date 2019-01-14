# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render
import json
from jsonschema import Draft4Validator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from TextMining.saveFile import savePaper

currentJsonfiles=[]

def uploadFiles(request):
    if request.method == 'GET':
        return render(request, 'upload/upload.html')

    if request.method == 'POST':
        global currentJsonfiles
        #print(request.FILES.getlist('JsonPaper'))
        validPaper = []
        invalidPaper = []
        json_data = open("Paperschema.json", "r")
        schema = json.load(json_data)
        v = Draft4Validator(schema)
        for uploadfile in request.FILES.getlist('JsonPaper'):
            print(uploadfile.name)
            jsondata=json.loads(uploadfile.read().decode('utf-8'))
            #print(jsondata)
            currentJsonfiles.append(jsondata)
            if v.is_valid(jsondata):
                validPaper.append(uploadfile)
                print("validFile:"+uploadfile.name)
            else:

                print("invalidFile:" + uploadfile.name)
                errors=[]
                for error in sorted(v.iter_errors(jsondata), key=str):
                    errors.append(error)
                    #print(error)
                #print(json.dumps(jsondata))
                invalidPaper.append({'filename':uploadfile,'data': json.dumps(jsondata),'errors':errors})

        #currentJsonfiles=request.FILES.getlist('JsonPaper')
        testfiles=None
        context={'validPaper':validPaper,'invalidPaper':invalidPaper,'filestest':testfiles}
        return render(request, 'upload/uploadSummary.html', context)

def completeUpload(request):
    if request.method == 'GET':
        global currentJsonfiles
        #print("Jsonfiles")
        #print(currentJsonfiles)
        for jsonfile in currentJsonfiles:
            print(jsonfile)
            #savePaper(jsonfile)
        currentJsonfiles=[]
        print("Alle files sollen jetzt gespeichert werden")
        return render(request, 'helloWorld.html')


@csrf_exempt
def uploadImprovedPaper(request):
    if request.method == 'POST':
        global currentJsonfiles
        print(request.POST)
        filename=request.POST.get('filename')
        response = {}
        filedata=request.POST.get('file')
        jsondata = json.loads(filedata)
        json_data = open("Paperschema.json", "r")
        schema = json.load(json_data)
        v = Draft4Validator(schema)

        if v.is_valid(jsondata):
            print("validFile:" + filename)
            response['valid'] = 'true'
            response['filename'] = filename
            currentJsonfiles.append(jsondata)
        else:
            print("invalidFile:" + filename)
            response['valid'] = 'false'
            response['errors'] = []
            for error in sorted(v.iter_errors(jsondata), key=str):
                response['errors'].append(str(error))
                print(error)
            response['filename'] = filename
            response['data'] = jsondata
            #response['errors'] = errors

        return JsonResponse(response)

