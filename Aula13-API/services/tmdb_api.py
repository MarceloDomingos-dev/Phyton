import os

import requests

TMDB_BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

_DEMO_FILMES = [
    {
        "id": 550,
        "title": "Clube da Luta",
        "overview": "Um homem solitário conhece um vendedor de sabonete.",
        "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "vote_average": 8.4,
        "release_date": "1999-10-15",
    },
    {
        "id": 27205,
        "title": "A Origem",
        "overview": "Um ladrão invade sonhos para plantar uma ideia.",
        "poster_path": "/oYu0037M7541PxH2N22L6Q26Ia.jpg",
        "vote_average": 8.8,
        "release_date": "2010-07-16",
    },
]


class TmdbApi:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY", "").strip()
        self.language = os.getenv("TMDB_LANGUAGE", "pt-BR")
        self.modo_demo = not self.api_key or self.api_key == "sua_chave_aqui"

    @property
    def usando_demo(self):
        return self.modo_demo

    def _get(self, endpoint, params=None):
        if self.modo_demo:
            return None
        params = params or {}
        params["api_key"] = self.api_key
        params.setdefault("language", self.language)
        try:
            resp = requests.get(f"{TMDB_BASE}{endpoint}", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None

    @staticmethod
    def poster_url(poster_path):
        if not poster_path:
            return None
        return f"{IMG_BASE}{poster_path}"

    def _normalizar(self, item):
        return {
            "id": item.get("id"),
            "titulo": item.get("title") or item.get("name", "Sem título"),
            "sinopse": item.get("overview") or "",
            "poster_url": self.poster_url(item.get("poster_path")),
            "nota": round(item.get("vote_average") or 0, 1),
            "ano": (item.get("release_date") or "")[:4] or "—",
        }

    def buscar(self, termo):
        if not termo.strip():
            return [], self.modo_demo
        if self.modo_demo:
            termo_lower = termo.lower()
            return [
                self._normalizar(f)
                for f in _DEMO_FILMES
                if termo_lower in f["title"].lower()
            ], True
        data = self._get("/search/movie", {"query": termo})
        if not data:
            return [], False
        return [self._normalizar(f) for f in data.get("results", [])], False

    def populares(self):
        if self.modo_demo:
            return [self._normalizar(f) for f in _DEMO_FILMES], True
        data = self._get("/movie/popular")
        if not data:
            return [], False
        return [self._normalizar(f) for f in data.get("results", [])], False
