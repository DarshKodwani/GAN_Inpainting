"""
Code taken from https://medium.com/datadriveninvestor/generative-adversarial-network-gan-using-keras-ce1c05cfdfd3
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.layers import Dense, Dropout, Input
from keras.models import Model, Sequential
from keras.datasets import mnist
from tqdm import tqdm
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import Adam

""" First lets make sure we understand the dataset from mnist (commented out for running)"""

#print(np.shape(mnist.load_data()))
(x_train, y_train), (x_test, y_test) = mnist.load_data()
""""
# Type of data
print("Type of x data:", type(x_train))
print("Type of y data:", type(y_train))

# Shape of data 
print("Shape of x shape:", np.shape(x_train))
print("Shape of y shape:", np.shape(y_train))

print("1st element of y:", y_train[0])

for i in range(4) :
    plt.imshow(x_train[i,:,:])
    plt.show()
#quit()
"""
### Masking info ###

def mask(x_ini, x_end, y_ini, y_end) : 
    return np.zeros((abs(x_ini - x_end), abs(y_ini - y_end)))

#Mask params
masking = True
x_ini = 5 ; x_end = 20 ; y_ini = 5; y_end = 20

"""
print(x_train[0,x_ini:x_end, y_ini:y_end])
plt.imshow(x_train[0, :, :])
plt.show()
print(x_train[0, x_ini:x_end, y_ini:y_end])
x_train[0, x_ini:x_end, y_ini:y_end] = mask(x_ini, x_end, y_ini, y_end)
plt.imshow(x_train[0, :, :])
plt.show()

quit()
print(x_train[0,15:20, 15:20]*np.zeros((5,5)))
print(type(x_train[0, 15:20, 15:20]))
print(np.shape(x_train[0, 15:20, 15:20]))
quit()
plt.imshow(x_train[0,:,:])
plt.show()
plt.imshow(x_train_new[0,:,:])
plt.show()
plt.imshow(x_train_new[0,:,:] - x_train[0,:,:])
plt.show()

print(x_train[0,:,:])
print(np.zeros[5,5])
quit()
"""

### Load data ###

def load_data(mask = False) : 
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = (x_train.astype(np.float32) - 127.5)/127.5 # Not sure what this is doing
    if mask == True :
        for i in range(len(x_train[:,0,0])) :
            x_train[i, x_ini:x_end, y_ini:y_end] = mask(x_ini, x_end, y_ini, y_end)
    # convert shape of x_train from (60000, 29, 29) to (60000, 784)
    #784 columns per row
    x_train = x_train.reshape(60000, 784)
    return (x_train, y_train, x_test, y_test)


(X_train, y_train, X_test, y_test) = load_data()

(X_train_mask, y_train_mask, X_test_mask, y_test_mask) = load_data(mask == True)

def adam_optimizer() :
    return Adam(lr = 0.0002, beta_1 = 0.5)

### Generator network ###
"""
def create_generator() : 
    generator = Sequential()
    generator.add(Dense(units = 256, input_dim = 100)) #DK TODO : set input dimension to 784 (i.e masked images)
    generator.add(LeakyReLU(0.2))
    
    generator.add(Dense(units = 512))
    generator.add(LeakyReLU(0.2))
    
    generator.add(Dense(units = 1024))
    generator.add(LeakyReLU(0.2))

    generator.add(Dense(units = 784, activation = 'tanh'))

    generator.compile(loss = 'binary_crossentropy', optimizer = adam_optimizer())
    
    return generator
"""
def create_generator() : 
    generator = Sequential()
    generator.add(Dense(units = 1024, input_dim = 784)) #DK TODO : set input dimension to 784 (i.e masked images)
    generator.add(LeakyReLU(0.2))
    
    generator.add(Dense(units = 2048))
    generator.add(LeakyReLU(0.2))
    
    generator.add(Dense(units = 1024))
    generator.add(LeakyReLU(0.2))

    generator.add(Dense(units = 784, activation = 'tanh'))

    generator.compile(loss = 'binary_crossentropy', optimizer = adam_optimizer())
    
    return generator

g = create_generator()
g.summary()

### Discriminator network ###
def create_discriminator() : 
    discriminator = Sequential()
    discriminator.add(Dense(units = 1024, input_dim = 784))
    discriminator.add(LeakyReLU(0.2))
    discriminator.add(Dropout(0.3))

    discriminator.add(Dense(units = 512))
    discriminator.add(LeakyReLU(0.2))
    discriminator.add(Dropout(0.3))

    discriminator.add(Dense(units = 256))
    discriminator.add(LeakyReLU(0.2))

    discriminator.add(Dense(units = 1, activation = 'sigmoid'))

    discriminator.compile(loss = 'binary_crossentropy', 
                          optimizer = adam_optimizer())

    return discriminator

d = create_discriminator()
d.summary()
                
### Create GAN ###

def create_gan(discriminator, generator) :
    discriminator.trainable = False 
    gan_input = Input(shape = (784,))
    X = generator(gan_input)
    gan_output = discriminator(X)
    gan = Model(inputs = gan_input, outputs = gan_output)
    gan.compile(loss = 'binary_crossentropy', optimizer = 'adam')
    return gan

gan = create_gan(d,g)
gan.summary()

### Plotting generated images from generator network ###

def plot_generated_images(epoch, generator, examples = 100, dim = (10, 10), figsize = (10, 10)) : 
    noise = np.random.normal(loc = 0, scale = 1, size = [examples, 100])
    generated_images = generator.predict(noise)
    generated_images = generated_images.reshape(100, 28, 28)
    plt.figure(figsize = figsize)
    for i in range(generated_images.shape[0]) : 
        plt.subplot(dim[0], dim[1], i+1)
        plt.imshow(generated_images[i], interpolation = 'nearest')
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('gan_generated_image_masked %d.pdf' %epoch)

### Train GAN ###

def training(epochs = 1, batch_size = 128) : 
    
    #Loading data
    (X_train, y_train, X_test, y_test) = load_data()
    (X_train_mask, y_train_mask, X_test_mask, y_test_mask) = load_data(mask == True)
    batch_count = X_train.shape[0] / batch_size 

    # Creating GAN
    generator = create_generator()
    discriminator = create_discriminator()
    gan = create_gan(discriminator, generator)

    for e in range(1, epochs+1) : 
        print("Epoch %d" %e)
        for _ in tqdm(range(batch_size)) : 
            #generate random noise as input to initialize the generator

            noise = X_train_mask[np.random.randint(low = 0, high = X_train.shape[0], size = batch_size)]

            #Generate fake MNIST images from noised input 
            generated_images = generator.predict(noise)
        
            #Get a random set of real images 
            image_batch = X_train[np.random.randint(low = 0, high = X_train.shape[0], size = batch_size)]
            
            #Construct different batches of real and fake data
            X = np.concatenate([image_batch, generated_images])
            
            #Labels for generated and real data 
            y_dis = np.zeros(2*batch_size)
            y_dis[:batch_size] = 0.9

            #Pre train discriminator on fake and real data before starting the gan
            discriminator.trainable = True
            discriminator.train_on_batch(X, y_dis)

            #Tricking the noised input of the Generator as real data
            noise = X_train_mask[np.random.randint(low = 0, high = X_train.shape[0], size = batch_size)]

            y_gen = np.ones(batch_size)
            
            #During the training of gan the weights of discriminator should be fixed. 
            discriminator.trainable = False

            #Training the GAN by alternative the training of Discriminator and training the chained GAN model with Discriminator's weights freezed. 

            gan.train_on_batch(noise, y_gen)
            
        if e == 1 or e % 20 ==0 : 
            plot_generated_images(e, generator)

training(400, 128)
