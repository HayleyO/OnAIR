
import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR


class ContrastingLoss(nn.Module):
    def __init__(self, margin=10.0):
        super(ContrastingLoss, self).__init__()
        self.margin = margin

    def inverse_weighting(self, anchor, x):
        weight = 1/torch.sqrt(torch.pow(anchor - x, 2))
        weighted_samples =  (weight * x)/torch.sum((weight))
        return weighted_samples

    def forward(self, output_1, output_2, target):
        mean_1 = torch.mean(output_1, dim=1)
        mean_2 = torch.mean(output_2, dim=1)
        #std_1 = torch.std(output_1, dim=1)

        mean_distance = torch.sqrt(torch.pow((mean_1 - mean_2), 2))
        euclidean_distance = nn.functional.pairwise_distance(output_1, output_2)        

        '''if self.margin is not None:
            contrastive_loss = torch.mean((1-target) * torch.pow(torch.clamp(self.margin - mean_distance, min=0.0), 2))
        if self.margin is None or contrastive_loss == 0.0:
            self.margin = int(torch.mean(((2*torch.pi)**(1/2))/torch.sqrt((torch.pow(std_1, 2)))).detach().item())'''

        #loss_contrastive = torch.mean((1 - target) * torch.pow(euclidean_distance, 2) + \
        #       (target)  * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
        loss_contrastive = torch.mean((1 - target)* torch.pow(euclidean_distance, 2) + \
               (target) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
        return loss_contrastive

class Twin(nn.Module):
    def __init__(self, latent_dim = 64, lr=0.1, gamma=0.7, margin=10):
        super(Twin, self).__init__()
        
        self.latent_dim = latent_dim

        # Neural Network Architecture Setup
        self.resnet = torchvision.models.resnet18(weights='DEFAULT') # Resnet model
        self.fc_in_features = self.resnet.fc.in_features
        self.resnet = torch.nn.Sequential(*(list(self.resnet.children())[:-1])) # Remove the last layer of the resnet 

        self.fc = torch.nn.Sequential(
            nn.Linear(self.fc_in_features, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, latent_dim))

        # Hyperparemeters 
        self.lr = lr
        self.gamma = gamma 
        self.margin = margin

    def forward_once(self, x):
        output = self.resnet(x)
        output = output.view(output.size()[0], -1)
        embedding = self.fc(output)
        return embedding
    
    def forward(self, input_1, input_2):
        embedding_1 = self.forward_once(input_1)
        embedding_2 = self.forward_once(input_2)
        return embedding_1, embedding_2
    
    def train_network(self, data_loader, epochs):
        #self.train()
        self.optimizer = optim.Adadelta(self.parameters(), lr=self.lr)
        self.scheduler = StepLR(self.optimizer, step_size=1, gamma=self.gamma)
        criterion = ContrastingLoss(self.margin)
        for epoch in range(1, epochs + 1):
            for batch_idx, (data_1, data_2, target) in enumerate(data_loader):
                self.optimizer.zero_grad()
                embedding_1, embedding_2 = self.forward(data_1, data_2)
                
                loss = criterion(embedding_1, embedding_2, target)
                loss.backward()
                self.optimizer.step()

                if batch_idx % 10 == 0:
                    print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        epoch, batch_idx * len(data_1), len(data_loader.dataset),
                        100. * batch_idx / len(data_loader), loss.item()))
            #self.scheduler.step()