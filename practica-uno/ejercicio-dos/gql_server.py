from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Field, Schema, Mutation

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()
    
class Query(ObjectType):
    plantas = List(Planta)
    plantas_por_especie = List(Planta, especie=String())
    plantas_con_frutos = List(Planta)

    def resolve_plantas(root, info):
        return plantas

    def resolve_plantas_por_especie(root, info, especie):
        listplantas = []
        for planta in plantas:
            if planta.especie==especie:
                listplantas.append(planta)
        return listplantas

    def resolve_plantas_con_frutos(root, info):
        listplantas = []
        for planta in plantas:
            if planta.frutos:
                listplantas.append(planta)
        return listplantas
    
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
        
    planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, frutos):
        global contador
        contador += 1
        nueva_planta = Planta(
            id=contador,
            nombre=nombre,
            especie=especie,
            edad=edad,
            altura=altura,
            frutos=frutos
        )
        plantas.append(nueva_planta)        
        return CrearPlanta(planta=nueva_planta)

class ActualizarPlanta(Mutation):
    class Arguments:
        id= Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, id, nombre, especie, edad, altura, frutos):
        for i, nueva_planta in enumerate(plantas):
            if nueva_planta.id == id:
                nueva_planta.nombre=nombre 
                nueva_planta.especie=especie
                nueva_planta.edad=edad
                nueva_planta.altura=altura
                nueva_planta.frutos=frutos
                return ActualizarPlanta(planta = nueva_planta)
        return None

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None


class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    actualizar_planta = ActualizarPlanta.Field()
    delete_planta = DeletePlanta.Field()

plantas = [
    Planta(id=1, nombre="Anea", especie="Typhaceae", edad=4, altura=15, frutos=False),
    Planta(id=2, nombre="Larre-oloa", especie="Gramineae", edad=7, altura=10, frutos=False),
    Planta(id=3, nombre="Malva", especie="Malvaceae", edad=9, altura=15, frutos=True),
]
contador=len(plantas)

schema = Schema(query=Query, mutation=Mutations)

class HTTPDataHandler:
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    def response_reader(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class GraphQlRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/graphql":
            data = HTTPDataHandler.response_reader(self)
            result = schema.execute(data["query"])
            HTTPDataHandler.response_handler(self, 200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})
        
def run_server():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, GraphQlRequestHandler)
        print(f"Iniciando servidor web en http://localhost:8000/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()
        
if __name__ == "__main__":
    run_server()