from django.shortcuts import render, get_object_or_404
from .models import Libro, Autor, Categoria
from .api import buscar_libros
import requests
from django.http import JsonResponse


def index(request):
    return render(request, 'catalogo/index.html')

def libros(request):
    query = "programming"
    start_index = request.GET.get('start', 0)
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&startIndex={start_index}&maxResults=10"
    response = requests.get(api_url)
    books = response.json().get('items', [])

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'books': books})

    context = {
        'books': books
    }
    return render(request, 'catalogo/libros.html', context)

def autores(request):
    start_index = int(request.GET.get('start', 0))
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor&startIndex={start_index}&maxResults=10"
    response = requests.get(api_url)
    authors = []

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})
                if 'authors' in volume_info and 'imageLinks' in volume_info:
                    for author_name in volume_info['authors']:
                        author = {
                            'name': author_name,
                            'image': volume_info['imageLinks'].get('thumbnail', ''),
                            'birthdate': volume_info.get('publishedDate', 'N/A'),
                            'description': volume_info.get('description', 'No description available.')
                        }
                        authors.append(author)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'authors': authors})

    context = {
        'authors': authors,
        'start_index': start_index + 10
    }
    return render(request, 'catalogo/autores.html', context)


def categorias(request):
    categorias = ['Ficción', 'Ciencia Ficción', 'Fantasía', 'Misterio', 'Romance']  # Ejemplo de categorías
    selected_category = request.GET.get('categoria', categorias[0])  # Obtener la categoría seleccionada

    # Consulta a la API de Google Books para libros de la categoría seleccionada
    query = f"subject:{selected_category.lower()}"
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"
    response = requests.get(api_url)
    books = []

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})
                book = {
                    'title': volume_info.get('title', 'No title'),
                    'authors': volume_info.get('authors', ['Unknown']),
                    'publishedDate': volume_info.get('publishedDate', 'Unknown'),
                    'description': volume_info.get('description', 'No description available.'),
                    'image': volume_info['imageLinks'].get('thumbnail', '') if 'imageLinks' in volume_info else ''
                }
                books.append(book)

    context = {
        'categorias': categorias,
        'selected_category': selected_category,
        'books': books
    }

    return render(request, 'catalogo/categorias.html', context)

def ver_mas(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, 'catalogo/ver_mas.html', {'libro': libro})

def buscar(request):
    query = request.GET.get('q')
    resultados = buscar_libros(query)
    return render(request, 'catalogo/buscar.html', {'resultados': resultados})
