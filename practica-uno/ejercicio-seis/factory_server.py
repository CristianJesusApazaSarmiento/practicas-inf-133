from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

animales = [
    {
        "id_animal": 1,
        "animal_type": "ave",
        "nombre": "Aguila",
        "especie": "volador",
        "genero": "macho",
        "edad": 5,
        "peso": 50,
    },
    {
        "id_animal": 2,
        "animal_type": "mamifero",
        "nombre": "Pumba",
        "especie": "felino",
        "genero": "hembra",
        "edad": 7,
        "peso": 40,
    },
]
contadorID = len(animales)

class AnimalZoologico:
    def __init__(self, animal_type, id_animal, nombre, especie, genero, edad, peso):
        self.animal_type = animal_type
        self.id_animal = id_animal
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

class Mamifero(AnimalZoologico):
    def __init__(self, id_animal, nombre, especie, genero, edad, peso):
        super().__init__("mamifero", id_animal, nombre, especie, genero, edad, peso)

class Ave(AnimalZoologico):
    def __init__(self, id_animal, nombre, especie, genero, edad, peso):
        super().__init__("ave", id_animal, nombre, especie, genero, edad, peso)

class Pez(AnimalZoologico):
    def __init__(self, id_animal, nombre, especie, genero, edad, peso):
        super().__init__("pez", id_animal, nombre, especie, genero, edad, peso)

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type, id_animal, nombre, especie, genero, edad, peso):
        if animal_type == "mamifero":
            return Mamifero(id_animal, nombre, especie, genero, edad, peso)
        elif animal_type == "ave":
            return Ave(id_animal, nombre, especie, genero, edad, peso)
        elif animal_type == "pez":
            return Pez(id_animal, nombre, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no válido")

class AnimalService:
    def __init__(self):
        self.factory = AnimalFactory()

    def agregar_animal(self, data):
        global contadorID
        contadorID += 1
        animal_type = data.get("animal_type", None)
        nombre = data.get("nombre", None)
        especie = data.get("especie", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)
        
        animal = self.factory.create_animal(animal_type, contadorID, nombre, especie, genero, edad, peso)
        
        animales.append(animal.__dict__)
        return {
            'animal_type': animal.animal_type, 'nombre':animal.nombre, 'especie':animal.especie, 'genero':animal.genero, 'edad':animal.edad, 'peso':animal.peso
        }

    def update_animal(self, animal_id, data):
        if animales[animal_id-1] in animales:
            animal = animales[animal_id-1]
            nombre = data.get("nombre", None)
            especie = data.get("especie", None)
            genero = data.get("genero", None)
            edad = data.get("edad", None)
            peso = data.get("peso", None)
            
            animal.update ({
                "nombre":nombre, "especie":especie, "genero":genero, 
                "edad":edad, "peso":peso
            })
            return animal
        else:
            return None

    def delete_animal(self, animal_id):
        if animales[animal_id-1] in animales:
            del animales[animal_id-1]
            return {"message": "Animal eliminado"}
        else:
            return None

    def buscar_animales_por(self, data):
        animalesfiltrados = []
        for animal in animales:
            if animal["especie"]==data or animal["genero"]==data:
                animalesfiltrados.append(animal)
        return animalesfiltrados
    
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

class AnimalRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.animal_service = AnimalService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.animal_service.agregar_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/animales":
            HTTPDataHandler.handle_response(self, 200, animales)
        elif parsed_path.path == "/animales":
            animales_filtrados = {}
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = self.animal_service.buscar_animales_por(especie)
                self.animal_service.verifica_lista(self, animales_filtrados)
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados = self.animal_service.buscar_animales_por(genero)
                self.animal_service.verifica_lista(self, animales_filtrados)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.animal_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.animal_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, AnimalRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()