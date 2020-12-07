from gva.data.flows import BaseOperator


class FakeGetFindingssOperator(BaseOperator):

    def execute(self, data={}, context={}):

        hosts = context.pop('host_list') or  []
        context['number_of_hosts'] = len(hosts)

        return data, context
