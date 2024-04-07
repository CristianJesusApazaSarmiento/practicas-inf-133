import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

# POST /deliveries
new_animal = {
    "animal_type": "mamifero",
    "nombre": "Jaguar",
    "especie": "felino",
    "genero": "hembra",
    "edad": 10,
    "peso": 70,
}
print("\n Crear un animal")
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.json())

print("\n Listar a todos los animales")
response = requests.get(url=url)
print(response.json())

print("\nBuscar animales por especie")
response = requests.get(url + "?especie=felino")
print(response.json())

print("\nBuscar animales por genero")
response = requests.get(url + "?genero=macho")
print(response.json())

animal_id_to_update = 2
updated_animal_data = {
    "animal_type": "mamifero",
    "nombre": "Pumba",
    "especie": "felino",
    "genero": "macho",
    "edad":8,
    "peso":50,
}
print("\n Actualizar animal con ID 2")
response = requests.put(f"{url}/{animal_id_to_update}", json=updated_animal_data)
print("Animal actualizado:", response.json())

print("\n Eliminar animal con ID 1")
animal_id_to_delete = 1
response = requests.delete(f"{url}/{animal_id_to_delete}")
print("Animal eliminado:", response.json())