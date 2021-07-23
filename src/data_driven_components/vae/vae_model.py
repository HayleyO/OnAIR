import os

import torch
from src.data_driven_components.data_learners import DataLearner
from src.data_driven_components.vae.vae import VAE, TimeseriesDataset
from src.data_driven_components.vae.vae_train import train
from src.data_driven_components.vae.vae_diagnosis import VAEExplainer
from torch.utils.data import DataLoader, Dataset


class VAEModel(DataLearner):

    def __init__(self, headers, window_size, z_units=5, hidden_units=100, 
            path=os.path.join('src','data_driven_components','vae','models','checkpoint_latest.pth.tar')):
        """
        :param headers: (string list) list of headers for each input feature
        :param window_size: (int) number of data points in our data sequence
        :param z_units: (int) dimensions of our latent space gaussian representation
        :param hidden_units: (int) dimension of our hidden_units
        :param path: (string) path of vae save relative to src directory
        """
        self.path = path
        self.headers = headers
        self.window_size = window_size
        self.model = VAE(headers, window_size, z_units, hidden_units)
        self.frames = [[0.0]*len(headers) for i in range(self.window_size)]
        self.explainer = VAEExplainer(self.model, self.headers, len(self.headers), self.window_size)
        self.has_baseline = False


        
    def apriori_training(self, data_train):
        """
        Given data, system should learn any priors necessary for realtime diagnosis.
        :param data_train: (Tensor) shape (batch_size, seq_size, feat_size)
        # TODO: double check sizes
        """
        try:
            self.model.load_state_dict(torch.load(os.path.join(os.environ['SRC_ROOT_PATH'], self.path)))
        except:
            _batch_size = len(data_train[0])
            _input_dim = len(data_train[0][0])

            transform = lambda x: torch.tensor(x).float()
            train_dataset = TimeseriesDataset(data_train, transform)
            train_dataloader = DataLoader(train_dataset, batch_size=_batch_size)

            train(self.model, {'train': train_dataloader}, phases=["train"], checkpoint=True)

        self.explainer.updateModel(self.model)

    def update(self, frame, status):
        """
        :param frame: (list of floats) input sequence of len (input_dim)
        :param status: (int) 0 for red, 1 yellow, 2 green, 3 no data
        :return: None
        """
        if status == 2 and not self.has_baseline:
            self.baseline = frame
            self.has_baseline = True

        self.frames.append(frame)
        self.frames.pop(0)

    ####################################################################################
    # def render_diagnosis(self):
    #     """
    #     System should return its diagnosis, do not run unless model is loaded
    #     """
    #     self.explainer = VAEExplainer(self.model, self.headers, len(self.headers), self.window_size)
    #     transformation = lambda x: torch.Tensor(x).float().unsqueeze(0)

    #     data = transformation(self.frames)
    #     if self.has_baseline:
    #         baseline = transformation(self.baseline)
    #     else:
    #         baseline = torch.zeros_like(data)

    #     self.explainer.shap(data, baseline)
    #     return self.explainer.viz(True)
    def render_diagnosis(self):
        """
        System should return its diagnosis, do not run unless model is loaded
        """

        self.explainer = VAEExplainer(self.model, self.headers, len(self.headers), self.window_size)
        transformation = lambda x: torch.Tensor(x).float().unsqueeze(0)

        data = transformation(self.frames)
        baseline = transformation(self.baseline)

        self.explainer.shap(data, baseline)

        vae_diagnosis = self.explainer.viz(True)
        shap = list(vae_diagnosis[0])
        data_vals = list(vae_diagnosis[1])
        hdrs = list(vae_diagnosis[2])
        ordered_shapleys, ordered_headers = zip(*sorted(zip(shap, hdrs), reverse=True))
        return ordered_headers
    ####################################################################################

