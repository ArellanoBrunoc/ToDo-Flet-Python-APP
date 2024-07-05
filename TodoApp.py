import flet as ft
import time as time
from math import pi
import random
from colour import Color
import os
import re







def main(page: ft.Page):
    print(page.client_storage.get_keys(""))
    page.fonts ={"Nunito": "Assets/Work_Sans/worksans.ttf"}
    page.theme = ft.Theme(font_family="Nunito")
    page.fonts
    page.theme_mode= ft.ThemeMode.DARK
    peso = ft.FontWeight.W_500
    peso2 = ft.FontWeight.W_300
    if not page.client_storage.contains_key("auth"):
        nombre = "Usuario"
    else:
        nombre = page.client_storage.get("auth")
        
    if not page.client_storage.contains_key("nightmode"):
        page.client_storage.set("nightmode", True)
    if page.client_storage.contains_key("nightmode"):
        modo = page.client_storage.get("nightmode")
        if modo:
            color_principal = "#020018"
            color_secundario= "#221336"
            color_acento = "#8D1F40"
            color_acento_secundario="#FD975A"
            color_texto ="#ffead6"
            color_texto_especial="#E6E6FA"
            start_color = Color("#020018")  
            end_color = Color("#1B0F2B")
            end_color_2 = Color("#221336")
            start_color_2 = Color("#020018")
        else:
            color_principal = "#FCF8F3"
            color_secundario= "#F2E7D3"
            color_acento = "#F9B197"
            color_acento_secundario="#7E483A"
            color_texto="#1E1E24"
            color_texto_especial="#AD5D5D"
            start_color = Color("#FCF8F3")
            end_color = Color("#FCF8F3")
            end_color_2 = Color("#F2E7D3")
            start_color_2 = Color("#AD5D5D")

    page.theme = ft.Theme(
    scrollbar_theme=ft.ScrollbarTheme(
        track_color={
            ft.MaterialState.DEFAULT: color_acento_secundario,
        },
        thumb_color={
            ft.MaterialState.HOVERED: color_acento,
            ft.MaterialState.DEFAULT: color_acento_secundario,
        },


        radius=15,

        )
        )
    # Generamos 6 colores intermedios para una transición suave
    gradient = list(start_color.range_to(end_color, 8))
    gradient_2 = list(start_color.range_to(end_color_2, 40))
    # Convertimos los colores a formato hexadecimal con el prefijo requerido
    hex_gradient = [f"0xff{color.hex.lstrip('#')}" for color in gradient]
    hex_gradient_2 = [f"0xff{color.hex.lstrip('#')}" for color in gradient_2]
    
    gradiente= ft.LinearGradient(begin=ft.alignment.top_center,end=ft.alignment.bottom_center,colors=hex_gradient,tile_mode=ft.GradientTileMode.MIRROR, rotation=pi*2)
    gradiente_2= ft.LinearGradient(begin=ft.alignment.top_center,end=ft.alignment.bottom_center,colors=hex_gradient_2,tile_mode=ft.GradientTileMode.MIRROR, rotation=pi*2)
    
    page.bgcolor= color_principal
    page.window_height=page.height
    x = page.width
    y = page.height
    x_offset = x*0.17
    page.padding= 0
    page.window_resizable=False
    page.window_maximizable=False
    paginas= {
    'Principal': "",
    'Música': "",
    'Tareas': ""
            }

    pestana = "Principal"
    
    #Variables y arreglos que manejan la musica y playlists
    audios_ya_reproducidos = []
    audios_pasados = []
    audios = []
    audios_permanentes = []
    audio1 = ft.Audio(src="Assets/Audios/buttonAudio.mp3", autoplay=False, volume=0.1)
    posicion_audio = ""
    reproductor_permiso = False
    posicion_cancion = 1
    tarea_pasada = ""
    playlist_parcial = []
    shuffle = False
    playlist_tracker = False
    lista_busqueda_eliminados = []
    play_list_actual = [["none"], "none"]
    playlist_a_eliminar = ""
    volumen_global = 0.5

    def subir_volumen(e):
        nonlocal posicion_audio,volumen_global

        volumen_actual = posicion_audio.volume
        if volumen_actual == None:
            volumen_actual = 0.5

        if volumen_actual+0.05 <= 1:
            posicion_audio.volume= volumen_actual+0.05
            volumen_global = posicion_audio.volume
            reproductor.content.controls[0].content.controls[2].content.controls[1].controls[4].value = int(posicion_audio.volume*100)
            posicion_audio.update()
        else:
            posicion_audio.volume= 1
            volumen_global = 1
            reproductor.content.controls[0].content.controls[2].content.controls[1].controls[4].value = int(posicion_audio.volume*100)
            posicion_audio.update()
        page.update()
    def bajar_volumen(e):
        nonlocal posicion_audio, volumen_global
        volumen_actual = posicion_audio.volume
        if volumen_actual == None:
            volumen_actual = 0.5
        if volumen_actual-0.05 > 0:
            posicion_audio.volume= volumen_actual-0.05
            volumen_global = posicion_audio.volume
            reproductor.content.controls[0].content.controls[2].content.controls[1].controls[4].value = int(posicion_audio.volume*100)
            posicion_audio.update()
        else:
            posicion_audio.volume = 0
            volumen_global = 0 
            reproductor.content.controls[0].content.controls[2].content.controls[1].controls[4].value = int(posicion_audio.volume*100)
            posicion_audio.update()
        page.update()
    
    def shuffle_mode(e):
        nonlocal shuffle
        if shuffle:
            e.control.icon_color = color_acento
            shuffle = False
        else:
            e.control.icon_color = color_texto_especial
            shuffle = True
        reproductor.update()

        
    #Funcion que salta las canciones hacia atrás
    def skipear_musica_atras(e):
        nonlocal audios_ya_reproducidos, audios_pasados, audios, posicion_audio
        indice_actual = audios.index(posicion_audio)
        # Calcular el nuevo índice adelante
        indice_nuevo = indice_actual - 1
        # Si el índice nuevo supera el último índice de la lista, volver al inicio
        if indice_nuevo < 0:
            indice_nuevo = -1
        posicion_audio.pause()
        posicion_audio = audios[indice_nuevo]
        
        play_audio_automatic(posicion_audio)
        
    def skipear_musica_adelante_non_control():
        nonlocal audios_ya_reproducidos, audios_pasados, audios, posicion_audio, shuffle

        if shuffle:
            nuevo_audio = random.choice(audios)
            while nuevo_audio in audios_ya_reproducidos:
                nuevo_audio = random.choice(audios)
            posicion_audio.pause()

            posicion_audio = nuevo_audio
            play_audio_automatic(nuevo_audio)
        else:
            indice_actual = audios.index(posicion_audio)
            # Calcular el nuevo índice adelante
            indice_nuevo = indice_actual + 1
            # Si el índice nuevo supera el último índice de la lista, volver al inicio
            if indice_nuevo > len(audios) - 1:
                indice_nuevo = 0
            posicion_audio.pause()
            posicion_audio = audios[indice_nuevo]
        
        play_audio_automatic(posicion_audio)
    
    #Funcion que salta las canciones hacia adelante
    def skipear_musica_adelante(e):
        nonlocal audios_ya_reproducidos, audios_pasados, audios, posicion_audio, shuffle
        if len(audios) == 0:

            return

        if posicion_audio not in audios_ya_reproducidos:
            if len(audios_ya_reproducidos)+1 == len(audios):
                audios_ya_reproducidos = [] 
            audios_ya_reproducidos.append(posicion_audio)

        if shuffle:
            nuevo_audio = random.choice(audios)
            while nuevo_audio in audios_ya_reproducidos:
                nuevo_audio = random.choice(audios)
            posicion_audio.pause()

            posicion_audio = nuevo_audio

        else:
            indice_actual = audios.index(posicion_audio)
            # Calcular el nuevo índice adelante
            indice_nuevo = indice_actual + 1
            # Si el índice nuevo supera el último índice de la lista, volver al inicio
            if indice_nuevo > len(audios) - 1:
                indice_nuevo = 0
            posicion_audio.pause()
            posicion_audio = audios[indice_nuevo]
        
        play_audio_automatic(posicion_audio)
        
    #Maneja atrasar 10 segundos hacia atrás
    def atrasar_musica(e):
        nonlocal posicion_cancion, reproductor_permiso
        posicion_actual_musica = posicion_audio.get_current_position()
        posicion_actual_musica -=  10000
        if posicion_actual_musica > 1:
            
            posicion_audio.seek(posicion_actual_musica)
            posicion_cancion -= 10
        else: 
            reproductor_permiso = True
            posicion_actual_musica =  1
            posicion_audio.seek(1)
            posicion_cancion = 1
            reproductor.content.controls[0].content.controls[1].content.value = 0
            reproductor.update()
        modificador_de_duracion(posicion_audio, posicion_cancion)
    
    #Maneja adelantar 10 segundos hacia adelante
    def adelantar_musica(e):
        nonlocal posicion_cancion, reproductor_permiso
        duracion = posicion_audio.get_duration()
        posicion_actual_musica = posicion_audio.get_current_position()
        posicion_actual_musica +=  10000
        if duracion - posicion_actual_musica >= 10000:

            posicion_audio.seek(posicion_actual_musica)
            posicion_cancion += 10
            modificador_de_duracion(posicion_audio, posicion_cancion)
        else: 
            reproductor_permiso = False
            
            posicion_actual_musica =  duracion
            posicion_audio.seek(duracion)
            posicion_cancion = int(duracion/1000)
            reproductor.content.controls[0].content.controls[1].content.value = 1
            reproductor.update()
    
    #Funcion que maneja la construccion de los formatos de tiempo
    def constructor_del_tiempo(segundos_entregados):
        minutos, segundos = divmod(segundos_entregados, 60)
        tiempo = f"{minutos:02d}:{segundos:02d}"
        return tiempo
    
    #Funcion que maneja la carga de la barra
    def modificador_de_duracion(musica, posicion_cancion_entregada): 
        nonlocal posicion_cancion, tarea_pasada
        tarea_actual = object()
        tarea_pasada = tarea_actual
        #consigue el tiempo en segundos de la cancion
        duracion = int((musica.get_duration()/1000))
        duracion_total_texto = constructor_del_tiempo(duracion)
        for posicion_cancion_entregada in range(posicion_cancion_entregada, duracion): 
            if reproductor_permiso:
                if tarea_actual == tarea_pasada:
                    tiempo = constructor_del_tiempo(posicion_cancion_entregada)+" - "+duracion_total_texto
                    tiempo_container = ft.Container(ft.Text(tiempo, size=12, color=color_texto_especial),margin=ft.margin.only(right=10, left=15))
                    reproductor.content.controls[0].content.controls[2].content.controls[0].controls = []
                    reproductor.content.controls[0].content.controls[2].content.controls[0].controls.append(tiempo_container)

                    reproductor.content.controls[0].content.controls[1].content.value = posicion_cancion_entregada/duracion
                    #print(posicion_cancion_entregada/duracion)
                    posicion_cancion = posicion_cancion_entregada
                    reproductor.update()
                    time.sleep(1)
                    
                else: 

                    return
            else: 
                return

    #Funcion que cambia los items del reproductor
    def modificador_de_reproductor(musica, nombre):
        nonlocal reproductor_permiso, posicion_audio

        reproductor.content.controls[0].content.controls[2].content.controls[1].controls[4].value = int(posicion_audio.volume*100)

        reproductor.content.controls[0].content.controls[0].content.content.value = nombre
        reproductor.content.controls[0].content.controls[3].content.controls[1] = ft.IconButton(icon=ft.icons.PAUSE,icon_color=color_acento, scale=0.9, on_click=pause_audio)
        reproductor_permiso = True
        reproductor.open=True
        reproductor.update()
        time.sleep(1)
        if reproductor.content.controls[0].left != 0:
            reproductor.content.controls[0].left = 0
            reproductor.content.controls[0].update()
        
        modificador_de_duracion(musica, 1)

    #Reanuda el audio
    def resume_audio(e):
        nonlocal reproductor_permiso, posicion_cancion
        reproductor_permiso = True
        posicion_audio.resume()
        posicion_audio.update()
        reproductor.content.controls[0].content.controls[3].content.controls[1] = ft.IconButton(icon=ft.icons.PAUSE,icon_color=color_acento, scale=0.9, on_click=pause_audio)
        reproductor.update()
        modificador_de_duracion(posicion_audio, posicion_cancion)
    
    #Pausa el audio
    def pause_audio(e):
        nonlocal posicion_audio, reproductor_permiso
        if posicion_audio != "":
            posicion_audio.pause()
            reproductor_permiso = False
            reproductor.content.controls[0].content.controls[3].content.controls[1] = ft.IconButton(icon=ft.icons.PLAY_ARROW,icon_color=color_acento, scale=0.9, on_click=resume_audio)
            reproductor.update()
        else:
            return
    
    #Reproduce los audios
    def play_audio(e):
        nonlocal posicion_audio, posicion_cancion, audios_pasados, audios_permanentes, audios, playlist_tracker, play_list_actual,volumen_global
        audios = audios_permanentes
        if playlist_tracker:
            playlist_tracker = False
            audios_pasados = []
            audios_ya_reproducidos = []
            play_list_actual = [["none"], "none"]
            interfaz_playlist.content.controls[1].content.controls = []
            for audio in page.client_storage.get("playlist_nombres"):
                playlist_to_audio_parser(audio)
        if posicion_audio != "":
            posicion_audio.pause()
            e.control.data.play()
            posicion_audio = e.control.data
            posicion_audio.volume =  volumen_global
            posicion_audio.update()
        else:
            e.control.data.play()
            posicion_audio = e.control.data
        audios_pasados.append(e.control.data)
        posicion_cancion = 1
        modificador_de_reproductor(e.control.data, str(e.control.data).split("Music/")[1].split(".mp3")[0])
    
    #Reproduce los audios de manera automatica (cuando no hay e.control.data)
    def play_audio_automatic(audio):
        nonlocal posicion_audio, posicion_cancion, audios_pasados
        if posicion_audio != "":
            posicion_audio.pause()
        audio.play()
        posicion_audio = audio
        posicion_audio.volume =  volumen_global
        posicion_audio.update()
        audios_pasados.append(audio)
        posicion_cancion = 1
        modificador_de_reproductor(audio, str(audio).split("Music/")[1].split(".mp3")[0])
        
    #Reproductor del la app
    reproductor = ft.SnackBar(content=(ft.Stack([ft.Container(
                                                content=ft.Column([
                                                            ft.Container(
                                                                ft.Container(
                                                                    ft.Text("Hola!", 
                                                                    color=color_texto, size=12, weight=peso), 
                                                                margin=ft.margin.only(top=10)), 
                                                width=x_offset-35,alignment=ft.alignment.center, margin=ft.margin.only(left=2.5)),
                                                                                
                                                            ft.Container(ft.ProgressBar(width=x_offset-50, value=0, color=color_acento, bgcolor= color_secundario), 
                                                            alignment=ft.alignment.center, margin=ft.margin.only(top=10)), 
                                                            ft.Container(ft.Column([
                                                                                    ft.Row([ft.Container(
                                                                                            ft.Text("TIEMPO!", size=10, color=color_texto_especial,)
                                                                                            , margin=ft.margin.only(right=10, left=15))
                                                                                ], 
                                                                                
                                                                            alignment=ft.MainAxisAlignment.CENTER, spacing=0, height=15),
                                                                
                                                                                ft.Row([
                                                                                
                                                                                ft.IconButton(icon=ft.icons.REPLAY_10,icon_color=color_acento, scale=0.9, on_click=atrasar_musica),
                                                                                ft.IconButton(icon=ft.icons.SHUFFLE_ROUNDED,icon_color=color_acento, scale=0.8, on_click=shuffle_mode),
                                                                                ft.IconButton(icon=ft.icons.FORWARD_10,icon_color=color_acento, scale=0.9, on_click=adelantar_musica),
                                                                                ft.IconButton(icon=ft.icons.VOLUME_UP_ROUNDED,icon_color=color_acento, scale=0.8, on_click=subir_volumen),
                                                                                ft.Text("100",size=10, color=color_texto_especial, weight=peso)
                                                                                ], 
                                                                                
                                                                            alignment=ft.MainAxisAlignment.CENTER, spacing=0, height=35, width=x_offset-35)],
                                                                                ), 
                                                            alignment=ft.alignment.center, margin=ft.margin.only(top=5) ),
                                                            ft.Container(ft.Row([
                                                                                
                                                                                ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, icon_color=color_acento, scale=0.8, on_click=skipear_musica_atras),
                                                                                ft.IconButton(icon=ft.icons.PAUSE,icon_color=color_acento, scale=0.8, on_click=pause_audio),
                                                                                ft.IconButton(icon=ft.icons.SKIP_NEXT,icon_color=color_acento, scale=0.8, on_click=skipear_musica_adelante),  
                                                                                ft.IconButton(icon=ft.icons.VOLUME_DOWN_ROUNDED,icon_color=color_acento, scale=1, on_click=bajar_volumen), 
                                                                                ], 
                                                                            alignment=ft.MainAxisAlignment.CENTER, spacing=0,height=35), 
                                                            alignment=ft.alignment.center, )                                                            
                                                            ],
                                                        spacing=0, expand=True),
                                                gradient=gradiente, height=170, width=x_offset-35, left=x_offset, margin=0, alignment=ft.alignment.bottom_center, border_radius=ft.border_radius.all(10),
                                                animate_position=ft.animation.Animation(400, "fastOutSlowIn"))
                                                
                                                ], 
                                        height=170, width=100,)), 
                            
                    open=False, duration=1000000000,   bgcolor=ft.colors.TRANSPARENT, elevation=0, behavior=ft.SnackBarBehavior.FLOATING,margin= ft.margin.only(left=0, right=x-x_offset)    )

    #Genera los contenedores de música
    def contenedor_de_musica(audio):
        gradient_playlist = list(start_color_2.range_to(end_color_2, 8))
        # Convertimos los colores a formato hexadecimal con el prefijo requerido
        hex_gradient = [f"0xff{color.hex.lstrip('#')}" for color in gradient_playlist]
        gradiente_playlist= ft.LinearGradient(begin=ft.alignment.center_left,end=ft.alignment.bottom_right,colors=hex_gradient,tile_mode=ft.GradientTileMode.CLAMP, rotation=0)
        nonlocal posicion_audio
        contenedor = ft.Row([ft.Container(
                        content=(
                            ft.Text(audio.src.split("Music/")[1].split(".mp3")[0], weight=peso,text_align=ft.TextAlign.CENTER, color=color_texto)),
                        height=y/10, width=(x/2/2)-20,margin=7, alignment=ft.alignment.center, border_radius=ft.border_radius.all(10), gradient=gradiente_playlist)
        , ft.IconButton(icon=ft.icons.PLAY_ARROW, on_click=play_audio, data=audio, icon_color=color_acento_secundario)])

        return contenedor
    
    #Funcion que controla la barra lateral
    def abrir_menu(e):
        nonlocal reproductor
        if page.controls[0].controls[0].left == 0:
            e.control.rotate = pi
            page.controls[0].controls[0].left = -page.controls[0].controls[0].width+40
            page.controls[0].controls[1].left = 40

            page.controls[0].controls[1].width = x-40
            
            if posicion_audio != "":
                reproductor.open=False
                reproductor.update()
                #Realiza una copia de los controles de la columna
                controles = reproductor.content.controls[0].content.controls
                #Pone una fila en lugar de una columna
                reproductor.content.controls[0].content = ft.Row([], spacing= 0)
                #Rellena los controles de la fila 
                reproductor.content.controls[0].content.controls = controles
                #Ajusta el Width del nombre de la cancion
                reproductor.content.controls[0].content.controls[0].width= ((x-100)/3.2)
                reproductor.content.controls[0].content.controls[1].content.width= ((x-100)/4.3)
                reproductor.content.controls[0].content.controls[2].content.width= ((x-100)/9)
                reproductor.content.controls[0].content.controls[3].content.width= ((x-100)/8)
                #Ajusta el tamaño de los iconos

                
                
                controles_tiempo = reproductor.content.controls[0].content.controls[2].content.controls
                reproductor.content.controls[0].content.controls[2].content = ft.Row(controles_tiempo)
                
                reproductor.content.height = 40
                reproductor.content.controls[0].height=40
                reproductor.content.controls[0].width=x
                reproductor.content.controls[0].gradient = None
                reproductor.content.controls[0].bgcolor = color_secundario
                reproductor.content.controls[0].content.controls[1].content.bgcolor = color_texto_especial
                reproductor.margin = ft.margin.only(left=50, right=50)
                reproductor.open=True
                
                reproductor.update()
            
            
        else:
            e.control.rotate = pi*2
            page.controls[0].controls[0].left = 0
            page.controls[0].controls[1].left = x_offset

            page.controls[0].controls[1].width = x-x_offset
            if posicion_audio != "":
                reproductor.open=False
                reproductor.update()
            
                controles = reproductor.content.controls[0].content.controls
                #Pone una fila en lugar de una columna
                reproductor.content.controls[0].content = ft.Column([], spacing= 0, expand=True)
                #Rellena los controles de la fila 
                reproductor.content.controls[0].content.controls = controles
                #Ajusta el Width del nombre de la cancion
                reproductor.content.controls[0].content.controls[0].width= x_offset-35
                reproductor.content.controls[0].content.controls[1].content.width= x_offset-50
                reproductor.content.controls[0].content.controls[2].content.width= None
                reproductor.content.controls[0].content.controls[3].content.width= None
                #Ajusta el tamaño de los iconos

                
                controles_tiempo = reproductor.content.controls[0].content.controls[2].content.controls
                reproductor.content.controls[0].content.controls[2].content = ft.Column(controles_tiempo)
                
                reproductor.content.height = 170
                reproductor.content.controls[0].height=170
                reproductor.content.controls[0].width=x_offset-35
                reproductor.content.controls[0].gradient = gradiente
                reproductor.content.controls[0].bgcolor = None
                reproductor.content.controls[0].content.controls[1].content.bgcolor = color_secundario
                reproductor.margin = ft.margin.only(left=0, right=x-x_offset)
                reproductor.open=True
                reproductor.update()
        page.update()
    
    #Funcion que controla el sonido de los botones al hacer hover
    def sonido_botones(a):
        nonlocal audio1
        audio1.pause()
        audio1.play()
    
    def verificar_termino(e):
        estado = str(e.data)
        nonlocal audios, posicion_audio, audios_ya_reproducidos

        if estado == "completed":
            if posicion_audio not in audios_ya_reproducidos:
                audios_ya_reproducidos.append(posicion_audio)
            if len(audios_ya_reproducidos) == len(audios):
                audios_ya_reproducidos = []
            skipear_musica_adelante_non_control()
    #Funcion que maneja la recuperación de la música
    def rocola():
        
        nonlocal audios, audios_permanentes
        music_directory = 'Music'  # Asegúrate de poner la ruta correcta a tu carpeta de música
        for file in os.listdir(music_directory):
            if file.endswith('.mp3'):
                audio = ft.Audio(src=f"{music_directory}/{file}", release_mode=ft.audio.ReleaseMode.STOP, on_state_changed= verificar_termino, volume=0.5)

                audios_permanentes.append(audio)
                page.overlay.append(audio)
                
    #Direccionador es una funcion auxiliar de "cambiar pestaña", esta maneja el desplazado del usuario por las secciones, recordando las modificaciones
    def direccionador(direccion):
        nonlocal paginas, pestana, audios, posicion_audio, playlist_tracker, play_list_actual
        playlists_nombres = page.client_storage.get("playlist_nombres")
        if paginas[str(direccion)]== "":
            page.controls[0].controls.pop()
            if direccion == "Música":
                

                
                page.controls[0].controls.append(interfaz_Musica)
                
                for audio in audios_permanentes:
                    
                    page.controls[0].controls[1].content.controls[1].content.controls[0].controls.append(contenedor_de_musica(audio))
                
                for nombre in playlists_nombres:
                    playlist_to_audio_parser(nombre)
                if playlist_tracker:

                    playlist_audio_circle(play_list_actual)
                
            elif direccion == "Tareas":
                #Las siguientes lineas gestionan la lectura y adicion de las tareas a la columna en el to_do
                tareas_list= page.client_storage.get("tareas")
                tareas_status= page.client_storage.get("tareas_status")
                display_tareas = []
                for tarea_data in tareas_list:
                    for key, value in tarea_data.items():
                        #Revisa el estado de la tarea
                        if tareas_status[str(key)] == "en_progreso":
                            tarea = ft.Container(ft.Row([ ft.Row([ft.Checkbox(fill_color=color_principal, check_color=color_texto, data=key, on_change=cambiar_estado_tarea ),ft.Text(value, color=color_texto, weight=peso, data=key)], data=key), 
                            ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data=key, on_click=cambiar_nombre),ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=key,on_click=eliminar_tarea)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=key), width=x/1.5)
                        else:
                            tarea = ft.Container(ft.Row([ ft.Row([ft.Checkbox(fill_color=color_principal, value=True,check_color=color_texto, data=key, on_change=cambiar_estado_tarea ),ft.Text(value, color=color_texto, weight=peso, data=key)], data=key), 
                            ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data=key, on_click=cambiar_nombre),ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=key,on_click=eliminar_tarea)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=key), width=x/1.5)
                        display_tareas.append(tarea)
                
                interfaz_todo.content.controls[1].content.controls[1].content.controls = display_tareas
                page.controls[0].controls.append(interfaz_todo)
            pestana = direccion
            
        else:#RETOMAR AQUI
            page.controls[0].controls.pop()
            page.controls[0].controls.append(paginas[direccion])
            if direccion == "Música":

                page.controls[0].controls[1].content.controls[1].content.controls[0].controls = []
                for audio in audios_permanentes:
                    
                    page.controls[0].controls[1].content.controls[1].content.controls[0].controls.append(contenedor_de_musica(audio))

                interfaz_playlist.content.controls[1].content.controls = []
                for nombre in playlists_nombres:
                    playlist_to_audio_parser(nombre)
                    

            
            pestana = direccion
        page.update()

    #Define la barra lateral
    def generador_de_barra():
        nonlocal nombre
        
        #maneja el evento de cambiar de pestaña
        def cambiar_pestaña(e):
            nonlocal pestana, paginas
            direccion = e.control.content.controls[0].value
            paginas[pestana] = page.controls[0].controls[1]

            direccionador(direccion)
            
        #Maneja el tema que esté usando el usuario
        def nightmode(e):
            nonlocal color_principal, color_secundario, color_acento, color_acento_secundario
            if page.client_storage.contains_key("nightmode"):
                modo = page.client_storage.get("nightmode")
                page.client_storage.remove("nightmode")
                if modo:
                    page.client_storage.set("nightmode", False)
                    e.control.icon = ft.icons.NIGHTLIGHT
                else:
                    page.client_storage.set("nightmode", True)
                    e.control.icon = ft.icons.SUNNY
            page.update()
        mode = page.client_storage.get("nightmode")
        if mode:
            nightmode =ft.Row([ft.Container(ft.IconButton(ft.icons.SUNNY,on_click=nightmode, icon_color=color_texto_especial,scale=1.2), width=x_offset/2, height=y/7.5, alignment=ft.alignment.top_left, padding=10),
                            ft.Container(ft.IconButton(ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color=color_texto_especial,scale=1.2, on_click=abrir_menu,animate_rotation=ft.animation.Animation(900, "elasticIn")), width=x_offset/2, height=y/9, alignment=ft.alignment.top_right, padding=10)]) 
        else:
            nightmode =ft.Row([ft.Container(ft.IconButton(ft.icons.NIGHTLIGHT,on_click=nightmode, icon_color=color_texto_especial,scale=1.2), width=x_offset/2, height=y/7.5, alignment=ft.alignment.top_left, padding=10),
                            ft.Container(ft.IconButton(ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color=color_texto_especial,scale=1.2,on_click=abrir_menu, animate_rotation=ft.animation.Animation(900, "elasticIn")), width=x_offset/2, height=y/9, alignment=ft.alignment.top_right, padding=10)]) 
    
        imagen = ft.Row([ft.Container(width=(((x_offset)-(y/9))/2)-10, height=y/20),ft.Image(src="profile.jpeg", scale=1,border_radius=ft.border_radius.all(1500), width=y/9, )], )
        nombre = ft.Container(ft.Text(nombre, weight=peso, color=color_texto_especial, size=20), alignment=ft.alignment.center)
        modulo_primero = ft.Container(ft.ElevatedButton(content=(ft.Row([ft.Text("Principal", weight=peso),ft.Icon(ft.icons.HOME)])), bgcolor={ft.MaterialState.HOVERED:color_acento,"":color_principal}, color=color_texto ,aspect_ratio=3
                                                ,on_hover=sonido_botones, on_click=cambiar_pestaña    ), alignment=ft.alignment.center,height=y/17, )
        modulo_segundo = ft.Container(ft.ElevatedButton(content=(ft.Row([ft.Text("Tareas", weight=peso, ),ft.Icon(ft.icons.TEXT_SNIPPET)])), bgcolor={ft.MaterialState.HOVERED:color_acento,"":color_principal}, color=color_texto ,aspect_ratio=3
                                                ,on_hover=sonido_botones,on_click=cambiar_pestaña), alignment=ft.alignment.center,height=y/17, )
        modulo_tercero= ft.Container(ft.ElevatedButton(content=(ft.Row([ft.Text("Música", weight=peso), ft.Icon(ft.icons.MUSIC_NOTE_ROUNDED),])), bgcolor={ft.MaterialState.HOVERED:color_acento,"":color_principal}, color=color_texto ,aspect_ratio=3
                                                ,on_hover=sonido_botones, on_click=cambiar_pestaña), alignment=ft.alignment.center,height=y/17, )
        modulo_cuarto= ft.Container(ft.ElevatedButton(content=(ft.Row([ft.Text("Calendario", weight=peso), ft.Icon(ft.icons.CALENDAR_TODAY_ROUNDED),])), bgcolor={ft.MaterialState.HOVERED:color_acento,"":color_principal}, color=color_texto ,aspect_ratio=3.5
                                                ,on_hover=sonido_botones, on_click=cambiar_pestaña), alignment=ft.alignment.center,height=y/17, )

        
        return [nightmode,imagen, nombre, modulo_primero, modulo_segundo, modulo_tercero, modulo_cuarto]
    
    #Interfaz de "PRINCIPAL"
    interfaz_inicial= ft.Stack([ft.Container(
                                    content=ft.Column(generador_de_barra()),
                                width=x_offset, left=0, height=y, bgcolor=color_secundario, animate_position=ft.animation.Animation(400, "linear")), 
                                ft.Container(
                                    content=ft.Stack([
                                        ft.Container(
                                            ft.Text("Principal",
                                            color=color_texto, size=22), 
                                        alignment=ft.alignment.center, width=x/1.5, height=y/10, top=20 ),
                                        ft.Card(
                                            ft.Stack([ft.Column()]),
                                        color=color_secundario, width=x/1.5, height=y/1.35,top=y/8)
                                        
                                            ], height=y, width=x/1.5),

                                width=x-x_offset, height=y, left=x_offset, animate_position=ft.animation.Animation(400, "linear"), 
                                animate_size=ft.animation.Animation(600, "linear"),    alignment=ft.alignment.center ,               
                                gradient=gradiente),
                        
                                ],height=y, width=x,)

    
    #Lleva el registro del estado de las tareas
    def cambiar_estado_tarea(e):
        data = str(e.control.data)
        tareas_status = page.client_storage.get("tareas_status")
        
        if data in tareas_status:

            if tareas_status[data] == "en_progreso":
                tareas_status[data] = "completada"
            elif tareas_status[data] == "completada":
                tareas_status[data] = "en_progreso"

            page.client_storage.set("tareas_status", tareas_status)

    #Maneja la gestion del evento de cancelacion de edicion de la tarea
    def cancelar_edicion(e):
        tareas_list= page.client_storage.get("tareas")
        tareas_status= page.client_storage.get("tareas_status")
        for tarea_data in tareas_list:
            for key, value in tarea_data.items():
                if str(e.control.data) == key:
                    numero_aleatorio, tarea = key, value
                    break
        for contenedor in page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls:

            if contenedor.content.controls[0].data == e.control.data:

                contenedor.content.alignment = ft.MainAxisAlignment.SPACE_EVENLY
                if tareas_status[str(e.control.data)] == "en_progreso":
                    contenedor.content.controls[0] =   ft.Row([
                                                    ft.Checkbox(fill_color=color_principal, check_color=color_texto, data= numero_aleatorio, on_change=cambiar_estado_tarea ),
                                                    ft.Text(tarea, color=color_texto, weight=peso, data= numero_aleatorio)], data=numero_aleatorio) 
                else:
                    contenedor.content.controls[0] =     ft.Row([
                                                    ft.Checkbox(fill_color=color_principal, value=True,check_color=color_texto, data= numero_aleatorio, on_change=cambiar_estado_tarea ),
                                                    ft.Text(tarea, color=color_texto, weight=peso, data= numero_aleatorio)], data=numero_aleatorio) 
                contenedor.content.controls[1] =  ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data= numero_aleatorio, on_click=cambiar_nombre),
                                                        ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=numero_aleatorio,on_click=eliminar_tarea)])
        page.update()
    
    #Maneja el cambio de nombre de la tarea
    def cambiar_nombre_confirmed(e):
        tareas_list = page.client_storage.get("tareas")
        tareas_status = page.client_storage.get("tareas_status")
        nuevo_nombre = ""
        for tarea in tareas_list:
            
            for key, value in tarea.items():
                if e.control.data == key:
                    for tarea2 in page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls:
                        if tarea2.content.controls[0].data == e.control.data:
                            nuevo_nombre = tarea2.content.controls[0].controls[0].value
                            if nuevo_nombre != "":
                                tarea2.content.alignment = ft.MainAxisAlignment.SPACE_EVENLY
                                if tareas_status[str(e.control.data)] == "en_progreso":
                                    tarea2.content.controls[0] =   ft.Row([
                                                    ft.Checkbox(fill_color=color_principal, check_color=color_texto, data= e.control.data, on_change=cambiar_estado_tarea ),
                                                    ft.Text(nuevo_nombre, color=color_texto, weight=peso, data= e.control.data)], data=e.control.data) 
                                else:
                                    tarea2.content.controls[0] =   ft.Row([
                                                    ft.Checkbox(fill_color=color_principal, check_color=color_texto, value=True,data= e.control.data, on_change=cambiar_estado_tarea ),
                                                    ft.Text(nuevo_nombre, color=color_texto, weight=peso, data= e.control.data)], data=e.control.data) 
                                tarea2.content.controls[1] =  ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data= e.control.data, on_click=cambiar_nombre),
                                                        ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=e.control.data,on_click=eliminar_tarea)])
                                tarea[key] = nuevo_nombre
                                tareas_list = page.client_storage.set("tareas", tareas_list)
                                page.update()
    
    #Maneja el disparador de cambio de nombre
    def cambiar_nombre(e):


            
        for tarea in page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls:

            if tarea.content.controls[0].data == e.control.data:
                
                tarea.content.alignment = ft.MainAxisAlignment.CENTER

                tarea.content.controls[0].controls = [ft.TextField(
                                                        data=e.control.data,
                                                        on_submit=cambiar_nombre_confirmed,
                                                        autofocus=True,
                                                        width=300,
                                                        height=50,
                                                        border_color=color_acento, 
                                                        cursor_color=color_acento, 
                                                        color=color_texto_especial, 
                                                        text_style=ft.TextStyle(size=15),
                                                        label="Nuevo nombre", 
                                                        label_style=ft.TextStyle(color=color_acento_secundario))]
                tarea.content.controls[1].controls = [ft.IconButton(icon=ft.icons.CHECK, icon_color=color_texto_especial, data= e.control.data, on_click=cambiar_nombre_confirmed),
                                                        ft.IconButton(icon=ft.icons.CANCEL,icon_color=color_texto_especial, data=e.control.data, on_click=cancelar_edicion)]
                page.update()

    #Maneja el evento de eliminacion de tarea
    def eliminar_tarea(e):
        data = str(e.control.data)
        tareas_status = page.client_storage.get("tareas_status")
        tareas_list = page.client_storage.get("tareas")
        numeros_aleatorios = page.client_storage.get("tarea_data")
        for tarea in tareas_list:
            for key, value in tarea.items():

                if key == data:

                    for tarea2 in page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls:
                            if str(tarea2.content.controls[0].data) == data:
                                page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls.remove(tarea2)
                                tareas_list.remove(tarea)
                                page.client_storage.set("tareas", tareas_list)
                                for numero in numeros_aleatorios:
                                    if str(numero) == data:
                                        numeros_aleatorios.remove(numero)
                                if tareas_list == []:
                                    numeros_aleatorios= []
                                page.client_storage.set("tarea_data", numeros_aleatorios)
                                
                                del tareas_status[data]
                                page.client_storage.set("tareas_status", tareas_status)

        page.update()
    
    #Maneja el evento de agregar tarea
    def agregar_tarea(e):
        tareas_status = page.client_storage.get("tareas_status")
        numeros_aleatorios = page.client_storage.get("tarea_data")
        tareas_list = page.client_storage.get("tareas")
        while True:
            numero_aleatorio = random.uniform(0, 100000)
            if numero_aleatorio not in numeros_aleatorios:
                numeros_aleatorios.append(numero_aleatorio)
                page.client_storage.set("tarea_data",numeros_aleatorios) 
                
                break

            
        
        tarea = page.controls[0].controls[1].content.controls[1].content.controls[0].content.controls[0].controls[0].value
        if tarea != "":
            template_todo = ft.Container(
                                        ft.Row([  
                                                ft.Row([
                                                    ft.Checkbox(fill_color=color_principal, check_color=color_texto, data= numero_aleatorio, on_change=cambiar_estado_tarea ),
                                                    ft.Text(tarea, color=color_texto, weight=peso, data= numero_aleatorio)], data=numero_aleatorio), 
                                                ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data= numero_aleatorio, on_click=cambiar_nombre),
                                                        ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=numero_aleatorio, on_click=eliminar_tarea)]) ] ,
                                            width=x/1.5, alignment=ft.MainAxisAlignment.SPACE_EVENLY), width=x/1.5)

            if len(tareas_list) == 0:
                interfaz_todo.content.controls[1].content.controls[1].content.controls = []
            page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls.append(template_todo)
            tareas_list.append({numero_aleatorio:tarea})
            page.client_storage.set("tareas", tareas_list)
            page.controls[0].controls[1].content.controls[1].content.controls[0].content.controls[0].controls[0].value = ""
            tareas_status[f"{numero_aleatorio}"] = "en_progreso"
            page.client_storage.set("tareas_status", tareas_status)

            page.update()
    
    #Filtra por todas las tareas
    def filtro_todas(e):
        tareas_status = page.client_storage.get("tareas_status")
        tareas_list = page.client_storage.get("tareas")
        display_tareas = []
        page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls = []
        for tarea_data in tareas_list:
            for key, value in tarea_data.items():
                #Revisa el estado de la tarea
                if tareas_status[str(key)] == "completada":
                    tarea = ft.Container(ft.Row([ ft.Row([ft.Checkbox(fill_color=color_principal, value=True,check_color=color_texto, data=key, on_change=cambiar_estado_tarea ),ft.Text(value, color=color_texto, weight=peso, data=key)], data=key), 
                            ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data=key, on_click=cambiar_nombre),ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=key,on_click=eliminar_tarea)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=key), width=x/1.5)
                else:
                    tarea = ft.Container(ft.Row([ ft.Row([ft.Checkbox(fill_color=color_principal,check_color=color_texto, data=key, on_change=cambiar_estado_tarea ),ft.Text(value, color=color_texto, weight=peso, data=key)], data=key), 
                            ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data=key, on_click=cambiar_nombre),ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=key,on_click=eliminar_tarea)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=key), width=x/1.5)
                display_tareas.append(tarea)
        if len(tareas_list) == 0:
            tarea = ft.Container(ft.Row([ ft.Row([ft.Text("Aún no tienes tareas.", color=color_texto, weight=peso)]), 
                            ft.Row([ft.Icon(name=ft.icons.INFO_ROUNDED, color=color_acento_secundario,)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.CENTER), width=x/1.5)
            display_tareas.append(tarea)
        interfaz_todo.content.controls[1].content.controls[0].content.controls[2].controls[0].controls = [ft.Text("Todas", color=color_acento_secundario, weight=peso, style=ft.TextStyle(italic=True, )),ft.Icon(ft.icons.ALL_INCLUSIVE, color=color_acento_secundario)]
        interfaz_todo.content.controls[1].content.controls[1].content.controls = display_tareas
        page.update()
    
    #Filtra por las tareas completas
    def filtro_tareas_completadas(e):
        tareas_status = page.client_storage.get("tareas_status")
        tareas_list = page.client_storage.get("tareas")
        display_tareas = []
        page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls = []
        for tarea_data in tareas_list:
            for key, value in tarea_data.items():   
                #Revisa el estado de la tarea
                if tareas_status[str(key)] == "completada":
                    tarea = ft.Container(ft.Row([ ft.Row([ft.Checkbox(fill_color=color_principal, value=True,check_color=color_texto, data=key, on_change=cambiar_estado_tarea ),ft.Text(value, color=color_texto, weight=peso, data=key)], data=key), 
                            ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data=key, on_click=cambiar_nombre),ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=key,on_click=eliminar_tarea)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=key), width=x/1.5)
                    display_tareas.append(tarea)
        
        if len(tareas_list) == 0:
            tarea = ft.Container(ft.Row([ ft.Row([ft.Text("Aún no tienes tareas.", color=color_texto, weight=peso)]),
                            ft.Row([ft.Icon(name=ft.icons.INFO_ROUNDED, color=color_acento_secundario,)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.CENTER), width=x/1.5)
            display_tareas.append(tarea)
        interfaz_todo.content.controls[1].content.controls[0].content.controls[2].controls[0].controls = [ft.Text("Completadas", color=color_acento_secundario, weight=peso, style=ft.TextStyle(italic=True, )),ft.Icon(ft.icons.CHECK, color=color_acento_secundario)]
        interfaz_todo.content.controls[1].content.controls[1].content.controls = display_tareas
        page.update()
    
    #Filtra por las tareas pendientes
    def flitro_tareas_pendientes(e):
        tareas_status = page.client_storage.get("tareas_status")
        tareas_list = page.client_storage.get("tareas")
        display_tareas = []
        page.controls[0].controls[1].content.controls[1].content.controls[1].content.controls = []
        for tarea_data in tareas_list:
            for key, value in tarea_data.items():
                #Revisa el estado de la tarea
                if tareas_status[str(key)] == "en_progreso":
                    tarea = ft.Container(ft.Row([ ft.Row([ft.Checkbox(fill_color=color_principal, check_color=color_texto, data=key, on_change=cambiar_estado_tarea ),ft.Text(value, color=color_texto, weight=peso, data=key)], data=key), 
                            ft.Row([ft.IconButton(icon=ft.icons.MODE_EDIT, icon_color=color_acento_secundario, data=key, on_click=cambiar_nombre),ft.IconButton(icon=ft.icons.RESTORE_FROM_TRASH_ROUNDED,icon_color=color_acento_secundario, data=key,on_click=eliminar_tarea)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=key), width=x/1.5)
                    display_tareas.append(tarea)
        if len(tareas_list) == 0:
            tarea = ft.Container(ft.Row([ ft.Row([ft.Text("Aún no tienes tareas.", color=color_texto, weight=peso)]),
                            ft.Row([ft.Icon(name=ft.icons.INFO_ROUNDED, color=color_acento_secundario,)]) ] ,width=x/1.5, alignment=ft.MainAxisAlignment.CENTER), width=x/1.5)
            display_tareas.append(tarea)
        interfaz_todo.content.controls[1].content.controls[0].content.controls[2].controls[0].controls = [ft.Text("Completadas", color=color_acento_secundario, weight=peso, style=ft.TextStyle(italic=True, )),ft.Icon(ft.icons.CHECK, color=color_acento_secundario)]
        interfaz_todo.content.controls[1].content.controls[1].content.controls = display_tareas
        page.update()
        interfaz_todo.content.controls[1].content.controls[0].content.controls[2].controls[0].controls = [ft.Text("Pendientes", color=color_acento_secundario, weight=peso, style=ft.TextStyle(italic=True, )),ft.Icon(ft.icons.PENDING, color=color_acento_secundario)]
        interfaz_todo.content.controls[1].content.controls[1].content.controls = display_tareas
        page.update()
        
    
    interfaz_todo= ft.Container(
                                    content=ft.Stack([
                                        ft.Container(
                                            ft.Text("Tareas",
                                            color=color_texto, size=22), 
                                        alignment=ft.alignment.center, width=x/1.5, height=y/10, top=20 ),
                                        ft.Card(
                                            ft.Stack([
                                                ft.Container(
                                                    content=(
                                                    ft.Column([
                                                    ft.Row([
                                                        ft.TextField(
                                                        width=x/1.5/2, border_color=color_acento, cursor_color=color_acento, color=color_texto_especial, label="¿Qué tarea tienes pendiente?", label_style=ft.TextStyle(color=color_acento_secundario), on_submit=agregar_tarea), 
                                                        ft.IconButton(
                                                        icon=ft.icons.ADD_BOX_ROUNDED,icon_size=50, icon_color=color_acento, on_click=agregar_tarea
                                                            )],
                                                    width=x/1.5, alignment=ft.MainAxisAlignment.CENTER, height=y/8/1.2, ),
                                                    ft.Row([
                                                            ft.ElevatedButton(content=(ft.Row([ft.Text("Todas", weight=peso), ft.Icon(ft.icons.ALL_INCLUSIVE),])), on_click=filtro_todas,bgcolor={ft.MaterialState.HOVERED: color_acento_secundario   ,"":color_acento}, color={ft.MaterialState.HOVERED: color_acento   ,"":color_texto}
                                                            ,on_hover=sonido_botones),
                                                            ft.ElevatedButton(content=(ft.Row([ft.Text("Pendientes", weight=peso), ft.Icon(ft.icons.PENDING),])),on_click=flitro_tareas_pendientes ,bgcolor={ft.MaterialState.HOVERED: color_acento_secundario   ,"":color_acento}, color={ft.MaterialState.HOVERED: color_acento   ,"":color_texto}
                                                            ,on_hover=sonido_botones),
                                                            ft.ElevatedButton(content=(ft.Row([ft.Text("Completadas", weight=peso), ft.Icon(ft.icons.CHECK),])), on_click=filtro_tareas_completadas,bgcolor={ft.MaterialState.HOVERED: color_acento_secundario   ,"":color_acento}, color={ft.MaterialState.HOVERED: color_acento   ,"":color_texto}
                                                            ,on_hover=sonido_botones),
                                                            ],
                                                    width=x/1.5, alignment=ft.MainAxisAlignment.CENTER,height=y/8/1.2),
                                                    ft.Row([
                                                            ft.Row([ft.Text("Todas", color=color_acento_secundario, weight=peso, style=ft.TextStyle(italic=True, )),ft.Icon(ft.icons.ALL_INCLUSIVE, color=color_acento_secundario)])
                                                            ],
                                                    width=x/1.5, alignment=ft.MainAxisAlignment.CENTER,height=y/8/4, spacing=0),
                                                    
                                                    ], spacing=0))
                                                    
                                                ,alignment=ft.alignment.center, width=x/1.5, height=y/3, margin=ft.margin.only(top=10) ),
                                                ft.Container(
                                                ft.Column(controls=[]
                                                    
                                                
                                                ,spacing=10, scroll=ft.ScrollMode.AUTO, width=x/1.5, auto_scroll=True)
                                                ,width=x/1.5 , margin=ft.margin.only( top=((y/8/1.2)*2)+40))    
                                                
                                                ]), 
                                        color=color_secundario, width=x/1.5, height=y/1.35,top=y/8)
                                        
                                            ], height=y, width=x/1.5),

                                width=x-x_offset, height=y, left=x_offset, animate_position=ft.animation.Animation(400, "linear"), 
                                animate_size=ft.animation.Animation(600, "linear"),    alignment=ft.alignment.center ,               
                                gradient=gradiente)
    
    
    def resultado_dialogo_eliminacionfinal(e):
        nonlocal playlist_a_eliminar
        for item in page.overlay:
            if item.data == "alertaRestaurarPlaylist2":
                item.open = False
                item.update()
                page.overlay.remove(item)
        if str(e.control.data) == "accept":
            playlists_nombres = page.client_storage.get("playlist_nombres")
            playlists = page.client_storage.get("playlists")
            del playlists[playlist_a_eliminar]
            playlists_nombres.remove(playlist_a_eliminar)
            
            page.client_storage.set("playlist_nombres", playlists_nombres)
            page.client_storage.set("playlists", playlists)
            
            interfaz_playlist.content.controls[1].content.controls = []
            for audio in page.client_storage.get("playlist_nombres"):
                playlist_to_audio_parser(audio)

    
    def alerta_eliminacion_final_playlist(modo,mensaje, mensaje_dos):
        if modo:
            alerta = ft.AlertDialog(bgcolor=color_principal,
                                on_dismiss=resultado_dialogo_eliminacionfinal,
                                modal=False,
                                title=ft.Text(mensaje, color=color_acento),
                                content=ft.Text(mensaje_dos, text_align=ft.alignment.center, color=color_texto),
                                actions=[
                                        ft.IconButton(ft.icons.CHECK_CIRCLE_ROUNDED, icon_color=color_acento_secundario, icon_size=30, data="accept", on_click=resultado_dialogo_eliminacionfinal),
                                        ft.IconButton(ft.icons.CANCEL_ROUNDED, icon_color=color_acento_secundario, icon_size=30, data="cancel", on_click=resultado_dialogo_eliminacionfinal),
                                        ],
                                actions_alignment=ft.MainAxisAlignment.CENTER,
                                data="alertaRestaurarPlaylist2"
                                )
        else:
            alerta = ft.AlertDialog(bgcolor=color_principal,
                                on_dismiss=resultado_dialogo_eliminacionfinal,
                                modal=False,
                                title=ft.Text(mensaje, color=color_acento),
                                content=ft.Text(mensaje_dos, text_align=ft.alignment.center, color=color_texto),
                                actions=[
                                        ft.IconButton(ft.icons.CHECK_CIRCLE_ROUNDED, icon_color=color_acento_secundario, icon_size=30, data="cancel", on_click=resultado_dialogo_eliminacionfinal),
                                        ],
                                actions_alignment=ft.MainAxisAlignment.CENTER,
                                data="alertaRestaurarPlaylist2"
                                )
        page.overlay.append(alerta)
        alerta.open = True
        page.update()

        
        
        
    def eliminacion_playlist(e):
        nonlocal play_list_actual, playlist_a_eliminar
        playlist_a_eliminar = e.control.data[1]
        if play_list_actual[1] == playlist_a_eliminar:
            alerta_eliminacion_final_playlist(False,f"No puedes eliminar \n playlists en curso.", "Porfavor reproduce otras para eliminar esta.")
            return
        
        alerta_eliminacion_final_playlist(True,f"¿Eliminar playlist {playlist_a_eliminar} ({len(e.control.data[0])} canciones)?", "Esta acción no se puede deshacer.")
        

        
    #Confirma la creación de una playlist
    def confirmar_creacion_playlist(e):
        nonlocal playlist_parcial
        if playlist_parcial == []:
            return
        playlist_simplificada = []
        playlists = page.client_storage.get("playlists")
        playlists_nombres = page.client_storage.get("playlist_nombres")
        nuevo_nombre = interfaz_Musica.content.controls[2].content.controls[0].content.controls[0].value
        interfaz_Musica.content.controls[2].content.controls[0].content.controls[0].value=""
        playlists_nombres.append(nuevo_nombre)
        
        #Actualiza los client storage
        for item in playlist_parcial:
            playlist_simplificada.append(str(item))
        playlists[nuevo_nombre] = playlist_simplificada
        
        page.client_storage.set("playlist_nombres", playlists_nombres)  
        page.client_storage.set("playlists", playlists)
        #llama al parser de audio que maneja la gestion de elementos de audio en formato str
        playlist_to_audio_parser(nuevo_nombre)
    
    

    #Funcion que inicia la reproducción de una playlist
    def reproducir_playlist(e):
        nonlocal audios, audios_pasados, audios_ya_reproducidos, posicion_audio, playlist_tracker, play_list_actual
        audios = e.control.data[0]
        play_list_actual = e.control.data
        audios_pasados = []
        audios_ya_reproducidos = []
        playlist_tracker = True
        playlist_audio_circle(e.control.data)
        play_audio_automatic(e.control.data[0][0])
        
    
    
    def playlist_audio_circle(audios_en_lista):
        

        if not playlist_tracker:
            return

        for playlist_container_positioned in interfaz_playlist.content.controls[1].content.controls:

            if playlist_container_positioned.controls[0].content.data == audios_en_lista:
      
                if len(playlist_container_positioned.controls[0].content.controls) == 3:
                    
                    playlist_container_positioned.controls[0].content.controls.append(ft.ProgressRing(color=color_secundario ,width=25, height=25, bgcolor=color_acento_secundario))
                    playlist_container_positioned.controls[0].content.controls[1].icon_color = ft.colors.TEAL_600
                    playlist_container_positioned.controls[0].content.controls[2].icon_color = ft.colors.RED_600
            else:
                if len(playlist_container_positioned.controls[0].content.controls) > 3:
                    playlist_container_positioned.controls[0].content.controls[1].icon_color = color_acento_secundario
                    playlist_container_positioned.controls[0].content.controls[2].icon_color = color_acento_secundario
                    playlist_container_positioned.controls[0].content.controls.pop()

        page.update()

        

                #playlist_container.controls[0].content.controls.append(ft.ProgressBar(color=color_acento, width=20))
    #crea un contenedor por cada playlist, con su nombre almacenado y los datos correspondientes a su reproduccion
    #Es el paso final del audio_parser
    def playlist_to_display(audios_en_lista, nombre):
        nonlocal play_list_actual
        
        gradient_playlist = list(start_color_2.range_to(end_color_2, 8))
        # Convertimos los colores a formato hexadecimal con el prefijo requerido
        hex_gradient = [f"0xff{color.hex.lstrip('#')}" for color in gradient_playlist]
        gradiente_playlist= ft.LinearGradient(begin=ft.alignment.top_left,end=ft.alignment.bottom_right,colors=hex_gradient,tile_mode=ft.GradientTileMode.CLAMP, rotation=0)


        if play_list_actual[1] == nombre:
            playlist_container = ft.Row([ft.Container(
                                    content=(ft.Row([ft.Text(nombre +f"({len(audios_en_lista)})", color=color_texto, weight=peso),
                                            ft.IconButton(icon=ft.icons.PLAY_ARROW, data=[audios_en_lista,nombre], on_click=reproducir_playlist, icon_color=ft.colors.TEAL_600),
                                            ft.IconButton(icon=ft.icons.REMOVE, data=[audios_en_lista,nombre] , icon_color=ft.colors.RED_600, on_click=eliminacion_playlist),
                                            ft.ProgressRing(color=color_secundario ,width=25, height=25, bgcolor=color_acento_secundario),

                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER, data=[audios_en_lista,nombre], spacing=0
                                                    )
                                            ),
                                    width=(x/4)-40,
                                    alignment=ft.alignment.center, 
                                    border_radius=ft.border_radius.all(10),
                                    margin=ft.margin.only(left=15), 
                                    
                                    padding=10,
                                    gradient=gradiente_playlist
                                                    )
                                    ],
                            width=x/4-40, alignment=ft.MainAxisAlignment.CENTER)
        else:
            playlist_container = ft.Row([ft.Container(
                                    content=(ft.Row([ft.Text(nombre +f"({len(audios_en_lista)})", color=color_texto, weight=peso),
                                            ft.IconButton(icon=ft.icons.PLAY_ARROW, data=[audios_en_lista,nombre], on_click=reproducir_playlist, icon_color=color_acento_secundario),
                                            ft.IconButton(icon=ft.icons.REMOVE, data=[audios_en_lista,nombre], icon_color=color_acento_secundario,on_click=eliminacion_playlist)
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER, data=[audios_en_lista,nombre], spacing=0
                                                    )
                                            ),
                                    width=(x/4)-40,
                                    alignment=ft.alignment.center, 
                                    border_radius=ft.border_radius.all(10),
                                    margin=ft.margin.only(left=15), 
                                    
                                    padding=10,
                                    gradient=gradiente_playlist
                                                    )
                                    ],
                            width=x/4-40, alignment=ft.MainAxisAlignment.CENTER)
        
        interfaz_playlist.content.controls[1].content.controls.append(playlist_container)
        page.end_drawer.open=False

        page.update()
    
    #Extrae el src de cualquier audio en formato str
    def extractor_de_datos_audio(audio):
        patron = re.compile(r"'src':\s*['\"](.*?)\.mp3")
        resultado = patron.search(audio)
    
        if resultado:
            # Agregamos la extensión .mp3 porque sabemos que todos son archivos mp3
            return resultado.group(1) + ".mp3"

        
    #Funcion principal que toma un nombre y termina con la adicion al display y al overlay de una lista de audios asociados a un nombre
    def playlist_to_audio_parser(nombre):
        audios_de_la_playlist = []
        playlist_en_audios = []
        playlists = page.client_storage.get("playlists")
        for audio in playlists[nombre]:
            audios_de_la_playlist.append(extractor_de_datos_audio(audio))
        for origen in audios_de_la_playlist:
            audio_convertido_en_objeto = ft.Audio(src=origen, release_mode=ft.audio.ReleaseMode.STOP, on_state_changed=verificar_termino, volume=0.5)
            
            playlist_en_audios.append(audio_convertido_en_objeto)
            if audio_convertido_en_objeto not in page.overlay:
                page.overlay.append(audio_convertido_en_objeto)
        
        playlist_to_display(playlist_en_audios, nombre)
        
    
    #Maneja la gestion de eliminacion de canciones del display
    def gestor_eliminacion(lista_a_eliminar):
        for cancion in lista_a_eliminar:
            end_drawer.controls[1].controls.remove(cancion)
            if cancion not in lista_busqueda_eliminados:
                lista_busqueda_eliminados.append(cancion)
    
    #Restaura las visualizacion perdidas que coincidan
    def restaurador_de_busqueda(resultado):
        nonlocal lista_busqueda_eliminados
        lista_restaurar = []
        for cancion_eliminada in lista_busqueda_eliminados:
            titulo = cancion_eliminada.controls[0].content.value.lower()
            titulo_formateado = re.sub(r'\s{2,}', ' ', titulo)
            if resultado in titulo_formateado:
                end_drawer.controls[1].controls.append(cancion_eliminada)
                lista_restaurar.append(cancion_eliminada)
        for cancion_restaurada in lista_restaurar:
            lista_busqueda_eliminados.remove(cancion_restaurada)
    
    #Ordena las canciones por titulo
    def ordenar_canciones_por_titulo():
        # Extraemos las canciones y sus títulos formateados en pares de (título formateado, objeto canción)
        canciones_y_titulos = [
        (re.sub(r'\s{2,}', ' ', cancion.controls[0].content.value.lower()), cancion)
        for cancion in end_drawer.controls[1].controls
    ]
        # Ordenamos los pares por el título formateado
        canciones_y_titulos.sort(key=lambda x: x[0])
            # Extraemos las canciones ordenadas de los pares
        canciones_ordenadas = [cancion for _, cancion in canciones_y_titulos]
        # Reasignamos las canciones ordenadas a end_drawer.controls[1].controls
        end_drawer.controls[1].controls = canciones_ordenadas
        end_drawer.controls[0].content.controls[2].controls[0].value = str(len(end_drawer.controls[1].controls))
        end_drawer.update()
    
    #Funcion principal que meaneja la busquerda
    def manejador_busqueda(e):
        nonlocal lista_busqueda_eliminados
        lista_a_eliminar = []
        busqueda = e.control.value.strip()  # Eliminar espacios exteriores
        busqueda = busqueda.lower()
        resultado = re.sub(r'\s{2,}', ' ', busqueda)

        for cancion in end_drawer.controls[1].controls:
            titulo= cancion.controls[0].content.value.lower()
            titulo_formateado = re.sub(r'\s{2,}', ' ', titulo)

            if resultado not in titulo_formateado:

                lista_a_eliminar.append(cancion)
                
            
        gestor_eliminacion(lista_a_eliminar)
        restaurador_de_busqueda(resultado)
        ordenar_canciones_por_titulo()

    #Maneja el evento de eliminar una cancion de la playlist en construcción
    def eliminar_de_playlist(e):
        nonlocal playlist_parcial
        e.control.icon = ft.icons.LIBRARY_ADD
        e.control.icon_color = ft.colors.TEAL_600

        e.control.on_click = agregar_a_playlist
        playlist_parcial.remove(e.control.data)
        end_drawer.controls[0].content.controls[2].controls[1].value = str(len(playlist_parcial))
        end_drawer.controls[0].content.controls[2].controls[1].update()

        e.control.update()
    
    #Maneja el evento de agregar una cancion de la playlist en construcción
    def agregar_a_playlist(e):
        nonlocal playlist_parcial
        e.control.icon = ft.icons.REMOVE_CIRCLE_ROUNDED
        e.control.icon_color = ft.colors.RED_600
        e.control.on_click = eliminar_de_playlist
        playlist_parcial.append(e.control.data)
        end_drawer.controls[0].content.controls[2].controls[1].value = str(len(playlist_parcial))
        end_drawer.controls[0].content.controls[2].controls[1].update()

        e.control.update()

    #genera los contenedores de la musica en la bara de playlist 
    def contenedor_de_musica_playlist(audio):
        
        nonlocal posicion_audio
        contenedor = ft.Row([ft.Container(
                        content=(
                            ft.Text(value=audio.src.split("Music/")[1].split(".mp3")[0], weight=peso,text_align=ft.TextAlign.CENTER, color=color_texto, size=12)),
                        width=x_offset-25,alignment=ft.alignment.center, border_radius=ft.border_radius.all(5), 
                        border=ft.border.all(1, color_principal),

                        padding=10,
                        bgcolor="transparent",
                        )
        , ft.IconButton(icon=ft.icons.PLAY_ARROW, on_click=play_audio, data=audio, icon_color=color_acento_secundario),
            ft.IconButton(icon=ft.icons.LIBRARY_ADD, on_click=agregar_a_playlist, data=audio, icon_color=ft.colors.TEAL_600)            ])

        return contenedor

    #maneja el evento del dialogo cuando se quiere reiniciar la playlist
    def resultado_dialogo_playlist(e):
        if str(e.control.data) == "accept":
            restaurador_de_playlist()
        for item in page.overlay:
            if item.data == "alertaRestaurarPlaylist":
                item.open = False
                item.update()
                page.overlay.remove(item)
    
    #genera el mensaje de reinicio
    def alerta_reinicio():
        alerta = ft.AlertDialog(bgcolor=color_principal,
                                on_dismiss=resultado_dialogo_playlist,
                                modal=False,
                                title=ft.Text("¿Deseas reiniciar la playlist \n en construcción?", color=color_acento),
                                content=ft.Text("Tendrás que empezar a construirla de nuevo.", text_align=ft.alignment.center, color=color_texto),
                                actions=[
                                        ft.IconButton(ft.icons.CHECK_CIRCLE_ROUNDED, icon_color=color_acento_secundario, icon_size=30, data="accept", on_click=resultado_dialogo_playlist),
                                        ft.IconButton(ft.icons.CANCEL_ROUNDED, icon_color=color_acento_secundario, icon_size=30, data="cancel", on_click=resultado_dialogo_playlist),
                                        ],
                                actions_alignment=ft.MainAxisAlignment.CENTER,
                                data="alertaRestaurarPlaylist"
                                )
        page.overlay.append(alerta)
        alerta.open = True
        page.update()

    #Restaura el selector de playlist
    def restart_playlist(e):
        nonlocal playlist_parcial
        if len(playlist_parcial) > 0:
            alerta_reinicio()

    #Funcion que carga el añadidor de playlist
    def restaurador_de_playlist():
        nonlocal audios_permanentes, lista_busqueda_eliminados, playlist_parcial
        playlist_parcial = []
        end_drawer_column = []
        #end_drawer.controls.controls = ft.Column([])
        for audio in audios_permanentes:
            end_drawer_column.append(contenedor_de_musica_playlist(audio))
        end_drawer.controls[1].controls = end_drawer_column
        end_drawer.controls[0].content.controls[0].value =""
        end_drawer.controls[0].content.controls[2].controls[1].value = str(len(playlist_parcial))
        end_drawer.controls[0].content.controls[2].controls[0].value = str(len(end_drawer.controls[1].controls))
        end_drawer.update()


    #Contenedor del añadidor de playlist
    end_drawer = ft.NavigationDrawer(
        bgcolor=end_color_2,
        
        controls=[ft.Container(ft.Row([ft.TextField(        on_change=manejador_busqueda,
                                                            width=x_offset-30,
                                                            border_color=color_acento_secundario, 
                                                            cursor_color=color_acento, 
                                                            color=color_texto_especial, 
                                                            label="Busqueda", 
                                                            label_style=ft.TextStyle(color=color_acento_secundario)),
                                        ft.Column([ft.IconButton(
                                                    icon=ft.icons.CHECK, 
                                                    icon_color=color_acento_secundario, 
                                                    bgcolor={ft.MaterialState.FOCUSED:color_texto, "": ft.colors.TRANSPARENT},
                                                    on_click=confirmar_creacion_playlist),
                                                    
                                                    ft.IconButton(
                                                    icon=ft.icons.RESTART_ALT_ROUNDED, 
                                                    on_click=restart_playlist,
                                                    icon_color=color_acento_secundario, 
                                                    bgcolor={ft.MaterialState.FOCUSED:color_texto, "": ft.colors.TRANSPARENT})
                                                
                                                
                                                ], 
                                        alignment=ft.MainAxisAlignment.CENTER)
                                        
                                        ,
                                        ft.Column([ft.Text("", color=color_texto_especial, weight=peso, size=17),
                                                    ft.Text("", color=ft.colors.TEAL_600, weight=peso, size=17)
                                                
                                                
                                                ], 
                                        alignment=ft.MainAxisAlignment.CENTER),

                                        ],
                                alignment=ft.MainAxisAlignment.CENTER) , 
                height=200, gradient=gradiente_2, alignment=ft.alignment.center),
                    ft.Column([
                            
                            ], 
                    spacing=30, width=x_offset, alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS, )
                    ],
        
    )
    
    
    
    
    page.end_drawer = end_drawer
                
    def openDrawer(e):
        restaurador_de_playlist()
        playlists_nombres = page.client_storage.get("playlist_nombres")
        nombre_playlists = interfaz_Musica.content.controls[2].content.controls[0].content.controls[0].value
        if nombre_playlists == "":
            interfaz_Musica.content.controls[2].content.controls[0].content.controls[0].label= "Pon un nombre"
            interfaz_Musica.update()
        elif nombre_playlists in playlists_nombres:
            interfaz_Musica.content.controls[2].content.controls[0].content.controls[0].label= "Nombre en uso..."
            interfaz_Musica.content.controls[2].content.controls[0].content.controls[0].value= ""
            interfaz_Musica.update()
        else:
            end_drawer.open=True
        end_drawer.update()
    
    
    interfaz_playlist = ft.Card(
                                ft.Stack([
                                        ft.Container(
                                                    ft.Row([
                                                            ft.TextField(
                                                            on_submit=openDrawer,
                                                            width=x/4/1.5,
                                                            border_color=color_acento, 
                                                            cursor_color=color_acento, 
                                                            color=color_texto_especial, 
                                                            label="Nombre", 
                                                            label_style=ft.TextStyle(color=color_acento_secundario)), 
                                                            ft.IconButton(ft.icons.LIBRARY_MUSIC_ROUNDED, icon_color=color_acento_secundario,on_click=openDrawer)], 
                                                    alignment=ft.MainAxisAlignment.CENTER ),
                                        width=x/4, top=10, alignment=ft.alignment.center),
                                        ft.Container(
                                                    ft.Column([
                                                                
                                                                ], 
                                        scroll=ft.ScrollMode.ALWAYS, width=x/4, spacing=10), margin=ft.margin.only(top=100))
                                        ]),
                                            
                        color=color_secundario, width=x/4, height=y/1.38,top=y/8, left=x/3)
    
    #Inferfaz de la musica
    interfaz_Musica =   ft.Container(
                                    content=ft.Stack([
                                        ft.Container(
                                            ft.Text(f"Todas tus canciones",
                                            color=color_texto, size=22), 
                                        alignment=ft.alignment.center, width=x/3.3, height=y/10, top=20 ),

                                        ft.Card(
                                            ft.Stack([ft.Column([], scroll=ft.ScrollMode.ALWAYS, width=x/2, spacing=0),
                                                    ]),
                                            
                                        color=color_secundario, width=x/3.3, height=y/1.38,top=y/8,),
                                        interfaz_playlist,
                                                                                ft.Container(
                                            ft.Text("Tus playlists",
                                            color=color_texto, size=22), 
                                        alignment=ft.alignment.center, width=x/3.3, height=y/10, top=20, left=x/2/1.65 )
                                        
                                        
                                            ], height=y, width=(x/3.3)*2),

                                width=x-x_offset, height=y, left=x_offset, animate_position=ft.animation.Animation(400, "linear"), 
                                animate_size=ft.animation.Animation(600, "linear"),    alignment=ft.alignment.center ,               
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_center,
                                    end=ft.alignment.bottom_center,
                                    colors=hex_gradient,
                                    tile_mode=ft.GradientTileMode.MIRROR,   
                                    rotation=pi*2
                                    ))
    

    
    
    
    
    
    

    
    #Funcion que controla el evento de un primer incio
    #page.client_storage.clear()

    def selector_nombre(e):
        page.client_storage.set("auth", page.overlay[0].content.controls[2].value)
        page.client_storage.set("tarea_data", [])
        page.client_storage.set("tareas", [])
        page.client_storage.set("tareas_status", {})
        page.client_storage.set("playlists", {})
        page.client_storage.set("playlist_nombres", [])
        page.window_close()

    
    autenticacion = ft.AlertDialog(
        modal=False,
        title=ft.Text("¡Bienvenido/a!", size=23, color=color_texto_especial),
        content=ft.Column([ft.Text(f"Es la primera vez que abres la aplicación, \npor favor dime cómo debería llamarte.", size=17, color=color_texto_especial),
                            ft.Text(f"Podrás cambiarlo luego, debes reiniciar la aplicación.", size=13, color=color_texto_especial, weight=peso2),
                            ft.TextField(value="",label="Nuevo nombre",on_submit=selector_nombre,label_style=ft.TextStyle(color=color_texto, weight=ft.FontWeight.W_500), color=color_texto, cursor_color=color_texto,border_color=color_texto_especial, text_style=ft.TextStyle(weight=ft.FontWeight.W_500))], height=y/5),
        actions=[ft.Container(
            ft.ElevatedButton(content=ft.Row([ft.Icon(name=ft.icons.CHECK), ft.Text("Aceptar")], ), on_click=selector_nombre,color=color_principal, bgcolor=color_acento),width=150, alignment=ft.alignment.center, ),
        ],
        bgcolor=color_principal,
        actions_alignment=ft.MainAxisAlignment.END,
        open=True
    )

    if not page.client_storage.contains_key("auth"):
        page.overlay.append(autenticacion)
    page.overlay.append(reproductor)
    page.overlay.append(audio1)
    page.add(interfaz_inicial)
    
    rocola()




ft.app(target=main)
