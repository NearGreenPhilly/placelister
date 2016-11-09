# Django
from django.shortcuts import render, render_to_response
# from django.contrib.auth import logout
# from django.template import RequestContext, loader
# from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
# from django.urls import reverse
from django.core.serializers import serialize



# Scripts
from scripts.instagram import *
from scripts.facebook import *
from scripts.googlePlus import *
from scripts.twitter import TwitterOauthClient
from scripts.getPlaces import *

# Python
# import oauth2 as oauth
# import simplejson as json
# import requests
from pprint import pprint

# Models
from listr.models import Place, List
from listr.forms import UserForm, ListForm

profile_track = None
getInstagram = InstagramOauthClient(settings.INSTAGRAM_CLIENT_ID, settings.INSTAGRAM_CLIENT_SECRET)
getTwitter = TwitterOauthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
getFacebook = FacebookOauthClient(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
getGoogle = GooglePlus(settings.GOOGLE_PLUS_APP_ID, settings.GOOGLE_PLUS_APP_SECRET)



class PlacesList(DetailView):

    template_name = 'listr/place_list.html'

    model = List

    def get_context_data(self, **kwargs):
        clist = List.objects.get(id = self.kwargs['pk'])
        pla = list(clist.places.all())

        gj = serialize('geojson', clist.places.all(),
          geometry_field='point',
          fields=('name',))

        # pprint(gj)

        context = super(PlacesList, self).get_context_data(**kwargs)
        context['clist'] = [clist]
        context['listid'] = self.kwargs['pk']
        context['places'] = pla
        context['geoj'] = gj
        context['lists'] = List.objects.all()


        return context

    def post(self, request, *args, **kwargs):


        data = {}

        data['name'] = str(request.POST.get('searchName').encode('utf8'))

        data['neighborhood'] = str(request.POST.get('searchNeighborhood').encode('utf8'))

        data['address'] = str(request.POST.get('searchAddress').encode('utf8'))

        data['city'] = str(request.POST.get('searchCity').encode('utf8'))

        data['state'] = str(request.POST.get('searchState').encode('utf8'))

        data['url'] = str(request.POST.get('searchURL').encode('utf8'))

        print(data)


        listid = self.kwargs['pk']

        if data != 'None':

            placer = processPlace(data)

            pprint(placer)

            clist = List.objects.get(id = self.kwargs['pk'])

            listed_places = list(clist.places.all())

            cplaces = Place.objects.filter(name=placer['name'],address=placer['address'])



            if len(cplaces) > 0:
                clist.places.add(cplaces[0])
                cplaces[0].list_count += 1
                print(cplaces[0].list_count)
                cplaces[0].save()


        clist = List.objects.get(id = self.kwargs['pk'])
        context = {}

        gj = serialize('geojson', clist.places.all(),
          geometry_field='point',
          fields=('name',))

        context['clist'] = [clist]
        context['listid'] = self.kwargs['pk']
        context['places'] = list(clist.places.all())
        context['geoj'] = gj
        # context['lists'] = List.objects.all()
        return self.render_to_response(context)


    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template depending if the request is ajax
        or not and it renders with the given context.
        """
        template = self.template_name

        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )

def lists(request):

    user_lists = List.objects.filter(created_by=request.user)

    context = {'lists': user_lists}

    resp =  render(request, "listr/lists.html", context)



    if request.method == 'POST':

        resp =  render(request, "listr/lists.html", context)


    return resp

def new_list(request):
    if request.method == 'POST':
        list_form = ListForm(data=request.POST)

        current_user = request.user

        list = list_form.save(commit=False)
        list.created_by = request.user
        if list_form.is_valid():
            list.save()
            registered = True
            return HttpResponseRedirect('/listr/lists/')
        else:
            print list_form.errors
    else:
        list_form = ListForm()


    return render(request,
            'listr/new_list.html',
            {'list_form': list_form} )


def places(request):

    places = Place.objects.order_by('-list_count')

    user_lists = List.objects.filter(created_by=request.user)

    data = { "places" : places, "user_lists" : user_lists }

    resp =  render(request, "listr/places.html", data)



    if request.method == 'POST':

        data = {}

        data['name'] = str(request.POST.get('searchName').encode('utf8'))

        data['neighborhood'] = str(request.POST.get('searchNeighborhood').encode('utf8'))

        data['address'] = str(request.POST.get('searchAddress').encode('utf8'))

        data['city'] = str(request.POST.get('searchCity').encode('utf8'))

        data['state'] = str(request.POST.get('searchState').encode('utf8'))

        data['url'] = str(request.POST.get('searchURL').encode('utf8'))

        print(data)



        if data != 'None':

            placer = processPlace(data)

            pprint(placer)


            places = Place.objects.order_by('-list_count')

            user_lists = List.objects.filter(created_by=request.user)

            # pprint(user_lists)

            data = { "places" : places, "user_lists" : user_lists }

            resp = render(request, "listr/places.html", data)

        else: ## A place is being added to a list

            the_new_list = request.POST.get('lists')

            the_place = str(request.POST.get('placename').encode("utf8"))

            place_obj = Place.objects.get(name=the_place)

            this_list = List.objects.get(created_by=request.user, id=the_new_list)

            this_list.places.add(place_obj)

            this_list.save()

            place_obj.list_count += 1

            place_obj.save()




    return resp


def index(request):
    print "index: " + str(request.user)

    # if not request.user.is_active:
    #     if request.GET.items():
    #         # if profile_track == 'twitter':
    #         #     oauth_verifier = request.GET['oauth_verifier']
    #         #     getTwitter.get_access_token_url(oauth_verifier)
    #         #
    #         #     try:
    #         #         user = User.objects.get(username = getTwitter.username + '_twitter')#(username=getTwitter.username)
    #         #     except User.DoesNotExist:
    #         #         username = getTwitter.username + '_twitter'
    #         #         new_user = User.objects.create_user(username, username+'@madewithtwitter.com', 'password')
    #         #         new_user.save()
    #         #         profile = TwitterProfile(user = new_user,oauth_token = getTwitter.oauth_token, oauth_token_secret= getTwitter.oauth_token_secret, twitter_user=getTwitter.username)
    #         #         profile.save()
    #         #     user = authenticate(username=getTwitter.username+'_twitter', password='password')
    #         #     login(request, user)
    #         # elif profile_track == 'instagram':
    #         #     code = request.GET['code']
    #         #     getInstagram.get_access_token(code)
    #         #
    #         #     try:
    #         #         user = User.objects.get(username=getInstagram.user_data['username']+'_instagram')
    #         #     except User.DoesNotExist:
    #         #         username = getInstagram.user_data['username']+'_instagram'
    #         #         new_user = User.objects.create_user(username, username+'@madewithinstagram.com', 'password')
    #         #         new_user.save()
    #         #         profile = InstagramProfile(user = new_user, access_token = getInstagram.access_token, instagram_user=getInstagram.user_data['username'])
    #         #         profile.save()
    #         #     user = authenticate(username=getInstagram.user_data['username']+'_instagram' , password='password')
    #         #     login(request, user)
    #         #
    #         # elif profile_track == 'facebook':
    #         #     code = request.GET['code']
    #         #     getFacebook.get_access_token(code)
    #         #     userInfo = getFacebook.get_user_info()
    #         #     username = userInfo['first_name'] + userInfo['last_name']
    #         #
    #         #     try:
    #         #         user = User.objects.get(username=username+'_facebook')
    #         #     except User.DoesNotExist:
    #         #         new_user = User.objects.create_user(username+'_facebook', username+'@madewithfacbook', 'password')
    #         #         new_user.save()
    #         #
    #         #         try:
    #         #             profile = FacebookProfile.objects.get(user=new_user.id)
    #         #             profile.access_token = getFacebook.access_token
    #         #         except:
    #         #             profile = FacebookProfile()
    #         #             profile.user = new_user
    #         #             profile.fb_user_id = userInfo['id']
    #         #             profile.profile_url = userInfo['link']
    #         #             profile.access_token = getFacebook.access_token
    #         #         profile.save()
    #         #     user = authenticate(username=username+'_facebook', password='password')
    #         #     login(request, user)
    #         #
    #         # elif profile_track == 'google':
    #         #     code = request.GET['code']
    #         #     state = request.GET['state']
    #         #     getGoogle.get_access_token(code, state)
    #         #     userInfo = getGoogle.get_user_info()
    #         #     username = userInfo['given_name'] + userInfo['family_name']
    #         #
    #         #     try:
    #         #         user = User.objects.get(username=username+'_google')
    #         #     except User.DoesNotExist:
    #         #         new_user = User.objects.create_user(username+'_google', username+'@madewithgoogleplus', 'password')
    #         #         new_user.save()
    #         #
    #         #         try:
    #         #             profle = GoogleProfile.objects.get(user = new_user.id)
    #         #             profile.access_token = getGoogle.access_token
    #         #         except:
    #         #             profile = GoogleProfile()
    #         #             profile.user = new_user
    #         #             profile.google_user_id = userInfo['id']
    #         #             profile.access_token = getGoogle.access_token
    #         #             profile.profile_url = userInfo['link']
    #         #         profile.save()
    #         #     user = authenticate(username=username+'_google', password='password')
    #         #     login(request, user)
    #
    #
    #
    # else:
    #     if request.GET.items():
    #         user = User.objects.get(username = request.user.username)
    #         # if profile_track == 'twitter':
    #         #     oauth_verifier = request.GET['oauth_verifier']
    #         #     getTwitter.get_access_token_url(oauth_verifier)
    #         #
    #         #     try:
    #         #         twitterUser = TwitterProfile.objects.get(user = user.id)
    #         #     except TwitterProfile.DoesNotExist:
    #         #         profile = TwitterProfile(user = user, oauth_token = getTwitter.oauth_token, oauth_token_secret= getTwitter.oauth_token_secret, twitter_user=getTwitter.username)
    #         #         profile.save()
    #         # elif profile_track == 'instagram':
    #         #     code = request.GET['code']
    #         #     getInstagram.get_access_token(code)
    #         #
    #         #     try:
    #         #         instagramUser = InstagramProfile.objects.get(user= user.id)
    #         #     except InstagramProfile.DoesNotExist:
    #         #         profile = InstagramProfile(user = user, access_token = getInstagram.access_token, instagram_user=getInstagram.user_data['username'])
    #         #         profile.save()


    context = {'hello': 'world'}
    return render(request, 'listr/index.html', context)


def api_examples(request):
    context = {'title': 'API Examples Page'}
    return render(request, 'listr/api_examples.html', context)



######################
# Registration Views #
######################

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponseRedirect('/listr/login/')
        else:
            print user_form.errors
    else:
        user_form = UserForm()


    return render(request,
            'listr/register.html',
            {'user_form': user_form, 'registered': registered} )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/listr/api/')
            else:
                return HttpResponse("Your Django Hackathon account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'listr/login.html', {})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/listr/login/')


# def instagram_login(request):
#     global profile_track
#     profile_track = 'instagram'
#     instagram_url = getInstagram.get_authorize_url()
#     return HttpResponseRedirect(instagram_url)
#
# def twitter_login(request):
#     global profile_track
#     profile_track = 'twitter'
#     twitter_url = getTwitter.get_authorize_url()
#     return HttpResponseRedirect(twitter_url)
#
#
# def facebook_login(request):
#     global profile_track
#     profile_track = 'facebook'
#     facebook_url = getFacebook.get_authorize_url()
#     return HttpResponseRedirect(facebook_url)
#
#
# def google_login(request):
#     global profile_track
#     profile_track = 'google'
#     google_url = getGoogle.get_authorize_url()
#     return HttpResponseRedirect(google_url)
#
#
# #################
# #  GOOGLE API   #
# #################
# def googlePlus(request):
#
#     userInfo = getGoogle.get_user_info()
#     return render(request, 'listr/googlePlus.html', {'userInfo' : userInfo})
#
#
#
# ####################
# #   INSTAGRAM API  #
# ####################
#
# def instagram(request):
#     print getInstagram.is_authorized
#
#     if getInstagram.is_authorized:
#         if request.method == 'GET':
#             if request.GET.items():
#                 instagram_tag = request.GET.get('instagram_tag')
#                 instagramUser = InstagramProfile.objects.get(user = request.user)
#                 tagged_media = getTaggedMedia(instagram_tag, instagramUser.access_token)
#             else:
#                 instagram_tag, tagged_media = '', ''
#     else:
#         global profile_track
#         profile_track = 'instagram'
#         instagram_url =getInstagram.get_authorize_url()
#         return HttpResponseRedirect(instagram_url)
#
#     context = {'title': 'Instagram', 'tagged_media': tagged_media, 'search_tag': instagram_tag}
#     return render(request, 'listr/instagram.html', context)
#
# def instagramUser(request):
#     ''' Returns JSON response about a specific Instagram User. '''
#
#     access_token = InstagramProfile.objects.get(instagram_user='mk200789').access_token
#     parsedData = getUserInfo(access_token)
#     return JsonResponse({ 'data': parsedData })
#
#
# ####################
# #   TWITTER API    #
# ####################
#
# def twitter(request):
#     if getTwitter.is_authorized:
#         value = getTwitter.get_trends_available(settings.YAHOO_CONSUMER_KEY)
#     else:
#         global profile_track
#         profile_track = 'twitter'
#         twitter_url = getTwitter.get_authorize_url()
#         return HttpResponseRedirect(twitter_url)
#
#     context ={'title': 'twitter', 'value': value}
#     return render(request, 'listr/twitter.html', context)

