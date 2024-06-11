import socket
from meta_agent_plugin import MetaAgent

def response(data):
    print(data)

if __name__ == '__main__':
    fleet = {'Agent1': (socket.gethostname(),12345), 'Agent2':(socket.gethostname(),12346)}
    topics = {'Ping': [('Agent1', response), ('Agent2', None)]}
    meta_agent = MetaAgent("Agent1", port=12345, fleet=fleet, topic_dictionary=topics)

    meta_agent.publish_to_topic('Ping', "Ping")