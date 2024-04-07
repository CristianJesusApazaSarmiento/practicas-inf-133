import requests

url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}

paciente = {
    "ci": 123456,
    "nombre": "Luis",
    "apellido": "Lopez",
    "edad": 21,
    "genero": "masculino",
    "diagnostico": "diabetes",
    "doctor": "Pedro Terez"
}
print("\n### Crear paciente ###")
response = requests.post(url, json=paciente, headers=headers)
print(response.json())

print("\n### Listar a todos los pacienes ###")
response = requests.get(url)
print(response.json())

print("\n### Buscar pacientes por CI ###")
response = requests.get(url + "/1111")
print(response.json())

print("\n### Buscar pacientes con diabetes ###")
response = requests.get(url + "?diagnostico=diabetes")
print(response.json())

print("\n### Buscar pacientes atendidos por el doctor Pedro Perez ###")
response = requests.get(url + "?doctor=Pedro Perez")
print(response.json())

actualizar_paciente = {
    "ci": 123456,
    "nombre": "Luis",
    "apellido": "Lopez",
    "edad": 21,
    "genero": "masculino",
    "diagnostico": "fiebre",
    "doctor": "Marcos"
}
print("\n### Actualizar paciente por CI ###")
response = requests.put(url + "/123456", json=actualizar_paciente, headers=headers)
print(response.json())

# DELETE /pizzas/1
print("\n### Eliminar paciente por CI ###")
response = requests.delete(url + "/123456")
print(response.json())