# -*- coding: utf-8 -*-
"""D23CSA004_DLOps_Assignment1_Q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TBgg2OS6B1JQoozFpHwslnCZfwMkIfhD
"""

from google.colab import drive
drive.mount('/content/drive')

"""An image in L*a*b* colorspace to the image in RGB
colorspace,
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter

# Define CAE architecture
class CAE(nn.Module):
    def __init__(self):
        super(CAE, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2)
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(3),
            nn.ReLU()
        )

    def forward(self, x):
        # Encoder forward pass
        x = self.encoder(x)
        # Decoder forward pass
        x = self.decoder(x)
        return x

# Custom dataset class
class CustomDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data = datasets.ImageFolder(root=data_path, transform=transform)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# Define transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Define data loaders
train_data = CustomDataset(data_path='/content/drive/MyDrive/hymenoptera_data', transform=transform)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

# Initialize CAE model
model = CAE()

# Define optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# Initialize Tensorboard writer
writer = SummaryWriter()

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    for images, _ in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, images)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)

    epoch_loss = running_loss / len(train_data)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}")
    writer.add_scalar('Loss/train', epoch_loss, epoch)

# Save the model
torch.save(model.state_dict(), 'cae_model.pth')

# After training, visualize some input-output pairs
model.eval()
with torch.no_grad():
    for images, _ in train_loader:
        reconstructions = model(images)
        for i in range(4):  # Visualize first 4 images
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.title('Original')
            plt.imshow(images[i].permute(1, 2, 0))
            plt.axis('off')
            plt.subplot(1, 2, 2)
            plt.title('Reconstructed')
            plt.imshow(reconstructions[i].permute(1, 2, 0))
            plt.axis('off')
            plt.show()
        break  # Only visualize one batch

# Close Tensorboard writer
writer.close()

"""RGB image to negative image,"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter

# Define CAE architecture
class CAE(nn.Module):
    def __init__(self):
        super(CAE, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2)
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(3),
            nn.ReLU()
        )

    def forward(self, x):
        # Encoder forward pass
        x = self.encoder(x)
        # Decoder forward pass
        x = self.decoder(x)
        return x

# Custom dataset class
class CustomDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data = datasets.ImageFolder(root=data_path, transform=transform)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# Define transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Define data loaders
train_data = CustomDataset(data_path='/content/drive/MyDrive/hymenoptera_data', transform=transform)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

# Initialize CAE model
model = CAE()

# Define optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# Initialize Tensorboard writer
writer = SummaryWriter()

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    for images, _ in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        # Generate negative of the original images
        neg_images = 1 - images
        loss = criterion(outputs, neg_images)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)

    epoch_loss = running_loss / len(train_data)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}")
    writer.add_scalar('Loss/train', epoch_loss, epoch)

# Save the model
torch.save(model.state_dict(), 'cae_negative_model.pth')

# After training, visualize some input-output pairs
model.eval()
with torch.no_grad():
    for images, _ in train_loader:
        reconstructions = model(images)
        neg_images = 1 - images
        for i in range(4):  # Visualize first 4 images
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.title('Original')
            plt.imshow(images[i].permute(1, 2, 0))
            plt.axis('off')
            plt.subplot(1, 2, 2)
            plt.title('Negative')
            plt.imshow(neg_images[i].permute(1, 2, 0))  # Display the generated negative images
            plt.axis('off')
            plt.show()
        break  # Only visualize one batch

# Close Tensorboard writer
writer.close()

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt

# Define CAE architecture
class CAE(nn.Module):
    def __init__(self):
        super(CAE, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2)
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(3),
            nn.ReLU()
        )

    def forward(self, x):
        # Encoder forward pass
        x = self.encoder(x)
        # Decoder forward pass
        x = self.decoder(x)
        return x

# Custom dataset class
class CustomDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data = datasets.ImageFolder(root=data_path, transform=transform)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx][0]  # Returning only the image, not the label

# Define transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Load the dataset
data_path = "/content/drive/MyDrive/hymenoptera_data"
train_dataset = CustomDataset(data_path, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Initialize CAE model
model = CAE()

# Define optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# Initialize Tensorboard writer
writer = SummaryWriter()

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    for images in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        # Flip images horizontally and calculate loss
        flipped_images = torch.flip(outputs, dims=[3])
        loss = criterion(outputs, flipped_images)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}")
    writer.add_scalar('Loss/train', epoch_loss, epoch)

# Save the model
torch.save(model.state_dict(), 'cae_horizontal_flipped_model.pth')

# After training, visualize some input-output pairs
model.eval()
with torch.no_grad():
    for images in train_loader:
        reconstructions = model(images)
        flipped_images = torch.flip(reconstructions, dims=[3])
        for i in range(4):  # Visualize first 4 images
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 3, 1)
            plt.title('Original')
            plt.imshow(images[i].permute(1, 2, 0))
            plt.axis('off')

            plt.subplot(1, 3, 2)
            plt.title('Output')
            plt.imshow(reconstructions[i].permute(1, 2, 0))
            plt.axis('off')

            plt.subplot(1, 3, 3)
            plt.title('Horizontal Flipped')
            plt.imshow(flipped_images[i].permute(1, 2, 0))
            plt.axis('off')

            plt.show()
        break  # Only visualize one batch

# Close Tensorboard writer
writer.close()