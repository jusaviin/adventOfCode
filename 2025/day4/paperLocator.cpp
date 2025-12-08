#include <iostream>
#include <fstream>

using namespace std;

/*
 * Advent of code puzzle 4-1
 * Find places from the map that contain less than 4 adjacent paper rolls
 *
 * Advent of code puzzle 4-2
 * Remove all paper rolls the forklift has an access to
 */

/*
 * Print the current warehouse map
 */
void printMap(vector<string> warehouseMap){

  for(auto mapLine : warehouseMap){
      cout << mapLine << endl;
  }

}

/*
 * Print the current warehouse map
 */
void printMap(vector<vector<char>> warehouseMap){

  for(auto mapLine : warehouseMap){
    for(auto mapChar : mapLine){
      cout << mapChar;
    }
    cout << endl;
  }

}

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
    cout<<"+  "<<argv[0]<<" [puzzleInput]"<<endl;
    cout<<"+  puzzleInput: Text file containing the puzzle input" <<endl;
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout << endl << endl;
    exit(1);
  }

  // Find the instructions on how to turn the dial from the input file
  vector<string> forkliftMap = readInputFile(argv[1]);

  int nColumns = forkliftMap.at(0).size() + 2;

  // Extend the forklift map by adding a padding of '.' characters to the map
  // Also transform it to vector of chars such that it can more easily be modified
  vector<vector<char>> paddedForkliftMap;
  vector<char> topBottomLine;
  for(int iColumn = 0; iColumn < nColumns; iColumn++){
    topBottomLine.push_back('.');
  }
  paddedForkliftMap.push_back(topBottomLine);

  vector<char> lineContent;
  for(string mapLine : forkliftMap){
    lineContent.clear();
    lineContent.push_back('.');
    for(char location : mapLine){
      lineContent.push_back(location);
    }
    lineContent.push_back('.');
    paddedForkliftMap.push_back(lineContent);
  }
  paddedForkliftMap.push_back(topBottomLine);

  //printMap(paddedForkliftMap);

  // Get the dimensions from the padded map
  int nRows = paddedForkliftMap.size();
  
  int nAdjacentRolls = 0;
  int removedRollsBefore = 0;
  int removedRollsAfter = 0;

  // Go through all locations in the map, and check adjacent locations for paper rolls '@'
  // Keep getting paper rolls until it is not possible anymore
  do{
    removedRollsBefore = removedRollsAfter;
    for(int iRow = 1; iRow < nRows-1; iRow++){
      for(int iColumn = 1; iColumn < nColumns-1; iColumn++){
        nAdjacentRolls = 0;
        if(paddedForkliftMap.at(iRow).at(iColumn) == '@'){
          if(paddedForkliftMap.at(iRow-1).at(iColumn) == '@'){
            nAdjacentRolls++;
          }
          if(paddedForkliftMap.at(iRow-1).at(iColumn-1) == '@'){
            nAdjacentRolls++;
          }
          if(paddedForkliftMap.at(iRow-1).at(iColumn+1) == '@'){
            nAdjacentRolls++;
          }
          if(paddedForkliftMap.at(iRow).at(iColumn-1) == '@'){
            nAdjacentRolls++;
          }
          if(paddedForkliftMap.at(iRow).at(iColumn+1) == '@'){
            nAdjacentRolls++;
          }
          if(paddedForkliftMap.at(iRow+1).at(iColumn-1) == '@'){
            nAdjacentRolls++;
          }
          if(paddedForkliftMap.at(iRow+1).at(iColumn) == '@'){
            nAdjacentRolls++;
          }
          if(paddedForkliftMap.at(iRow+1).at(iColumn+1) == '@'){
            nAdjacentRolls++;
          }

          if(nAdjacentRolls < 4) {
            removedRollsAfter++;
            paddedForkliftMap.at(iRow).at(iColumn) = '.';
          }

        } // Checking adjacent locations

      } // Loop over columns
    } // Loop over rows
  } while (removedRollsAfter > removedRollsBefore);

  // Print the number of possible locations
  cout << "Forklift can remove " << removedRollsAfter << " rolls from the warehouse" << endl;

}