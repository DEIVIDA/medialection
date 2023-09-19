from collections.abc import Callable
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import models
import os


class TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.test_engine = create_engine('sqlite:///test.db')
        models.Base.metadata.create_all(self.test_engine)
        self.session = sessionmaker(self.test_engine)()
        self.genre_rock = models.Genre(name='Rock')
        self.genre_rap = models.Genre(name='Rap')
        self.artist_metallica = models.Artist(name='Metallica')
        self.artist_dre = models.Artist(name='Dr.Dre')
        self.artist_snoop = models.Artist(name='Snoop Dog')
        self.song_fuel = models.Song(name='Fuel', duration=267, genre=self.genre_rock)
        self.song_enter_sandman = models.Song(name='Enter Sandman', duration=332, genre=self.genre_rock)
        self.song_still_dre = models.Song(name='Still Dre', duration=290, genre=self.genre_rap)
        self.artist_metallica.songs = [self.song_fuel, self.song_enter_sandman]
        self.song_still_dre.artists = [self.artist_dre, self.artist_snoop]
        genres = [self.genre_rap, self.genre_rock]
        artists = [self.artist_dre, self.artist_metallica, self.artist_snoop]
        songs = [self.song_enter_sandman, self.song_fuel, self.song_still_dre]
        self.session.add_all(genres)
        self.session.add_all(songs)
        self.session.add_all(artists)
        self.session.commit()

    def tearDown(self) -> None:
        self.session.close()
        self.test_engine.dispose()
        os.remove('test.db')

    def test_song_artist(self):
        dre = self.session.query(models.Artist).filter_by(name="Dr.Dre").one()
        dog = self.session.query(models.Artist).filter_by(name="Snoop Dog").one()
        self.assertEqual(dre.songs[0].name, "Still Dre")
        self.assertEqual(dog.songs[0].name, "Still Dre")
        self.assertEqual(dog.songs[0].genre.name, 'Rap')


if __name__ == "__main__":
    unittest.main()
