import sys
from math import ceil
from random import choices
from typing import List, Literal, Dict, Tuple

from src.canontype import CanonTypeAbbr
from src.note import Note

from musx.midi.midiseq import MidiSeq
from musx.midi.midifile import MidiFile
from musx.scheduler import Scheduler
from musx.rhythm import rhythm
from musx.midi.midinote import MidiNote


NoteLeap = Literal['no_jump', 'jump_up', 'jump_down']

ROOT_MIDI_NUMBER = {
    "c": 60,
    "d-flat": 61,
    "d": 62,
    "e-flat": 63,
    "e": 64,
    "f": 65,
    "g-flat": 66,
    "g": 67,
    "a-flat": 68,
    "a": 69,
    "b-flat": 70,
    "b": 71,
}


TEMPO = rhythm('q', 60)


def _find_closest_midi(target: int, int_list: List[int]) -> int:
    min_distance = sys.maxsize
    ret = -1
    for i in int_list:
        if (dist := abs(i - target)) < min_distance:
            min_distance = dist
            ret = i
    return ret


def note_series_to_midi_number(note_list: List[Note], root: int):
    upper_bound = root + 9
    lower_bound = root - 9

    ret = [note_list[0].convert_to_midi(root)]
    for i in range(1, len(note_list)):
        all_possible_midi = note_list[i].get_all_possible_midi(root)
        candidate = _find_closest_midi(ret[i - 1], all_possible_midi)
        if candidate > upper_bound:
            candidate -= 12
        elif candidate < lower_bound:
            candidate += 12
        ret.append(candidate)

    return ret


def _write_midi_sequence(q: Scheduler, key_list: List[int], channel: int):
    for key in key_list:
        midi_note = MidiNote(time=q.now, dur=TEMPO, key=key, amp=0.5, chan=channel)
        q.out.addevent(midi_note)
        yield TEMPO


def write_midi(primary: List[int], secondary: List[int], file_name: str):
    meta = MidiSeq.metaseq()
    t1 = MidiSeq()
    q: Scheduler = Scheduler(t1)
    q.compose(_write_midi_sequence(q, primary, 0))
    q.compose(_write_midi_sequence(q, secondary, 1))
    MidiFile(file_name, [meta, t1]).write()

