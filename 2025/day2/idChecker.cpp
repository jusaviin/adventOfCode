#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

/*
 * Advent of code puzzle 2-1
 * Check if numbers consist of two repeating parts (like 11221122)
 *
 * Advent of code puzzle 2-2
 * Check if numbers consist of two or more repeating parts
 */

/*
 * Find ID numbers that are fake from the given number range
 */
void findFakeNumbers(vector<long long>& fakeIdNumbers, string numberRange){

  // Determine first and last number in the range from the string
  vector<string> bothRanges;
  string currentToken;

  stringstream rangeTokenizer(numberRange);
  while(getline(rangeTokenizer, currentToken, '-')){
    bothRanges.push_back(currentToken);
  }

  long long firstNumber = atoll(bothRanges.at(0).c_str());
  long long lastNumber = atoll(bothRanges.at(1).c_str());

  // Based on the larger of the numbers, determine the the maximum length of a pattern that might be repeating for these numbers
  string stringifiedNumber = to_string(lastNumber);
  int numberLength = stringifiedNumber.size();
  int maxPatternLength = numberLength / 2;

  // In outer loop, loop over all possible pattern sizes. 
  // Inner loop is over all the relevant numbers. Skip those we know cannot contain repeating patterns of specific size
  vector<long long> patternPieces;

  // We need to try to find all possible patterns of the defined pattern length
  // Also we must avoid double counting patterns like 1111, which could have period of 1 or 2
  for(int patternLength = 1; patternLength <= maxPatternLength; patternLength++){
    for(long long iNumber = firstNumber; iNumber <= lastNumber; iNumber++){

      stringifiedNumber = to_string(iNumber);
      numberLength = stringifiedNumber.size();

      // Check if you can divide the current number to the current pattern length
      if(numberLength % patternLength != 0){

        // If we cannot divide with the pattern length, advance the iNumber counter to a place which has one more number
        iNumber = 9;
        for(int iLength = 1; iLength < numberLength; iLength++){
          iNumber += 9 * pow(10,iLength);
        }
      
      } else {

        // Divide the number in pieces where each piece has a length of patternLength
        patternPieces.clear();
        for(int iPattern = 0; iPattern < numberLength / patternLength; iPattern++){
          patternPieces.push_back(atoll(stringifiedNumber.substr(iPattern*patternLength, patternLength).c_str()));
        } // Loop over patterns

        // If all the pattern pieces are the same, this is a fake ID!
        // Exception: if there is only one number, nothing can repeat
        // Add it to the fake ID vector if it is already not there
        if(patternPieces.size() > 1){ 
          if(count(patternPieces.begin(), patternPieces.end(), patternPieces.at(0)) == patternPieces.size()){
            if(find(fakeIdNumbers.begin(), fakeIdNumbers.end(), iNumber) == fakeIdNumbers.end()){
              fakeIdNumbers.push_back(iNumber);
            }
          } 
        }

        // Here it is possible to optimize the running time by directly jumping to next fake ID number
        // However, for the purposes of solving this problem, it is not necessary

      } // Check that the number can be divided by the pattern length

    } // Loop over numbers

  } // Loop over pattern lengths

}

/*
 * Read the first line from the file. It contains the ID range that needs to be checked
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   string of the ID numbers that need to be checked given in the file
 */
string readInputFile(string inputFileName){

  // Define variables that will be filled
  string idNumbers;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Read the first line
    getline(file_stream, idNumbers);
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return idNumbers;

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
  string idNumbersRanges = readInputFile(argv[1]);

  // Tokenize the ID number ranges with spaces
  vector<string> allRanges;
  string currentToken;

  stringstream idNumberTokenizer(idNumbersRanges);
  while(getline(idNumberTokenizer, currentToken, ',')){
    allRanges.push_back(currentToken);
  }

  // For each range, find all fake ID numbers and add them to the vector
  vector<long long> fakeIdNumbers;
  for(string currentRange : allRanges){
    findFakeNumbers(fakeIdNumbers, currentRange);
  }

  // Calculate the checksum from the fake ID numbers
  long long checkSum = 0;
  for(long long fakeID : fakeIdNumbers){
    checkSum += fakeID;
  }

  // Check that things work
  cout << "Checksum for fake IDs is: " << checkSum << endl;

}