from os import kill
import signal
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.conf import settings
from pathlib import Path
import os
import shutil
import zipfile
from django.http import HttpResponse
from django.conf import settings

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class restartGateway(APIView):
    def get(self, request):

        with open("process.json") as file:
            data = json.load(file)
        kill(data["pid"], signal.SIGKILL)
        data["pid"] = 0
        new_program = subprocess.Popen(['python', '../main.py'])
        data["pid"] = new_program.pid
        data["state"] = True
        with open("process.json", "w") as file:
            json.dump(data, file)

        return JsonResponse({'message': 'Gateway reiniciado.'})
    

class activateGateway(APIView):
    def get(self, request):

        program = subprocess.Popen(['python', '../main.py'])
        with open("process.json") as file:
            data = json.load(file)
            data["pid"] = program.pid
            data["state"] = True
        with open("process.json", "w") as file:
            json.dump(data, file)

        return JsonResponse({'state': True})
    
class deactivateGateway(APIView):
    def get(self, request):

        with open("process.json") as file:
            data = json.load(file)
        kill(data["pid"], signal.SIGKILL)
        data["pid"] = 0
        data["state"] = False
        with open("process.json", "w") as file:
            json.dump(data, file)

        return JsonResponse({'state': False})
    
class getStateGateway(APIView):
    def get(self, request):
        
        with open("process.json") as file:
            data = json.load(file)
        return JsonResponse({'state': data["state"]})

class getGateway(APIView):
    def get(self, request):
        cur_path = settings.BASE_DIR
        path = str(Path(cur_path, '../'))
        print(path)
        filepath = str(Path(cur_path, '../', 'allora_code/LoRa.json'))
        f = open(filepath)
        data = json.load(f)
        f.close()
        data = {
            "gateway": data
        }
        return JsonResponse(data)
    
class getNodes(APIView):
    def get(self, request):
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        f.close()
        data = {
            "nodes": data
        }
        return JsonResponse(data)
    
    def post(self, request):
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        for d in data:
            if d['name'] == request.POST.get('name'):
                return JsonResponse({"node": d})
        f.close()
        data = {
            "node": False
        }
        return JsonResponse(data)

class setActiveNode(APIView):
    def post(self, request):
        nodo = request.POST.get('nodo')
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        for d in data:
            if d['mac_address'] == nodo:
                d['active'] = not d['active']
                
                break

        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        f.close()
        data = {
            "nodes": data
        }
        return JsonResponse(data)

class setMeshNode(APIView):
    def post(self, request):
        nodo = request.POST.get('nodo')
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        for d in data:
            if d['mac_address'] == nodo:
                d['sleep_mesh'] = not d['sleep_mesh']
                break

        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        f.close()
        data = {
            "nodes": data
        }
        return JsonResponse(data)
    
class deleteNode(APIView):
    def post(self, request):
        nodo = request.POST.get('nodo')
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        for d in data:
            if d['mac_address'] == nodo:
                data.remove(d)
                break

        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        f.close()
        data = {
            "nodes": data
        }
        return JsonResponse(data)
    
class updateNode(APIView):
    def post(self, request):
        nodo = dict(request.data)

        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)

        for d in data:
            if d['name'] == nodo['name']:
                d['mac_address'] = nodo['mac_address']
                d['sleep_mesh'] = nodo['sleep_mesh']
                d['active'] = nodo['active']
                break
    
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

        data = {
            'nodes': data
        }
        return JsonResponse(data)
    
class addNode(APIView):
    def post(self, request):
        nodo = dict(request.data)

        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)

        nodo['name'] = nodo['name'][0]
        nodo['mac_address'] = nodo['mac_address'][0]
        if nodo['active'][0] == 'true':
            nodo['active'] = True
        elif nodo['active'][0] == 'false':
            nodo['active'] = False

        if nodo['sleep_mesh'][0] == 'true':
            nodo['sleep_mesh'] = True
        elif nodo['sleep_mesh'][0] == 'false':
            nodo['sleep_mesh'] = False

        data.append(nodo)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        data = {
            'nodes': data
        }
        return JsonResponse(data)

class getNode(APIView):
    def get(self, request):
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'allora_code/Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        name = request.POST.get('name')
        for d in data:
            if d['name'] == name:
                return JsonResponse({"node": d})
        return JsonResponse({"node": False})
    
class getData(APIView):
    def get(self, request):
        
        cur_path = settings.BASE_DIR
        ruta_carpeta = str(Path(cur_path, '../', 'allora_code/'))
        # Especifica la ruta de la carpeta que quieres explorar

        # Obtiene la lista de directorios dentro de la carpeta
        directorios = next(os.walk(ruta_carpeta))[1]
        mac_address = []
        # Imprime los nombres de los directorios
        for directorio in directorios:
            mac_address.append(directorio)
            print(directorio)
        data = {
            "mac_address": mac_address
        }
        return JsonResponse(data)

class downloadData(APIView):
    def get(self, request):

        # Nombre del archivo ZIP
        nombre_zip = 'carpeta_descargada.zip'
        cur_path = settings.BASE_DIR
        ruta_carpeta = str(Path(cur_path, '../', 'allora_code/9a76ba3f'))

        ruta_zip = os.path.join(settings.MEDIA_ROOT, nombre_zip)

        # Comprimir la carpeta en el archivo ZIP
        shutil.make_archive(ruta_zip[:-4], 'zip', ruta_carpeta)

        # Devolver la URL del archivo ZIP relativa al frontend
        url_zip = os.path.join(settings.MEDIA_URL, nombre_zip)
        return JsonResponse({'url_zip': url_zip})
    
class downloadDataNode(APIView):
    def get(self, request):
        node = request.POST.get('node')
        cur_path = settings.BASE_DIR
        ruta_json = str(Path(cur_path, '../', 'allora_code/'))
        ruta_json = ruta_json+'/'+(str(node))
        ruta_json = ruta_json+'/data.json'
        print(ruta_json)
        file = open(ruta_json)
        data = json.load(file)

        return JsonResponse(data)

class downloadAll(APIView):
    def get(self, request):
        print("holi")
        cur_path = settings.BASE_DIR
        ruta_carpeta = str(Path(cur_path, '../', 'allora_code/'))
        # Especifica la ruta de la carpeta que quieres explorar

        # Obtiene la lista de directorios dentro de la carpeta
        directorios = next(os.walk(ruta_carpeta))[1]
        data_all = []
        mac_address = []
        # Imprime los nombres de los directorios
        for directorio in directorios:
            mac_address.append(directorio)
            cur_path = settings.BASE_DIR
            ruta_json = str(Path(cur_path, '../', 'allora_code/'))
            ruta_json = ruta_json+'/'+(str(directorio))
            ruta_json = ruta_json+'/data.json'
            print(ruta_json)
            file = open(ruta_json)
            data = json.load(file)
            data_all.append(data)
        context = {
            "mac_address": mac_address,
            "data": data_all,
            
        }
        return JsonResponse(context)

class api(APIView):
    def get(self, request):
        # Lógica de la función GET
        #reiniciar_programa()
        return JsonResponse({'message': 'Configuraciones modificadas y programa reiniciado.'})

    def post(self, request):
        # Lógica de la función POST
        return Response("¡Hola desde la función POST!")

    def put(self, request, pk=None):
        # Lógica de la función PUT
        return Response("¡Hola desde la función PUT!")

    def delete(self, request, pk=None):
        # Lógica de la función DELETE
        return Response("¡Hola desde la función DELETE!")