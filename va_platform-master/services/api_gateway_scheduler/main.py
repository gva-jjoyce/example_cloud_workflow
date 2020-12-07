from flask import Flask, request, jsonify, make_response
import gva.logging
from gva.services import create_http_task
import uuid

CREDENTIALS_FILE = "bqro.json"
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

app = Flask(__name__)

logger = gva.logging.get_logger()
logger.setLevel(10)

@app.route('/<job_name>/<action>', methods=['POST'])
def process_command(job_name, action):
    if action.lower() != 'start':
        return "invalid action", 500
    try:
        job_name = job_name.lower()
        context = request.form.to_dict() # we may get passed other info in the request
        context['job_name'] = job_name
        context['uuid'] = str(uuid.uuid4())
        context['task-flow'] = 'start'  # all flows begin with a 'start'
        # TODO: create an entry in the database for this job
        create_http_task(project='vulnerability-analytics',
                        queue=job_name,
                        url=F"https://dispatcher.flows.gva.services/{job_name}",
                        payload=context,
                        credentials=credentials)

        message = F"[API_GATEWAY_SCHEDULER] Job {job_name} triggered with identifier {context.get('uuid')}"
        logger.debug(message)
        return message
    except Exception as err:
        message = F"[API_GATEWAY_SCHEDULER] Job {job_name} trigger failed - {type(err).__name__} - {err}"
        logger.error(message)
        return message, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2100)
