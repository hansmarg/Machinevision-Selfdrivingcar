Introduction
============

The project will be the data-collecting part of an autonomous driving
car. The program will analyze a dashcam video and will contain the
following:

-   Street detection

    -   road segmentation

    -   lane slope detection

-   Object detection

    -   other cars

    -   signs

    -   pedestrians

-   Calculate distance

-   Calculate relative speed

-   3D mapping of the world

Plan
====

Street Detection
----------------

### Segmentation

First we would down sample and filter the image, by using the
appropriate the appropriate filters like: Laplace, Gaussian, or
Difference of Gaussian.

Then we would experiment with different segmentation algorithms to
highlight the road.

### Lane detection

Use the Sobel filter to highlight lines in the picture and then run
RANSAC to find the lane lines.

Object Detection
----------------

Train a neural network to recognize cars using the training data
available from open source machine learning training databases. If this
works out, then we would train the network to recognize pedestrians and
street signs.

Calculate Distance
------------------

We can use the width of the lane lines (closest to the car) as a
constant to calculate distance since they are mostly parallel.

Calculate Relative Speed
------------------------

```
relative_velocity = (new_estimated_object_distance - old_estimated_object_distance) / time
```
Given time we will experiment with using histogram of gradients to
calculate the velocity.

3D reconstruction
-----------------

Use most of the information we gain to reconstruct a very simple 3d
figure of the environment. Like the one shown in the picture.

Questions
=========

-   Do you have a database for better a trainingset than ours?

-   Any suggestions of how we would use the histogram of gradients to
    calculate the relative speed?
