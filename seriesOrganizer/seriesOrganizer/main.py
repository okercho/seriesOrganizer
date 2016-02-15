# -*- encoding: utf-8 -*-
import os, shutil, urllib2, datetime


#Variables 
servidorPlex = "192.168.1.10:32400"
carpetaSeries = "/volume1/Incoming/SeriesDescargas/"
carpetaDestino = "/volume1/Media/Series/"
#Ficheros a eliminar
eliminar = ['.txt','.url']

#Buscamos si los elementos de Eliminar estan en la carpeta, devolvemos la lista de ficheros que queremos
def limpiarArraySubdir(array):
    limpieza = []
    for elemento in array:
        for elim in eliminar:
            if elemento.find(elim) != -1:
                limpieza.append(elemento)
    for lim in limpieza:
        array.remove(lim)
    return array

#Devuelve la extension del Fichero
def extension(capitulo):
    ext = capitulo[::-1]
    ext = ext[:ext.find('.')]
    ext = ext[::-1]
    return ext

## MAIN ##
print datetime.datetime.now()
for base, dirs,files in os.walk(carpetaSeries):
    carpeta = base.replace(carpetaSeries,'')
    if len(carpeta) > 1:
        serie = carpeta[:carpeta.find('-')-1]
        temporada = carpeta[carpeta.find('Temporada')+10:]
        temporada = (temporada[:temporada.find(' ')]).strip()
        capitulo = carpeta[carpeta.find('Cap')+4:]
        capitulo = capitulo[:capitulo.find('][')]
        capitulo = capitulo[len(temporada):]
        for base,dirs,files in os.walk(carpetaSeries+carpeta):
            limpio = limpiarArraySubdir(files)
            if len(limpio) == 0: shutil.rmtree(carpetaSeries+carpeta) #Carpeta sin capitulos - Borramos
            for cap in limpio:
                ext = extension(cap)
                if len(temporada) < 2: 
                    temp="0"+temporada
                else:
                    temp = temporada
                if len(limpio) == 1: 
                    nuevoNombre = temp+"x"+capitulo+"."+ext
                else:
                    numero = cap[cap.find(temporada+"x")+2:cap.find(temporada+"x")+4]
                    nuevoNombre = temp+"x"+numero+"."+ext
                if not os.path.isdir(carpetaDestino+serie): os.makedirs(carpetaDestino+serie)
                if not os.path.isdir(carpetaDestino+serie+"/"+temp): os.makedirs(carpetaDestino+serie+"/"+temp)
                print carpetaSeries+carpeta+"/"+cap+" -> "+carpetaDestino+serie+"/"+temp+"/"+nuevoNombre
                os.rename(carpetaSeries+carpeta+"/"+cap,carpetaDestino+serie+"/"+temp+"/"+nuevoNombre)
            shutil.rmtree(carpetaSeries+carpeta)
            print "-------------"
print datetime.datetime.now()
urllib2.urlopen("http://"+servidorPlex+"/library/sections/all/refresh")