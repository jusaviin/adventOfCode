#include <iostream>
#include <fstream>

using namespace std;

/*
 * Advent of code puzzle 3-1
 * Choose the batteries that combine to the highest Joltage
 *
 * Advent of code puzzle 3-2
 * Choose twelve batteries instead of two from each battery bank
 */

/*
 * Find the maximum joltage in the input battery bank
 *
 * Arguments:
 *  string batteryBank = String describing the joltages of batteries that are being combined
 *  int nBatteries = Number of batteries that will be combined to get the joltage
 *
 * Return:
 *  long long maximum joltage value
 */
long long findMaxJoltage(string batteryBank, int nBatteries){

  // First, decode the batteryBank to a vector of ints
  vector<int> allJoltages;
  for(auto joltage : batteryBank){
    allJoltages.push_back(joltage - '0');
  }

  // Find nBatteries batteries that combine for the largest joltage
  vector<int> chosenJoltages;
  int maxJoltage;
  int maxJoltageIndex = -1;
  for(int iBattery = 0; iBattery < nBatteries; iBattery++){
    maxJoltage = 0;

    // Starting from the previous highest joltage, find the hishest joltage such that we can choose the desired amount of batteries
    for(int iJoltage = maxJoltageIndex+1; iJoltage < allJoltages.size() - nBatteries + iBattery + 1; iJoltage++){
      if(allJoltages.at(iJoltage) > maxJoltage){
        maxJoltage = allJoltages.at(iJoltage);
        maxJoltageIndex = iJoltage;
      }
    }

    // Once we have find the highest joltage, add it to the chosen joltages vector
    chosenJoltages.push_back(maxJoltage);
  }

  // Combine all the batteries to produce the total joltage
  long long totalJoltage = 0;
  for(int iBattery = 0; iBattery < nBatteries; iBattery++){
    totalJoltage += pow(10, nBatteries - iBattery - 1) * chosenJoltages.at(iBattery);
  }

  return totalJoltage;

}

/*
 * Read all the lines in the input file to a vector of strings
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<string> of the battery Joltages given in the file
 */
vector<string> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<string> joltages;

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
      joltages.push_back(line);
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return joltages;

}

/*
 * Main program
 */
int main(int argc, char** argv){

  //==== Read arguments =====
  if ( argc<3 ) {
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout<<"+ Usage of the macro: " << endl;
    cout<<"+  "<<argv[0]<<" [puzzleInput] [nBatteries]"<<endl;
    cout<<"+  puzzleInput: Text file containing the puzzle input" <<endl;
    cout<<"+  nBatteries: Number of batteries combined for joltage" <<endl;
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout << endl << endl;
    exit(1);
  }

  // Find the instructions on how to turn the dial from the input file
  vector<string> batteryJoltages = readInputFile(argv[1]);
  int nBatteries = atoi(argv[2]);

  // Loop over all joltages and add the maximum joltage from each line to the total Joltage number
  long long totalJoltage = 0;
  for(string batteryBank : batteryJoltages){
    totalJoltage += findMaxJoltage(batteryBank, nBatteries);
  }

  // Print maximum joltage
  cout << "Total joltage is " << totalJoltage << endl;

}