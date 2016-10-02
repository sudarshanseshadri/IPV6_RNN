### modified from http://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/
# Load LSTM network and generate text
# import os    
# os.environ['THEANO_FLAGS'] = "floatX=float32,device=gpu"
# import theano

import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import copy

# Obtain the corpus of character sequence to train from.
input_file = 'IPV6Addresses.txt'
with open(input_file, 'r') as f:
    addresses = f.readlines()
addresses = map(lambda s: s.strip(), addresses)
raw_text = ''.join(addresses)

# create mapping of unique chars to integers, and a reverse mapping
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print "Total Characters: ", n_chars
print "Total Vocab: ", n_vocab

# prepare the dataset of input to output pairs encoded as integers
seq_length = 256
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 32):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])

n_patterns = len(dataX)
print "Total Patterns: ", n_patterns
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(X, y, nb_epoch=5, batch_size=256)

# generate characters
pattern = copy.copy(dataX[0])
print "Seed:"
print "\"", ''.join([int_to_char[value] for value in pattern]), "\""
for i in range(X.shape[1]):
    if i % 32 == 0:
        print '\n'

    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]
    sys.stdout.write(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]

print "\nDone."