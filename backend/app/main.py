
import requests
from fastapi import FastAPI, HTTPException
from backend.app.integrations.lastfm import get_weekly_albums

app = FastAPI(
    title="MySpace.fm API",
    description="API para gerar colagens musicais com dados do Last.fm.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "MySpace.fm API is running!",
        "status": "online"
    }


@app.get("/albums/weekly")
def weekly_albums():
    try:
        albums = get_weekly_albums()

        return {
            "total": len(albums),
            "albums": albums
        }

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível conectar ao Last.fm."
        )

    except (ValueError, RuntimeError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
