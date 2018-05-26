import tensorflow as tf
import numpy as np
import cv2 as cv

import csv


# Autti format [frame, xmin, ymin, xmax, ymax, occluded, label, attributes (Only appears on traffic lights)]

# tensor format [pc, bx, by, bh, bw, c1, c2, c3 ,c4]
									#c1 = car
									#c2 = truck
									#c3 = pedestrian
									#c4 = street lights



def make_Autti_dset(autti_labels = "../../dataset/final_set/object-dataset/labels.csv", outputfile = "./build/tensor_rdy.csv"):


# Autti format [frame, xmin, ymin, xmax, ymax, occluded, label, attributes (Only appears on traffic lights)]
# tensor format [pc, bx, by, bh, bw, c1, c2, c3 ,c4]

	with open(autti_labels, 'r') as csvfile:
		autti_format = csv.reader(csvfile, delimiter=' ', quotechar='|')

		for row in autti_format:
			print (', '.join(row))

	print(autti_format)


if __name__ == "__main__":
	make_Autti_dset()
