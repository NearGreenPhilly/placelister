from googleplaces import GooglePlaces, types, lang

from listr.models import Place

from django.contrib.gis.geos import GEOSGeometry


def doSearch(place):


    YOUR_API_KEY = 'AIzaSyCUSkUaTU4DJhuheYoh3_x2y1BBD40N3yc'

    google_places = GooglePlaces(YOUR_API_KEY)

    loc_st = "{0}, {1}".format(place['city'], place['state'])

    # You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(
            location=loc_st, keyword=place['name'],
            radius=20000)

    return query_result

def makePlace(aplace):

    ap = Place()

    ap.name = aplace['name']
    ap.type = aplace['type']
    ap.city = aplace['city']
    ap.address = aplace['address']
    ap.state = aplace['state']
    ap.lon = aplace['lon']
    ap.lat = aplace['lat']

    ap.point = GEOSGeometry('POINT({0} {1})'.format(aplace['lon'], aplace['lat']), srid=4326) #


    ap.save()

def processPlace(ast):


    stateDict = {
        'New York' : 'NY'
        }

    the_place_result = ast.split(",")
    new_place = {}
    aplace = {}
    new_place['name'] = str(the_place_result[0].encode('utf8')).strip()
    new_place['city'] = str(the_place_result[len(the_place_result)-3].encode('utf8')).strip()
    new_place['state'] = str(the_place_result[len(the_place_result)-2].encode('utf8')).strip()
    if len(new_place['state']) != 2:
        new_place['city'] = new_place['state']
        new_place['state'] = stateDict[new_place['city']]
        new_place['context'] = str(the_place_result[len(the_place_result)-3].encode('utf8')).strip()

    if len(the_place_result) > 4:
        new_place['context'] = str(the_place_result[1].encode('utf8')).strip()

    query_results = doSearch(new_place)

    for gresult in query_results.places:

        if str((gresult.name).encode('utf8')) == new_place['name'] or str((gresult.name).encode('utf8')) in new_place['name'] or str((gresult.name).encode('utf8')).replace("'","") in new_place['name'].replace("'",""):

            # print("Name is the same")


            aplace = new_place
            aplace['lat'] = float(gresult.geo_location['lat'])
            aplace['lon'] = float(gresult.geo_location['lng'])



            gresult.get_details()

            a = gresult.formatted_address.split(",")

            city = str(a[len(a)-3].encode('utf8')).strip()
            state = str(a[len(a)-2].encode('utf8')).strip()


            if city == new_place['city']:

                # print("City is the same")

                aplace['address'] = str(a[0].encode('utf8'))
                aplace['type'] = str(gresult.types[0].encode('utf8'))

                cplaces = Place.objects.filter(name=aplace['name'])


                if len(cplaces) == 0:
                    if 'context' in aplace:
                        if aplace['context'] in aplace['address']:

                            makePlace(aplace)
                    else:
                        makePlace(aplace)

                    makePlace(aplace)
                    print("Place made")


                # else:
                #     if 'context' in aplace:
                #         if aplace['context'] in aplace['address']:
                #             for tp in cplaces:
                #                 if aplace['context'] not in tp.address and aplace['context'] not in tp.name:
                #                     makePlace(aplace)




    return aplace