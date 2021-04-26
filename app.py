from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    canon_root = request.args.get('root')
    canon_type = request.args.get('type')
    canon_num_note = int(request.args.get('notenum'))

    if canon_type == 'R':
        pass
    elif canon_type == 'IR':
        pass
    elif canon_type == 'IS':
        pass


if __name__ == '__main__':
    app.run()
