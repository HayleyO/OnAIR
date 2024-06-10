import socket
import asyncio
from typing import Dict, Callable
# Maybe later integrate as complex reasoning? Not sure where to put this "meta-agent"
# from onair.src.reasoning.complex_reasoning_interface import ComplexReasoningInterface

# TODO:
# 1. Topics initialized with topic stabalizing broadcast message
# 2. Test an Agent 1, Agent 2 back and forth messaging system
# 3. What does decentralized or across networks look like? 
# 4. Finish up 

class MetaAgent():
    def __init__(self, vehicle_name:str, fleet:Dict[str, (str, str)] = {}):
        """
        Parameters
        ----------
        vehicle_name : str
            Unique ID or name for vehicle for reference
        fleet : Dict[str, (str, str)], defaults to empty
            A dictionary with a vehicle name that maps to a tuple with the vehicle IP address and port: [vehicle_name] -> (IP_address, Port)

        """
        # Note: The vehicle name is a way of uniquely describing the vehicle (to allow multiple vehicles on the same IP like through sim)
        ## This may not be needed and can probably be worked around but keeping it in for now? 
        self.vehicle_name = vehicle_name # A unique identifier for a vehicle

        # Server sockets for listening - used in address fleet book 
        ## Each meta-agent onboard an agent should have a server with a UNIQUE ip_address, port combination (either port or IP needs to be identifying)
        ### TODO: Intelligently get (IP, Port) - ex: if all the fleets have the same IP then the ports all need to be unique
        self.server_socket = socket.socket()            # Create socket object for server socket #socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = socket.gethostname(), 12345        # Set host IP address and port
        self.server_socket.bind((host, port))           # Bind that IP and port to the server socket

        # "Address book" of IPs and ports or ways to access server sockets of other vehicles in fleet network
        ## The idea is that you know the vehicles in your fleet ahead of time and that is initalized in the code -- either manually typed in or through a config of some type
        self.fleet_address_book = fleet
        
        self.topic_dictionary = {} # Empty dictionary to be filled with topics to send and recieve information

        # Keeping track of meta data for the frame?
        asyncio.run(self.listen())

    def add_vehicle_to_fleet(self, vehicle_name:str, ip_address:str, port:str):
        """Adds a vehicle's ip and port to fleet so it can be accessed.

        Parameters
        ----------
        vehicle_name : str
            Unique ID or name for vehicle to be reference even if the vehicle is on the same IP and port as other vehicles (like in sim)
        ip_address : str
            IP of vehicle being added to the fleet
        port : str
            port of vehicle being added to the fleet
        """
        if bool(vehicle_name.strip()) and bool(ip_address.strip()) and bool(port.strip()):
            self.fleet_address_book[vehicle_name] = (ip_address, port)
            # TODO: Ping for address book update broadcast
        else:
            print("ERROR: Make sure your vehicle name, ip address, and port aren't empty strings")
            

    def broadcast(self, message):
        """Send/publish message to every vehicle in fleet

        Parameters
        ----------
        message 
            Message to be sent
        """
        for vehicle in self.fleet_address_book:
            ip_address = self.fleet_address_book[vehicle][0]
            port = self.fleet_address_book[vehicle][1]

            # TODO: Implement server connection and send messages
            pass

    async def listen(self):
        ''' Listen indefinitely on a seperate thread for new information
        '''
        disconnect_message = "disconnect"
        self.server_socket.listen(5) # Set server to listen
        # Listen indefinitely 
        while True:
            connection, client_addr = self.server_socket.accept()     
            connected = True
            while connected:
                msg_length = connection.recv(64).decode('UTF-8') # Assume the header is of length 64 and the format is UTF-8
                if msg_length:
                    msg_length = int(msg_length)
                    msg = connection.recv(msg_length).decode('UTF-8')
                    self.on_recieve(msg)
                    if msg == disconnect_message:
                        connected = False
                    print(f"[{client_addr}] {msg}")
                #connection.send("Msg received".encode(FORMAT))
            # Close the connection with the client 
            connection.close()
   
    async def on_recieve(self, data):
        # Check if message is from self, ignore if it is
        # Check if from a subscribed to topic, if yes run callback async 
        # Check if it's a topic dictionary update broadcast message
        # Check if it's an address book topic update broadcast message
        pass

    def register_topic(self, topic_name:str):
        # Broadcast new topic information to every agent in fleet, allowing for the shared, onboard lists of topics to update
        pass

    def publish_to_topic(self, ):
        pass

    def subscribe_to_topic(self, topic_name:str, callback:Callable):
        # Add agent to topic dictionary, broadcast topic dictionary updates
        # Add agent callback method to topic dictionary
        pass
