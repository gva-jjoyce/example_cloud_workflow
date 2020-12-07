from gva.services import GoogleTaskOperator
from flask import Flask, request, jsonify, make_response
from operators import FakeGetHostsOperator
from gva.data.flows.operators import EndOperator
from gva.data.flows import runner
import gva.logging

CREDENTIALS_FILE = "bqro.json"

app = Flask(__name__)

get_hosts = FakeGetHostsOperator()
create_gcp_cloud_task = GoogleTaskOperator(credentials_file=CREDENTIALS_FILE)
end = EndOperator()

flow = get_hosts > create_gcp_cloud_task > end

logger = gva.logging.get_logger()
logger.setLevel(10)

@app.route('/', methods=['POST'])
def process_command():
    try:
        context = request.get_json(force=True)
        job_name = context.get('job_name')
        
        runner.go(flow=flow, context=context)

        message = F"[GETHOSTS] {job_name} run okay - {context.get('uuid')}"
        logger.debug(message)
        return message
    except Exception as err:
        message = F"[GETHOSTS] {job_name} failed - {context.get('uuid')} - {type(err).__name__} - {err}"
        logger.error(message)
        return message, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2100)
