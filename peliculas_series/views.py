from django.shortcuts import render

def bienvenida(request):
    # Criterio 1: Variables y tipos de datos pertinentes
    nombre_plataforma = "TitanStream"
    total_usuarios = 1500
    
    # Estructura de datos compleja
    peliculas_destacadas = [
        {'titulo': 'Shingeki no Kyojin: The Final Chapters', 'genero': 'Anime', 'año': 2023},
        {'titulo': 'El Padrino', 'genero': 'Drama', 'año': 1972},
        {'titulo': 'Interstellar', 'genero': 'Ciencia Ficción', 'año': 2014},
    ]
    
    # Empaquetamos los datos en un diccionario para enviarlos al HTML
    contexto = {
        'nombre': nombre_plataforma,
        'usuarios': total_usuarios,
        'peliculas': peliculas_destacadas,
    }
    
    # Criterio 2.3: Integración de la lógica en la vista
    return render(request, 'bienvenida.html', contexto)