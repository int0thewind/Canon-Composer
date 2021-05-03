from flask import Flask, request, make_response
from src.composer import shift, reverse, reverse_shift, inverse_shift, inverse_reverse_shift,\
    shift_melodic, reverse_shift_melodic, reverse_melodic

app = Flask(__name__)


def make_error_response(msg: str):
    res = make_response({'error': msg}, 400)
    return res


@app.route('/')
def index():
    root = request.args.get('root')
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

    # Generate Midi files and return


if __name__ == '__main__':
    app.run()
