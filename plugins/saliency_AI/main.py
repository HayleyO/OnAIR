
import numpy as np
from onair.src.ai_components.ai_plugin_abstract.ai_plugin import AIPlugin

class Plugin(AIPlugin):
    def __init__(self, name, headers):
        """
        :param headers: (int) length of time agent examines
        :param window_size: (int) size of time window to examine
        """
        super().__init__(name, headers)
        self.frames = []
        self.component_name = name
        self.headers = headers

    #### START: Classes mandated by plugin architecture
    def update(self, frame):
        """
        :param frame: (list of floats) input sequence of len (input_dim)
        :return: None
        """
        pass

    def render_reasoning(self):
        """
        System should return its diagnosis
        """
        pass
    #### END: Classes mandated by plugin architecture
