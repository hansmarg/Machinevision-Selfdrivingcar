import tensorflow as tf
import numpy as np
import cv2 as cv
import datareader


N_ANCHORS = 5
N_CLASSES = 4
GRID_H = 13
GRID_W = 13

SAVE_FILE = "./build/saves"
SAVE_INTERVAL = 1000


## TEMP ##
LAMBDA_COORD = 5.0
LAMBDA_NO_OBJ = 0.5
BATCH_SIZE = 24
LEARNING_RATE = 0.0001
#N_IMAGES = 100000	## burde sjekkes
NUM_ITERS = 100000  ## skal kanskje være (N_IMAGES / BATCH_SIZE)

## TEMP ##
IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH = 416, 416, 3

#x = tf.placeholder(shape = [416, 416, 3], dtype = tf.float32, name = "input_placeholder")
#y = tf.placeholder(shape = [13, 13, N_ANCHORS * (5 + N_CLASSES)], dtype = tf.float32, name = "output_placeholder")

									### KANSKJE UTDATERT ###
							# resize image to 416,416,3 to match CNN input
							#new_size = [416/image.size().width, 416/image.size().height, 3]
									### KANSKJE UTDATERT ###

def neural_network(image, trainit = True):



	# Layer kernel 	stride 	Output_dimensions
	# conv 	3x3		1		(416, 416, 16)
	conv1 = tf.layers.conv2d(
								inputs=image,
								filters=16,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution1"
							)
	conv1 = tf.layers.batch_normalization(conv1, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

	# max	2x2		2		(208, 208, 16)
	max1 = tf.layers.max_pooling2d(
									inputs=conv1,
									pool_size = (2,2),
									strides = 2,
									padding = "valid",
									data_format = "channels_last",
									name = "Maxpool1"
								)

	# conv 	3x3		1		(208, 208, 32)
	conv2 = tf.layers.conv2d(
								inputs=max1,
								filters=32,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution2"
							)
	conv2 = tf.layers.batch_normalization(conv2, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

	# max	2x2		2		(104, 104, 32)
	max2 = tf.layers.max_pooling2d(
									inputs=conv2,
									pool_size = (2,2),
									strides = 2,
									padding="valid",
									data_format="channels_last",
									name="Maxpool2"
								)

	# conv 	3x3		1		(104, 104, 64)
	conv3 = tf.layers.conv2d(
								inputs=max2,
								filters=64,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution3"
							)
	conv3 = tf.layers.batch_normalization(conv3, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

	# max	2x2		2		(52, 52, 64)
	max3 = tf.layers.max_pooling2d(
									inputs=conv3,
									pool_size = (2,2),
									strides = 2,
									padding="valid",
									data_format="channels_last",
									name="Maxpool3"
								)

	# conv 	3x3		1		(52, 52, 128)
	conv4 = tf.layers.conv2d(
								inputs=max3,
								filters=128,
								kernel_size=[3, 3],
								strides=(1, 1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution4"
							)
	conv4 = tf.layers.batch_normalization(conv4, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

	# max	2x2		2		(26, 26, 128)
	max4 = tf.layers.max_pooling2d(
									inputs=conv4,
									pool_size=(2,2),
									strides=2,
									padding="valid",
									data_format="channels_last",
									name="Maxpool4"
								)

	# conv 	3x3		1		(26, 26, 256)
	conv5 = tf.layers.conv2d(
								inputs=max4,
								filters=256,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution5"
							)
	conv5 = tf.layers.batch_normalization(conv5, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

	# max	2x2		2		(13, 13, 256)
	max5 = tf.layers.max_pooling2d(
									inputs=conv5,
									pool_size=(2,2),
									strides=2,
									padding="valid",
									data_format="channels_last",
									name="Maxpool5"
								)

	# conv 	3x3		1		(13, 13, 512)
	conv6 = tf.layers.conv2d(
								inputs=max5,
								filters=512,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution6"
							)
	conv6 = tf.layers.batch_normalization(conv6, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

	# max	2x2		1		(13, 13, 512)
	max6 = tf.layers.max_pooling2d(
									inputs=conv6,
									pool_size=(2,2),
									strides=1,
									padding="same",
									data_format="channels_last",
									name="Maxpool6"
								)

	# conv 	3x3		1		(13, 13, 1024)
	conv7 = tf.layers.conv2d(
								inputs=max6,
								filters=1024,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution7"
							)
	conv7 = tf.layers.batch_normalization(conv7, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)


	# conv 	3x3		1		(13, 13, 1024)
	conv8 = tf.layers.conv2d(
								inputs=conv7,
								filters=1024,
								kernel_size=[3, 3],
								strides=(1,1),
								padding="same",
								activation=tf.nn.relu,
								name="Convolution8"
							)
	conv8 = tf.layers.batch_normalization(conv8, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

							#13, 13, N_ANCHORS * (5 + N_CLASSES)
	# conv 	1x1		1		(13, 13, 45)
	conv9 = tf.layers.conv2d(
								inputs=conv8,
								filters=N_ANCHORS * (5 + N_CLASSES),
								kernel_size=[3, 3],
								padding="same",
								activation=tf.nn.relu,
								name="Convolution9"
							)
	conv9 = tf.layers.batch_normalization(conv9, training=trainit, momentum=0.99, epsilon=0.001, center=True, scale=True)

	output = tf.reshape(conv9, shape=(-1, GRID_H, GRID_W, N_ANCHORS, N_CLASSES + 5), name='output_network')

	return output

# proper loss functions
# pc | logistic regression loss
#
# bx |
# by | squared error
# bh |
# bw |
#
# c1 |
# c2 | log-likelyhood loss
# c3 |


def slice_tensor(x, start, end=None):
	
	if end != None and end < 0:
		y = x[...,start:]
		
	else:
		if end is None:		
			end = start
		y = x[...,start:end + 1]
   
	return y


## Simple loss function
# pc |
# bx |
# by |
# bh |	Squared errors
# bw |
# c1 |
# c2 |
# ci |
def simple_yolo_loss(pred, label, lambda_coord, lambda_no_obj):

	mask = slice_tensor(label, 5)
	label = slice_tensor(label, 0, 4)
	
	mask = tf.cast(tf.reshape(mask, shape=(-1, GRID_H, GRID_W, N_ANCHORS)),tf.bool)
		 
	with tf.name_scope('mask'):
		masked_label = tf.boolean_mask(label, mask)
		masked_pred = tf.boolean_mask(pred, mask)
		neg_masked_pred = tf.boolean_mask(pred, tf.logical_not(mask))

	with tf.name_scope('pred'):
		masked_pred_xy = tf.sigmoid(slice_tensor(masked_pred, 0, 1))
		masked_pred_wh = tf.exp(slice_tensor(masked_pred, 2, 3))
		masked_pred_o = tf.sigmoid(slice_tensor(masked_pred, 4))
		masked_pred_no_o = tf.sigmoid(slice_tensor(neg_masked_pred, 4))
		masked_pred_c = tf.nn.softmax(slice_tensor(masked_pred, 5, -1))
		
	with tf.name_scope('lab'):
		masked_label_xy = slice_tensor(masked_label, 0, 1)
		masked_label_wh = slice_tensor(masked_label, 2, 3)
		masked_label_c = slice_tensor(masked_label, 4)
		masked_label_c_vec = tf.reshape(tf.one_hot(tf.cast(masked_label_c, tf.int32), depth=N_CLASSES), shape=(-1, N_CLASSES))
	
	with tf.name_scope('merge'):
		with tf.name_scope('loss_xy'):
			loss_xy = tf.reduce_sum(tf.square(masked_pred_xy-masked_label_xy))
		with tf.name_scope('loss_wh'):	
			loss_wh = tf.reduce_sum(tf.square(masked_pred_wh-masked_label_wh))
		with tf.name_scope('loss_obj'):
			loss_obj = tf.reduce_sum(tf.square(masked_pred_o - 1))
		with tf.name_scope('loss_no_obj'):
			loss_no_obj = tf.reduce_sum(tf.square(masked_pred_no_o))
		with tf.name_scope('loss_class'):	
			loss_c = tf.reduce_sum(tf.square(masked_pred_c - masked_label_c_vec))
		
		loss = lambda_coord*(loss_xy + loss_wh) + loss_obj + lambda_no_obj*loss_no_obj + loss_c
	
	return loss


def make_batches(batch_size = 24):
	images = []
	labels = []
	path = "../../../dataset/final_set/object-dataset/labels.csv"

	# height and width of each anchor compared to grid cell
	anchors = np.matrix([[0.23640576  , 0.27998272],
                         [0.7750528   , 0.8502528 ],
                         [1.3791072   , 2.2543776 ],
                         [3.27872     , 1.4701696 ],
                         [4.059776    , 3.799712  ]], dtype=np.float64)

    # define grid
	grid = (13, 13)

    # loop through data
	for img, lbl in datareader.csv2data(path, grid, anchors, start_frame=None, scale=0.25):
		images.append(img)
		labels.append(lbl)
	
	return images, labels

def train():

	with tf.name_scope('batch'):
		batch_image, batch_label = make_batches()

	batch_image = tf.train.batch(
									batch_image, 
									batch_size = BATCH_SIZE,
								    num_threads=1,
								    capacity=32,
								    enqueue_many=False,
								    shapes=None,
								    dynamic_pad=False,
								    allow_smaller_final_batch=False,
								    shared_name=None,
								    name=None
								)

	batch_label = tf.train.batch(
									batch_label, 
									batch_size = BATCH_SIZE,
								    num_threads=1,
								    capacity=32,
								    enqueue_many=False,
								    shapes=None,
								    dynamic_pad=False,
								    allow_smaller_final_batch=False,
								    shared_name=None,
								    name=None
								)

	image = tf.placeholder(shape = [None, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH], dtype=tf.float32, name='image_placeholder')
	label = tf.placeholder(shape = [None, GRID_H, GRID_W, N_ANCHORS * (5 + N_CLASSES)], dtype=tf.float32, name='label_palceholder')

	train_flag = tf.placeholder(dtype=tf.bool, name='flag_placeholder')

	with tf.variable_scope('net'):
		y = neural_network(image, train_flag)

	with tf.name_scope('loss'):
		loss = simple_yolo_loss(y, label, LAMBDA_COORD, LAMBDA_NO_OBJ)

	opt = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE)
	print("AdamOptimizer")

	update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
	with tf.control_dependencies(update_ops):
		train_step = opt.minimize(loss)
	
	print("First sess")
	sess = tf.Session()
	sess.run(tf.global_variables_initializer())
	coord = tf.train.Coordinator()
	saver = tf.train.Saver()
	threads = tf.train.start_queue_runners(sess=sess, coord=coord)

	print("starts iters")
	for i in range(NUM_ITERS):
		
		image_data, label_data = sess.run([batch_image, batch_label])

		_, loss_data, data = sess.run([train_step, loss, y], feed_dict={train_flag: True, image: image_data, label: label_data})

		print ('iter: %i, loss: %f' % (i, loss_data))

		if (i+1)%SAVE_INTERVAL == 0:
			make_dir(SAVE_FILE)
			saver.save(sess, os.path.join(SAVE_FILE, 'yolo'), global_step=i+1)

	saver.save(sess, os.path.join(SAVE_FILE,'yolo'), global_step=i+1)

if __name__ == "__main__":



	train()




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
