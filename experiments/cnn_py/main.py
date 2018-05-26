import tensorflow as tf
import numpy as np
import cv2 as cv


def neural_network(image):

	# resize image to 416,416,3 to match CNN input

	#new_size = [416/image.size().width, 416/image.size().height, 3]

	anchors = 5
	classes = 4

	cv.resize(	
				InputArray = image,
				OutputArray = input_layer,
				dsize = [416, 416, 3],
				fx = 0,
				fy = 0,
				interpolation = cv.INTER_AREA 
			)		

	input_layer = np.asarray(input_layer)

	# Layer kernel 	stride 	Output_dimensions
	# conv 	3x3		1		(416, 416, 16)
	conv1 = tf.layers.conv2d(
								inputs=input_layer,
								filters=16,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 1"
							)

	# max	2x2		2		(208, 208, 16)
	max1 = tf.layers.max_pooling2d(
									inputs=conv1,
									pool_size = (2,2),
									strides = 2,
									padding = 'valid',
									data_format = 'channels_last',
									name = "Maxpool 1"
								)

	# conv 	3x3		1		(208, 208, 32)
	conv2 = tf.layers.conv2d(
								inputs=max1,
								filters=32,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 2"
							)

	# max	2x2		2		(104, 104, 32)
	max2 = tf.layers.max_pooling2d(
									inputs=conv2,
									pool_size = (2,2),
									strides = 2,
									padding='valid',
									data_format='channels_last',
									name="Maxpool 2"
								)

	# conv 	3x3		1		(104, 104, 64)
	conv3 = tf.layers.conv2d(
								inputs=max2,
								filters=64,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 3"
							)

	# max	2x2		2		(52, 52, 64)
	max3 = tf.layers.max_pooling2d(
									inputs=conv3,
									pool_size = (2,2),
									strides = 2,
									padding='valid',
									data_format='channels_last',
									name="Maxpool 3"
								)

	# conv 	3x3		1		(52, 52, 128)
	conv4 = tf.layers.conv2d(
								inputs=max3,
								filters=128,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 4"
							)

	# max	2x2		2		(26, 26, 128)
	max4 = tf.layers.max_pooling2d(
									inputs=conv4,
									pool_size=(2,2),
									strides=2,
									padding='valid',
									data_format='channels_last',
									name="Maxpool 4"
								)

	# conv 	3x3		1		(26, 26, 256)
	conv5 = tf.layers.conv2d(
								inputs=max4,
								filters=256,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 5"
							)

	# max	2x2		2		(13, 13, 256)
	max5 = tf.layers.max_pooling2d(
									inputs=conv5,
									pool_size=(2,2),
									strides=2,
									padding='valid',
									data_format='channels_last',
									name="Maxpool 5"
								)
	# conv 	3x3		1		(13, 13, 512)
	conv6 = tf.layers.conv2d(
								inputs=max5,
								filters=512,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 6"
							)

	# max	2x2		1		(13, 13, 512)
	max6 = tf.layers.max_pooling2d(
									inputs=conv6,
									pool_size=(2,2),
									strides=2,
									padding='valid',
									data_format='channels_last',
									name="Maxpool 6"
								)

	# conv 	3x3		1		(13, 13, 1024)
	conv7 = tf.layers.conv2d(
								inputs=max6,
								filters=1024,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 7"
							)

	# conv 	3x3		1		(13, 13, 1024)
	conv8 = tf.layers.conv2d(
								inputs=conv7,
								filters=1024,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 8"
							)

							#13, 13, anchors * (5 + classes)
	# conv 	1x1		1		(13, 13, 125)
	conv9 = tf.layers.conv2d(
								inputs=conv8,
								filters=anchors * (5 + classes),
								kernel_size=[3, 3],
								padding="same",
								activation=tf.nn.relu,
								name="Convolution 9"
							)

	return conv9


'''
	// Layer	Kernel	Stride 	output.shape
	
	// input				(416, 416, 3)
	
	# conv 	3x3		1		(416, 416, 16)
	# max	2x2		2		(208, 208, 16)

	# conv 	3x3		1		(208, 208, 32)
	# max	2x2		2		(104, 104, 32)

	# conv 	3x3		1		(104, 104, 64)
	# max	2x2		2		(52, 52, 64)

	# conv 	3x3		1		(52, 52, 128)
	# max	2x2		2		(26, 26, 128)

	# conv 	3x3		1		(26, 26, 256)
	# max	2x2		2		(13, 13, 256)

	# conv 	3x3		1		(13, 13, 512)
	# max	2x2		1		(13, 13, 512)

	# conv 	3x3		1		(13, 13, 1024)
	# conv 	3x3		1		(13, 13, 1024)

	# conv 	1x1		1		(13, 13, 125)
'''

if __name__ == "__main__":
	pass