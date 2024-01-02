# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

##Prueba técnica Grupo R5  - Data Quality Engineer Junior
##Spotify API

##Primera parte
##Instalar librerias Pandas y Json
!pip install pandas
!pip install json

##Llamar a las librerias 
import pandas as pd
import json 

##Ubicación del archivo en mi equipo 
json_file_path = 'C:/Users/dallys.sinisterra/.spyder-py3/taylor_swift_spotify.json'

# Cargar el archivo
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

##Crear una lista a partir de las comlumnas idetnficiadas para almacenar la 
##información contenida en el archivo, para esto uso un ciclo for 
songs = [] 

for album in data.get("albums", []):
    album_id = album.get("album_id", "")
    album_name = album.get("album_name", "")
    album_release_date = album.get("album_release_date", "")
    
    for track in album.get("tracks", []):
        disc_number = track.get("disc_number", "")
        duration_ms = track.get("duration_ms", "")
        explicit = track.get("explicit", False)
        track_number = track.get("track_number", "")
        track_popularity = track.get("track_popularity", "")
        track_id = track.get("track_id", "")
        track_name = track.get("track_name", "")
        
        # Agregar información faltante a la lista para nombrar las columnas
        songs.append({
            "album_id": album_id,
            "album_name": album_name,
            "album_release_date": album_release_date,
            "disc_number": disc_number,
            "duration_ms": duration_ms,
            "explicit": explicit,
            "track_number": track_number,
            "track_popularity": track_popularity,
            "track_id": track_id,
            "track_name": track_name,
        })

# Crear un DataFrame de Pandas con la lista de canciones que anteriormente nombré
df = pd.DataFrame(songs)

# Guardar el DataFrame como un archivo CSV (este se guardará en mi misma carpeta)
df.to_csv('dataset.csv', index=False)


### Segunda Parte 
##Para validar las inconsistencias en la data, visualizaremos el contenido
##dentro de las variables 


# Mostrar los nombres de los álbumes
album_names = [album.get("album_name", "") for album in data.get("albums", [])]
print("Nombres de los álbumes:")
for name in album_names:
    print(name)
    
    
##Inconsistencias sobre los nombre de los álbumes, en términos de la escritura
##con información faltante en alguno de ellos, que es igual a los demás. 


##Validaciones sobre la fecha de lanzamiento de los albumes
##Se genera gráfica para validaciones (el 2027 no se ordena, al parece viene en
#diferente formato)

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

plt.figure(figsize=(10, 6))
plt.plot(df['album_release_date'], marker='o', linestyle='-', color='b')
plt.title('Fechas de lanzamiento de los álbumes')
plt.xlabel('Número de álbumes')
plt.ylabel('Fechas de lanzamiento')
plt.grid(True)
plt.show()

###Se observan fechas de lanzamiendo mayores a la fecha de hoy.

# Ahora validamos sobre los valores minimos y máximos de la duracción
##de los álbumes 

min_duration = df['duration_ms'].min()
max_duration = df['duration_ms'].max()

print(f"Duración mínima: {min_duration} ms")
print(f"Duración máxima: {max_duration} ms")

##Al ser los valores de duración de la pista en ms, se presenta una inconsistencia
##al observar valores negativos. 

##Ahora vamos a la popularidad que tiene la pista en Spotify,
##contenida en la variable track_popularity

min_popularity = df['track_popularity'].min()
max_popularity = df['track_popularity'].max()


print(f"Popularidad mínima: {min_popularity}")
print(f"Popularidad máxima: {max_popularity}")

##Al ser el número que ocupa en posición de popularidad, debe almacenar
##solo valores enteros positivos.

# Ahora, al igual que debe hacerse con la base completa, 
##se identificarán los valores faltantes en la variable track_id
missing_track_ids = df[df['track_id'].isna()]

print("MISSINGS")
print(missing_track_ids)

##Se deben depurar los valores faltantes para esta variable, dado que pueden
##generar sesgo al momento de generar resultados.


##Por último validaremos la variable final, correspondiente a track_name
# Mostrar los nombres de los discos, esta mnanera es diferente a la usada 
##para mostrar los nombre de los álbumes

track_names = df['track_name']
print("Nombres almacenados en la variable track_name:")
print(track_names)

##Nuevamente, se debe validar sobre los nombres para que sea consecuente la 
##escritura de unos con otros y poder agruparlos. 

##De manera general, a la base se le deben depurar los NA, posteriormente
## validar sobre cada variable, para así evitar problemas entre ella 
## y que puedan correlacionarse. 

##Además de incluir conclusiones ligadas al contexto real, como por ejemplo, 
##Taylor Swift, nació en 1989, por ende sería imposible que existan álbumes
##que hayan sido lanzados en esa fecha. 