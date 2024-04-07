from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def sumar(x,y):
    return "Resultado Suma --> {}".format(x+y)

def restar(x,y):
    return "Resultado Resta --> {}".format(x-y)

def multiplicar(x,y):
    return "Resultado Multiplicacion --> {}".format(x*y)

def dividir(x,y):
    return "Resultado Division --> {}".format(x//y)

dispatcher = SoapDispatcher(
    "soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "SumarDosNumeros",
    sumar,
    returns={"resultado": str},
    args={"x": int, "y":int},
)

dispatcher.register_function(
    "RestarDosNumeros",
    restar,
    returns={"resultado": str},
    args={"x": int, "y":int},
)

dispatcher.register_function(
    "MultiplicarDosNumeros",
    multiplicar,
    returns={"resultado": str},
    args={"x": int, "y":int},
)

dispatcher.register_function(
    "DividirDosNumeros",
    dividir,
    returns={"resultado": str},
    args={"x": int, "y":int},
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Iniciando el servidor Soap en http://localhost:8000/")
server.serve_forever()