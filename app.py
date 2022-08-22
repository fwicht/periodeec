from dataclasses import dataclass
import logging
import os
import time
import requests
import spotipy

s = requests.Session()


@dataclass
class Environment:
    deemix_url: str
    deezer_email: str
    deezer_password: str
    spotify_client_id: str
    spotify_client_secret: str
    spotify_usernames: str
    interval: int


# Read ENV variables
env = Environment(
    deemix_url=os.getenv("DEEMIX_URL"),
    deezer_email=os.getenv("DEEZER_EMAIL"),
    deezer_password=os.getenv("DEEZER_PASSWORD"),
    spotify_client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    spotify_client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    spotify_usernames=os.getenv("SPOTIFY_USERNAMES"),
    interval=int(os.getenv("INTERVAL")),
)


def login():
    response = s.post(
        f"{env.deemix_url}/api/loginEmail",
        json={
            "accessToken": "",
            "email": env.deezer_email,
            "password": env.deezer_password,
        },
    )
    arl = response.json()["arl"]
    response = s.post(f"{env.deemix_url}/api/loginArl", json={"arl": arl})
    print(response.json())


def download(url: str):

    response = s.post(
        f"{env.deemix_url}/api/addToQueue",
        json={
            "bitrate": "null",
            "url": url,
        },
    )
    print(f"downloading {url}")


def playlists() -> list:
    ccm = spotipy.SpotifyClientCredentials(
        env.spotify_client_id, env.spotify_client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=ccm)
    playlists = [
        item["external_urls"]["spotify"]
        for username in env.spotify_usernames.split(",")
        for item in sp.user_playlists(username)["items"]
    ]
    return playlists


def main():
    login()
    while True:
        for playlist in playlists():
            download(playlist)
        print(f"sleeping for {env.interval} seconds")
        time.sleep(env.interval)


if __name__ == "__main__":
    main()
