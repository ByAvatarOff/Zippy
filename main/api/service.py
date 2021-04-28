import socket

from django.contrib.gis.geoip2 import GeoIP2
import http.client

from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect
from geoip2.errors import AddressNotFoundError
from django.contrib.gis.measure import D
from django.db.models import Q


def get_user(request):
    return request.user


def get_ip():
    try:
        conn = http.client.HTTPConnection('ifconfig.me')
        conn.request('GET', '/ip')
        t = conn.getresponse().read()
        return t.decode('utf-8')
    except socket.gaierror:
        return '0.0.0.0'


def get_location():
    geo = GeoIP2()
    try:
        lng, lat = geo.lat_lon(get_ip())
        point = Point(lng, lat)
        return point
    except AddressNotFoundError:
        return None


def filter_group(request):
    from main.models import Profile
    profile = Profile.objects.get(user=request.user)
    if profile.group.lower() == 'base':
        return Profile.objects.filter(Q(geo_location__distance_lte=(profile.geo_location, D(km=10))))[:11]
    elif profile.group.lower() == 'premium':
        return Profile.objects.filter(Q(geo_location__distance_lte=(profile.geo_location, D(km=25))))[:101]
    elif profile.group.lower() == 'vip':
        return Profile.objects.all()
    else:
        return None


def match(request, pk):
    from main.models import Profile, Like
    try:
        like_profile = Profile.objects.get(pk=pk)
        owner_profile = Profile.objects.get(user=request.user)
        like = Like.objects.get(profile=like_profile, user=request.user) # обьекта лайка, которые лайкали юзера
        like1 = Like.objects.get(profile=owner_profile, user=like_profile.user) # обьекты лайка, которые лайкал юзер
        if like.like and like1.like:
            return HttpResponseRedirect(redirect_to='profiles')
        else:
            print('Not like')
    except Like.DoesNotExist:
        print('Object doe not exist')





