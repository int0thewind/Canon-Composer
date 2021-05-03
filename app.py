from flask import Flask, request, make_response, send_file
from src.composer import shift, reverse, reverse_shift, inverse_shift, inverse_reverse_shift,\
    shift_melodic, reverse_shift_melodic, reverse_melodic
from src.midi import ROOT_MIDI_NUMBER, note_series_to_midi_number, write_midi

app = Flask(__name__)


def make_error_response(msg: str):
    res = make_response({'error': msg}, 400)
    return res


@app.route('/')
def index():
    root = ROOT_MIDI_NUMBER[request.args.get('root')]
    canon_type = request.args.get('type')
    num_note = int(request.args.get('notenum'))
    melodic = bool(request.args.get('melodic'))

    if canon_type == 'S':
        pri, sec = shift(num_note) if not melodic else shift_melodic(num_note)
    elif canon_type == 'R':
        pri, sec = reverse(num_note) if not melodic else reverse_melodic(num_note)
    elif canon_type == 'RS':
        pri, sec = reverse_shift(num_note) if not melodic else reverse_shift_melodic(num_note)
    elif canon_type == 'IS':
        pri, sec = inverse_shift(num_note)
    elif canon_type == 'IRS':
        pri, sec = inverse_reverse_shift(num_note)
    else:
        return make_error_response('Incorrect canon type')

    # Generate Midi Series
    pri_midi = note_series_to_midi_number(pri, root)
    print(pri_midi)
    sec_midi = note_series_to_midi_number(sec, root - 12)

    # Generate Midi files and return
    write_midi(pri_midi, sec_midi, 'canon.mid')
    return send_file('canon.mid', 'audio/midi')


if __name__ == '__main__':
    app.run(debug=True)
