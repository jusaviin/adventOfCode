#include <iostream>
#include <fstream>

using namespace std;

/*
 * Advent of code puzzle 7-1
 * Count the number of times tachyon beam splits
 *
 * Advent of code puzzle 7-2
 * Count how many individual paths the beam can take
 */

/*
 * Print the current lab map
 */
void printMap(vector<vector<char>> labMap){

  for(auto mapLine : labMap){
    for(auto mapChar : mapLine){
      cout << mapChar;
    }
    cout << endl;
  }

}

/*
 * Print the current multiplicity map
 */
void printMap(vector<vector<int>> multiplicityMap){

  for(auto mapLine : multiplicityMap){
    for(auto mapChar : mapLine){
      cout << mapChar;
    }
    cout << endl;
  }

}

/*
 * Find the beam starting position.
 *
 *  Arguments: 
 *   vector<vector<char>> labMap = Map of the lab
 *
 *  Return:
 *   pair<int,int> with x and y coordinates of the beam.
 */
pair<int,int> findBeamStart(vector<vector<char>> warehouseMap){

  for(size_t yCoordinate = 0; yCoordinate < warehouseMap.size(); yCoordinate++){
    for(size_t xCoordinate = 0; xCoordinate < warehouseMap.at(yCoordinate).size(); xCoordinate++){
      if(warehouseMap.at(yCoordinate).at(xCoordinate) == 'S'){
        return make_pair(xCoordinate, yCoordinate);
      }
    }
  }

  // Return non-sensical value if we cannot find the robot
  return make_pair(-1,-1);

}

/*
 * Count the number of paths the beam can take from the current location until the bottom of the map
 * Recursive implementation is neat, but not viable for large maps
 * Much more efficient implementation is presented in the main program
 */
int countTimeLines(vector<vector<char>> labMap, int iRow, int iColumn){

  // If we are in the last row, this is the only remaining path.
  if(iRow == labMap.size()-1){
    return 1;
  }

  // If we are not in the last row, check what is in the map in the direction of the beam
  char nextLocation = labMap.at(iRow+1).at(iColumn);

  // Check if there is a splitter in the path of the beam
  if(nextLocation == '^'){
    // If we hit a splitter, return the combined timelines of both paths taken
    return countTimeLines(labMap, iRow+1, iColumn+1) + countTimeLines(labMap, iRow+1, iColumn-1);
  } else {
    // If there is no splitter, we continue in the same timeline
    return countTimeLines(labMap, iRow+1, iColumn);
  }

}

/*
 * Read all the lines in the input file to a vector of strings
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<vector<char>> of the tachyon beam splitter lab map
 */
vector<vector<char>> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<vector<char>> labMap;
  vector<char> charredLine;

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

      // Make a char vector out of string
      charredLine.clear();
      for(char location : line){
        charredLine.push_back(location);
      }
      
      // Create the map of the maze
      labMap.push_back(charredLine);
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return labMap;

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
  vector<vector<char>> labMap = readInputFile(argv[1]);
  vector<vector<long long>> beamMultiplicity;

  // Initialize the beam multiplicity to 0
  vector<long long> rowMultiplicity;
  for(auto mapRow : labMap){
    rowMultiplicity.clear();
    for(auto location : mapRow){
      rowMultiplicity.push_back(0);
    }
    beamMultiplicity.push_back(rowMultiplicity);
  }

  // The beam multiplicity is 1 in the original location of the beam
  pair<int,int> beamStart = findBeamStart(labMap);
  beamMultiplicity.at(beamStart.second).at(beamStart.first) = 1;

  // Go through the map line by line and advance the beam
  int nSplits = 0;
  for(int iRow = 1; iRow < labMap.size(); iRow++){
    for(int iColumn = 0; iColumn < labMap.at(iRow).size(); iColumn++){

      // The beam moves from up to down. Check if in the previous row there is a beam to move.
      if(labMap.at(iRow-1).at(iColumn) == 'S'){

        // Check if there is a beam splitter or not in this location
        if(labMap.at(iRow).at(iColumn) == '^'){
          // Splitter splits the beam
          labMap.at(iRow).at(iColumn-1) = 'S';
          labMap.at(iRow).at(iColumn+1) = 'S';
          // Increase the beam multiplicity in these locations
          beamMultiplicity.at(iRow).at(iColumn-1) += beamMultiplicity.at(iRow-1).at(iColumn);
          beamMultiplicity.at(iRow).at(iColumn+1) += beamMultiplicity.at(iRow-1).at(iColumn);
          nSplits++;
        } else {
          // If there is no splitter, the beam moves straight
          labMap.at(iRow).at(iColumn) = 'S';
          // Increase the beam multiplicity in the new location
          beamMultiplicity.at(iRow).at(iColumn) += beamMultiplicity.at(iRow-1).at(iColumn);
        }

      } // Check if there is beam

    } // Loop over columns
  } // Loop over rows

  // We can get the number of timelines by adding the beam multiplicities in the last row
  long long nTimeLines = 0;
  for(int iLocation = 0; iLocation < beamMultiplicity.back().size(); iLocation++){
    nTimeLines += beamMultiplicity.back().at(iLocation);
  }

  // Print the number of splits
  cout << "The beam splits " << nSplits << " times" << endl;
  cout << "Tachyon particles have " << nTimeLines << " different timelines" << endl;

}