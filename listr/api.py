from tastypie.resources import ModelResource
from tastypie import fields
from listr.models import List, Place



class ListResource(ModelResource):
    places = fields.ToManyField('listr.api.PlaceResource', 'places')
    # places = fields.ToManyField(PlaceResource, 'places', related_name='list')
    class Meta:
        queryset = List.objects.all()
        resource_name = 'list'

# class RemoveFromList(ModelResource):
#
#     def obj_delete(self, bundle, **kwargs):
#          # get post id
#          list = List.objects.get(pk=bundle.data.id) # or or whatever way you can get the id
#          # delete all comments with that post id
#          Comment.objects.filter(post=comment.post).delete()
#          return super(RemoveFromList, self).obj_delete(bundle, user=bundle.request.user)
#
#     def apply_authorization_limits(self, request, object_list):
#         return object_list.filter(user=request.user)


class PlaceResource(ModelResource):
    list = fields.ToOneField(ListResource, 'list')
    class Meta:
        queryset = Place.objects.all()
        resource_name = 'place'