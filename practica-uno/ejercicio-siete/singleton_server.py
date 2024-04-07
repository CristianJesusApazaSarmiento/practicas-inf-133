from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json, random

class Partida:
    def __init__(self, id_partida, element_player, element_server, result):
        self.id_partida = id_partida
        self.element_player = element_player
        self.element_server = element_server
        self.result = result

class PartidaManager:
    
    def __init__(self):
        self.partidas = []
        self.id_partida=0
        self.elementos = ["piedra", "papel", "tijera"]
    
    _instance = None   
    @staticmethod
    def get_instance():
        if not PartidaManager._instance:
            PartidaManager._instance = PartidaManager()
        return PartidaManager._instance
        
    def crear_partida(self, element_player):
        self.id_partida += 1
        element_server = random.choice(self.elementos)
        result = self.resultado(element_player, element_server)
        new_partida = Partida(self.id_partida, element_player, element_server, result)
        self.partidas.append(new_partida.__dict__)
        return new_partida
    
    def resultado(self, element_player, element_server):
        return "empate" if element_player == element_server else "gano" if (element_player == "piedra" and element_server == "tijera") or (element_player == "papel" and element_server == "piedra") or (element_player == "tijera" and element_server == "papel") else "perdio"
    
    def partidas_resultados(self, resultado):
        partidasfiltradas = []
        for partida in self.partidas:
            if partida["result"]==resultado:
                partidasfiltradas.append(partida)
        return partidasfiltradas
    
    @staticmethod
    def verifica_lista(self, lista):
        if lista!=[]:
            HTTPDataHandler.handle_response(self, 200, lista)
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
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))
    
class PartidaHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs): #args =  se envian listas y kwargs = se envian diccionarios
        self.partida_manager = PartidaManager.get_instance()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if self.path == "/partidas":
            HTTPDataHandler.handle_response(self, 200, self.partida_manager.partidas)
        elif parsed_path.path== "/partidas":
            if "result" in query_params:
                result = query_params["result"][0]
                partidas_filtradas=self.partida_manager.partidas_resultados(result)
                self.partida_manager.verifica_lista(self, partidas_filtradas)
        else:
            self.send_response(404)
            self.end_headers()
        
    def do_POST(self):
        if self.path == "/partidas":
            data = HTTPDataHandler.handle_reader(self)
            nueva_partida = self.partida_manager.crear_partida(data.get('element_player'))
            HTTPDataHandler.handle_response(self, 200, nueva_partida.__dict__)
        else:
            self.send_response(404)
            self.end_headers()
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PartidaHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()