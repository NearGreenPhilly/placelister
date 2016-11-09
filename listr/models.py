from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.

class Place(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True)

    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5, null=True)

    list_count = models.IntegerField(default=0)

    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    point = models.PointField()

    # Returns the string representation of the model.
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name

class List(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='collaborators')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    places = models.ManyToManyField(Place)

    collaborators = models.ManyToManyField(User, related_name='created_by')

    def __unicode__(self):              # __unicode__ on Python 2
        return str(self.id)


# class ListedPlace(models.Model):
#     place = models.ForeignKey(Place, on_delete=models.CASCADE)
#     in_list = models.ForeignKey(List)
#
#     added_by = models.ForeignKey(User)
#     added_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):              # __unicode__ on Python 2
#         return self.id



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Profile(models.Model):
    user = models.ForeignKey(User)
    friends = models.ManyToManyField(User, related_name='user')
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.user)




class InstagramProfile(models.Model):
    user = models.ForeignKey(User)
    instagram_user = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.user)

class FacebookProfile(models.Model):
    user = models.ForeignKey(User)
    fb_user_id = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    profile_url = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100)

class GoogleProfile(models.Model):
    user = models.ForeignKey(User)
    google_user_id = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=100)
    profile_url = models.CharField(max_length=100)

class TwitterProfile(models.Model):
    user = models.ForeignKey(User)
    twitter_user = models.CharField(max_length=200)
    oauth_token = models.CharField(max_length=200)
    oauth_token_secret = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.user)

