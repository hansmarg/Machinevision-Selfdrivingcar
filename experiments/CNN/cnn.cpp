#include <stdio.h>

#include <iostream>
#include <fstream>

#include <sstream>

#include <string>
#include <vector>
#include <algorithm>

#include <tensorflow/c/c_api.h>

#include "Image.cpp"	//class to contain the image, all related data and objects

//#include <opencv2/opencv.hpp>

std::vector<int> extract_integers(std::string line)
{
	std::vector<int> ret;
	std::stringstream ss;    
	/* Storing the whole string into string stream */
	ss << line;
	/* Running loop till the end of the stream */
	std::string temp;
	int found;

	while (!ss.eof()) {
		/* extracting word by word from stream */
		ss >> temp;

		// FORAT SHITTY HOTFIX THAT FIXED THE PROBLEM 
		if(temp[0] == '('){
			temp[0] = ' ';
		}
 
		/* Checking the given word is integer or not */
		if (std::stringstream(temp) >> found)
		{
			ret.push_back(found);
		}
 
		/* To save from space at the end of string */
		temp = "";
	}

	return ret;
}

std::string get_object_label(std::string line)
{
	int label_start = line.find(":"); int whatever = 255;
	std::string temp = line;
	std::string label;

	
	for (int i = label_start; i < temp.length(); ++i)
	{
		if (!isalpha(temp[i])) {
			temp[i] = ' ';
		}
	}

	label = temp.substr(label_start, whatever);
	label.erase(remove_if(label.begin(), label.end(), isspace), label.end());	

	return label;
}

Image get_image(std::string filename)
{
	Image new_image;

	std::cout << std::endl << "Reading file from: " << filename << std::endl << std::endl;

	std::string line;
	std::ifstream readFile;

	std::vector<int> image_size;	// image data
	std::vector<int> top_left;		//

	std::string object_label;						// object data
	std::vector< std::pair<int,int> > bounding_box;	// (Xmin, Ymin), (Xmax, Ymax)

	std::vector<int> temp_vect;


	readFile.open(filename.c_str());

	if(readFile.is_open()) 						//
	{											//	Reads data from image.txt file, and creates the objects
		while (std::getline(readFile, line))	//
		{

			if (line.find("Image size") != std::string::npos) {

				image_size = extract_integers(line);

			} else if (line.find("Top left") != std::string::npos) {

				top_left = extract_integers(line);

			} else if (line.find("Original label for object") != std::string::npos) {

				object_label = get_object_label(line);

			} else if (line.find("Bounding box") != std::string::npos) {

				temp_vect = extract_integers(line);

				bounding_box.push_back(std::pair<int, int>(temp_vect[1], temp_vect[2]));
				bounding_box.push_back(std::pair<int, int>(temp_vect[3], temp_vect[4]));

				new_image.add_object(bounding_box, object_label);

				object_label = "EMPTY_PLACEHOLDER!";	// Should never have an object with this name
				bounding_box.clear();					// Clear object data

			} else {

				continue;
			}
		}

	} else {

		std::cout << "Shit... File "+filename+" did not open" << std::endl;
	}
	return new_image;
}


int main(int argc, char const *argv[])
{

	//std::string img_annot_src = "~/Machinevision---Self-driving-car/dataset/pascal/VOC2005_1/Annotations/Caltech_cars/";
	std::string img_annot_src = "../../../dataset/pascal/VOC2005_1/Annotations/Caltech_cars/";

	Image testers = get_image(img_annot_src+"image_0001.txt");

	// Layer	Kernel	Stride 	output.shape
	
	// input					(416, 416, 3)
	
	// conv 	3x3		1		(416, 416, 16)
	// max		2x2		2		(208, 208, 16)

	// conv 	3x3		1		(208, 208, 32)
	// max		2x2		2		(104, 104, 32)

	// conv 	3x3		1		(104, 104, 64)
	// max		2x2		2		(52, 52, 64)

	// conv 	3x3		1		(52, 52, 128)
	// max		2x2		2		(26, 26, 128)

	// conv 	3x3		1		(26, 26, 256)
	// max		2x2		2		(13, 13, 256)

	// conv 	3x3		1		(13, 13, 512)
	// max		2x2		1		(13, 13, 512)

	// conv 	3x3		1		(13, 13, 1024)
	// conv 	3x3		1		(13, 13, 1024)

	// conv 	1x1		1		(13, 13, 125)


	return 0;
}










/*

/**/

