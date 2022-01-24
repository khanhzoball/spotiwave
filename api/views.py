from django.shortcuts import redirect, render
from django.template import RequestContext
from requests import get, post
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from dotenv import load_dotenv
import os
from .util import get_tokens, top_artists, top_tracks, update_tokens, refresh_tokens
import collections
import json
import http
from django.views.decorators.csrf import csrf_exempt


load_dotenv()

# Create your views here.
def login(request) :
    query_params = {
        'client_id': os.getenv('CLIENT_ID'),
        'response_type': 'code',
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'scope': 'user-top-read',
    }

    url = "https://accounts.spotify.com/authorize"

    url_parse = urlparse(url)
    query = url_parse.query
    query = url_parse.query
    url_dict = dict(parse_qsl(query))
    url_dict.update(query_params)
    url_new_query = urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    new_url = urlunparse(url_parse)

    return redirect(new_url)

def access_token_request(request):
    code = request.GET.get('code')
    
    tokens_response = post("https://accounts.spotify.com/api/token", data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),    
    }).json()

    access_token = tokens_response.get('access_token')
    refresh_token = tokens_response.get('refresh_token')
    expires_in = tokens_response.get('expires_in')

    user_profile = get("https://api.spotify.com/v1/me", headers={
        'Authorization': "Bearer " + access_token,
        'Content-Type': 'application/json'
    }).json()

    user_id = user_profile.get('id')

    update_tokens(user_id=user_id, access_token=access_token, refresh_token=refresh_token,expires_in=expires_in)

    return redirect("http://127.0.0.1:8000/" + "?user_id=" + user_id)


@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def retrieve_info(request):
    user_id = json.loads(request.body.decode('utf-8'))['user_id']

    refresh_tokens(user_id)

    access_token = get_tokens(user_id).access_token
    
    user_profile = get("https://api.spotify.com/v1/me", headers={
        'Authorization': "Bearer " + access_token,
        'Content-Type': 'application/json'
    }).json()

    user_name = user_profile.get('display_name')
    user_id = user_profile.get('id')
    user_image_url =  user_profile.get('images')[0]['url']
    user_followers_count = user_profile.get('followers')['total']

    user_top_tracks_long_term_arr = []
    user_top_tracks_medium_term_arr = []
    user_top_tracks_short_term_arr = []
    user_top_artists_long_term_arr = []
    user_top_artists_medium_term_arr = []
    user_top_artists_short_term_arr = []
    user_top_genre = {}

    top_tracks(access_token=access_token, term="long_term", arr=user_top_tracks_long_term_arr)
    top_tracks(access_token=access_token, term="medium_term", arr=user_top_tracks_medium_term_arr)
    top_tracks(access_token=access_token, term="short_term", arr=user_top_tracks_short_term_arr)
    top_artists(access_token=access_token, term="long_term", arr=user_top_artists_long_term_arr)
    top_artists(access_token=access_token, term="medium_term", arr=user_top_artists_medium_term_arr)
    top_artists(access_token=access_token, term="short_term", arr=user_top_artists_short_term_arr)

    for artist in user_top_artists_long_term_arr:
        for genre in artist['genre']:
            user_top_genre[genre] = user_top_genre.get(genre, 0) + 1
    for artist in user_top_artists_medium_term_arr:
        for genre in artist['genre']:
            user_top_genre[genre] = user_top_genre.get(genre, 0) + 3
    for artist in user_top_artists_short_term_arr:
        for genre in artist['genre']:
            user_top_genre[genre] = user_top_genre.get(genre, 0) + 4

    user_top_genre = collections.Counter(user_top_genre).most_common()[0:10]

    data = {
        'user_name': user_name,
        'user_id': user_id,
        'user_image_url': user_image_url,
        'user_top_tracks_long_term_arr': user_top_tracks_long_term_arr,
        'user_top_tracks_medium_term_arr': user_top_tracks_medium_term_arr,
        'user_top_tracks_short_term_arr': user_top_tracks_short_term_arr,
        'user_top_artists_long_term_arr': user_top_artists_long_term_arr,
        'user_top_artists_medium_term_arr': user_top_artists_medium_term_arr,
        'user_top_artists_short_term_arr': user_top_artists_short_term_arr,
        'user_top_genre': user_top_genre
    }

    return Response(data=json.dumps(data), status=status.HTTP_200_OK)