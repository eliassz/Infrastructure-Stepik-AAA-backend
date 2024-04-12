import logging
from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
from clients import ImageClient

IDS = set(10022, 9965)

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
@app.route('/get_multiples_plates')
def get_one_plates():
    im_id = request.args.get('im_id')

    validate_id(im_id)

    image_bytes, status = image_client.get_image(im_id)

    if status != 200:
        return image_bytes, status
    try:
        res = plate_reader.read_text(image_bytes)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image'}, 400

    return {'plate_number': res}, 200


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
