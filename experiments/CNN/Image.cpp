#include <stdio.h>
#include <string>
#include <vector>

#include "Object.cpp"


// This class contains the image, all related data, and the objects in the image


class Image
{
	public:
		Image();
		Image(	std::string fname, 		// image filename
				int img_size[3], 		// image size
				int coords[2], 			// coordinates of the top left pixel 
				int num_of_objects);	// number of detectable objects in image

		Object object(int i);								// returns the object at index i
		std::vector<Object> get_objects(void);				// returns all objects in the image
		void add_object(std::vector< std::pair<int, int> > b_box, std::string label);	// adds an object to the Image

		void rescale(int resolution[2]);	// Scales the data and objects to match a new resolution. 


	private:
		std::string filename;	
		int image_size[3];		// size of the image (X, Y, C), C = channels
		int top_left_coords[2];	// Top left coordinates (vet ikke om den trengs)
		int number_of_objects;	// total number of objects in the image
		
		std::vector<Object> objects;	// all the objects in the image

};

Image::Image()
{
	std::cout << "Empty Image created" << std::endl;
}

Image::Image(std::string fname, int img_size[3], int coords[2], int num_of_objects)
{
	filename = fname;

	for (int i = 0; i < 3; ++i) image_size[i] = img_size[i];	// fordi arrayA = arrayB funker ikke uten -std=c++11 compiler support. 
	for (int i = 0; i < 2; ++i) top_left_coords[i] = coords[i];	//

	number_of_objects = num_of_objects;
}

Object Image::object(int i)
{
	return objects.at(i);
}

std::vector<Object> Image::get_objects(void)
{
	return objects;
}

void Image::add_object(std::vector< std::pair<int, int> > b_box, std::string new_label)
{
	Object new_object = Object(b_box, new_label);
	objects.push_back(new_object);
}

void Image::rescale(int resolution[2])
{
	std::cout << "Image::rescale PLACEHOLDER function" << std::endl;
}

/*

void Image::set_num_of_obj(int number)
{
	number_of_objects = number;
}

void Image::set_img_size(int size[3])	// X x Y x C
{
	image_size = size;
}

void Image::set_top_left_coords(int coords[2])
{
	top_left_coords = coords;
}
/**/