from django.contrib import admin
from listr.models import UserProfile, Profile, InstagramProfile, TwitterProfile, List, Place

# Register your models here.
class TwitterProfileAdmin(admin.ModelAdmin):
	list_display = ('user','twitter_user')

admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(List)
admin.site.register(Profile)
admin.site.register(InstagramProfile)
admin.site.register(TwitterProfile, TwitterProfileAdmin)

