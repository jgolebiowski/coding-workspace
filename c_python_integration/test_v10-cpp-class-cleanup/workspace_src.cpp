#include <iostream>
#include <iomanip>
#include <string>
#include <memory>
#include <Eigen/Dense>

#include <typeinfo>

extern "C"
{

void hello_world(){
    std::cout<< "Hello world!" << std::endl;
    std::string day = "What a beautiful day!";
    std::cout << day << std::endl;
    }





int main()
{
	hello_world();

	int nAtoms(10);
	std::vector< std::vector<int> > neighbourList;
	neighbourList.resize(nAtoms);

	for (int i = 0; i < nAtoms; i++)
	{
		neighbourList.at(i).resize(i, -1);
	}

	for (unsigned int i=0; i < neighbourList.size(); ++i)
	{
		for (unsigned int j=0; j < neighbourList.at(i).size(); ++j)
		{
			std::cout << neighbourList[i][j] << " ";
		}
		std::cout << std::endl;
	}
    	

}


//End of extern C
}