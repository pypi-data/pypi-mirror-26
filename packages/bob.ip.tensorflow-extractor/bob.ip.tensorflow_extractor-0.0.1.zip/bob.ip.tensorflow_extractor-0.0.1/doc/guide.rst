===========
 User guide
===========

Using as a feature extractor
----------------------------

In this example we'll take pretrained network using MNIST and 

In this example we take the output of the layer `fc7` of the VGG face model as
features.

.. doctest:: tensorflowtest

   >>> import numpy
   >>> import bob.ip.tensorflow_extractor
   >>> import bob.db.mnist
   >>> from bob.ip.tensorflow_extractor import scratch_network
   >>> import os
   >>> import pkg_resources
   >>> import tensorflow as tf

   >>> # Loading some samples from mnist
   >>> db = bob.db.mnist.Database()
   >>> images = db.data(groups='train', labels=[0,1,2,3,4,5,6,7,8,9])[0][0:3]
   >>> images = numpy.reshape(images, (3, 28, 28, 1)) * 0.00390625 # Normalizing the data

   >>> # preparing my inputs
   >>> inputs = tf.placeholder(tf.float32, shape=(None, 28, 28, 1))
   >>> graph = scratch_network(inputs)

   >>> # loading my model and projecting
   >>> filename = os.path.join(pkg_resources.resource_filename("bob.ip.tensorflow_extractor", 'data'), 'model.ckp')
   >>> extractor = bob.ip.tensorflow_extractor.Extractor(filename, inputs, graph)
   >>> extractor(images).shape
   (3, 10)


.. note::

   The models will automatically download to the data folder of this package as
   soon as you start using them.

Using as a convolutional filter
-------------------------------

In this example we plot some outputs of the convolutional layer `conv1`.

.. plot:: plot/convolve.py
   :include-source: False
