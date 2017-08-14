import torch
from torchvision import datasets, transforms
import torch.autograd as autograd
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import argparse

from torch import nn

parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
parser.add_argument('--batch-size', type=int, default=128, metavar='N',
                    help='input batch size for training (default: 64)')
parser.add_argument('--epochs', type=int, default=10, metavar='N',
                    help='number of epochs to train (default: 2)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='enables CUDA training')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='how many batches to wait before logging training status')
args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

class AE(nn.Module):
	def __init__(self):
		super(AE, self).__init__()

		self.fc1 = nn.Linear(784, 400)
		self.fc21 = nn.Linear(400, 20)
		self.fc3 = nn.Linear(20, 400)
		self.fc4 = nn.Linear(400, 784)

		self.relu = nn.ReLU()
		self.sigmoid = nn.Sigmoid()

	def encode(self, x):
		h1 = self.relu(self.fc1(x))
		return self.fc21(h1)

	def decode(self, z):
		h3 = self.relu(self.fc3(z))
		return self.sigmoid(self.fc4(h3))

	def forward(self, x):
		h1 = self.encode(x.view(-1, 784))
		return self.decode(h1)


reconstruction_function = nn.BCELoss()
reconstruction_function.size_average = False

def loss_function(recon_x, x):
	BCE = reconstruction_function(recon_x, x)
	return BCE


model = AE()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

batch_size = 256
train_loader = torch.utils.data.DataLoader(datasets.MNIST('data/', train=True, download=True,
											 transform=transforms.ToTensor()),
										     batch_size=batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(datasets.MNIST('data/', train=False, transform=transforms.ToTensor()),
    										batch_size=1000)


def train(epoch):
	model.train()
	train_loss = 0
	for batch_idx, (data, _) in enumerate(train_loader):
		data = data.view(-1, 784)
		data = np.absolute(np.fft.fft(data.numpy()))
		data = Variable(torch.FloatTensor(data))
		print data[0].view(784,-1)
		break

		optimizer.zero_grad()
		output = model(data)
		loss = loss_function(output, data)
		loss.backward()
		train_loss += loss.data[0]
		optimizer.step()
		if batch_idx % args.log_interval == 0:
			print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
			epoch, batch_idx * len(data), len(train_loader.dataset),
			100. * batch_idx / len(train_loader),
			loss.data[0] / len(data)))

	print('====> Epoch: {} Average loss: {:.4f}'.format(
	      epoch, train_loss / len(train_loader.dataset)))
	

def test(epoch):
	model.eval()
	test_loss = 0
	for data, _ in test_loader:
		data = Variable(data, volatile=True)
		output = model(data)
		test_loss += loss_function(output, data).data[0]

	test_loss /= len(test_loader.dataset)
	print('====> Test set loss: {:.4f}'.format(test_loss))


for epoch in range(20):
    train(epoch)
    break
    test(epoch)