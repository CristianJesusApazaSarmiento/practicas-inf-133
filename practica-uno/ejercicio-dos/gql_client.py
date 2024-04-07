import requests
url = 'http://localhost:8000/graphql'

query_lista = """
    {
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""

print("\nCrear plantas")
query_crear = """
mutation {
        crearPlanta(nombre: "Espiguilla", especie: "Gramineae", edad: 7, altura: 12, frutos: true) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

print("\nLista de plantas")
response = requests.post(url, json={'query': query_lista})
print(response.text)

print("\nBuscar plantas por especie")
query_especie = """
    {
        plantasPorEspecie(especie: "Gramineae"){
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response = requests.post(url, json={'query': query_especie})
print(response.text)

print("\nBuscar plantas con frutos")
query_frutos = """
    {
        plantasConFrutos{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response = requests.post(url, json={'query': query_frutos})
print(response.text)

print("\nActualizar planta por ID")
query_actualizar = """
mutation {
    actualizarPlanta(id: 3, nombre: "Malva", especie: "Malvaceae", edad: 5, altura: 5, frutos: false) {
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
response_mutation = requests.post(url, json={'query': query_actualizar})
print(response_mutation.text)

print("\nEliminar planta por ID")
query_eliminar = """
mutation {
        deletePlanta(id: 1) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

print("\nLista de plantas")
response = requests.post(url, json={'query': query_lista})
print(response.text)