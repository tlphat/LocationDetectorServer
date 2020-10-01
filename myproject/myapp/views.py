from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from myapp.forms import AndroidForm
from django.views.decorators.csrf import csrf_exempt
from myapp.models import ServerInfo, ImageNode
import json

# Create your views here.
# def home(request):
#     return HttpResponse("Hello World")

def get_features(request):
    server_info = ServerInfo.objects.all().first()
    return JsonResponse({"version": str(server_info.version)})

@csrf_exempt
def images_handler(request):
    if request.method == 'GET':
        all_images = ImageNode.objects.all()
        response = []
        for image in all_images:
            response.append({"id": image.id})
        return JsonResponse(response, safe=False)
    elif request.method == 'POST':
        form = AndroidForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"id": ImageNode.objects.all().last().id}, status=201)
        print("Upload form error!")
        return HttpResponse('form error', status=400)
    else:
        return HttpResponse('Method Not Supported', status=405)

@csrf_exempt
def images_detail(request, id):
    if request.method == 'GET':
        print(f"Requested image {id}")
        try:
            image = ImageNode.objects.get(id=id)
        except ImageNode.DoesNotExist:
            return HttpResponse("Image Not Found!", status=404)
        return FileResponse(image.image)
    else:
        return HttpResponse('Method Not Supported', status=405)

def success(request): 
    return HttpResponse('successfully uploaded')

def retrieve_location_json(request):
    data = {}
    with open('res/location.json') as json_file:
        data = json.load(json_file)
    return HttpResponse(json.dumps(data), content_type="application/json")