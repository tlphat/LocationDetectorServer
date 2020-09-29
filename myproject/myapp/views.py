from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from myapp.forms import AndroidForm
from django.views.decorators.csrf import csrf_exempt
import base64
import json

# Create your views here.
# def home(request):
#     return HttpResponse("Hello World")

# def add(request):
#     if request.method == 'GET':
#         a = float(request.GET['a'])
#         b = float(request.GET['b'])
#         c = a + b 
#         return HttpResponse(str(c))
#     else:
#         return HttpResponse('method not supported')

@csrf_exempt
def android_image_view(request):
    if request.method == 'POST':
        form = AndroidForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('successfully uploaded')
        return HttpResponse('form error')
    else:
        return HttpResponse('method not supported')

def retrieve_image(request):
    if request.method == 'GET':
        name = 'media/images/' + str(request.GET['name'])
        image_data = ''
        with open(name, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        image_file.close()
        return HttpResponse(image_data)
    else:
        return HttpResponse('method not supported')

def success(request): 
    return HttpResponse('successfully uploaded')

def retrieve_location_json(request):
    data = {}
    with open('res/location.json') as json_file:
        data = json.load(json_file)
    return HttpResponse(json.dumps(data), content_type="application/json")