"""
This is a stub for the dispatcher.

https://dispatcher.flows.gva.services/

- flow is static (although programatically defined)
- end point is static

This does not persist anything to a database
"""
import networkx as nx
from flask import Flask, request, jsonify
import json
import gva.logging
from gva.services import create_http_task

#####################################################################

# The easiest way to quickly describe a DAG
# This should probably be defined in a relational database instead
# see comments in get_next_operations

dags = {}

dags['qvm'] = nx.DiGraph()
dags['qvm'].add_node('start')
dags['qvm'].add_node('gethosts', url='https://getfakehosts.qvm.flows.gva.services')
dags['qvm'].add_node('getfindings', url='https://getfindings.qvm.flows.gva.services')
dags['qvm'].add_node('end')

dags['qvm'].add_edge('start', 'gethosts')
dags['qvm'].add_edge('gethosts', 'getfindings')
dags['qvm'].add_edge('getfindings', 'end')

#####################################################################

logger = gva.logging.get_logger()
logger.setLevel(10)

app = Flask(__name__)
CREDENTIALS_FILE = "bqro.json"
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

def get_next_task_flows(job_name, previous_task_flow):
    # this should read the flow from a database
    # that will externalize the control of the flow
    # i.e. implement Inversion of Control 
    dag = dags.get(job_name)
    next_task_flows = []
    if dag:
        outgoing_edges = dag.out_edges(previous_task_flow, default=[])
        for _, next_task_flow in outgoing_edges:
            next_task_flows.append(next_task_flow)
    return next_task_flows

def get_task_flow_url(job_name, task_flow):
    dag = dags.get(job_name)
    return dag.nodes()[task_flow].get('url')

@app.route('/<job_name>', methods=['POST'])
def process_command(job_name):
    try:
        context = request.get_json(force=True)
        context['job_name'] = job_name
        previous_task_flow = context.get('task-flow')
        next_task_flows = get_next_task_flows(job_name=job_name, previous_task_flow=previous_task_flow)

        logger.debug(F"[DISPATCHER] Start - {job_name} - {previous_task_flow} - {len(next_task_flows)}")

        for task_flow in next_task_flows:
            if task_flow == 'end':
                # this should finalize a flow execution in the database
                logger.debug(F'[DISPATCHER] {job_name} completed.')
                return F"[DISPATCHER] {job_name} completed."
            context['task-flow'] = task_flow
            # trigger the next operation(s)
            create_http_task(project='vulnerability-analytics',
                            queue=str(job_name),
                            url=get_task_flow_url(job_name, task_flow),
                            payload=context,
                            credentials=credentials)
            logger.debug(F"[DISPATCHER] Okay {job_name} - {previous_task_flow} - {task_flow}")

        return F"[DISPATCHER] Okay {job_name} {previous_task_flow}"
    except Exception as err:
        logger.error(f"{type(err).__name__} {err}")
        return F"[DISPATCHER] Exception {type(err).__name__} {err}", 500

if __name__ == '__main__':
    # this should be running on dispatcher.flows.gva.services
    app.run(host="0.0.0.0", port=2100)