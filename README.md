# Creador de Catálogo de Vinilos

Este repositorio contiene un programa en Python que automatiza la creación de un catálogo de vinilos a partir de imágenes de portadas. El script utiliza Selenium para realizar una búsqueda inversa de imágenes en Google, extraer el ID de la release en Discogs y consultar la Discogs API para obtener datos del álbum (título, artista, tracklist, año y thumb). Posteriormente, genera un archivo HTML (index.html) que muestra la información en una tabla estética usando Bootstrap y JavaScript.

## Características

- **Búsqueda inversa de imágenes:** Recorre la carpeta `imagenes` y para cada archivo sube la imagen a Google Imágenes.
- **Extracción de datos:** A partir del link de Discogs obtenido, extrae el ID de la release y consulta la API de Discogs para obtener detalles del vinilo.
- **Generación de catálogo:** Crea un HTML con una tabla que muestra:
  - Imagen local
  - Imagen web (thumb)
  - Álbum
  - Artista
  - Tracklist
  - Año
- **Filtrado interactivo:** La tabla incluye inputs en el encabezado que permiten filtrar por cualquier columna (por ejemplo, buscar "anibal" y encontrar "aníbal" gracias a la normalización de cadenas).
- **Vista ampliada (Lightbox):** Al hacer click en cualquiera de las imágenes, se muestra una vista ampliada inline en la misma página.
- **Lazy Loading:** Se activa lazy loading para todas las imágenes usando el atributo `loading="lazy"`.

## Estructura del Proyecto
```plaintext
/ (root)
│
├── imagenes/         # carpeta con las imágenes de las portadas de vinilos
│    ├── IMG_3229.jpg
│    ├── IMG_3259(1).jpg
│    └── ... 
│
├── index.html        # html generado (catálogo de vinilos)
│
└── catalogo.py       # script de python que automatiza el proceso
```

## Requisitos

- **Python 3.x**
- Librerías:
  - `requests`
  - `beautifulsoup4`
  - `selenium`
- Navegador Chrome y [Chromedriver](https://sites.google.com/chromium.org/driver/) (la ruta debe configurarse en el script)

## Uso

1. Coloca las imágenes de las portadas en la carpeta `imagenes`.
2. Ejecuta el script con:

   ```bash
   python catalogo.py
   ```

## Despliegue

Puedes subir este sitio a un hosting estático (por ejemplo, GitHub Pages, Netlify, Vercel o Surge). Asegúrate de mantener la misma estructura (el HTML en el directorio raíz y la carpeta `imagenes` al mismo nivel) para que las rutas relativas funcionen correctamente.

## Notas

- El script utiliza JavaScript puro y Bootstrap (CDN) para darle un aspecto estético y moderno al HTML.
- La funcionalidad de filtrado normaliza las cadenas para eliminar acentos, por lo que buscar "anibal" encontrará "aníbal".
- El código añade lazy loading a todas las imágenes para optimizar la carga.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](https://opensource.org/licenses/MIT).
