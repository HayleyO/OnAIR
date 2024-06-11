import time
from meta_agent_plugin import MetaAgent

def response(data):
    print(data)

if __name__ == '__main__':
    host = 'localhost'
    port = 65432
    fleet = {'Agent1': (host,port), 'Agent2':(host, 12345)} # Requires knowing the ip of agents in fleet and their ports
    topics = {'Ping': [('Agent1', response), ('Agent2', None)]} # There must be a better way to setup the topic dictionary
    meta_agent = MetaAgent("Agent1", port=port, fleet=fleet, topic_dictionary=topics, ip_address=host)

    meta_agent.publish_to_topic('Ping', "Ping")

    while True:
        time.sleep(0.1)