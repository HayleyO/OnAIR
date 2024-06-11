import time
from meta_agent_plugin import MetaAgent

def response(data):
    global meta_agent
    print(data)
    meta_agent.publish_to_topic('Ping', "Pong") 
    

if __name__ == '__main__':
    host = 'localhost'
    port = 12345
    fleet = {'Agent1': (host, 65432), 'Agent2':(host, port)}
    topics = {'Ping': [('Agent1', None), ('Agent2', response)]}
    meta_agent = MetaAgent("Agent2", port=port, fleet=fleet, topic_dictionary=topics, ip_address=host)

    while True:
        time.sleep(0.1)