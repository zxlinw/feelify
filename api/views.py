from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Load the environment variables from .env
load_dotenv()

class EmotionPlaylistView(APIView):
    def get_spotify_playlist(self, emotion):
        try:
            # Spotify Credentials
            client_id = os.getenv("SPOTIFY_CLIENT_ID")
            client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

            # Get access token
            auth_response = requests.post(
                "https://accounts.spotify.com/api/token",
                data={"grant_type": "client_credentials"},
                auth=(client_id, client_secret),
            )

            if auth_response.status_code != 200:
                return None

            access_token = auth_response.json().get("access_token")
            if not access_token:
                return None

            # Search Spotify for a playlist
            search_url = "https://api.spotify.com/v1/search"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"q": emotion, "type": "playlist", "limit": 1}

            search_response = requests.get(search_url, headers=headers, params=params)
            if search_response.status_code != 200:
                return None

            playlists = search_response.json().get("playlists", {}).get("items", [])

            if not playlists:
                return None

            return playlists[0].get("external_urls", {}).get("spotify")

        except Exception as e:
            # Log the error for debugging (optional)
            print(f"Error fetching playlist: {e}")
            return None

    def get(self, request):
        emotion = request.GET.get("emotion")
        if not emotion:
            return JsonResponse({"error": "Emotion parameter is required"}, status=400)

        playlist_url = self.get_spotify_playlist(emotion)

        if playlist_url:
            return JsonResponse({"playlist_url": playlist_url})
        else:
            return JsonResponse({"message": "No playlist found for that emotion."}, status=200)
