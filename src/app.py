import logging
from flask import Flask, request, jsonify
from models.plate_reader import PlateReader, InvalidImage
from clients import ImageClient

IDS = {10022, 9965}

PATH_TO_MODEL = './model_weights/plate_reader_model.pth'
IMAGE_HOST = 'http://178.154.220.122:7777/images/'

app = Flask(__name__)
plate_reader = PlateReader.load_from_file(PATH_TO_MODEL)
image_client = ImageClient(host=IMAGE_HOST)


def validate_id(im_id):
    if im_id is None:
        logging.error('Field "image_ids" is not specified')
        return None, 400

    try:
        im_id = int(im_id)
    except (TypeError, ValueError):
        logging.error('Invalid image ID')
        return None, 400

    if im_id not in IDS:
        logging.error('There is no such id, try 10022, 9965')
        return None, 400


# curl http://localhost:8080/get_one_plate?im_id=10022
@app.route('/get_one_plate')
def get_one_plate():
    im_id = request.args.get('im_id')

    validate_id(im_id)

    image_bytes, status = image_client.get_image(im_id)

    if status != 200:
        return jsonify({'result': image_bytes, 'status': status})
    try:
        res = plate_reader.read_text(image_bytes)
    except InvalidImage:
        error = 'invalid image'
        logging.error(error)
        return jsonify({'result': error, 'status': 400})

    return jsonify({'result': res, 'status': 200})


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.json.ensure_ascii = False
    app.run(host='0.0.0.0', port=8080, debug=True)
