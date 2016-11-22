from tastypie.resources import ModelResource
from tastypie import fields
from listr.models import List, Place



class ListResource(ModelResource):
    places = fields.ToManyField('listr.api.PlaceResource', 'places')
    # places = fields.ToManyField(PlaceResource, 'places', related_name='list')
    class Meta:
        queryset = List.objects.all()
        resource_name = 'list'


class PlaceResource(ModelResource):
    list = fields.ToOneField(ListResource, 'list')
    class Meta:
        queryset = Place.objects.all()
        resource_name = 'place'