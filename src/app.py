import io
# Убран импорт requests, поскольку он неправильно использовался для доступа к данным запроса
from flask import Flask, request, jsonify
import logging

from models.plate_reader import PlateReader, InvalidImage

app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')

@app.route('/')
def hello_world():
    return '<h1><center>Hello, Ilya!</center></h1>'

@app.route('/greetings')
def greetings():
    name = request.args.get("name", "Ilya")
    return jsonify({
        "key 1": f'Hi, {name}',
        "key 2": 'Such a nice day, buddy',
    })

@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    im = request.get_data()
    im = io.BytesIO(im)
    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return jsonify({'error': 'invalid image'}), 400
    return jsonify({
        'plate_number': res,
    })

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.json.ensure_ascii = False
    app.run(host='0.0.0.0', port=8080, debug=True)
