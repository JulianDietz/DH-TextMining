# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from jsonschema import Draft4Validator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from os.path import join

import json

currentJsonfiles=[]

# Get-Methode lädt die Seite zum Hochladen der JSON-Dateien, POST-Methode validiert und gibt Ergebnisse der Validation zurück
def uploadFiles(request):
    if request.method == 'GET':
        return render(request, 'upload/upload.html')

    if request.method == 'POST':
        global currentJsonfiles
        validPaper = []
        invalidPaper = []
        json_data = open("./static/jsonSchema/Paperschema.json", "r")
        schema = json.load(json_data)
        v = Draft4Validator(schema)
        for uploadfile in request.FILES.getlist('JsonPaper'):
            jsondata=json.loads(uploadfile.read().decode('utf-8'))
            currentJsonfiles.append({'name':uploadfile.name,'file':jsondata})
            if v.is_valid(jsondata):
                validPaper.append(uploadfile)
            else:
                errors=[]
                for error in sorted(v.iter_errors(jsondata), key=str):
                    errors.append(error)
                invalidPaper.append({'filename':uploadfile,'data': json.dumps(jsondata),'errors':errors})

        testfiles=None
        context={'validPaper':validPaper,'invalidPaper':invalidPaper,'filestest':testfiles}
        return render(request, 'upload/uploadSummary.html', context)

# Schreibt hochgeladene Files in Ordner zum upload
def completeUpload(request):
    if request.method == 'GET':
        global currentJsonfiles
        readpath = "./static/uploadFiles"
        for jsonfile in currentJsonfiles:
            file = open(join(readpath,jsonfile['name']), 'w', encoding="utf-8")
            json.dump(jsonfile['file'], file, ensure_ascii=False)
        currentJsonfiles=[]
        return redirect('readJsonFilesView')

# Wird beim Ausbessern der invaliden Paper verwendet
@csrf_exempt
def uploadImprovedPaper(request):
    if request.method == 'POST':
        global currentJsonfiles
        filename=request.POST.get('filename')
        response = {}
        filedata=request.POST.get('file')
        jsondata = json.loads(filedata)
        json_data = open("./static/jsonSchema/Paperschema.json", "r")
        schema = json.load(json_data)
        v = Draft4Validator(schema)

        if v.is_valid(jsondata):
            response['valid'] = 'true'
            response['filename'] = filename
            currentJsonfiles.append({'name': filename, 'file': jsondata})
        else:
            response['valid'] = 'false'
            response['errors'] = []
            for error in sorted(v.iter_errors(jsondata), key=str):
                response['errors'].append(str(error))
                print(error)
            response['filename'] = filename
            response['data'] = jsondata

        return JsonResponse(response)

