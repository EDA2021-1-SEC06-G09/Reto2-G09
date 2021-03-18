"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    print("Comienza proceso de carga de videos...")
    loadVideos(catalog)
    print("Videos cargados.")
    loadCategorys(catalog)


def loadVideos(catalog):
    videosfile = cf.data_dir + "videos-large.csv"
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addvideo(catalog, video)

def loadCategorys(catalog):
    categorysfile = cf.data_dir + "category-id.csv"
    input_file = csv.DictReader(open(categorysfile, encoding='utf-8'), delimiter = "\t")
    for cat in input_file:
        model.addcategory(catalog, cat)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
