#include <string>
#include <fstream>
#include <iostream>

int main() {
	for (int i=0; i<1000; i++)
	{
		//Open a file for writing
		// std::ios::trunc - If the file is opened for output operations and it 
		// already existed, its previous content is deleted and replaced by the new one.
    	std::fstream myInpFile( "fileio.txt", std::ios::out | std::ios::trunc  );
    	//myInpFile.exceptions( std::ios::failbit );   
	
    	myInpFile << "Testline" << std::endl
    		   << "Hello" << std::endl
    	       << "world!" << std::endl;
		myInpFile.close();

		//Open the file for reading
		std::fstream myOutFile( "fileio.txt", std::ios::in);
    	//Position the get position at the beggining and 
    	myOutFile.seekg( 0 );
	
    	//Skip entries untill a character "\n" is reached. Stop skipping aftre 1000 chars
    	myOutFile.ignore( 10000, '\n' );
	
    	//Define a string and then read line by line untill end is reached
    	std::string file_line;
    	while ( std::getline( myOutFile, file_line ) )
    	{
    		// std::cout << file_line << std::endl;
    	}
    	
    	myOutFile.close();
    }
}