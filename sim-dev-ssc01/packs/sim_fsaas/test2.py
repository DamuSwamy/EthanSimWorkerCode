import requests

url = "https://vb4-isi1-mgmt.fs.ethoria.services:8080/platform/3/cluster/config"

headers = {
  'Authorization': 'Basic dmI0LWlzaTEtYXBpLVJPOnR1bmVyLVpiRkMyaXdlaXo2UWUhaEFrZGpM'
}

response = requests.request("GET", url, headers=headers)

print(response.text)
