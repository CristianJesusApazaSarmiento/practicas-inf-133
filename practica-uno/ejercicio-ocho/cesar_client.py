import requests

url = "http://localhost:8000/"

print("\nCrear Mensaje")
ruta_post = url + "mensajes"
mensaje = {
    "contenido": "A veces las soluciones no son tan simples",
}
post_response = requests.request(method="POST", url=ruta_post, json=mensaje)
print(post_response.json())
mensaje = {
    "contenido": "A veces el adios es la unica manera",
}
post_response = requests.request(method="POST", url=ruta_post, json=mensaje)
print(post_response.json())

print("\nListar a todos los mensajes")
ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.json())

print("\nBuscar mensaje por ID")
ruta_get = url + "mensajes/1"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.json())

print("\nActualizar mensaje por ID")
ruta_actualizar = url + "mensajes/1"
mensaje_actualizado = {
    "contenido": "Y el sol se pondra para ti",
}
put_response = requests.request(method="PUT", url=ruta_actualizar, json=mensaje_actualizado)
print(put_response.json())

print("\nEliminar mensaje por ID")
ruta_eliminar = url + "mensajes/1"
eliminar_response = requests.request(method="DELETE", url=ruta_eliminar)
print(eliminar_response.json())