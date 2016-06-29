import datetime
from collections import defaultdict

from conga.models import (BaseAlbum, BaseArtist, BasePlayList, BaseTrack,
                          BaseTrackList)


class Artist(BaseArtist):

    def __init__(self, data):
        self.name = data['artist']
        self.uri = 'gmusic:artist:%s' % data.get('artistId', [-1])[0]

        picture = data.get('artistArtRef')
        if picture:
            self.image = picture[0]['url']


class Album(BaseAlbum):

    def __init__(self, data, artist, num_tracks):
        self._name = data['album']
        self._uri = 'gmusic:album:%s' % data.get('albumId', -1)
        self._raw_date = data.get('year', None)
        self._date = datetime.datetime(self._raw_date, 1, 1, 1, 1)\
            if self.raw_date else datetime.datetime(1970, 1, 1, 1, 1)
        self._artists = [artist]
        self._artist = artist

        picture = data.get('albumArtRef')
        self._image = picture[0]['url'] if picture else ''

        self._num_tracks = num_tracks


class Track(BaseTrack):

    def __init__(self, data, album, artist):
        self.name = data['title']
        self.uri = 'gmusic:track:%s' % data['id']
        self.length = int(data['durationMillis'])
        self.album = album
        self.artists = [artist]
        self.track_number = data.get("trackNumber", 0)


class TrackList(BaseTrackList):

    def __init__(self, data=None):
        if data:
            albums = defaultdict(int)
            for track in data:
                albums[track['album']] += 1

            for track in data:
                artist = Artist(track)
                album = Album(track, artist, num_tracks=albums[track['album']])
                self.append(Track(track, album, artist))


class PlayList(BasePlayList):

    def __init__(self, data, tracks):
        self.name = data['name']
        self.uri = 'gmusic:playlist:%s' % data['id']
        self.tracks = tracks
        self.image = None
