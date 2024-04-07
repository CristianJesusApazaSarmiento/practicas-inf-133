import requests

url = "http://localhost:8000/"

print("\n### Listar a todos los pacientes ###")
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_post = url + "pacientes"
nuevo_paciente = {
    "ci": 1234567,
    "nombre": "Ashley",
    "apellido": "Rodriguez",
    "edad": 19,
    "genero": "femenino",
    "diagnostico": "tuberculosis",
    "doctor": "Pedro Perez",
}
print("\n### Agregar un paciente ###")
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)

print("\n### Listar a todos los pacientes ###")
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("\n### Buscar pacientes por CI ###")
ruta_get = url + "pacientes/1234567"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("\n### Listar pacientes con diabetes ###")
ruta_get = url + "pacientes?diagnostico=diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print("\n### Buscar pacientes atendidos por el doctor Pedro Perez ###")
ruta_get = url + "pacientes?doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_actualizar = url + "pacientes/1234567"
paciente_actualizado = {
    "ci": 1234567,
    "nombre": "Ashley",
    "apellido": "Rodriguez",
    "edad": 19,
    "genero": "femenino",
    "diagnostico": "fiebre",
    "doctor": "Marcos Aguilar",
}
print("\n### Actualizar paciente por CI ###")
put_response = requests.request(method="PUT", url=ruta_actualizar, json=paciente_actualizado)
print(put_response.text)

print("\n### Eliminar paciente por CI ###")
ruta_eliminar = url + "pacientes/11111"
eliminar_response = requests.request(method="DELETE", url=ruta_eliminar)
print(eliminar_response.text)
