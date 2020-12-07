import datetime
from gva.data.flows import BaseOperator
from google.cloud import storage
import json
import gva.logging

logger = gva.logging.get_logger()
logger.setLevel(10)

class SaveStringToBlobOperator(BaseOperator):

    def __init__(self, project, bucket, path, credentials_file):
        super().__init__()
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        client = storage.Client(project=project, credentials=credentials)
        self.bucket = client.get_bucket(bucket)
        self.path = path

    def execute(self, data={}, context={}):
        path = datetime.datetime.today().strftime(self.path)
        blob = self.bucket.blob(path)
        blob.upload_from_string(json.dumps(data))

        logger.debug(F'[SAVE_BLOB] {path}')

        return data, context