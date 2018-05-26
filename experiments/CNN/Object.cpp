#include <stdio.h>
#include <string>
#include <vector>
#include <utility>

class Object
{
	public: 
		Object();
		Object(std::vector< std::pair<int, int> > b_box, std::string new_label);
		void set_name(std::string new_label);	
		
		void set_bnd_box(std::vector< std::pair<int, int> > b_box);			// coordinates for the bounding box of the object
											// (Xmin, Ymin, Xmax, Ymax) == (x0, y0, x1, y1)
	private: 
		std::vector< std::pair<int, int> > bounding_box;
		std::string label;	// name of object

};

Object::Object(void)
{
	std::cout << "Empty Object created" << std::endl;
}

Object::Object(std::vector< std::pair<int, int> > b_box, std::string new_label)
{
	label = new_label;
	bounding_box = b_box;

	printf("Object created with values\n");
	printf("Label : %s\n", label.c_str());
	//printf("(Xmin, Ymin) - (Xmax, Ymax) : (%d, %d) - (%d, %d)", bounding_box[0,0], bounding_box[0,1], bounding_box[1,0], bounding_box[1,1]);
	std::cout << "Bounding box : ";
	std::cout << "(" << bounding_box[0].first << ", " << bounding_box[0].second << ")" << ", ";
	std::cout << "(" << bounding_box[1].first << ", " << bounding_box[1].second << ")\n" << std::endl;
	
}

void Object::set_name(std::string new_label)
{
	label = new_label;
}

void Object::set_bnd_box(std::vector< std::pair<int, int> > b_box)
{
	bounding_box = b_box;
}