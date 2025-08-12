from models import Song, Track, Note
from typing import List
import guitarpro as gp

def parse_song(song_path: str) -> gp.models.Song:
    """Parse a Guitar Pro song file into a Guitar Pro song object.

    Args:
        song_path (str): Path to the Guitar Pro song file.

    Returns:
        gp.models.Song: The parsed Guitar Pro song object.
    """
    return gp.parse(song_path)

def convert_song(song: gp.models.Song) -> Song:
    """Gets the key features from a Guitar Pro song object and converts it into a Song object.

    Args:
        song (gp.models.Song): The Guitar Pro song object.

    Returns:
        Song: 
    """

    newSong = Song()

    for track in song.tracks:
        if (track.isPercussionTrack):
            continue

        newSong.title = track.song.title
        newSong.artist = track.song.artist

        newTrack = __get_track_details(track.measures)
        newTrack.title = track.name

        newSong.tracks.append(newTrack)

    return newSong


def __get_track_details(measures: list[gp.models.Measure]) -> Track:
    """Gets the key features from a list of Guitar Pro measures and converts it into a Track object.

    Args:
        measures (list[gp.models.Measure]): The list of Guitar Pro measures.

    Returns:
        Track:
    """

    newTrack = Track()

    for measure in measures:
        tempo = measure.track.song.tempo        
        for voice in measure.voices:            
            for beat in voice.beats:
                duration = beat.duration.value
                for note in beat.notes:
                    pitch = note.realValue
                    octave = (pitch // 12) - 1
                    noteValue = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][pitch % 12]

                    newNote = Note(tempo=tempo, duration=duration, value=str(noteValue), pitch=octave)
                    newTrack.notes.append(newNote)

    return newTrack


