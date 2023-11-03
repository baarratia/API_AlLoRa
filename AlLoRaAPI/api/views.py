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
from django.http import HttpResponse
from django.conf import settings
import requests
from datetime import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class restartGateway(APIView):
    def get(self, request):

        with open("process.json") as file:
            data = json.load(file)
        if data["pid"] != 0:
            try:
                kill(data["pid"], signal.SIGKILL)
                data["pid"] = 0
            except ProcessLookupError as ex:
                print(f"Error al matar el proceso: {ex}")
            except Exception as ex:
                print(f"Otro error inesperado: {ex}")
        
        working_directory = '../'

        command = 'python3 main.py'  

        program = subprocess.Popen(command, shell=True, cwd=working_directory)

        with open("process.json") as file:
            data = json.load(file)
            data["pid"] = program.pid
            data["state"] = True
        with open("process.json", "w") as file:
            json.dump(data, file)

        return JsonResponse({'state': True})
    

class activateGateway(APIView):
    def get(self, request):

        working_directory = '../'

        command = 'python3 main.py'  

        program = subprocess.Popen(command, shell=True, cwd=working_directory)

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
        try:
            kill(data["pid"], signal.SIGKILL)
            data["pid"] = 0
        except ProcessLookupError as ex:
            print(f"Error al matar el proceso: {ex}")
        except Exception as ex:
            print(f"Otro error inesperado: {ex}")
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
        filepath = str(Path(cur_path, '../', 'LoRa.json'))
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
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        f.close()
        data = {
            "nodes": data
        }
        return JsonResponse(data)
    
    def post(self, request):
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
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
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
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
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
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
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
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
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
        f = open(filepath)
        data = json.load(f)

        for d in data:
            if d['name'] == nodo['name'][0]:
                d['mac_address'] = nodo['mac_address'][0]
                d['sleep_mesh'] = nodo['sleep_mesh'][0]
                d['active'] = nodo['active'][0]
                d['listening_time'] = nodo['listening_time'][0]
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
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
        f = open(filepath)
        data = json.load(f)

        nodo['name'] = nodo['name'][0]
        nodo['mac_address'] = nodo['mac_address'][0]
        nodo['listening_time'] = nodo['listening_time'][0]
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
        filepath = str(Path(cur_path, '../', 'Nodes.json'))
        f = open(filepath)
        data = json.load(f)
        mac_address = request.POST.get('mac_address')
        for d in data:
            if d['mac_address'] == mac_address:
                return JsonResponse({"node": d})
        return JsonResponse({"node": False})
    
class setSerialPort(APIView):
    def post(self, request):
        serial_port = request.POST.get('serial_port')
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'LoRa.json'))
        f = open(filepath)
        data = json.load(f)
        data['serial_port'] = serial_port
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        f.close()
        data = {
            "gateway": data
        }
        return JsonResponse(data)

class setResultPath(APIView):
    def post(self, request):
        result_path = request.POST.get('result_path')
        cur_path = settings.BASE_DIR
        filepath = str(Path(cur_path, '../', 'LoRa.json'))
        f = open(filepath)
        data = json.load(f)
        data['results_path'] = result_path
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        f.close()
        data = {
            "gateway": data
        }
        return JsonResponse(data)

    
class getData(APIView):
    def get(self, request):
        
        cur_path = settings.BASE_DIR
        ruta_carpeta = str(Path(cur_path, '../'))
        # Especifica la ruta de la carpeta que quieres explorar

        # Obtiene la lista de directorios dentro de la carpeta
        directorios = next(os.walk(ruta_carpeta))[1]
        mac_address = []
        # Imprime los nombres de los directorios
        for directorio in directorios:
            mac_address.append(directorio)
        data = {
            "mac_address": mac_address
        }
        return JsonResponse(data)

class downloadData(APIView):
    def get(self, request):

        # Nombre del archivo ZIP
        nombre_zip = 'carpeta_descargada.zip'
        cur_path = settings.BASE_DIR
        ruta_carpeta = str(Path(cur_path, '../', '9a76ba3f'))

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
        ruta_json = str(Path(cur_path, '../', ''))
        ruta_json = ruta_json+'/'+(str(node))
        ruta_json = ruta_json+'/data.json'
        file = open(ruta_json)
        data = json.load(file)

        return JsonResponse(data)

class downloadAll(APIView):
    def get(self, request):
        cur_path = settings.BASE_DIR
        ruta_carpeta = str(Path(cur_path, '../'))
        # Especifica la ruta de la carpeta que quieres explorar

        # Obtiene la lista de directorios dentro de la carpeta
        directorios = next(os.walk(ruta_carpeta))[1]
        data_all = []
        mac_address = []
        # Imprime los nombres de los directorios
        for directorio in directorios:
            mac_address.append(directorio)
            cur_path = settings.BASE_DIR
            ruta_json = str(Path(cur_path, '../'))
            
            ruta_json = ruta_json+'/'+(str(directorio))
            archivos = os.listdir(ruta_json)
            archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(ruta_json, archivo))]
            for archivo in archivos:
                
                file = open(ruta_json+'/'+archivo)
                data = json.load(file)
                data_all.append(data)
        context = {
            "mac_address": mac_address,
            "data": data_all,
        }
        return JsonResponse(context)
    
class writeInfluxdb(APIView):
    def post(self, request):
        
        text = ""
        cur_path = settings.BASE_DIR
        ruta_carpeta = str(Path(cur_path, '../'))

        # Obtiene la lista de directorios dentro de la carpeta
        directorios = next(os.walk(ruta_carpeta))[1]
        mac_address = []
        # Imprime los nombres de los directorios
        dict = {}
        for directorio in directorios:
            mac_address.append(directorio)

        for mac in mac_address:
            cur_path = settings.BASE_DIR
            ruta_json = str(Path(cur_path, '../'))
            ruta_json = ruta_json+'/'+(str(mac))
            archivos = next(os.walk(ruta_json))[2]
            dict[mac] = archivos
        
        #temperature,location=kitchen value=32.1
        #temperature,location=living value=10
        
        for mac in dict:
            
            if dict[mac] != []:
                
                for archivo in dict[mac]:
                    text = text + "sentiments,"
                    text = text + "mac_address=" + mac + " "
                    cur_path = settings.BASE_DIR
                    ruta_json = str(Path(cur_path, '../'))
                    ruta_json = ruta_json+'/'+(str(mac))
                    ruta_json = ruta_json+'/'+(str(archivo))
                    file = open(ruta_json)
                    data = json.load(file)
                    
                    for d in data:
                        if d == "timestamp":
                            pass
                        else:
                            text = text + d
                            text = text + "="
                            text = text + str(data[d])
                            text = text + ","
                    text = text[:-1]
                    
                    text = text + "\n"
        text = text.split('\n')

        #Auth:
        
        INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', '0')
        headers = {
            "Authorization": f"Token {INFLUXDB_TOKEN}",
        }
        response = requests.get("https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/", headers=headers)
    
        if response.status_code == 200:
            #Write:
            INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', '0')
            bucket_id = "ed4cdad145964fb2"
            org_id = "57e1f0c70382c0a2"
            headers = {
                "Authorization": f"Token {INFLUXDB_TOKEN}",
                "Content-Type": "text/plain"
            }
            for linea in text:
                response = requests.post(f"https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?bucket={bucket_id}&org={org_id}&precision=s", headers=headers, data=linea)
          
            return JsonResponse({'message': 'Datos escritos en InfluxDB.'})
        else:
            return JsonResponse({'message': 'No fue autorizado.'})
        
    
class getDataInfluxDB(APIView):
    def get(self, request):
        INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', '0')
        bucket_id = "ed4cdad145964fb2"
        org_id = "57e1f0c70382c0a2"
        headers = {
            "Authorization": f"Token {INFLUXDB_TOKEN}",
            "Content-Type": "applicacion/json"
        }

        data = {
            "query": "from(bucket: \"allora\")\n  |> range(start: -1d)\n  |> filter(fn: (r) => r[\"_measurement\"] == sentiments)"
        }
        response = requests.post(f"https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/query/analyze?orgID={org_id}", headers=headers, data=data)
        print(response.json())
        return JsonResponse({'message': 'Datos recibidos de InfluxDB.'})