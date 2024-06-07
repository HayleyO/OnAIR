
from onair.src.ai_components.ai_plugin_abstract.ai_plugin import AIPlugin


class MetaAgentPlugin(AIPlugin):
    def __init__(self, name, headers):
        super().__init__(name, headers)

        # Centralized or decentralized comm flag

        # "Address book" of IPs or alternative ways to access other vehicles in network



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