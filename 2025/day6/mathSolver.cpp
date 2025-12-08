#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

/*
 * Advent of code puzzle 6-1
 * Solve a sheet of math problems
 *
 * Advent of code puzzle 6-2
 * Solve the sheet encrypted with cephalopod cypher
 */

/*
 * Solve a math problem given in a string vector
 */
long long solveProblem(vector<string> problem){

  // The last index in the string tells whether this is a multiplication or addition problem
  long long result;
  if(problem.back() == "*"){
    result = 1;
    for(int iNumber = 0; iNumber < problem.size() - 1; iNumber++){
      result *= atoi(problem.at(iNumber).c_str());
    }
  } else if(problem.back() == "+"){
    result = 0;
    for(int iNumber = 0; iNumber < problem.size() - 1; iNumber++){
      result += atoi(problem.at(iNumber).c_str());
    }
  } else {
    cout << "ERROR! Unknown operator!" << endl;
    cout << "Cannot solve the problem!" << endl;
    return 0;
  }

  // Return the result of the math problem
  return result;
}

/*
 * Decode the information in the input file from cepholopod cypher
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<vector<string>> of the homework problems
 */
vector<vector<string>> readInputFileCepholopodStyle(string inputFileName){

  // Define variables that will be filled
  vector<vector<string>> homeWork;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  vector<string> fileContents;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);

      // Skip empty lines
      if(line == "") continue;

      fileContents.push_back(line);
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  // The separator columns are given by + and * signs. Separetors are one left from these signs
  vector<int> separatorColumns;
  for(int iColumn = 1; iColumn < fileContents.back().size(); iColumn++){
    if(fileContents.back()[iColumn] == '+' || fileContents.back()[iColumn] == '*'){
      separatorColumns.push_back(iColumn-1);
    }
  }

  // Once we know which columns separate the problems, we can decode the cepholopod cypher
  vector<string> decodedProblem;
  vector<char> numberPieces;
  string mathOperator;
  bool firstColumn = true;
  for(int iColumn = 0; iColumn < fileContents.back().size(); iColumn++){

    // If we are in a separator column, add the problem to homework and more to next problem
    if(find(separatorColumns.begin(), separatorColumns.end(), iColumn) != separatorColumns.end()){
      decodedProblem.push_back(mathOperator);
      homeWork.push_back(decodedProblem);
      decodedProblem.clear();
      firstColumn = true;
      continue;
    }

    // If we are in the first column of a problem, read the math operator for this problem
    if(firstColumn){
      mathOperator = fileContents.back()[iColumn];
    }

    // Read the pieces used to construct the number
    numberPieces.clear();
    for(int iRow = 0; iRow < fileContents.size()-1; iRow++){
      numberPieces.push_back(fileContents.at(iRow)[iColumn]);
    }

    // Create a string from the vector of chars
    string currentNumber(numberPieces.begin(), numberPieces.end());

    // Add the number to the decoded problem
    decodedProblem.push_back(currentNumber);

    // We are not in the first column of a problem anymore
    firstColumn = false;

    // If we are at the last index, at this point we need to add the decoded problem to homework
    if(iColumn == fileContents.back().size() - 1){
      decodedProblem.push_back(mathOperator);
      homeWork.push_back(decodedProblem);
    }

  }


  return homeWork;

}

/*
 * Read all the lines in the input file to a vector of vectors of strings
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<vector<string>> of the homework problems
 */
vector<vector<string>> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<vector<string>> homeWork;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  string currentToken;
  vector<string> tokenVector;
  int vectorIndex;
  bool firstLoop = true;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);

      // Skip empty lines
      if(line == "") continue;

      vectorIndex = 0;
      istringstream homeWorkTokenizer(line);
      while(homeWorkTokenizer >> currentToken){

        // Different behavior if we need to create vectors for output or not
        if(firstLoop){
          // If we are in first loop, we need to create vectors to add to the homeWork
          tokenVector.clear();
          tokenVector.push_back(currentToken);
          homeWork.push_back(tokenVector);
        } else {
          // If we are not in the first loop, there is already vector to which we can push
          homeWork.at(vectorIndex++).push_back(currentToken);
        }
      }

      firstLoop = false;
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return homeWork;

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
  vector<vector<string>> homeWorkProblems = readInputFileCepholopodStyle(argv[1]);

  // Print what we see:
  /*for(auto problem : homeWorkProblems){
    for(auto problemPiece : problem){
      cout << problemPiece << " ";
    }
    cout << endl;
  }*/

  // Check that the output is reasonable
  long long checkSum = 0;
  for(auto problem : homeWorkProblems){
    checkSum += solveProblem(problem);
  }

  // Print the checkSum to concole
  cout << "Homework checksum is " << checkSum << endl;

}