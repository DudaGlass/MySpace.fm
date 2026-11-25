
import os
import requests
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_URL = "https://ws.audioscrobbler.com/2.0/"


def lastfm_request(params):
    response = requests.get(
        LASTFM_API_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise RuntimeError(data.get("message", "Erro na API do Last.fm"))

    return data


def get_weekly_albums():
    api_key = os.getenv("LASTFM_API_KEY")
    username = os.getenv("LASTFM_USERNAME")

    if not api_key or not username:
        raise ValueError(
            "Configure LASTFM_API_KEY e LASTFM_USERNAME no .env"
        )

    base_params = {
        "user": username,
        "api_key": api_key,
        "format": "json"
    }

    # Primeiro: descobrir os períodos semanais disponíveis
    chart_data = lastfm_request({
        **base_params,
        "method": "user.getWeeklyChartList"
    })

    charts = chart_data.get("weeklychartlist", {}).get("chart", [])

    if isinstance(charts, dict):
        charts = [charts]

    if not charts:
        return []

    # Selecionar o período mais recente
    latest_chart = charts[-1]

    # Segundo: buscar os álbuns desse período
    album_data = lastfm_request({
        **base_params,
        "method": "user.getWeeklyAlbumChart",
        "from": latest_chart["from"],
        "to": latest_chart["to"]
    })

    albums = album_data.get("weeklyalbumchart", {}).get("album", [])

    if isinstance(albums, dict):
        albums = [albums]

    results = []

    for album in albums:
        artist = album.get("artist", {})

        if isinstance(artist, dict):
            artist = artist.get("#text", "")

        results.append({
            "name": album.get("name"),
            "artist": artist,
            "playcount": int(album.get("playcount", 0)),
            "cover": ""
        })

    return results
