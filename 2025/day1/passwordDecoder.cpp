#include <iostream>
#include <fstream>

#include "Dial.h"

using namespace std;

/*
 * Advent of code puzzle 1-1
 * Count the number of times dial stops at 0
 *
 * Advent of code puzzle 1-2
 * Count the number of times dial hits zero at any time during rotation
 */

/*
 * Read all the lines in the input file to a vector of strings
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<string> of the instructions given in the file
 */
vector<string> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<string> instructions;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);

      // Skip empty lines
      if(line == "") continue;
      
      // Create the map of the maze
      instructions.push_back(line);
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return instructions;

}

/*
 * Main program
 */
int main(int argc, char** argv){

  //==== Read arguments =====
  if ( argc<2 ) {
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout<<"+ Usage of the macro: " << endl;
    cout<<"+  "<<argv[0]<<" [puzzleInput] <dialMin> <dialMax> <dialStart>"<<endl;
    cout<<"+  puzzleInput: Text file containing the puzzle input" <<endl;
    cout<<"+  dialMin: Minimum value in the dial. Default = 0" <<endl;
    cout<<"+  dialMax: Minimum value in dial. Default = 99" <<endl;
    cout<<"+  dialStart: Starting number for the dial. Default = 50" <<endl;
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout << endl << endl;
    exit(1);
  }

  // Find the instructions on how to turn the dial from the input file
  vector<string> dialInstructions = readInputFile(argv[1]);

  // Determine the values in the dial
  const int dialMin = argc >= 3 ? atoi(argv[2]) : 0;
  const int dialMax = argc >= 4 ? atoi(argv[3]) : 99;
  int dialValue = argc >= 5 ? atoi(argv[4]) : 50;

  // Create a dial object to take care of the dial value
  Dial* safeDial = new Dial(dialMin, dialMax, dialValue);

  // Turn the dial according to instructions and record the times it hits 0
  int zeroValues = 0;
  int zeroClicks = 0;
  for(auto instruction : dialInstructions){
  	zeroClicks += safeDial->TurnDial(instruction);
  	dialValue = safeDial->GetDialValue();
  	if(dialValue == 0) zeroValues++;
  }
  cout << "Zero value is obtained " << zeroValues << " times" << endl;
  cout << "Zero values is clicked " << zeroClicks << " times" << endl;

}