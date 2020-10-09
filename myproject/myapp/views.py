import math
import json
import base64
import subprocess
from pathlib import Path

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from myapp.forms import AndroidForm
from myapp.models import ServerInfo, ImageNode

from PIL import Image

from src.match_images import match_image
from src.extract_features import extract_features

# Create your views here.
class ImageList(ListView):
    model = ImageNode

def get_features(request):
    server_info = ServerInfo.objects.all().first()
    return JsonResponse({"version": str(server_info.version)})

@csrf_exempt
def images_handler(request):
    if request.method == 'GET':
        all_images = ImageNode.objects.all()
        response = []
        for image in all_images:
            with open(image.thumbnail.path, 'rb') as f:
                data = f.read()
                thumbnail_encoded = base64.b64encode(data).decode('utf-8')
            response.append({"id": image.id, "name": Path(image.image.path).name, "thumbnail": thumbnail_encoded})
        return JsonResponse(response, safe=False)
    elif request.method == 'POST':
        form = AndroidForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"id": ImageNode.objects.all().last().id}, status=201)
        print("Upload form error!")
        return HttpResponse('form error', status=400)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

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
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def find_location(request, id):
    if request.method == 'GET':
        print(f"Finding location of image id {id}")

        scores = []
        locations = []
        for location_path in Path("locations").iterdir():
            imgs_to_extract = []
            for img_path in location_path.iterdir():
                feature_path = img_path.parent / (img_path.stem + '.delf')
                if not feature_path.exists():
                    img = Image.open(img_path)

                    h, w = img.size
                    if max(h, w) > 1024:
                        factor = 1024 / max(h, w) 
                        img = img.resize((int(h * factor), int(w * factor)))
                        img.save(img_path)

                    imgs_to_extract.append(img_path)
            
            if len(imgs_to_extract) > 0:
                extract_features(imgs_to_extract, location_path)

            locations.append({
                "name": location_path.name,
                "images": [img_path for img_path in location_path.iterdir() if not img_path.suffix == '.delf'],
                "features": [img_path for img_path in location_path.iterdir() if img_path.suffix == '.delf']
            })

        query_image = ImageNode.objects.get(id=id)
        with Image.open(query_image.image.path) as img:
            h, w = img.size
            if max(h, w) > 1024:
                factor = 1024 / max(h, w) 
                img = img.resize((int(h * factor), int(w * factor)))
                img_name = Path(query_image.image.path).name
                img.save("tmp\\query\\" + img_name)
                extract_features([r"tmp\query\\" + img_name], r"tmp\query")
            else: 
                extract_features([query_image.image.path], r"tmp\query")

        loc_scores = []
        for location_dict in locations:
            img_scores = []
            for img_path, feature_path in zip(location_dict["images"], location_dict["features"]):
                print(f"Matching with {img_path}")
                score = match_image(str(feature_path), str(Path("tmp") / "query" / (Path(query_image.image.path).stem + ".delf")))
                img_scores.append(score)
            loc_scores.append(sum(img_scores) / len(img_scores))

        max_score = max(loc_scores)
        if max_score < 50:
            return HttpResponseNotFound()
        else:
            for i, score in enumerate(loc_scores):
                if math.isclose(score, max_score):
                    print(f"Response = {locations[i]['name']}")
                    return HttpResponse("notradame")
    else:
        return HttpResponseNotAllowed(['GET'])

def retrieve_location_json(request):
    data = {}
    with open('res/location.json') as json_file:
        data = json.load(json_file)
    return HttpResponse(json.dumps(data), content_type="application/json")