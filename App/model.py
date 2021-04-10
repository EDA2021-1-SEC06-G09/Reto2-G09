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
                                      maptype='CHAINING', loadfactor=4.0,
                                      comparefunction=compareCategory)

    catalog["countries"] = mp.newMap(numelements = 10, maptype="PROBING", loadfactor=0.5 )

    return catalog


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    addCategory(catalog, video)
    addVideoCountry(catalog, video)


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


#TODO: Req 2
def addVideoCountry(catalog, video):
    try:
        countries = catalog["countries"]
        if (video["country"] != ""):
            vidCountry = video["country"]
        existCountry = mp.contains(countries, vidCountry)
        if existCountry:
            entry = mp.get(countries, vidCountry)
            country = me.getValue(entry)
        else:
            country = newCountry(vidCountry)
            mp.put(countries, vidCountry, country)
        lt.addLast(country["videos"], video)
    except Exception:
        return None



def newCountry(country):
    entry = {"pais": "", "videos": None}
    entry["pais"] = country
    entry["videos"] = lt.newList("ARRAY_LIST", compareCountry)
    return entry


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

def getCategoryId(catalog, category_name):
    for n in range(1,lt.size(catalog["category_names"])+1):
        category = lt.getElement(catalog["category_names"], n)
        if category["name"].lower() == category_name.lower():
            return category["id"]
    return None

#TODO REQUERIMIENTO #1

def bestCountry_Category(catalog, Acategory, Acountry):
    vids = getVidsByCountry(catalog, Acountry)
    if(vids):
        list_of_vids = lt.newList("ARRAY_LIST")
        for vid in lt.iterator(vids):
            if(vid["category_id"] == Acategory):
                lt.addLast(list_of_vids, vid)
        sorted_list = sa.sort(list_of_vids, compare_views)
        return sorted_list



#TODO ahora
def bestVidCountry(catalog, country):
    vids = getVidsByCountry(catalog, country)

    sortedVids = sa.sort(vids, compareId)
    
    if(sortedVids):
        previousId = ""
        count = 1
        bestVid = ""
        MaxCount = 0
        for vid in lt.iterator(sortedVids):
            if(vid["video_id"] == previousId):
                count +=1
            else:
                count = 1
            previousId = vid["video_id"]
            if(count >= MaxCount):
                MaxCount = count
                bestVid = vid
        print(MaxCount)
        print(bestVid)
        return bestVid, MaxCount
        

            

def getVidsByCountry(catalog, country):
    country = mp.get(catalog["countries"], country)
    if country:
        return me.getValue(country)["videos"]
    return None



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

def compareCountry(country1, country2):
    if country1 == country2:
        return 0
    elif country1 > country2:
        return 1
    else:
        return 0

# Funciones de ordenamiento


def compareId(video1, video2):
    return video1["video_id"] > video2["video_id"]

def compare_views(video1, video2):
    return (int(video1["views"]) > int(video2["views"]))