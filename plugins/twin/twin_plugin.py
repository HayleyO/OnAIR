import os
import re
import cv2
import torch
import pickle
import numpy as np
from classes.TwinNetwork import Twin
from onair.src.ai_components.ai_plugin_abstract.ai_plugin import AIPlugin

class Plugin(AIPlugin):
    def __init__(self, name, headers):
        super().__init__(name, headers)
        self.twin_model = self.load_trained_twin_network(path="models", name="twin_batch_32_margin_2")
        self.knn_model = self.load_trained_resoner(path="models", name="knn_n_5.pkl")
        self.image_sizes = (500,250) # I set this because my personal computer couldn't handle the full image size training
        self.current_camera_data = None

    def load_trained_twin_network(self, path, name):
        full_path = os.path.join(os.path.dirname(__file__), path, name)
        model = Twin(latent_dim=25, lr=0.1, margin=0.2)
        model.load_state_dict(torch.load(full_path))
        return model

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
        # Currently, using a KNN model to predict 'Typical' or 'Atypical', 'Atypical' is Moon for now. 
        
        if self.current_camera_data != "-":
            image = cv2.resize(self.current_camera_data, dsize=self.image_sizes)
            embed = self.twin_model.forward_once(image.unsqueeze(0))
            prediction = self.knn_model.predict(embed)
            if prediction == 'Atypical':
                return 'camera'
        return None
