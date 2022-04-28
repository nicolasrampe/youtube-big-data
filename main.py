# API client library
import json
import tkinter as tk
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from tkinter import ttk
from tkinter import *
import googleapiclient.discovery as youtube
import pathlib

# API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'AIzaSyBYwVqhlTzox2YdwHMk9ZKRQJkNkj2F2N0'  # Generada en Google Cloud Platform
# API client
youtube = youtube.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)  # Construir objeto tipo googleapiclient.discovery


def get_comments(video_id):
    request = youtube.commentThreads().list(
        part="id,snippet",
        videoId=video_id
    )
    try:  # Hay vídeos que tienen bloqueados los comentarios
        search_response = request.execute()
        print(search_response)
        for search_result in search_response.get("items", []):
            with open("./json/comments/" + search_result["id"] + "_Videos.json", "w") as outfile:
                json.dump(search_response, outfile)
    except Exception:
        print("Oops! ")


def createWordsCloud():
    # Start with one review:
    text = df.description[0]

    # Create and generate a word cloud image:
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def createjson_Videos():
    request = youtube.search().list(
        part="id,snippet",
        regionCode='CO',
        type='video',
        q=search_box_palabra_clave.get(),
        videoDuration='short',
        videoDefinition='high',
        maxResults=50
    )  # Método de búsqueda de vídeos
    # Request execution
    search_response = request.execute()
    for search_result in search_response.get("items", []):
        get_comments(search_result["id"]["videoId"])
    print(search_response)
    with open("./json/videos/" + search_box_palabra_clave.get() + " Videos.json", "w") as outfile:
        json.dump(search_response, outfile)
    createWordsCloud()




ventana = tk.Tk()
ventana.title("Conversor de temperatura")
ventana.config(width=400, height=300)

etiqueta_palabra_clave = ttk.Label(text="Palabra clave:")
etiqueta_palabra_clave.place(x=20, y=20)
search_box_palabra_clave = ttk.Entry()
search_box_palabra_clave.place(x=110, y=20, width=60)

etiqueta_pais = ttk.Label(text="País:")
etiqueta_pais.place(x=200, y=20)

OPTIONS = [
"CO",
"EC",
"AR"
] #etc


variable = StringVar(ventana)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(ventana, variable, *OPTIONS)
w.place(x=240, y=15, width=60)

boton_convertir = ttk.Button(text="Buscar comentarios", command=createjson_Videos)
boton_convertir.place(x=20, y=60)
etiqueta_temp_kelvin = ttk.Label(text="Temperatura en K: n/a")
etiqueta_temp_kelvin.place(x=20, y=120)
etiqueta_temp_fahrenheit = ttk.Label(text="Temperatura en ºF: n/a")
etiqueta_temp_fahrenheit.place(x=20, y=160)
ventana.mainloop()