
from gmusicapi import Mobileclient
import requests

from .models import PlayList, TrackList


class Plugin:
    name = 'gmusic'

    def __init__(self, username, password):
        self.client = Mobileclient()
        self.client.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
        # self.webclient = Webclient()
        # self.webclient.login(username, password)

    def get_tracks(self, artist=None, album=None):
        """
        Fetches tracks from api.

        If no filter is defined, it will get user tracks
        """
        return TrackList(self.client.get_all_songs())

    def get_playlists(self):
        """
        Get playlists and radios
        """
        playlists = []
        for playlist in self.client.get_all_user_playlist_contents():
            tracks = TrackList([self.client.get_track_info(x['trackId']) for x in playlist['tracks']])
            playlists.append(PlayList(playlist['name'], tracks))
        return playlists

    def stream(self, track):
        def _stream(url):
            inp = requests.get(url, stream=True)
            chunk_size = 1024
            for chunk in inp.iter_content(chunk_size):
                if not chunk:
                    continue
                yield chunk
        song_id = track.uri.split(':')[-1]
        return _stream(self.client.get_stream_url(song_id))

    def search(self, keywords, matches):
        results = self.client.search(keywords)
        if matches == 'artist':
            return {'artists': results.get('artist_hits', [])}
        elif matches == 'album':
            return {'albums': results.get('album_hits', [])}
        elif matches == 'tracks':
            return {'tracks': results.get('song_hits', [])}
        elif matches == 'all':
            return {'artists': results.get('artist_hits', []),
                    'albums': results.get('album_hits', []),
                    'tracks': results.get('song_hits', [])}
