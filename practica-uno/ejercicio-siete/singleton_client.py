import requests
url = "http://localhost:8000/"

#Crear partida
print("\nCrear partidas")
nueva_partida = requests.post(url + "partidas", json={"element_player": "piedra"})
print(nueva_partida.json())
nueva_partida = requests.post(url + "partidas", json={"element_player": "tijera"})
print(nueva_partida.json())
nueva_partida = requests.post(url + "partidas", json={"element_player": "papel"})
print(nueva_partida.json())

print("\nListar todas las partidas")
response = requests.get(url + "partidas")
print(response.json())

print("\nListar partidas perdidas")
response = requests.get(url + "partidas?result=perdio")
print(response.json())

print("\nListar partidas ganadas")
response = requests.get(url + "partidas?result=gano")
print(response.json())