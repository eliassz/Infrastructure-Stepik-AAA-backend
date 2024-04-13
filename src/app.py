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


def base_validate_id(im_id):
    if im_id is None:
        error = 'Field "image_id" is not specified'
        logging.error(error)
        return error, 400
    return im_id, 200


def advanced_validate_id(im_id):
    logging.info(f'Start of advanced validation of {im_id}')
    try:
        im_id = int(im_id)
    except (TypeError, ValueError):
        error = 'Invalid image ID'
        logging.error(error)
        return error, 400

    if im_id not in IDS:
        error = 'There is no such id, try 10022, 9965'
        logging.error(error)
        return error, 400

    return im_id, 200


# curl http://localhost:8080/get_one_plate?im_id=10022
@app.route('/get_one_plate')
def get_one_plate():
    im_id = request.args.get('im_id')

    result, status = base_validate_id(im_id)

    if status != 200:
        return jsonify({'result': result, 'status': status})

    result, status = advanced_validate_id(im_id)

    if status != 200:
        return jsonify({'result': result, 'status': status})

    image_bytes, status = image_client.get_image(im_id)

    if status != 200:
        return jsonify({'result': image_bytes, 'status': status})
    try:
        res = plate_reader.read_text(image_bytes)
    except InvalidImage:
        error = 'Invalid image'
        logging.error(error)
        return jsonify({'result': error, 'status': 400})

    return jsonify({'result': res, 'status': 200})


# curl "http://localhost:8080/get_multiple_plates?im_id=10022,9965"
@app.route('/get_multiple_plates')
def get_multiple_plates():
    im_ids = request.args.get('im_id')

    result, status = base_validate_id(im_ids)

    if status != 200:
        return jsonify({'result': result, 'status': status})

    im_ids = im_ids.split(',')

    answers = {}
    for im_id in im_ids:
        result, status = advanced_validate_id(im_id)
        if status != 200:
            answers[im_id] = f'{status}, {result}'
            continue

        image_bytes, status = image_client.get_image(im_id)

        if status != 200:
            logging.error(f'{im_id}: {status} {image_bytes}')
            answers[im_id] = f'{status}, {image_bytes}'
            continue

        try:
            res = plate_reader.read_text(image_bytes)
            answers[im_id] = res
        except InvalidImage:
            error = 'Invalid image'
            logging.error(error)
            answers[im_id] = f'{im_id}: {404}, {error}'

    return jsonify(answers)


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.json.ensure_ascii = False
    app.run(host='0.0.0.0', port=8080, debug=True)
