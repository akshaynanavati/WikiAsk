import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
from pprint import pprint


class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()
result = nlp.parse("David was a real man. He was the manliest man. He could climb at least 6 buildings. But only if he wanted to.")
pprint(result)

from nltk.tree import Tree
tree = Tree.parse(result['sentences'][0]['parsetree'])
pprint(tree)
print result['sentences'][0].keys()
print result['coref']
print type(result['coref'])
