from os import kill
import signal
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.conf import settings
from pathlib import Path

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
    
       


class api(APIView):
    def get(self, request):
        # Lógica de la función GET
        #reiniciar_programa()
        return JsonResponse({'message': 'Configuraciones modificadas y programa reiniciado.'})

    def post(self, request):
        # Lógica de la función POST
        iniciar_programa()
        return Response("¡Hola desde la función POST!")

    def put(self, request, pk=None):
        # Lógica de la función PUT
        return Response("¡Hola desde la función PUT!")

    def delete(self, request, pk=None):
        # Lógica de la función DELETE
        return Response("¡Hola desde la función DELETE!")