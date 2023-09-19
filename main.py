import PySimpleGUI as sg
from sqlalchemy.orm import sessionmaker
import models


session = sessionmaker(models.db_engine)()

def load_songs(session=session):
    db_songs = session.query(models.Song).all()
    songs = []
    for song in db_songs:
        songs.append([song.name, song.duration, song.genre])
    return songs

def load_authors(session=session):
    db_artists = session.query(models.Artist).all()
    return [[artist.name] for artist in db_artists]

def load_genres(session=session):
    db_genres = session.query(models.Genre).all()
    return [[genre.name] for genre in db_genres]

def confirm_add_song(title, authors, duration, genre, session=session) -> bool:
    return True

def manage_authors(parent_window: sg.Window, session=session):
    pass

def manage_genres(parent_window: sg.Window, session=session):
    pass

def add_song(parent_window: sg.Window, session=session):
    parent_window.hide()
    layout = [
        [sg.Text('title', 15), sg.Input(size=20, key='-TITLE-')],
        [
            sg.Text('select author(s)', 11), 
            sg.Button('\u270F', key='-MANAGE-AUTHORS-'), 
            sg.Listbox(values=load_authors(session), size=(20, 7), key='-AUTHORS-'),
        ],
        [sg.Text('duration (s)', 15), sg.Input(size=4, key='-DURATION-')],
        [
            sg.Text('genre', 11), 
            sg.Button('\u270F', key='-MANAGE-GENRES-'),
            sg.Combo(values=load_genres(), size=20, key='-GENRE-'), 
        ],
        [sg.Button('Add this song', key='-CONFIRM-')],
    ]
    window = sg.Window('Add a song', layout, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-CONFIRM-':
            success = confirm_add_song(values['-TITLE-'], values['-AUTHORS-'], values['-DURATION-'], values['-GENRE-'], session)
            if success:
                break
        if event == '-MANAGE-AUTHORS-':
            manage_authors(parent_window=window, session=session)
        if event == '-MANAGE-GENRES-':
            manage_genres(parent_window=window, session=session)
    parent_window.un_hide()
    window.close()

def main(session=session):
    songs = load_songs(session)
    layout = [
        [sg.Table(
            values=songs,
            headings=['title', 'duration', 'genre'],
            key='-SONGS-',
            # size=(50, 20),
        )],
        [sg.Button('Add', key='-ADD-SONG-')],
    ]
    window = sg.Window('Media\'lection', layout, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-ADD-SONG-':
            add_song(window, session)
    window.close()

main()
