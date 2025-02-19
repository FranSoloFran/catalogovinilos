import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def reverse_image_search(image_path, driver):
    driver.get("https://images.google.com")
    time.sleep(2)
    try:
        camera_icon = driver.find_element(By.XPATH, '//div[@aria-label="Búsqueda por imagen"]')
        camera_icon.click()
    except Exception as e:
        print(f"error al hacer click en cámara: {e}")
        return None
    time.sleep(1)
    try:
        upload_tab = driver.find_element(By.XPATH, '//span[contains(text(), "sube un archivo")]')
        upload_tab.click()
    except Exception as e:
        print(f"error al seleccionar 'sube un archivo': {e}")
        return None
    time.sleep(1)
    try:
        file_input = driver.find_element(By.NAME, "encoded_image")
        file_input.send_keys(os.path.abspath(image_path))
    except Exception as e:
        print(f"error al subir la imagen: {e}")
        return None
    time.sleep(5)
    return driver.page_source

def get_discogs_link(google_html):
    soup = BeautifulSoup(google_html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ("discogs.com/release/" in href) or ("discogs.com/es/release/" in href):
            return href
    return None

def extract_release_id(discogs_link):
    m = re.search(r"/release/(\d+)-", discogs_link)
    if m:
        return m.group(1)
    return None

def get_release_data(release_id):
    url = f"https://api.discogs.com/releases/{release_id}"
    headers = {"User-Agent": "vinyl-batch-catalog/1.0"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        print("error en la api, status code:", r.status_code)
        return None

def parse_release_data(data):
    album = data.get("title", "desconocido")
    year = data.get("year", "no encontrado")
    artist = "desconocido"
    if "artists" in data and len(data["artists"]) > 0:
        artist = data["artists"][0].get("name", "desconocido")
    tracks = []
    for t in data.get("tracklist", []):
        pos = t.get("position", "")
        title = t.get("title", "")
        tracks.append(f"{pos} - {title}")
    tracks_str = ", ".join(tracks) if tracks else "no encontrado"
    thumb = data.get("thumb", "")
    return album, artist, tracks_str, year, thumb

def main():
    carpeta = "imagenes"
    imagenes = [f"{carpeta}/{f}" for f in os.listdir(carpeta)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(executable_path=r"C:\Users\neope\OneDrive\Documents\code\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    resultados = []
    for img in imagenes:
        print("procesando:", img)
        google_html = reverse_image_search(img, driver)
        if not google_html:
            resultados.append({
                "imagen": os.path.basename(img),
                "img_local": img,
                "album": "error",
                "artista": "error",
                "tracks": "error",
                "año": "error",
                "thumb": ""
            })
            continue
        discogs_link = get_discogs_link(google_html)
        if discogs_link:
            print("encontrado discogs link:", discogs_link)
            release_id = extract_release_id(discogs_link)
            if release_id:
                data = get_release_data(release_id)
                if data:
                    album, artist, tracks, year, thumb = parse_release_data(data)
                else:
                    album, artist, tracks, year, thumb = "no encontrado", "no encontrado", "no encontrado", "no encontrado", ""
            else:
                album, artist, tracks, year, thumb = "no encontrado", "no encontrado", "no encontrado", "no encontrado", ""
        else:
            album, artist, tracks, year, thumb = "no encontrado", "no encontrado", "no encontrado", "no encontrado", ""
        resultados.append({
            "imagen": os.path.basename(img),
            "img_local": img,
            "album": album,
            "artista": artist,
            "tracks": tracks,
            "año": year,
            "thumb": thumb
        })
    driver.quit()

    html = """<html>
<head>
  <meta charset='utf-8'>
  <title>Catálogo de Vinilos</title>
  <!-- bootstrap cdn -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <style>
    body { padding: 20px; }
    #enlargedContainer {
      display: none;
      position: fixed;
      top: 5%;
      left: 5%;
      width: 90%;
      height: 90%;
      background: rgba(0,0,0,0.8);
      z-index: 1050;
      text-align: center;
      padding-top: 20px;
    }
    #enlargedContainer img {
      max-width: 100%;
      max-height: 100%;
    }
    table img {
      cursor: pointer;
      transition: transform 0.2s;
    }
    table img:hover {
      transform: scale(1.05);
    }
    thead input.filter {
      width: 100%;
      padding: 5px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  </style>
</head>
<body>
<div class="container">
  <h1 class="my-4">Catálogo de Vinilos</h1>
  <table class="table table-striped table-hover" id="vinylTable">
    <thead>
      <tr>
        <th>Imagen Local</th>
        <th>Imagen Web (Thumb)</th>
        <th>Álbum</th>
        <th>Artista</th>
        <th>Tracks</th>
        <th>Año</th>
      </tr>
      <tr>
        <th><input type='text' class='filter' data-col='0' placeholder='filtrar archivo'></th>
        <th></th>
        <th><input type='text' class='filter' data-col='2' placeholder='filtrar álbum'></th>
        <th><input type='text' class='filter' data-col='3' placeholder='filtrar artista'></th>
        <th><input type='text' class='filter' data-col='4' placeholder='filtrar tracks'></th>
        <th><input type='text' class='filter' data-col='5' placeholder='filtrar año'></th>
      </tr>
    </thead>
    <tbody>
"""
    for res in resultados:
        html += (f"<tr>"
                 f"<td data-filename='{res['imagen']}'><img src='{res['img_local']}' width='100' onclick=\"showEnlarged('{res['img_local']}')\"></td>"
                 f"<td><img src='{res['thumb']}' width='100' onclick=\"showEnlarged('{res['thumb']}')\"></td>"
                 f"<td>{res['album']}</td>"
                 f"<td>{res['artista']}</td>"
                 f"<td>{res['tracks']}</td>"
                 f"<td>{res['año']}</td>"
                 f"</tr>")
    html += """</tbody>
  </table>
  <div id="enlargedContainer" onclick="hideEnlarged()"></div>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  // agregar lazy loading a todas las imágenes
  document.querySelectorAll('img').forEach(function(img){
    img.setAttribute('loading', 'lazy');
  });

//función para ampliar imagen
function showEnlarged(src) {
  var container = document.getElementById('enlargedContainer');
  container.innerHTML = '<img src="' + src + '">';
  container.style.display = 'block';
}
function hideEnlarged() {
  document.getElementById('enlargedContainer').style.display = 'none';
}

// Normalización de strings para filtrado de tabla
function normalizeString(str) {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}
//filtrado de tabla para buscar por columna
document.querySelectorAll('input.filter').forEach(function(input) {
  input.addEventListener('keyup', function() {
    var colIndex = parseInt(this.getAttribute('data-col'));
    var filterValue = normalizeString(this.value.toLowerCase());
    var rows = document.querySelectorAll('#vinylTable tbody tr');
    rows.forEach(function(row) {
      var cell = row.cells[colIndex];
      var cellText = cell.dataset.filename ? cell.dataset.filename.toLowerCase() : cell.innerText.toLowerCase();
      cellText = normalizeString(cellText);
      if(cellText.indexOf(filterValue) > -1) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  });
});
</script>
</body>
</html>
"""
    with open("catalogo_vinilos.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("proceso terminado. revisá catalogo_vinilos.html")

if __name__ == "__main__":
    main()
