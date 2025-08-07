from pydantic import BaseModel

class Note(BaseModel):
    tempo: int 
    duration: int
    value: str
    pitch: int

class Track(BaseModel):
    title: str = None
    notes: list[Note] = []

class Song(BaseModel):
    artist: str = None
    title: str = None
    tracks: list[Track] = []