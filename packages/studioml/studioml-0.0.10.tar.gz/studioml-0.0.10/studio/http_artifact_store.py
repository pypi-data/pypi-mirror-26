import logging
import requests

from .tartifact_store import TartifactStore
from .util import download_file
logging.basicConfig()


class HTTPArtifactStore(TartifactStore):
    def __init__(self, url,
                 timestamp=None,
                 compression=None,
                 verbose=logging.DEBUG):

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(verbose)

        self.url = url
        self.timestamp = timestamp

        super(HTTPArtifactStore, self).__init__(
            False,
            compression=compression,
            verbose=verbose)
    '''
    def _upload_file(self, key, local_path):
        with open(local_path, 'rb') as f:
            resp = requests.post(
                self.post['url'],
                files={'file': f},
                data=self.post['fields'])

        if resp.status_code != 204:
            # You'd think the code that we are checking
            # against should be 200 (OK)
            # but for some reason S3 runs the operation
            # correctly, and yet returns 204
            self.logger.error(str(resp))
    '''

    def _upload_file(self, key, local_path):
        with open(local_path, 'rb') as f:
            resp = requests.put(
                self.url,
                data=f.read())

        if resp.status_code != 200:
            self.logger.error(str(resp.reason))

    def _download_file(self, key, local_path):
        download_file(self.url, local_path, self.logger)

    def _delete_file(self, key):
        raise NotImplementedError

    def _get_file_url(self, key):
        raise NotImplementedError

    def _get_file_post(self, key):
        return self.client.generate_presigned_post(
            Bucket=self.bucket,
            Key=key)

    def _get_file_timestamp(self, key):
        return self.timestamp

    def get_qualified_location(self, key):
        return self.endpoint + '/' + key
