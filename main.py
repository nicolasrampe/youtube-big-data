# API client library
import json
import tkinter as tk
import csv
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import googleapiclient.discovery as youtube
import pathlib

# API information
api_service_name = "youtube"
api_version = "v3"
#DEVELOPER_KEY = 'AIzaSyBYwVqhlTzox2YdwHMk9ZKRQJkNkj2F2N0'  # Generada en Google Cloud Platform
DEVELOPER_KEY = 'AIzaSyBrilxyR-EhvbWWOtZuj2JL0Hj7CrFWoRM'  # Generada en Google Cloud Platform
# API client
youtube = youtube.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)  # Construir objeto tipo googleapiclient.discovery

word_list = []

def get_comments(video_id):
    request = youtube.commentThreads().list(
        part="id,snippet",
        videoId=video_id
    )
    try:  # Hay vídeos que tienen bloqueados los comentarios
        search_response = request.execute()
        #print(search_response)
        with open("./json/comments/" + video_id + "_Videos.json", "w") as outfile:
            json.dump(search_response, outfile)

        for search_result in search_response.get("items", []):
            word_list.append(search_result["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
    except Exception:
        print("Oops! "+ video_id)


def createWordsCloud():
    unique_string=(" ").join(word_list)
    wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

def createjson_Videos():
    ventana.config(cursor="watch")
    request = youtube.search().list(
        part="id,snippet",
        regionCode=drop_down_region_code.get(),
        type='video',
        q=search_box_palabra_clave.get(),
        videoDuration='short',
        videoDefinition='high',
        maxResults=50
    )  # Método de búsqueda de vídeos
    # Request execution
    search_response = request.execute()
    word_list.clear()
    for search_result in search_response.get("items", []):
        get_comments(search_result["id"]["videoId"])
    print(search_response)
    with open("./json/videos/"+ drop_down_region_code.get() + "_" + search_box_palabra_clave.get() + "_Videos.json", "w") as outfile:
        json.dump(search_response, outfile)
    createWordsCloud()
    ventana.config(cursor="arrow")


def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        ventana.destroy()

ventana = tk.Tk()
ventana.title("Buscador de comentarios")
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


drop_down_region_code = StringVar(ventana)
drop_down_region_code.set(OPTIONS[0]) # default value

w = OptionMenu(ventana, drop_down_region_code, *OPTIONS)
w.place(x=240, y=15, width=60)

boton_convertir = ttk.Button(text="Buscar comentarios", command=createjson_Videos)
boton_convertir.place(x=20, y=60)

ventana.protocol("WM_DELETE_WINDOW", on_close)


ventana.mainloop()