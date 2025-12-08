#include <iostream>
#include <fstream>
#include <sstream>
#include <tuple>

using namespace std;

/*
 * Advent of code puzzle 5-1
 * Find out which ingradients are spoiled
 *
 * Advent of code puzzle 5-2
 * Find the total number of fresh ingredients
 */

/*
 * Find the fresh and availble ingredients from the input file
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   List of fresh ingredients, and list of available ingredients
 */
tuple<vector<pair<long long, long long>>, vector<long long>> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<pair<long long, long long>> freshIngredients;
  vector<long long> availableIngredients;
  bool freshPart = true;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);
      
      // If we find an empty line, that marks the change from fresh ingredients to available ingredients
      if(line.compare("") == 0) {
        freshPart = false;
        continue;
      }

      // Determine if we are in the fresh or available ingredient part
      if(freshPart){
        // If we are in the fresh ingredient part, tokenize the string into a pair of numbers

        vector<string> bothRanges;
        string currentToken;

        stringstream rangeTokenizer(line);
        while(getline(rangeTokenizer, currentToken, '-')){
          bothRanges.push_back(currentToken);
        }

        freshIngredients.push_back(make_pair(atoll(bothRanges.at(0).c_str()), atoll(bothRanges.at(1).c_str())));

      } else {
        // If we are reading available ingredients, just add them to the vector
        availableIngredients.push_back(atoll(line.c_str()));
      }
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return make_tuple(freshIngredients, availableIngredients);

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

  // Find fresh and available ingredients from the input file
  vector<pair<long long, long long>> freshIngredients;
  vector<long long> availableIngredients;
  tie(freshIngredients, availableIngredients) = readInputFile(argv[1]);

  // Count the number of fresh ingredients from available ingredients
  int nFreshIngredients = 0;
  for(auto ingredient : availableIngredients){
    for(auto freshRange : freshIngredients){
      if(ingredient >= freshRange.first && ingredient <= freshRange.second){
        nFreshIngredients++;
        break;
      }
    }
  }

  // Print the result
  cout << "The list contains " << nFreshIngredients << " fresh ingredients that are available" << endl;

  // Merge the overlapping ranges in the fresh ingredients vector

  // Start by sorting the vector
  sort(freshIngredients.begin(), freshIngredients.end());

  // Helper variables
  vector<pair<long long, long long>> compactFreshIngredients;
  pair<long long, long long> mergedIngredient;
  pair<long long, long long> comparedIngredient;
  long long lowIngredient;
  long long highIngredient;
  bool previousRangesOverlap = false;

  // Go through adjacent pairs in the fresh ingredients vector and merge overlapping ranges
  for(int iIngredient = 0; iIngredient < freshIngredients.size()-1; iIngredient++){

    // First, we need to determine what is the basis of comparison
    // We can either compare to previously merged range, or to a direct value from vector
    if(previousRangesOverlap){
      // If the previous compared ranges overlap, we should check the next range with respect to merged ingredient range
      comparedIngredient = mergedIngredient;
    } else {
      // If the previous compared ranges do not overlap, we should check the next range with respect to value from the vector
      comparedIngredient = freshIngredients.at(iIngredient);
    }

    // Check if the ranges overlap
    if(comparedIngredient.second < freshIngredients.at(iIngredient+1).first){
      // If the ranges do not overlap, we can add the ingredient to the compacted vector
      compactFreshIngredients.push_back(comparedIngredient);
      previousRangesOverlap = false;

      // If we are in the last index, we need to add also the last range to compacted vector
      if(iIngredient == freshIngredients.size()-2){
        compactFreshIngredients.push_back(freshIngredients.at(iIngredient+1));
      }

    } else {
      // If the ranges overlap, we should merge the ranges and not add anything to compacted vector
      lowIngredient = comparedIngredient.first;
      highIngredient = comparedIngredient.second;
      if(freshIngredients.at(iIngredient+1).second > highIngredient){
        highIngredient = freshIngredients.at(iIngredient+1).second;
      }
      mergedIngredient = make_pair(lowIngredient, highIngredient);
      previousRangesOverlap = true;

      // If we are in the last index, we need to add the merged ingredient to compacted vector
      if(iIngredient == freshIngredients.size()-2){
        compactFreshIngredients.push_back(mergedIngredient);
      }
    }

  } // Loop over all fresh ingredient ranges

  // Print the compacted vector
  //for(auto ingredient : compactFreshIngredients){
  //  cout << ingredient.first << "-" << ingredient.second << endl;
  //}

  // Now that we have all the overlapping ranges fixed, we can directly count the number of ingredients from the compacted vector
  long long allFreshIngredients = 0;
  for(auto ingredient : compactFreshIngredients){
    allFreshIngredients += ingredient.second - ingredient.first + 1;
  }

  // Print the number of fresh ingredients
  cout << "There is a grand total of " << allFreshIngredients << " fresh ingredients" << endl;

}