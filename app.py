from flask import Flask, request, make_response
from src.generator import shift, reverse, reverse_shift, inverse_shift, inverse_reverse_shift

app = Flask(__name__)


def make_error_response(msg: str):
    res = make_response({'error': msg}, 400)
    return res


@app.route('/')
def index():
    root = request.args.get('root')
    canon_type = request.args.get('type')
    num_note = int(request.args.get('notenum'))
    reduce_leap = bool(request.args.get('reduceleap'))
    reduce_unison = bool(request.args.get('reduceunison'))

    if canon_type == 'S':
        series = shift(num_note, reduce_leap, reduce_unison)
    elif canon_type == 'R':
        series = reverse(num_note, reduce_leap, reduce_unison)
    elif canon_type == 'RS':
        series = reverse_shift(num_note, reduce_leap, reduce_unison)
    elif canon_type == 'IS':
        series = inverse_shift(num_note, reduce_leap, reduce_unison)
    elif canon_type == 'IRS':
        series = inverse_reverse_shift(num_note, reduce_leap, reduce_unison)
    else:
        return make_error_response('Incorrect canon type')

    # Generate Midi Series

    # Generate Midi files and return


if __name__ == '__main__':
    app.run()
