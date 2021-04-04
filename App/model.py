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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initCatalog():
    catalog = {'videos': None,
               'categories': None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['category_names'] = lt.newList('ARRAY_LIST', cmpfunction=compareCategoryIds)
    catalog['categories'] = mp.newMap(32,
                                      maptype='PROBING', loadfactor=0.3,
                                      comparefunction=compareCategory)

    return catalog


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    addCategory(catalog, video)


def addCategory(catalog, video):
    try:
        categories = catalog['categories']
        category = video['category_id'] 

        existcategory = mp.contains(categories, category)
        if existcategory:
            entry = mp.get(categories, category)
            cat = me.getValue(entry)
        else:
            cat = newCategory(category)
            mp.put(categories, category, cat)
        lt.addLast(cat['videos'], video)
    except Exception:
        return None


def addCategoryName(catalog, category):
    poscategory = lt.isPresent(catalog['category_names'], category['id'])
    if poscategory == 0:
        c = newCategoryName(category['name'].strip(), category['id'])
        lt.addLast(catalog['category_names'], c)


# Funciones para creacion de datos

def newCategory(name):
    category = {'id': "",
                'videos': None}
    category['id'] = name
    category['videos'] = lt.newList('SINGLE_LINKED', compareCategory)
    return category


def newCategoryName(name, id):
    category = {'id': "", 'name': ""}
    category['id'] = id
    category['name'] = name
    return category


# Funciones de consulta

# Funciones de comparacion

def compareCategoryIds(category1, category):
    if (category1 in category['id']):
        return 0
    return -1


def compareCategory(keyname, category):
    catentry = me.getKey(category)
    if (keyname == catentry):
        return 0
    elif (keyname > catentry):
        return 1
    else:
        return -1


# Funciones de ordenamiento
