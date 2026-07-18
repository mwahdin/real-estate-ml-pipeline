import requests
import csv

class DivarClient:
    BASE_URL = "https://api.divar.ir"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                ),
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def viewport(self, payload: dict):
        url = f"{self.BASE_URL}/v8/mapview/viewport"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_post_detail(self, token: str):
        url = f"{self.BASE_URL}/v8/posts-v2/web/{token}"

        headers = {
            "Accept": "application/json-filled",
            "Origin": "https://divar.ir",
            "Referer": "https://divar.ir/",
            "x-render-type": "CSR",
        }

        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def search(self, payload: dict):
        url = f"{self.BASE_URL}/v8/postlist/w/search"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

