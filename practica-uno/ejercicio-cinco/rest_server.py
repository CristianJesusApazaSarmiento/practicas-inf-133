from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

animales = [
    {
        "id": 1,
        "nombre": "Aguila",
        "especie": "volador",
        "genero": "macho",
        "edad": 5,
        "peso": 50,
    },
    {
        "id": 2,
        "nombre": "Pumba",
        "especie": "felino",
        "genero": "hembra",
        "edad": 7,
        "peso": 40,
    },
]
contadorID=len(animales)
class AnimalesService:
    @staticmethod
    def buscar_animal(id):
        return next((animal for animal in animales if animal["id"] == id),None,)
    
    @staticmethod
    def buscar_animales_por(data):
        animalesLista = []
        for animal in animales:
            if animal["especie"]==data or animal["genero"]==data:
                animalesLista.append(animal)
        return animalesLista
        
    @staticmethod
    def search_index_for_id(id):
        return next((animales.index(animal) for animal in animales if animal["id"] == id), None,)
        
    @staticmethod
    def verifica_lista(self, lista):
        if lista!=[]:
            return HTTPDataHandler.handle_response(self, 200, lista)
        else:
            return HTTPDataHandler.handle_response(self, 204, [])
        
    @staticmethod
    def agregar_paciente(data):
        global contadorID
        contadorID += 1
        data["id"]=contadorID
        animales.append(data)
        return animales

    @staticmethod
    def actualizar_paciente(id, data):
        animal = AnimalesService.buscar_animal(id)
        if animal:
            animal.update(data)
            return animal
        else:
            return None

    @staticmethod
    def eliminar_pacientes(id):
        index = AnimalesService.search_index_for_id(id)
        if index != None:
            return animales.pop(index)
        return None

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if self.path == "/animales":
                HTTPDataHandler.handle_response(self, 200, animales)
        elif parsed_path.path == "/animales":
            animales_filtrados = []
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = AnimalesService.buscar_animales_por(especie)
                AnimalesService.verifica_lista(self, animales_filtrados)
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados = AnimalesService.buscar_animales_por(genero)
                AnimalesService.verifica_lista(self, animales_filtrados)
            else:
                HTTPDataHandler.handle_response(self, 200, animales)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            animales = AnimalesService.agregar_paciente(data)
            HTTPDataHandler.handle_response(self, 201, animales)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            ci = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            animales = AnimalesService.actualizar_paciente(ci, data)
            if animales:
                HTTPDataHandler.handle_response(self, 200, animales)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animales = AnimalesService.eliminar_pacientes(id)
            HTTPDataHandler.handle_response(self, 200, animales)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

def run_server():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:8000/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()