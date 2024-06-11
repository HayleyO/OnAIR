import time
from meta_agent_plugin import MetaAgent

def response(data):
    print(data)

if __name__ == '__main__':
    host = 'localhost'
    port = 65432
    fleet = {'Agent1': (host,port), 'Agent2':(host, 12345)}
    topics = {'Ping': [('Agent1', response), ('Agent2', None)]}
    meta_agent = MetaAgent("Agent1", port=port, fleet=fleet, topic_dictionary=topics, ip_address=host)

    meta_agent.publish_to_topic('Ping', "Ping")

    while True:
        time.sleep(0.1)