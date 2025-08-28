import json
import mido 
from mido import tempo2bpm, MetaMessage, MidiTrack
from models import Song, Track, Note

PIANO_PROGRAMS = range(0, 8)
GUITAR_PROGRAMS = range(24, 32)

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def parse_song(song_path: str) -> mido.MidiFile:
    """Parse a MIDI song file into a MIDI song object.

    Args:
        song_path (str): Path to the MIDI song file.

    Returns:
        mido.MidiFile: The parsed MIDI song object.
    """
    artist, title = __file_name_to_song_title(song_path)

    mid = mido.MidiFile(song_path)    

    meta_track = MidiTrack()
    meta_track.append(MetaMessage('track_name', name=title))
    meta_track.append(MetaMessage('track_name', name=artist))
    mid.tracks.append(meta_track) 
     
    return mid

def __file_name_to_song_title(file_path: str) -> str:
    """Converts a file path to a song title.

    Args:
        file_path (str): The file path to convert.

    Returns:
        str: The converted song title.
    """
    
    file_path = file_path.split("/")
    artist = file_path[-2].replace("_", " ")
    title = file_path[-1].replace(".mid", "").replace("_", " ")

    return artist, title

def note_name_and_octave(note_number: int):
    note = NOTE_NAMES[note_number % 12]
    octave = note_number // 12 - 1
    return note, octave

def beats_to_note_value(beats: float) -> int:
    """Converts beats to a note value.

    Args:
        beats (float): The number of beats.

    Returns:
        int: The note value.
    """

    if beats == 0:
        return None
    
    note_value = 4 / beats

    candidates = [1, 2, 4, 8, 16, 32, 64, 128]
    closest = min(candidates, key=lambda x: abs(x - note_value))
    return closest

def convert_song(mid: mido.MidiFile) -> Song:
    """Converts a MIDI song file into a Song object.

    Args:
        mid (mido.MidiFile): The MIDI song file to convert.

    Returns:
        Song: The converted Song object.
    """
    
    current_tempo = 500000
    time_signature = (4, 4)
    
    song = Song()    

    [artist, title] = mid.tracks[-1]

    song.artist = artist.name
    song.title = title.name       

    for track in mid.tracks[:-1]:        
        current_program = None 
        abs_time_ticks = 0
        active_notes = {}        

        output_track = Track()
        output_track.title = track.name

        for msg in track:    
            abs_time_ticks += msg.time                                        

            match msg.type:
                case "program_change":
                    current_program = msg.program
                case "set_tempo":
                    current_tempo = msg.tempo
                case "time_signature":
                    time_signature = (msg.numerator, msg.denominator)
                case "note_on":
                    if current_program in PIANO_PROGRAMS or current_program in GUITAR_PROGRAMS:
                        active_notes[msg.note] = abs_time_ticks                        
                case "note_off":                                        
                    if current_program in PIANO_PROGRAMS or current_program in GUITAR_PROGRAMS:
                        if msg.note in active_notes:
                            start_ticks = active_notes.pop(msg.note)
                            duration_ticks = abs_time_ticks - start_ticks
                            
                            duration_beats = duration_ticks / mid.ticks_per_beat
                            duration_value = beats_to_note_value(duration_beats)

                            bpm = tempo2bpm(current_tempo)
                            note_name, octave = note_name_and_octave(msg.note)

                            note = Note(tempo=int(bpm), duration=duration_value, value=note_name, pitch=octave, timeSignature=f"{time_signature[0]}/{time_signature[1]}")

                            output_track.notes.append(note)

        song.tracks.append(output_track)

    return song                    
    
if __name__ == "__main__":
    filename = "./temp/ABBA/Dancing_Queen.2.mid"
    mid = parse_song(filename)
    song = convert_song(mid)