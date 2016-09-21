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