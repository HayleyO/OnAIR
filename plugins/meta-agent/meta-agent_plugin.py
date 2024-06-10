from typing import Dict
from onair.src.ai_components.ai_plugin_abstract.ai_plugin import AIPlugin


class MetaAgentPlugin(AIPlugin):
    def __init__(self, name, headers, centralized:bool=True, fleet:Dict[str, (str, str)] = {}):
        """
        Parameters
        ----------
        name
            The name as required by the AIPlugin Abstract
        headers 
            The headers as required by the AIPlugin Abstract
        centralized : bool, defaults to True
            A flag for the type of communication (centralized or decentralized)
        fleet : Dict[str, (str, str)], defaults to empty
            A dictionary with a vehicle name that maps to a tuple with the vehicle IP address and port: (IP_address, Port)

        """
        super().__init__(name, headers)
       
        self.centralized = centralized # Centralized or decentralized comm flag 
        # "Address book" of IPs and ports or ways to access other vehicles in fleet network
        ## Note: The vehicle name in the dictionary is a way of uniquely describing the vehicle (even if they're on the same IP on sim)
        self.fleet_address_book = fleet # A dictionary with a vehicle name that maps to a tuple with the vehicle IP address and port: (IP_address, Port)
        self.topic_address_book = {} # Empty dictionary to be filled with topics to send and recieve information

        # Keeping track of meta data for the frame

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
        else:
            print("ERROR: Make sure your vehicle name, ip address, and port aren't empty strings")
            
    def broadcast(self, message):
        """Send message to every vehicle in fleet

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

    def register_topic(self, ):
        pass

    def subscribe_to_topic():
        pass



    def update(self,low_level_data=[], high_level_data={}):
        """
        Given streamed data point, system should update internally
        """
        pass

    def render_reasoning(self):
        """
        System should return its diagnosis, etc.
        """
        pass