﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Videos con mas views para una categoria y pais")
    print("3- Video con mas dias trending en un pais")
    print("4- Video con mas dias de trending para una categoria")
    print("5- Videos con mas like para un tag y pais")


catalog = None


def initCatalog():
    return controller.initCatalog()


def loadData(catalog):
    return controller.loadData(catalog)


def getCategoryId(catalog, category_name):
    category_id = controller.getCategoryId(catalog, category_name)
    if category_id is None:
        print("\nNo se encontró la categoría")
    return category_id


def bestCountry_Category(catalog, category, country):
    return controller.bestCountry_Category(catalog, category, country)


def printCountry_Category(list, number_of_vids):
    videos_printed = 0
    for video in lt.iterator(list):

        print("\nDia de tendencia: " + video["trending_date"] + ", Titulo: " + video["title"] +
              ", Canal: " + video["channel_title"] + ", Tiempo de publicacion: " + video["publish_time"] +
              ", Vistas: " + video["views"] + ", Likes: " + video["likes"] + ", Dislikes: " + video["dislikes"])

        videos_printed += 1
        if(videos_printed == int(number_of_vids)):
            break


def printFirstVideo(catalog):
    firstVideo = lt.getElement(catalog["videos"], 1)
    print("Titulo: " + firstVideo["title"] + ", Canal: " + firstVideo["channel_title"] +
          ", Dia de tendencia: " + firstVideo["trending_date"] + ", Pais: " + firstVideo["country"] +
          ", Vistas: " + firstVideo["views"] + ", Likes: " + firstVideo["likes"] + ", Dislikes: " + firstVideo["dislikes"])


def printTrendCategory(result, cateogry_id):
    video = result[0]
    print("\nTitulo: " + video["title"] + ", Canal: " + video["channel_title"] + ", ID de la categoria: " +
          category_id + ", Numero de dias: " + str(result[1]))


def printBestTag(videos, number):
    if number < lt.size(videos):
        toprange = number+1
    else:
        toprange = lt.size(videos)+1
    for n in range (1,toprange):
        video = lt.getElement(videos, n)
        print("\nTitulo: " + video["title"] + ", Canal: " + video["channel_title"] +
            ", Tiempo de publicacion: " + video["publish_time"] + ", Vistas: " + video["views"] + ", Likes: " +
            video["likes"] + ", Dislikes: " + video["dislikes"] + ", Tags: " + video["tags"])



def printtrendCountry(result):
    video = result[0]
    print("Titulo: " + video["title"] + ", Canal: " + video["channel_title"] + ", Pais: " + video["country"] + ", Numero de dias trending: " + str(result[1]))


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        answer = loadData(catalog)
        print("No. videos cargados:", lt.size(catalog["videos"]))
        print("No. categorías cargadas:", lt.size(catalog["category_names"]))

        print("\nPRIMER VIDEO CARGADO:")
        printFirstVideo(catalog)

        print("\nCATEGORIAS CARGADAS:")
        for n in range(1, lt.size(catalog["category_names"])+1):
            print(lt.getElement(catalog["category_names"], n))

        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")

    elif int(inputs[0]) == 2:
        category_name = input("Nombre de la categoria a buscar: ")
        category_id = getCategoryId(catalog, category_name)

        if category_id is not None:
            country = input("Nombre del pais a buscar: ")
            number = input("Numero de videos a listar: ")
            printCountry_Category(bestCountry_Category(catalog, category_id, country), number)

    elif int(inputs[0]) == 3:
        country = input("Nombre del pais a buscar: ")
        if country is not None:
            result = controller.bestVidCountry(catalog, country)
            printtrendCountry(result)

    elif int(inputs[0]) == 4:
        category_name = input("Nombre de la categoria a buscar: ")
        category_id = getCategoryId(catalog, category_name)

        if category_id is not None:
            result = controller.getTrendCategory(catalog, category_id)
            if result is not None:
                printTrendCategory(result, category_id)

    elif int(inputs[0]) == 5:
        tag = input("Nombre del tag a buscar: ")
        country = input("Nombre del pais a buscar: ")
        number = input("Numero de videos a listar: ")

        if mp.contains(catalog['countries'], country):
            result = controller.getBestTag(catalog, tag, country, number)

            print("\nTOP " + number + " VIDEOS DE " + tag.upper() + ":")
            printBestTag(result, int(number))

    else:
        catalog.clear()
        sys.exit(0)
sys.exit(0)
