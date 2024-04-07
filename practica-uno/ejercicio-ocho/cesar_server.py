from http.server import HTTPServer, BaseHTTPRequestHandler
import json

mensajes = []
contadorID=len(mensajes)

class Mensaje:
    def __init__(self, id_mensaje, contenido):
        self.id_mensaje = id_mensaje
        self.contenido = contenido
        self.encriptado = MensajesService.encriptar(contenido)

class MensajesService:
    def encriptar(mensaje):
        encriptacion = ""
        for caracter in mensaje:
            if caracter.isalpha():
                desplazar = 3 if caracter.islower() else -23
                codigo = ord(caracter) + desplazar
                if caracter.islower():
                    encriptacion += chr((codigo - 97) % 26 + 97)
                else:
                    encriptacion += chr((codigo - 65) % 26 + 65)
            else:
                encriptacion += caracter
        return encriptacion
    
    def agregar_mensaje(self, contenido):
        global contadorID
        contadorID+=1
        mensaje = Mensaje(contadorID, contenido)
        mensajes.append(mensaje.__dict__)
        return mensaje
    
    @staticmethod
    def buscar_mensaje(id_mensaje):
        return next((mensaje for mensaje in mensajes if mensaje["id_mensaje"] == id_mensaje),None,)

    @staticmethod
    def search_index_for_id(id_mensaje):
        return next((mensajes.index(mensaje) for mensaje in mensajes if mensaje["id_mensaje"] == id_mensaje), None,)
        
    @staticmethod
    def verifica_lista(self, lista):
        if lista!=[]:
            return HTTPDataHandler.handle_response(self, 200, lista)
        else:
            return HTTPDataHandler.handle_response(self, 204, [])

    @staticmethod
    def actualizar_paciente(id_mensaje, data):
        mensaje = MensajesService.buscar_mensaje(id_mensaje)
        if mensaje:
            content = MensajesService.encriptar(data)
            mensaje = mensajes[id_mensaje-1]={
                "id_mensaje": id_mensaje, 
                "contenido": data, 
                "encriptado": content,
            }
            return mensaje
        else:
            return None

    @staticmethod
    def eliminar_mensaje(id_mensaje):
        index = MensajesService.search_index_for_id(id_mensaje)
        if index != None:
            return mensajes.pop(index)
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
    def __init__(self, *args, **kwargs):
        self.controller = MensajesService()
        super().__init__(*args, **kwargs)
    def do_GET(self):
        if self.path == "/mensajes":
                HTTPDataHandler.handle_response(self, 200, mensajes)
        elif self.path.startswith("/mensajes/"):
            id_mensaje = int(self.path.split("/")[-1])
            mensaje = MensajesService.buscar_mensaje(id_mensaje)
            if mensaje:
                HTTPDataHandler.handle_response(self, 200, [mensaje])
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/mensajes":
            data = HTTPDataHandler.handle_reader(self)
            mensajes = self.controller.agregar_mensaje(data["contenido"])
            HTTPDataHandler.handle_response(self, 201, mensajes.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id_mensaje = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            mensajes = MensajesService.actualizar_paciente(id_mensaje, data["contenido"])
            if mensajes:
                HTTPDataHandler.handle_response(self, 200, mensajes)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id_mensaje = int(self.path.split("/")[-1])
            mensajes = MensajesService.eliminar_mensaje(id_mensaje)
            HTTPDataHandler.handle_response(self, 200, mensajes)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

def run_server(port=8000):
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