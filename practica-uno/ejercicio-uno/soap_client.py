from zeep import Client
client = Client('http://localhost:8000')

result = client.service.SumarDosNumeros(10,20)
print(result)
result = client.service.RestarDosNumeros(40,20)
print(result)
result = client.service.MultiplicarDosNumeros(5,10)
print(result)
result = client.service.DividirDosNumeros(30,3)
print(result)