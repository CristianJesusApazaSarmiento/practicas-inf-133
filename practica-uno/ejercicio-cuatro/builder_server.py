from http.server import BaseHTTPRequestHandler, HTTPServer
import json 
from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "ci": 1111,
        "nombre": "Carlos",
        "apellido": "Huanca",
        "edad": 25,
        "genero": "masculino",
        "diagnostico": "fiebre",
        "doctor": "Pedro Perez"
    },
    {
        "ci": 12345,
        "nombre": "Luis",
        "apellido": "Lopez",
        "edad": 32,
        "genero": "masculino",
        "diagnostico": "diabetes",
        "doctor": "Juan Carlos",
    }
]

class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

    def __str__(self):
        return f"Ci: {self.ci}, Nombre: {self.nombre}, Apellido: {self.apellido}, Edad: {self.edad}, Genero: {self.genero}, Diagnostico: {self.diagnostico}, Doctor: {self.doctor}"

class PacienteBuilder:
    def __init__(self):
        self.paciente= Paciente()

    def set_ci(self, ci):
        self.paciente.ci = ci

    def set_nombre(self, nombre):
        self.paciente.nombre = nombre

    def set_apellido(self, apellido):
        self.paciente.apellido = apellido

    def set_edad(self, edad):
        self.paciente.edad = edad
        
    def set_genero(self, genero):
        self.paciente.genero = genero
    
    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico
        
    def set_doctor(self, doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente

class Hospital:
    def __init__(self, builder):
        self.builder = builder

    def create_paciente(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()

class PacienteService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)

    def create_paciente(self, post_data):
        ci = post_data.get("ci", None)
        nombre = post_data.get("nombre", None)
        apellido = post_data.get("apellido", None)
        edad = post_data.get("edad", None)
        genero = post_data.get("genero", None)
        diagnostico = post_data.get("diagnostico", None)
        doctor = post_data.get("doctor", None)

        paciente = self.hospital.create_paciente(ci, nombre, apellido, edad, genero, diagnostico, doctor)
        pacientes.append(paciente.__dict__)
        
        return {
            'ci': paciente.ci, 'nombre':paciente.nombre, 'apellido':paciente.apellido, 'edad':paciente.edad, 'genero':paciente.genero, 'diagnostico':paciente.diagnostico, 'doctor':paciente.doctor
        }
        
    def search_index_by_ci(self, ci):
        return next((pacientes.index(paciente) for paciente in pacientes if paciente["ci"]==ci), None,)
    
    def update_paciente(self, ci, post_data):
        index = self.search_index_by_ci(ci)
        if index!=None:
            paciente = pacientes[index]
            ci = post_data.get("ci", None)
            nombre = post_data.get("nombre", None)
            apellido = post_data.get("apellido", None)
            edad = post_data.get("edad", None)
            genero = post_data.get("genero", None)
            diagnostico = post_data.get("diagnostico", None)
            doctor = post_data.get("doctor", None)
            
            paciente.update({
                "ci": ci, "nombre": nombre, "apellido": apellido, "edad": edad, "genero": genero, "diagnostico": diagnostico, "doctor": doctor
            })
            return paciente
        else:
            return None

    def delete_paciente(self, ci):
        index = self.search_index_by_ci(ci)
        if index != None:
            return pacientes.pop(index)
        else:
            return None

    def buscar_paciente_por_ci(self, ci):
        return next((paciente for paciente in pacientes if paciente["ci"] == ci),None,)

    def buscar_pacientes_por(self, data):
        pacientesfiltrados = []
        for paciente in pacientes:
            if paciente["diagnostico"]==data or paciente["doctor"]==data:
                pacientesfiltrados.append(paciente)
        return pacientesfiltrados
    
    @staticmethod
    def verifica_lista(self, lista):
        if lista!=[]:
            return HTTPDataHandler.handle_response(self, 200, lista)
        else:
            return HTTPDataHandler.handle_response(self, 204, [])

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PacienteService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_paciente(data)
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/pacientes":
            HTTPDataHandler.handle_response(self, 200, pacientes)
            
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = self.controller.buscar_paciente_por_ci(ci)
            if paciente:
                HTTPDataHandler.handle_response(self, 200, [paciente])
            else:
                HTTPDataHandler.handle_response(self, 204, [])
                
        elif parsed_path.path == "/pacientes":
            pacientesfiltrados = []
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientesfiltrados = self.controller.buscar_pacientes_por(diagnostico)
                self.controller.verifica_lista(self, pacientesfiltrados)
                
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientesfiltrados = self.controller.buscar_pacientes_por(doctor)
                self.controller.verifica_lista(self, pacientesfiltrados)
            else:
                HTTPDataHandler.handle_response(self, 200, pacientes)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(ci, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de paciente no válido"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            deleted_paciente = self.controller.delete_paciente(ci)
            if deleted_paciente:
                HTTPDataHandler.handle_response(self, 200, {"message": "Paciente eliminado correctamente"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Índice de paciente no válido"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run_server(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    try:
        server_address = ("", port)
        httpd = server_class(server_address, handler_class)
        print(f"Iniciando servidor HTTP en puerto {port}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor web...")
        httpd.socket.close()
        
if __name__ == "__main__":
    run_server()