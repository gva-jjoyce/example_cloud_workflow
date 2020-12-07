import time
from gva.data.flows import BaseOperator

def chunker(array=[], chunk_size=100):
    for i in range(0, len(array), chunk_size):
        yield array[i:i + chunk_size]

class FakeGetHostsOperator(BaseOperator):
    """
    Although this is a stub, it still includes chunking functionality so
    that the size of the context doesn't exceed its limits.
    """
    def execute(self, data={}, context={}):

        hosts = ["ABC123"]
        chunk_size = int(context.get("chunk_size", 100))
        
        for chunk in chunker(array=hosts, chunk_size=chunk_size):
            context['host_list'] = chunk
            yield data, context