import requests

def buscar_libros(query):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': query, 'maxResults': 10}
    response = requests.get(url, params=params)
    return response.json().get('items', [])