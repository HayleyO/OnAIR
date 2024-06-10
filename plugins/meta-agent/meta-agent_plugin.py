
from typing import List
from onair.src.ai_components.ai_plugin_abstract.ai_plugin import AIPlugin


class MetaAgentPlugin(AIPlugin):
    def __init__(self, name, headers, centralized:bool=True, fleet:List[(str, str)] = []):
        """
        Parameters
        ----------
        name
            The name as required by the AIPlugin Abstract
        headers 
            The headers as required by the AIPlugin Abstract
        centralized : bool, defaults to True
            A flag for the type of communication (centralized or decentralized)
        fleet : List[(str, str)], defaults to empty
            A list of tuples which represent (IP_Address, Port) for each vehicle in a fleet

        """
        super().__init__(name, headers)
       
        self.centralized = centralized # Centralized or decentralized comm flag 
        # "Address book" of IPs and ports or ways to access other vehicles in fleet network
        self.fleet_address = fleet # List of string tuples (IP_Addres, Port), perhaps there's a better data structure for this

        # Keeping track of meta data for the frame

    def add_vehicle_to_fleet(self, ip_address:str, port:str):
        """Adds a vehicle's ip and port to fleet so it can be accessed.

        Parameters
        ----------
        ip_address : str
            IP of vehicle being added to the fleet
        port : str
            port of vehicle being added to the fleet
        """
        if bool(ip_address.strip()) and bool(port.strip()):
            self.fleet_address.append((ip_address, port))
        else:
            print("ERROR: Make sure your ip address and port aren't empty strings")
            

    def register_topic():
        pass

    def subscribe_to_topic():
        pass

    def broadcast():
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