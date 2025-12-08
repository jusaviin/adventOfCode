#include <iostream>
#include <fstream>
#include <sstream>

#include <tuple>

using namespace std;

/*
 * Advent of code puzzle 8-1
 * Make N connections. Multiply together 3 largest circuits
 *
 * Advent of code puzzle 8-2
 * Make shortest connections until everything is in one circuit
 */

/*
 * Read all the lines in the input file to a vector of strings
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<vector<int>> locations of junction boxes
 */
vector<vector<int>> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<vector<int>> junctionBoxes;
  vector<int> thisBox;
  string currentToken;

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
      
      // Find the location of the junction from the line contents
      stringstream junctionTokenizer(line);
      thisBox.clear();
      while(getline(junctionTokenizer, currentToken, ',')){
        thisBox.push_back(atoi(currentToken.c_str()));
      }

      // Once this junction box location is confirmed, add it to list of all boxes
      junctionBoxes.push_back(thisBox);
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return junctionBoxes;

}

/*
 * Main program
 */
int main(int argc, char** argv){

  //==== Read arguments =====
  if ( argc<3 ) {
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout<<"+ Usage of the macro: " << endl;
    cout<<"+  "<<argv[0]<<" [puzzleInput] <nConnections>"<<endl;
    cout<<"+  puzzleInput: Text file containing the puzzle input" <<endl;
    cout<<"+  nConnections: Number of connections made between junction boxes" <<endl;
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout << endl << endl;
    exit(1);
  }

  // Find the instructions on how to turn the dial from the input file
  vector<vector<int>> junctionBoxes = readInputFile(argv[1]);
  int nConnections = atoi(argv[2]);

  // Calculate the distances between the boxes
  vector<tuple<double, int, int>> boxDistances;
  double currentDistance;
  tuple<double, int, int> boxAndDistance;
  for(int iBox = 0; iBox < junctionBoxes.size(); iBox++){
    for(int jBox = iBox+1; jBox < junctionBoxes.size(); jBox++){
      currentDistance = sqrt(pow(junctionBoxes.at(iBox).at(0) - junctionBoxes.at(jBox).at(0), 2) + pow(junctionBoxes.at(iBox).at(1) - junctionBoxes.at(jBox).at(1), 2) + pow(junctionBoxes.at(iBox).at(2) - junctionBoxes.at(jBox).at(2), 2));
      boxAndDistance = make_tuple(currentDistance, iBox, jBox);

      boxDistances.push_back(boxAndDistance);
    }
  }

  // Sort the distances from smallest to largest
  sort(boxDistances.begin(), boxDistances.end());

  // In the beginning there are no connections between the junction boxes
  // Thus every junction box forms it's own circuit
  vector<vector<int>> connectedCircuits;
  vector<int> myCircuit;
  for(int iBox = 0; iBox < junctionBoxes.size(); iBox++){
    myCircuit.clear();
    myCircuit.push_back(iBox);
    connectedCircuits.push_back(myCircuit);
  }

  // Make connections between nConnections closest boxes
  int firstBoxCircuit, secondBoxCircuit;
  int firstBoxID, secondBoxID;
  if(nConnections < 0) nConnections = INT_MAX;
  for(int iConnection = 0; iConnection < nConnections; iConnection++){
    
    // Check if the current shortest connections is in one of the connected circuits
    firstBoxCircuit = -1;
    secondBoxCircuit = -1;
    firstBoxID = get<1>(boxDistances.at(iConnection));
    secondBoxID = get<2>(boxDistances.at(iConnection));
    for(int iCircuit = 0; iCircuit < connectedCircuits.size(); iCircuit++){
      for(int iBox = 0; iBox < connectedCircuits.at(iCircuit).size(); iBox++){
        if(connectedCircuits.at(iCircuit).at(iBox) == firstBoxID){
          firstBoxCircuit = iCircuit;
        }
        if(connectedCircuits.at(iCircuit).at(iBox) == secondBoxID){
          secondBoxCircuit = iCircuit;
        }
      }
    }

    // If the two boxes are in different circuits, connect the circuits
    if (firstBoxCircuit != secondBoxCircuit){
      // If the junction boxes are in different circuits, these are now connected into a single circuit
      myCircuit.clear();
      for(int box : connectedCircuits.at(firstBoxCircuit)){
        myCircuit.push_back(box);
      }
      for(int box : connectedCircuits.at(secondBoxCircuit)){
        myCircuit.push_back(box);
      }
      if(firstBoxCircuit > secondBoxCircuit){
        connectedCircuits.erase(connectedCircuits.begin() + firstBoxCircuit);
        connectedCircuits.erase(connectedCircuits.begin() + secondBoxCircuit);
      } else {
        connectedCircuits.erase(connectedCircuits.begin() + secondBoxCircuit);
        connectedCircuits.erase(connectedCircuits.begin() + firstBoxCircuit);
      }
      connectedCircuits.push_back(myCircuit);
    }

    // Note that there is also a case where both boxes are already in a same circuit.
    // In that case nothing needs to be done, so we do not need explicit check for that

    // If everything is in the same circuit, we can break the loop
    if(connectedCircuits.size() == 1) break;

  }

  // Based in the input, we want to print different output
  if(nConnections == INT_MAX){

    long long firstNumber = junctionBoxes.at(firstBoxID).at(0);
    long long secondNumber = junctionBoxes.at(secondBoxID).at(0);
    long long multiplicationResult = firstNumber * secondNumber;

    cout << "Two last junctions to connect to make a single circuit x-multiply to: " << multiplicationResult << endl;

  } else {

    // Sort the connected circuits based on the size of the circuits
    sort(connectedCircuits.begin(), connectedCircuits.end(), [](const std::vector<int>& a, const std::vector<int>& b) {return a.size() > b.size();});
  
    // Multiply together the sizes of the three largest circuits
    cout << "Three largest circuits multiply to: " << connectedCircuits.at(0).size() * connectedCircuits.at(1).size() * connectedCircuits.at(2).size() << endl; 
  }

}