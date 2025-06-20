import requests
from collections import defaultdict, deque

class ArtistSimilarityService:
    def __init__(self, max_degree=2, max_related_per_artist=3):
        self.max_degree = max_degree
        self.max_related_per_artist = max_related_per_artist

    def get_artist_id(self, artist_name):
        url = f"https://api.deezer.com/search/artist?q={artist_name}"
        response = requests.get(url)
        data = response.json()
        if data['data']:
            return data['data'][0]['id']
        return None

    def get_similar_artists(self, artist_id):
        url = f"https://api.deezer.com/artist/{artist_id}/related"
        response = requests.get(url)
        data = response.json()
        return [artist['name'].lower() for artist in data['data']]

    def expand_artist_dict(self, base_artists):
        expanded = defaultdict(int)
        visited = set()
        queue = deque([(artist, 1) for artist in base_artists.keys()])

        for artist in base_artists:
            expanded[artist] += base_artists[artist]  # Include base artists with initial score
            visited.add(artist)

        while queue:
            current_artist, degree = queue.popleft()

            if degree > self.max_degree:
                continue

            artist_id = self.get_artist_id(current_artist)
            if not artist_id:
                continue

            related_artists = self.get_similar_artists(artist_id)[:self.max_related_per_artist]

            for related in related_artists:
                expanded[related] += 1  # Add +1 every time it appears as a similar artist
                if related not in visited:
                    queue.append((related, degree + 1))
                    visited.add(related)

        return dict(expanded)

    def recommend_from_favorites(self, favorite_artists):
        base_dict = {a.lower(): 3 for a in favorite_artists}
        expanded = self.expand_artist_dict(base_dict)
        sorted_artists = sorted(expanded.items(), key=lambda x: x[1], reverse=True)
        return sorted_artists
