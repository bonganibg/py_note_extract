import pytest
import guitarpro as gp
from py_note_extract.guitar_pro import parse_song, convert_song
from models import Song, Track, Note
import os

@pytest.fixture
def song_path():
    return os.path.join(os.path.dirname(__file__), "../../data/guitar_pro/song.gp3")

@pytest.fixture
def actual_song():
    return gp.parse_song(os.path.join(os.path.dirname(__file__), "../../data/guitar_pro/song.gp3"))

def test_parse_song(song_path):
    song = parse_song(song_path)
    assert isinstance(song, gp.models.Song)