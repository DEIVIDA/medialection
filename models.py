from sqlalchemy import create_engine, Table, Column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


db_engine = create_engine('sqlite:///music_collection.db')
Base = declarative_base()


table_song_artist = Table(
    'song_artist', 
    Base.metadata, 
    Column('song_id', Integer, ForeignKey('song.id')),
    Column('artist_id', Integer, ForeignKey('artist.id')),
)


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    songs = relationship('Song', back_populates='genre')

    def __repr__(self):
        return f"{self.name}"


class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, default=0, nullable=False)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship('Genre', back_populates='songs')
    artists = relationship('Artist', secondary=table_song_artist, back_populates='songs')

    def __repr__(self):
        return f"{self.name}"


class Artist(Base):
    __tablename__ = 'artist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    songs = relationship('Song', secondary=table_song_artist, back_populates='artists')

    def __repr__(self):
        return f"{self.name}"


Base.metadata.create_all(db_engine)
