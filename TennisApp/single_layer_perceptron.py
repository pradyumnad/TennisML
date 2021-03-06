import neurolab as nl
import numpy as np

from data import prepare_data

__author__ = 'pradyumnad'

train, train_target, test, test_target = prepare_data()

print('Train: ', len(train))
print('Test : ', len(test))

input = list(train[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm']].values)
target = list(train_target)
target = [[i] for i in target]

# print input
# print target

# Create net with 3 inputs and 1 neuron
net = nl.net.newp([[0, 1], [0, 1], [0, 1]], 1)
error = net.train(input, target, epochs=140, show=10, lr=0.1)

# Plot results
import pylab as pl

pl.plot(error)
pl.xlabel('Epoch number')
pl.ylabel('Train error')
pl.grid()
pl.show()


# Testing
test_input = list(test[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm']].values)
target = list(test_target)
target = [[i] for i in target]
predictions = net.sim(test_input)
print predictions
print target

diff = predictions - target
err = np.square(diff).sum()
# print('diff', diff)
print('err', err / len(predictions))
