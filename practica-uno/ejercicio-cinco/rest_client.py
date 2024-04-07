import requests
url = "http://localhost:8000/"

print("\n### Listar a todos los animales ###")
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_post = url + "animales"
nuevo_animal = {
    "nombre": "Tigre",
    "especie": "felino",
    "genero": "hembra",
    "edad": 8,
    "peso" : 50,
}
print("\n### Agregar un animal ###")
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)

print("\n### Listar a todos los animales ###")
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("\n### Buscar animales por especie ###")
ruta_get = url + "animales?especie=felino"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("\n### Buscar animales por genero ###")
ruta_get = url + "animales?genero=hembra"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_actualizar = url + "animales/2"
animal_actualizado = {
    "id": 2,
    "nombre": "Pumba",
    "especie": "Mamifero",
    "genero": "hembra",
    "edad": 9,
    "peso": 40,
}
print("\n### Actualizar animal por ID ###")
put_response = requests.request(method="PUT", url=ruta_actualizar, json=animal_actualizado)
print(put_response.text)

print("\n### Eliminar paciente por ID ###")
ruta_eliminar = url + "animales/1"
eliminar_response = requests.request(method="DELETE", url=ruta_eliminar)
print(eliminar_response.text)