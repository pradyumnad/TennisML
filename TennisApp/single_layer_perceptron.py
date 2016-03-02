__author__ = 'pradyumnad'

import neurolab as nl
import pandas
import numpy as np

df1 = pandas.read_csv("data/us_open_final.csv")
df2 = pandas.read_csv("data/au_open_final.csv")

frames = [
    df1[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm', 'Won']],
    df2[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm', 'Won']]
]

df = pandas.concat(frames)

N = len(df[1:])

# tennis_data = df[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm', 'Won']]
print("Total Data : ", N)
split = int(N * 0.6)

train = df.sample(n=split)
train_target = train['Won']
test = df.drop(train.index)
test_target = test['Won']

print('Train: ', len(train))
print('Test : ', len(test))

input = list(train[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm']].values)
target = list(train_target)
target = [[i] for i in target]

# print input
# print target

# Create net with 3 inputs and 1 neuron
net = nl.net.newp([[0, 1], [0, 1], [0, 1]], 1)
error = net.train(input, target, epochs=100, show=10, lr=0.1)

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
