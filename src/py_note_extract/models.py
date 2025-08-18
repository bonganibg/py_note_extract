from pydantic import BaseModel
import pandas as pd
from datetime import datetime

class Note(BaseModel):
    tempo: int 
    duration: int
    value: str
    pitch: int
    timeSignature: str = None

class Track(BaseModel):
    title: str = None    
    notes: list[Note] = []    

class Song(BaseModel):
    artist: str = None
    title: str = None    
    tracks: list[Track] = []    

def song_to_dataframe(song: Song) -> pd.DataFrame:
    """Converts a Song object into a pandas DataFrame.

    Args:
        song (Song): The Song object to convert.

    Returns:
        pd.DataFrame: The converted DataFrame.
    """

    song_sequences = []

    for track in song.tracks:
        song_details = {
            "tempo": [],
            "duration": [],
            "note": [],
            "pitch": [],
            "timeSignature": [],
            "timestamp": []
        }

        for note in track.notes:
            song_details["tempo"].append(note.tempo)
            song_details["duration"].append(note.duration)
            song_details["pitch"].append(note.pitch)
            song_details["note"].append(note.value)
            song_details["timeSignature"].append(note.timeSignature)
            song_details["timestamp"].append(datetime.now())        

        df = pd.DataFrame(song_details)
        df.attrs["song"] = song.title
        df.attrs["artist"] = song.artist
        df.attrs["track"] = track.title

        song_sequences.append(df)
    return song_sequences
    