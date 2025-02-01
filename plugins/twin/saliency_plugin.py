import os
import re
import pickle
import numpy as np
from onair.src.ai_components.ai_plugin_abstract.ai_plugin import AIPlugin

class Plugin(AIPlugin):
    def __init__(self, name, headers):
        super().__init__(name, headers)
        self.svm_model = self.load_trained_resoner(path="models", name="svm_model.pkl")
        self.pca_model = self.load_trained_resoner(path="models", name="pca_model.pkl")
        self.current_camera_data = None

    def load_trained_resoner(self, path, name):
        full_path = os.path.join(os.path.dirname(__file__), path, name)
        with open(full_path, 'rb') as f:
            model = pickle.load(f)
        return model
    
    def update(self, low_level_data=[], high_level_data={}):
        data_keys = [header.partition(".")[2] for header in self.headers]

        self.knowledge = dict(zip(data_keys, low_level_data))
        
        self.current_camera_data = self.knowledge['camera']

    def render_reasoning(self):
        # Currently, use an SVM on embedded data to predict 'Typical' or 'Atypical'
        # TODO: Get actual degree of saliency rather than just 'Atypical event' 
        if self.current_camera_data != "-" and len(np.array(self.current_camera_data).shape) == 2:
            embed = self.pca_model.transform(self.current_camera_data)
            prediction = self.svm_model.predict(embed)
            if prediction == 'Atypical':
                return 'camera'
        return None
