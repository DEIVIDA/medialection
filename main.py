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

def load_artists(session=session):
    db_artists = session.query(models.Artist).all()
    return db_artists # [artist.name for artist in db_artists]

def load_genres(session=session):
    db_genres = session.query(models.Genre).all()
    return db_genres # [genre.name for genre in db_genres]

def manage_artists(parent_window: sg.Window, session=session):
    parent_window.hide()
    layout = [
        [sg.Listbox(values=load_artists(), size=(20, 7), key='-ARTISTS-', enable_events=True, select_mode=sg.SELECT_MODE_MULTIPLE)],
        [sg.Input(size=20, key='-NAME-')], 
        [sg.Button('Add', key='-ADD-'), sg.Button('Update', key='-UPDATE-', disabled=True), sg.Button('Delete', key='-DELETE-', disabled=True)],
    ]
    window = sg.Window('Artists', layout, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-ARTISTS-':
            if len(values['-ARTISTS-']) > 0:
                window['-NAME-'].update(values['-ARTISTS-'][0])
                window['-UPDATE-'].update(disabled=False)
                window['-DELETE-'].update(disabled=False)
            else:
                window['-UPDATE-'].update(disabled=True)
                window['-DELETE-'].update(disabled=True)
        if event == '-UPDATE-':
            artist:models.Artist = values['-ARTISTS-'][0]
            if len(values['-NAME-']) > 0 and not session.query(models.Artist).filter_by(name=values['-NAME-']).all():
                artist.name = values['-NAME-']
                session.add(artist)
                session.commit()
                window['-ARTISTS-'].update(values=load_artists(session))
                window['-NAME-'].update('')
            else:
                sg.popup("name cannot be empty and must be unique", title='ERROR')
        if event == '-ADD-':
            if len(values['-NAME-']) > 0 and not session.query(models.Artist).filter_by(name=values['-NAME-']).all():
                session.add(models.Artist(name=values['-NAME-']))
                session.commit()
                window['-ARTISTS-'].update(values=load_artists(session))
                window['-NAME-'].update('')
            else:
                sg.popup("name cannot be empty and must be unique", title='ERROR')
        if event == '-DELETE-':
            for artist in values['-ARTISTS-']:
                session.delete(artist)
                session.commit()
                window['-ARTISTS-'].update(values=load_artists(session))
    parent_window['-ARTISTS-'].update(values=load_artists(session))
    parent_window.un_hide()

def manage_genres(parent_window: sg.Window, session=session):
    parent_window.hide()
    layout = [
        [sg.Listbox(values=load_genres(), size=(20, 7), key='-GENRES-', enable_events=True, select_mode=sg.SELECT_MODE_MULTIPLE)],
        [sg.Input(size=20, key='-NAME-')], 
        [sg.Button('Add', key='-ADD-'), sg.Button('Update', key='-UPDATE-', disabled=True), sg.Button('Delete', key='-DELETE-', disabled=True)],
    ]
    window = sg.Window('Genres', layout, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-GENRES-':
            if len(values['-GENRES-']) > 0:
                window['-NAME-'].update(values['-GENRES-'][0])
                window['-UPDATE-'].update(disabled=False)
                window['-DELETE-'].update(disabled=False)
            else:
                window['-UPDATE-'].update(disabled=True)
                window['-DELETE-'].update(disabled=True)
        if event == '-UPDATE-':
            genre:models.Genre = values['-GENRES-'][0]
            if len(values['-NAME-']) > 0 and not session.query(models.Genre).filter_by(name=values['-NAME-']).all():
                genre.name = values['-NAME-']
                session.add(genre)
                session.commit()
                window['-GENRES-'].update(values=load_genres(session))
                window['-NAME-'].update('')
            else:
                sg.popup("name cannot be empty and must be unique", title='ERROR')
        if event == '-ADD-':
            if len(values['-NAME-']) > 0 and not session.query(models.Genre).filter_by(name=values['-NAME-']).all():
                session.add(models.Genre(name=values['-NAME-']))
                session.commit()
                window['-GENRES-'].update(values=load_genres(session))
                window['-NAME-'].update('')
            else:
                sg.popup("name cannot be empty and must be unique", title='ERROR')
        if event == '-DELETE-':
            for genre in values['-GENRES-']:
                session.delete(genre)
                session.commit()
                window['-GENRES-'].update(values=load_genres(session))
    parent_window['-GENRE-'].update(values=load_genres(session))
    parent_window.un_hide()

def validate_song(title, authors, duration, genre) -> int:
    errors = []
    if not len(title) > 0:
        errors.append("title cannot be empty")
    if not len(duration) > 0:
        errors.append("duration must be not empty")
    try:
        duration = int(duration)
    except ValueError:
        errors.append("duration must be a number in seconds")
    if not duration > 0:
        errors.append("duration must be a positive number")
    if not len(authors) > 0:
        errors.append("there must be at least one artist")
    if not genre or not isinstance(genre, models.Genre):
        errors.append("there must be a genre set")
    if len(errors) > 0:
        sg.popup(";\n".join(errors))
    else:
        return duration

def confirm_add_song(title, artists, duration, genre, session=session) -> bool:
    duration = validate_song(title, artists, duration, genre)
    if duration:
        new_song = models.Song(name=title, duration=duration, genre=genre)
        new_song.artists = artists
        session.add(new_song)
        session.commit()
        return True

def add_song(parent_window: sg.Window, session=session):
    parent_window.hide()
    layout = [
        [sg.Text('title', 15), sg.Input(size=20, key='-TITLE-')],
        [
            sg.Text('select artist(s)', 11), 
            sg.Button('\u270F', key='-MANAGE-ARTISTS-'), 
            sg.Listbox(values=load_artists(session), size=(20, 7), key='-ARTISTS-', select_mode=sg.SELECT_MODE_MULTIPLE),
        ],
        [sg.Text('duration (sec.)', 15), sg.Input('0', size=4, key='-DURATION-')],
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
            success = confirm_add_song(values['-TITLE-'], values['-ARTISTS-'], values['-DURATION-'], values['-GENRE-'], session)
            if success:
                break
        if event == '-MANAGE-ARTISTS-':
            manage_artists(parent_window=window, session=session)
        if event == '-MANAGE-GENRES-':
            manage_genres(parent_window=window, session=session)
    parent_window.un_hide()
    parent_window['-SONGS-'].update(values=load_songs(session))
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
