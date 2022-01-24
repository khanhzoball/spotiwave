from datetime import timedelta
from genericpath import exists
from django.forms import models
from .models import Token
from django.utils import timezone
from requests import get, post
from dotenv import load_dotenv
import os


load_dotenv()

def get_tokens(user_id):
    user_tokens = Token.objects.filter(user_id=user_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def update_tokens(user_id, access_token, refresh_token, expires_in):
    tokens = get_tokens(user_id)
    if tokens:
        tokens.access_token =  access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = timezone.now() + timedelta(seconds=expires_in)
        tokens.save()
    else:
        tokens = Token(
            user_id = user_id,
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = timezone.now() + timedelta(seconds=expires_in)
        )
        tokens.save()

def refresh_tokens(user_id):
    tokens = get_tokens(user_id)
    if tokens:
        if tokens.expires_in <= timezone.now():
            token_response = post('https://accounts.spotify.com/api/token', data={
                'grant_type': 'refresh_token',
                'refresh_token': tokens.refresh_token,
                'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET'), 
            }).json()

            print("\n\n\n\n\n\n\n\n")
            print("\n\n\n\n\n\n\n\n")

            update_tokens(
                user_id = tokens.user_id,
                access_token = token_response.get('access_token'),
                refresh_token = tokens.refresh_token,
                expires_in = token_response.get('expires_in')
            )
    else:
        return 0

def top_tracks(access_token, term, arr):
    user_top_tracks = get("https://api.spotify.com/v1/me/top/tracks?limit=50&time_range=" + term, headers={
        'Authorization': "Bearer " + access_token,
        'Content-Type': 'application/json'
    }).json()

    for i in range(len(user_top_tracks.get('items'))):
        arr.append(
            {
                'name': user_top_tracks.get('items')[i]['name'],
                'artist': user_top_tracks.get('items')[i]['artists'][0]['name'],
                'image_url': user_top_tracks.get('items')[i]['album']['images'][0]['url'],

            }
        )
    
def top_artists(access_token, term, arr):
        user_top_artists = get("https://api.spotify.com/v1/me/top/artists?limit=50&time_range=" + term, headers={
        'Authorization': "Bearer " + access_token,
        'Content-Type': 'application/json'
        }).json()

        for i in range(len(user_top_artists.get('items'))):
            arr.append(
                {
                    'artist': user_top_artists.get('items')[i]['name'],
                    'image_url': user_top_artists.get('items')[i]['images'][0]['url'],
                    'genre': user_top_artists.get('items')[i]['genres'],
                }
            )

