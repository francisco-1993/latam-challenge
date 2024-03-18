#envío del challenge-evidencia
import requests

url = 'https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/data-engineer'
data = {
    'name': 'Francisco Arriola',
    'mail': 'francisco.arriola@ug.uchile.cl',
    'github_url': 'https://github.com/francisco-1993/latam-challenge'
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())


#200
#{'status': 'OK', 'detail': 'your request was received'}