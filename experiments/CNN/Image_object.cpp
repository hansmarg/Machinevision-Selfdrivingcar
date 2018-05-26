#include <stdio.h>
#include <string>
#include <vector>

#include "Object.cpp"


class Image_object
{
	public:
		Image_object();
		Object::Object object(int i);
		std::vector<Object*> objects();


	private:
		std::string filename;
		std::int image_size[3];
		std::int top_left_coords[2];
		std::int number_of_objects;
		
		std::vector<Object*> objects;

}
Image_object::Image_object()
{
	std::cout << "Image_object created" << std::endl;
}

Image_object::object(int i)
{
	return objects[i];
}

std::vector<Object*> Image_object::objects(void)
{
	return objects;
}

void Image_object::set_num_of_obj(int number)
{
	number_of_objects = number;
}

void Image_object::set_img_size(int size[3])	// X x Y x C
{
	image_size = size;
}

void Image_object::set_top_left_coords(int coords[2])
{
	top_left_coords = coords;
}

void add_object(int coords[4])
{

}