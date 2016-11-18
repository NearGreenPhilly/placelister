from googleplaces import GooglePlaces, types, lang

from listr.models import Place

from django.contrib.gis.geos import GEOSGeometry


def doSearch(place):


    YOUR_API_KEY = 'AIzaSyCUSkUaTU4DJhuheYoh3_x2y1BBD40N3yc'

    google_places = GooglePlaces(YOUR_API_KEY)

    loc_st = "{0}, {1}".format(place['city'], place['state'])

    # You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(
            location=loc_st, keyword=place['name'].decode('utf-8'),
            radius=20000)

    return query_result

def makePlace(aplace):

    ap = Place()

    ap.name = aplace['name']
    ap.type = aplace['type']
    ap.city = aplace['city']
    ap.address = aplace['address']
    ap.neighborhood = aplace['neighborhood']
    ap.url = aplace['url']
    ap.state = aplace['state']
    ap.lon = aplace['lon']
    ap.lat = aplace['lat']

    ap.point = GEOSGeometry('POINT({0} {1})'.format(aplace['lon'], aplace['lat']), srid=4326) #


    ap.save()

def processPlace(new_place):


    query_results = doSearch(new_place)

    isMade = False

    for gresult in query_results.places:

        if isMade == False:

            if str((gresult.name).encode('utf8')) == new_place['name']:

                # print("Name is the same")

                aplace = new_place
                aplace['lat'] = float(gresult.geo_location['lat'])
                aplace['lon'] = float(gresult.geo_location['lng'])



                gresult.get_details()

                a = gresult.formatted_address.split(",")

                this_address = str(a[0].encode('utf8'))
                aplace['type'] = str(gresult.types[0].encode('utf8'))
                aplace['url'] = str(gresult.url)


                cplaces = Place.objects.filter(name=aplace['name'], address=aplace['address'])


                if len(cplaces) == 0:


                    makePlace(aplace)
                    isMade = True
                    print("Place made")


                    # else:
                    #     if 'context' in aplace:
                    #         if aplace['context'] in aplace['address']:
                    #             for tp in cplaces:
                    #                 if aplace['context'] not in tp.address and aplace['context'] not in tp.name:
                    #                     makePlace(aplace)




    return aplace