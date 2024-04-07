from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": 312331,
        "nombre": "Luis",
        "apellido": "Lopez",
        "edad": 17,
        "genero": "masculino",
        "diagnostico": "diabetes",
        "doctor": "Jose",
    },
    {
        "ci": 11111,
        "nombre": "Pablo",
        "apellido": "Escobar",
        "edad": 43,
        "genero": "masculino",
        "diagnostico": "dolor de estomago",
        "doctor": "Pedro Perez"
    }
]

class PacientesService:
    @staticmethod
    def buscar_paciente(ci):
        return next((paciente for paciente in pacientes if paciente["ci"] == ci),None,)

    def buscar_pacientes_por(data):
        pacientes_filtrados = []
        for paciente in pacientes:
            if paciente["diagnostico"]==data or paciente["doctor"]==data:
                pacientes_filtrados.append(paciente)
        return pacientes_filtrados
        
    @staticmethod
    def agregar_paciente(data):
        pacientes.append(data)
        return pacientes

    @staticmethod
    def actualizar_paciente(ci, data):
        paciente = PacientesService.buscar_paciente(ci)
        if paciente:
            paciente.update(data)
            return paciente
        else:
            return None

    @staticmethod
    def eliminar_pacientes(ci):
        for i in range(0,len(pacientes),1):
            if pacientes[i].get("ci")==ci:
                return pacientes.pop(i)
        return None

    @staticmethod
    def verifica_lista(self, lista):
        if lista!=[]:
            return HTTPDataHandler.handle_response(self, 200, lista)
        else:
            return HTTPDataHandler.handle_response(self, 204, [])

    @staticmethod
    def verifica_paciente(self, paciente):
        if paciente:
            HTTPDataHandler.handle_response(self, 200, [paciente])
        else:
            HTTPDataHandler.handle_response(self, 204, [])
    
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

        if self.path == "/pacientes":
                HTTPDataHandler.handle_response(self, 200, pacientes)
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.buscar_paciente(ci)
            PacientesService.verifica_paciente(self, paciente)
        elif parsed_path.path == "/pacientes":
            pacientes_filtrados = []
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.buscar_pacientes_por(diagnostico)
                PacientesService.verifica_lista(self, pacientes_filtrados)
                
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.buscar_pacientes_por(doctor)
                PacientesService.verifica_lista(self, pacientes_filtrados)
            else:
                HTTPDataHandler.handle_response(self, 200, pacientes)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            pacientes = PacientesService.agregar_paciente(data)
            HTTPDataHandler.handle_response(self, 201, pacientes)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            paciente = PacientesService.actualizar_paciente(ci, data)
            if paciente:
                HTTPDataHandler.handle_response(self, 200, paciente)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            pacientes = PacientesService.eliminar_pacientes(ci)
            HTTPDataHandler.handle_response(self, 200, pacientes)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()