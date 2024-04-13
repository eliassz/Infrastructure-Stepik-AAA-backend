import io
import logging
import requests

# Setup basic configuration for logging
logging.basicConfig(
    format='[%(levelname)s] [%(asctime)s] %(message)s',
    level=logging.INFO,
)


class ImageClient:
    """A client for fetching images from a given host URL."""

    def __init__(self, host: str, timeout=5):
        """
        Initialize the client with a host URL and a timeout.

        :param host: Base URL of the image server
        :param timeout: Timeout for network requests
        """
        self.host = host
        self.timeout = timeout

    def get_image(self, img_id: int):
        """
        Retrieve an image by its ID from the host and return it as
        a byte stream.

        :param img_id: Integer ID of the image to retrieve
        :return: Tuple containing an image stream and a status code
        """
        try:
            url = f"{self.host}/{img_id}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            image_bytes = response.content
            return io.BytesIO(image_bytes), 200

        except requests.HTTPError as e:
            status_code = e.response.status_code
            error = f"HTTP error ({status_code}) occurred: {e}"
            logging.error(error)
            return error, status_code

        except requests.RequestException as e:
            error = f"Network-related error occurred: {str(e)}"
            logging.error(error)
            return error, 503

        except Exception as e:
            error = f"Unexpected error occurred: {str(e)}"
            logging.error(error)
            return error, 500


if __name__ == '__main__':
    client = ImageClient(host='http://178.154.220.122:7777/images/')
    image_stream, status = client.get_image(10021)
    # image_stream, status = client.get_image(10022)
    print(f"Status: {status}, Image stream type: {type(image_stream)}")
