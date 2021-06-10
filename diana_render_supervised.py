#Autor: Ing. Alberto Lepe de los Angeles
#Version: 1
# Blender 2.90
# script para generar aleatoriamente renders 
#

import bpy
import random
import math
import mathutils
import bpy_extras
import csv
import os

def mover_flechas_fuera(locacion):
    for obj in bpy.data.collections['Flechas'].all_objects:
      #print("Flechas: ", obj.name)
      obj.location = locacion

def punto_en_diana(diametro):
    radio = diametro/2
    radio2 = radio**2
    px = random.uniform(-radio, radio)
    py = random.uniform(-radio, radio)
    if (px**2 + py**2) < radio2:
        punto = [px, py]
    else:
        punto = punto_en_diana(diametro)
    return punto

def punto_en_aro(aro, diametro):
    p = punto_en_diana(diametro)
    punto = calculateScore(p[0], p[1], diametro)
    if punto == aro:
        return p
    else:
        return punto_en_aro(aro, diametro)

def calculateScore(arrowx, arrowy, diametro):
    radio = diametro / 2
    lims = radio / 10
    score = 0
    d = math.sqrt(arrowx**2 + arrowy**2)
    if d >= 0.0 and d <= (lims*1):
        score = 10
    if d > (lims*1) and d <= (lims*2):
        score = 9
    if d > (lims*2) and d <= (lims*3):
        score = 8
    if d > (lims*3) and d <= (lims*4):
        score = 7
    if d > (lims*4) and d <= (lims*5):
        score = 6
    if d > (lims*5) and d <= (lims*6):
        score = 5
    if d > (lims*6) and d <= (lims*7):
        score = 4
    if d > (lims*7) and d <= (lims*8):
        score = 3
    if d > (lims*8) and d <= (lims*9):
        score = 2
    if d > (lims*9) and d <= (lims*10):
        score = 1
    return score

def get_aro_aleat(aros_l, aros_cp):
    aro = 0
    if len(aros_cp) < 1:
        for i in aros_l:
            aros_cp.append(i)
        random.shuffle(aros_cp)
        aro = aros_cp[-1]
    else:
        aro = aros_cp[-1]
    aros_cp.pop()
    return aro

#Obtiene de manera aleatoria de una lista de numeros la cantidad de flechas a mostrar
def get_flch_aleat(lst, cont):
    n_fl = 0
    if len(lst) > 0:
        n_fl = lst[-1]
    else:
        for i in range(1,cont+1):
            lst.append(i)
        random.shuffle(lst)
        n_fl = lst[-1]
    lst.pop()
    return n_fl
    
def gen_xy_points(aros_list, n_x_aro):
    
    blanco = bpy.data.objects["Blanco"]
    diametro = round(blanco.dimensions.y, 3)
    
    flch_location = []

    for i in range(n_x_aro):
        puntos = []
        for aro in aros_list:
            p = punto_en_aro(aro, diametro)
            score = calculateScore(p[0], p[1], diametro)
            puntos.append( [aro,score, p] )
        flch_location.append( puntos )
    return flch_location
    
def mover_flechas_diana():
    scores = ""
    puntos = []
    blanco = bpy.data.objects["Blanco"]
    diametro = round(blanco.dimensions.y, 3)
    for flch in bpy.data.collections['Flechas'].all_objects:
        p = punto_en_diana(diametro)
        flch.location = (0.0, p[0], p[1])
        aro = calculateScore(p[0], p[1], diametro)
        scores = scores + "_" + str(aro) + ""
        #print(f"{flch.name}, Punto: {aro}")
        puntos.append([flch.name, aro])
    return [scores, puntos]

def mover_flechas_aro_diana(aros_list):
    scores = ""
    puntos = []
    blanco = bpy.data.objects["Blanco"]
    diametro = round(blanco.dimensions.y, 3)
    aros_cp = aros_list.copy()
    for flch in bpy.data.collections['Flechas'].all_objects:
        aro = get_aro_aleat(aros_cp)
        p = punto_en_aro(aro, diametro)
        flch.location = (0.0, p[0], p[1])
        aro = calculateScore(p[0], p[1], diametro)
        scores = scores + "_" + str(aro) + ""
        puntos.append([flch.name, aro])
    return [scores, puntos]

def mover_lista_flechas_aro_diana(lst_flechas, aros_list):
    scores = ""
    puntos = []
    blanco = bpy.data.objects["Blanco"]
    diametro = round(blanco.dimensions.y, 3)
    flechas = bpy.data.collections['Flechas'].all_objects
    aros_cp = aros_list.copy()
    for f in lst_flechas:
        flch = flechas[f]
        aro = get_aro_aleat(aros_list, aros_cp)
        p = punto_en_aro(aro, diametro)
        flch.location = (0.0, p[0], p[1])
        aro = calculateScore(p[0], p[1], diametro)
        scores = scores + "_" + str(aro) + ""
        puntos.append([flch.name, aro])
    return [scores, puntos]
    
def mover_lista_flechas_aro_diana_xy_points(lst_flechas, aros_list, lst_xy_points):
    scores = ""
    puntos = []
    blanco = bpy.data.objects["Blanco"]
    diametro = round(blanco.dimensions.y, 3)
    flechas = bpy.data.collections['Flechas'].all_objects
    aros_cp = aros_list.copy()
    for f in lst_flechas:
        flch = flechas[f]
        #aro = get_aro_aleat(aros_list, aros_cp)
        
        aro = random.randint(1, 10)
        id_point = random.randint(0, len(lst_xy_points) -1)
        p = lst_xy_points[id_point][aro - 1][2]

        flch.location = (0.0, p[0], p[1])
        aro = calculateScore(p[0], p[1], diametro)
        scores = scores + "_" + str(aro) + ""
        puntos.append([flch.name, aro])
    return [scores, puntos]

def mover_sol_horario(dia,mes,anio,hora):
    scene = bpy.context.scene
    scene.sun_pos_properties.co_parser = "20.6970409,-103.3909337"
    scene.sun_pos_properties.day = dia
    scene.sun_pos_properties.month = mes
    scene.sun_pos_properties.year = anio
    scene.sun_pos_properties.time = hora

def horario_aleatorio():
    dia = random.randint(1, 28)
    mes = random.randint(1,12)
    anio = 2021
    hora = random.uniform(10.0, 18.0)
    return [dia,mes,anio,hora]

def get_render_location(mypoint):
    v1 = mathutils.Vector(mypoint)
    scene = bpy.context.scene
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, scene.camera, v1)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (int(scene.render.resolution_x * render_scale), int(scene.render.resolution_y * render_scale))
    y_resol = scene.render.resolution_y
    return [round(co_2d.x * render_size[0]), y_resol - round(co_2d.y * render_size[1])]


def get_px_render_flechas(list_flch):
    lista = []
    flechas = bpy.data.collections['Flechas'].all_objects
    for idx in list_flch:
        flecha = flechas[idx]
        if flecha.location != bpy.context.scene.cursor.location:
            flch_global_coord = flecha.matrix_world.translation
            coordenada_px = get_render_location(flch_global_coord)
        else:
            coordenada_px = [-1, -1]
        lista.append(coordenada_px)
    return lista


def renderizar(nombre_archivo):
    bpy.context.scene.render.filepath = nombre_archivo
    bpy.ops.render.render(write_still=1)


def render_all_camaras(directorio, n_render, aros_list, n_flechas):
    lista_render = []
    cont = 0
    flechas = bpy.data.collections['Flechas'].all_objects
    lst_n_flchs = list( range(1,len(flechas) + 1) )
    random.shuffle(lst_n_flchs)

    for _ in range(n_render):
        hr = horario_aleatorio()
        mover_sol_horario(hr[0],hr[1],hr[2],hr[3])
        try:
            #n_flchs = get_flch_aleat(lst_n_flchs, len(flechas))
            n_flchs = n_flechas
            puntos, lst_flechas = mover_n_flechas(flechas, n_flchs, aros_list)
        except:
            print("Algo salio mal...")
        else:
            print("OK Renderizando...") 
            camaras = bpy.data.collections['Camaras']
            for cam in camaras.all_objects:
                bpy.context.scene.camera = cam
                scene = bpy.context.scene
                scene.camera = cam
                #archivo = str(cont) + "_" + cam.name + "_" + puntos[0] + ".jpg"
                archivo = str(cont) + "_" + cam.name + "_" + "N" + str(n_flchs)+ "N" + "P" + puntos[0] + "P" +".jpg"
                renderizar(directorio + "/" + archivo )
                lista_fl_px = get_px_render_flechas(lst_flechas)
                lista_render.append([archivo, n_flchs, puntos[1], lista_fl_px])
                cont = cont + 1
                print(archivo)
    return lista_render


def render_random_camara(directorio, n_render, aros_list):
    lista_render = []
    cont = 0
    camaras = bpy.data.collections['Camaras'].all_objects
    for _ in range(n_render):
        hr = horario_aleatorio()
        mover_sol_horario(hr[0],hr[1],hr[2],hr[3])
        try:
            #puntos = mover_flechas_diana(diametro) 
            puntos = mover_flechas_aro_diana(aros_list)
        except:
            print("Algo salio mal...")
        else:
            print("OK Renderizando...") 
            aleat_id_cam = random.randint(0, len(camaras) -1)
            cam = camaras[aleat_id_cam]
            scene = bpy.context.scene
            scene.camera = camaras[aleat_id_cam]
            archivo = str(cont) + "_" + cam.name + "_" + puntos[0] + ".jpg"
            renderizar(directorio + "/" + archivo )
            lista_fl_px = get_px_render_flechas(lst_flechas)
            lista_render.append([archivo, puntos[1], lista_fl_px])
            cont = cont + 1
            print(archivo)
    return lista_render

def escoger_lista_flechas(lst, n_flchs):
    random.shuffle(lst)
    eleccion = len(lst) - n_flchs
    if eleccion != 0:
        for _ in range(0,eleccion):
            lst.pop()
    return lst

def escoger_lista_flechas2(lst, n_flchs):
    #random.shuffle(lst)
    eleccion = len(lst) - n_flchs
    if eleccion != 0:
        for _ in range(0,eleccion):
            lst.pop()
    return lst

def mover_n_flechas(flechas, mover_n_flchs, aros_list):
    escena_fuera = bpy.context.scene.cursor.location
    mover_flechas_fuera(escena_fuera)

    lista = list(range(0,len(flechas)))
    lista_flechas = escoger_lista_flechas(lista, mover_n_flchs)
    puntos = mover_lista_flechas_aro_diana(lista_flechas, aros_list)
    return puntos, lista_flechas
    
def mover_n_flechas2(flechas, mover_n_flchs, aros_list, lst_xy_points):
    escena_fuera = bpy.context.scene.cursor.location
    mover_flechas_fuera(escena_fuera)

    lista = list(range(0,len(flechas)))
    lista_flechas = escoger_lista_flechas(lista, mover_n_flchs)
    puntos = mover_lista_flechas_aro_diana_xy_points(lista_flechas, aros_list, lst_xy_points)
    return puntos, lista_flechas

def render_n_flechas(directorio, n_render, aros_list, n_flechas):
    lista_render = []
    cont = 0
    flechas = bpy.data.collections['Flechas'].all_objects
    camaras = bpy.data.collections['Camaras'].all_objects

    lst_n_flchs = list( range(1,len(flechas) + 1) )
    random.shuffle(lst_n_flchs)

    for _ in range(n_render):
        hr = horario_aleatorio()
        mover_sol_horario(hr[0],hr[1],hr[2],hr[3])
        try:
            #n_flchs = get_flch_aleat(lst_n_flchs, len(flechas))
            n_flchs = n_flechas
            puntos, lst_flechas = mover_n_flechas(flechas, n_flchs, aros_list)
        except:
            print("Algo salio mal...")
        else:
            print("OK Renderizando...") 
            aleat_id_cam = random.randint(0, len(camaras) -1)
            #aleat_id_cam = 4
            cam = camaras[aleat_id_cam]
            scene = bpy.context.scene
            scene.camera = camaras[aleat_id_cam]
            #archivo = str(cont) + "_" + cam.name + "_" + puntos[0] + ".jpg"
            archivo = str(cont) + "_" + cam.name + "_" + "N" + str(n_flchs)+ "N" + "P" + puntos[0] + "P" +".jpg"
            renderizar(directorio + "/" + archivo )
            lista_fl_px = get_px_render_flechas(lst_flechas)
            lista_render.append([archivo, n_flchs, puntos[1], lista_fl_px])
            cont = cont + 1
            print(archivo)
    return lista_render
    
def render_n_flechas_xy_points(directorio, n_render, aros_list, n_flechas, lst_xy_points):
    lista_render = []
    cont = 0
    flechas = bpy.data.collections['Flechas'].all_objects
    camaras = bpy.data.collections['Camaras'].all_objects

    lst_n_flchs = list( range(1,len(flechas) + 1) )
    random.shuffle(lst_n_flchs)

    for _ in range(n_render):
        hr = horario_aleatorio()
        mover_sol_horario(hr[0],hr[1],hr[2],hr[3])
        puntos, lst_flechas = mover_n_flechas2(flechas, n_flechas, aros_list, lst_xy_points)
        
        print("OK Renderizando...") 
        aleat_id_cam = random.randint(0, len(camaras) -1)
        cam = camaras[aleat_id_cam]
        scene = bpy.context.scene
        scene.camera = camaras[aleat_id_cam]
        archivo = str(cont) + "_" + cam.name + "_" + "N" + str(n_flechas)+ "N" + "P" + puntos[0] + "P" +".jpg"
        renderizar(directorio + "/" + archivo )
        lista_fl_px = get_px_render_flechas(lst_flechas)
        lista_render.append([archivo, n_flechas, puntos[1], lista_fl_px])
        cont = cont + 1
        print(archivo)
    return lista_render

def render_consecutivos(directorio, mover_n_flchs, aros_list):
    scores = ""
    puntos = []
    lista_render = []
    escena_fuera = bpy.context.scene.cursor.location
    mover_flechas_fuera(escena_fuera)
    blanco = bpy.data.objects["Blanco"]
    diametro = round(blanco.dimensions.y, 3)
    flechas = bpy.data.collections['Flechas'].all_objects
    lista = list(range(0,len(flechas)))
    lista_flechas = escoger_lista_flechas2(lista, mover_n_flchs)

    for f in lista_flechas:
        flch = flechas[f]
        aro = get_aro_aleat(aros_list)
        p = punto_en_aro(aro, diametro)
        flch.location = (0.0, p[0], p[1])
        aro = calculateScore(p[0], p[1], diametro)
        scores = scores + "_" + str(aro) + ""
        puntos.append([flch.name, aro])
        cam = bpy.context.scene.camera
        archivo = str(f) + "_" + cam.name + "_" + flch.name + "_" + scores + ".jpg"
        renderizar(directorio + "/" + archivo)
        lista_fl_px = get_px_render_flechas()
        lista_render.append([archivo, puntos, lista_fl_px])

    return lista_render

def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
        
def guardar_csv(archivo_csv, contenido):        
    file = open(archivo_csv, 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(contenido)
        
def get_px_ellipse():
    lista = []
    for punto in bpy.data.collections['puntos'].all_objects:
        if punto.location != bpy.context.scene.cursor.location:
            global_coord = punto.matrix_world.translation
            coordenada_px = get_render_location(global_coord)
        else:
            coordenada_px = [-1, -1]
        lista.append(coordenada_px)
        
    diana = bpy.data.objects["Blanco"]
    global_coord = diana.matrix_world.translation
    centro_px = get_render_location(global_coord)
    lista.append(centro_px)
    return lista

def change_scene_cam_aleat(camaras):
    #camaras = bpy.data.collections['Camaras'].all_objects
    cam = camaras[random.randint(0, len(camaras) -1)]
    scene = bpy.context.scene
    scene.camera = cam
    n_ini = scene.frame_start
    n_fin = scene.frame_end
    scene.frame_current = random.randint(n_ini, n_fin)
    return cam
    
def render_getpoints_diana(directorio, n_renders, aros_list):
    print("OK Renderizando...") 
    lista_render = []
    cont = 0
    camaras = bpy.data.collections['Camaras'].all_objects 
    flechas = bpy.data.collections['Flechas'].all_objects

    for i in range(n_renders):
        n_flchs = 6
        puntos, lst_flechas = mover_n_flechas(flechas, n_flchs, aros_list)
            
        cam = change_scene_cam_aleat(camaras)
        archivo = str(cont) + "_" + cam + "_" + ".jpg"
        renderizar(directorio + "/" + archivo )
        lista_px = get_px_ellipse()
        lista_render.append([archivo, lista_px])
        cont = cont + 1
        print(archivo)
    guardar_csv(directorio + "/puntos.csv", lista_render)
   
def render_n_flechas_elipse(directorio, n_render, aros_list, n_flechas):
    lista_render_fl = []
    lista_render_el = []
    cont = 0
    flechas = bpy.data.collections['Flechas'].all_objects
    camaras = bpy.data.collections['Camaras'].all_objects

    lst_n_flchs = list( range(1,len(flechas) + 1) )
    random.shuffle(lst_n_flchs)

    for _ in range(n_render):
        hr = horario_aleatorio()
        mover_sol_horario(hr[0],hr[1],hr[2],hr[3])
        try:
            #n_flchs = get_flch_aleat(lst_n_flchs, len(flechas))
            n_flchs = n_flechas
            puntos, lst_flechas = mover_n_flechas(flechas, n_flchs, aros_list)
        except:
            print("Algo salio mal...")
        else:
            print("OK Renderizando...") 
            cam = change_scene_cam_aleat(camaras)
            
            archivo_img = str(cont) + "_" + cam.name + "_" + "N" + str(n_flchs)+ "N" + "P" + puntos[0] + "P" +".jpg"
            
            renderizar(directorio + "/" + archivo_img )
            
            lista_fl_px = get_px_render_flechas(lst_flechas)
            lista_el_px = get_px_ellipse()
            
            lista_render_fl.append([archivo_img, n_flchs, puntos[1], lista_fl_px])
            lista_render_el.append([archivo_img, lista_el_px])
            cont = cont + 1
            print(archivo_img)
    return lista_render_fl, lista_render_el
    
def principal_consecutivos(root_dir, name_dataset, n_muestras):
    print("INICIO ####")
    for i in range(n_muestras):
        nombre_dataset = name_dataset + str(i)
        create_dir(root_dir + "/" + nombre_dataset)
        dataset = root_dir + "/" + nombre_dataset + "/" + nombre_dataset + ".csv"
        midir = root_dir + "/" + nombre_dataset

        lista = render_consecutivos(midir, 12, aros_cons)
        file = open(dataset, 'w+', newline='')
        with file:
            write = csv.writer(file)
            write.writerows(lista)
    print("FIN ####")

def principal(directorio, name_dataset, aros_list, si_render, muestras, n_flechas, xy_points):

    create_dir(directorio + "/" + name_dataset)
    dataset_fl = directorio + "/" + name_dataset + ".csv"
    dataset_el = directorio + "/" + "elipses_" + name_dataset + ".csv"
    directorio = directorio + "/" + name_dataset

    print("INICIO ####")
    datos_csv = []
    if si_render == 1:
        datos_csv = render_random_camara(directorio, muestras, aros_list)
        guardar_csv(dataset_fl, datos_csv)
    if si_render == 2:
        datos_csv = render_all_camaras(directorio, muestras, aros_list, n_flechas)
        guardar_csv(dataset_fl, datos_csv)
    if si_render == 3:
        datos_csv = render_n_flechas(directorio, muestras, aros_list, n_flechas)
        guardar_csv(dataset_fl, datos_csv)
    if si_render == 4:
        datos_csv = render_n_flechas_elipse(directorio, muestras, aros_list, n_flechas)
        guardar_csv(dataset_fl, datos_csv[0])
        guardar_csv(dataset_el, datos_csv[1])
    if si_render == 5:
        datos_csv = render_n_flechas_xy_points(directorio, muestras, aros_list, n_flechas, xy_points)
        guardar_csv(dataset_fl, datos_csv)

    print("FIN ####")
    
carpeta = "C:/Users/alepe/Proyecto_Diana/renders"

aros_cons = [1,2,3,4,5,6,7,8,9,10]
random.shuffle(aros_cons)
xy_points = gen_xy_points([1,2,3,4,5,6,7,8,9,10], 10)
principal(carpeta, "6_train_448", aros_cons, 5, 8192, 6, xy_points)
principal(carpeta, "6_test_448", aros_cons, 5, 2048, 6, xy_points)

#principal(carpeta, "1_train_448", aros_cons, 5, 8192, 1, xy_points)
#principal(carpeta, "1_test_448", aros_cons, 5, 2048, 1, xy_points)



