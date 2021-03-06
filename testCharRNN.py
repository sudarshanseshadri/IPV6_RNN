import sys
import random
import numpy as np
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout

inputFile = sys.argv[1]
outputFile = sys.argv[2]

# load up our text
text = open(inputFile, 'r').read()

# extract all (unique) characters
# these are our "categories" or "labels"
chars = list(set(text))

# set a fixed vector size
# so we look at specific windows of characters
addr_len = 5 
max_len = 2*addr_len 

model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(max_len, len(chars))))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

step = 1
inputs = []
outputs = []
for i in range(0, len(text) - max_len, step):
    inputs.append(text[i:i+max_len])
    outputs.append(text[i+max_len])

char_labels = {ch:i for i, ch in enumerate(chars)}
labels_char = {i:ch for i, ch in enumerate(chars)}

# using bool to reduce memory usage
X = np.zeros((len(inputs), max_len, len(chars)), dtype=np.bool)
y = np.zeros((len(inputs), len(chars)), dtype=np.bool)

# set the appropriate indices to 1 in each one-hot vector
for i, example in enumerate(inputs):
    for t, char in enumerate(example):
        X[i, t, char_labels[char]] = 1
    y[i, char_labels[outputs[i]]] = 1

def generate(seed):
    if seed is None or len(seed) < max_len:
        raise Exception('Seed text must be at least {} chars long'.format(max_len))

    # if no seed text is specified, randomly select a chunk of text
    sentence = seed
    generated = '' 
    savedProbs = []
    incorrectMsg = ''
    while len(generated) < 10*max_len: 
        

	# generate the input tensor
        # from the last max_len characters generated so far
        x = np.zeros((1, max_len, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_labels[char]] = 1.

        # this produces a probability distribution over characters
        probs = model.predict(x, verbose=0)[0]
	savedProbs.append(probs)
        # sample the character to use based on the predicted probabilities
        next_idx = np.argmax(probs)
        next_char = labels_char[next_idx]

        generated += next_char
        sentence = sentence[1:] + next_char
    return generated + '\n' + incorrectMsg

epochs = 10
for i in range(epochs):
    epoch_num = 10
    # set nb_epoch to 1 since we're iterating manually
    model.fit(X, y, batch_size=32, nb_epoch=epoch_num, shuffle=False)

    seed = str(inputs[int(random.random() * len(inputs) / max_len) * max_len])
    # preview
    with open(outputFile, 'a') as f:
	f.write('epoch: {}\n'.format(i*epoch_num))
	f.write('seed: {}\n'.format(seed))
	f.write('generated: {}\n'.format(generate(seed)))

for _ in range(20):
    seed = str(inputs[int(random.random() * len(inputs) / max_len) * max_len])
    with open(outputFile, 'a') as f:
	f.write('seed: {}\n'.format(seed))
	f.write('generated: {}\n'.format(generate(seed)))
