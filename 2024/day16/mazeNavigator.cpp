#include <iostream>
#include <fstream>
#include <tuple>
#include <ranges>

using namespace std;

/*
 * Advent of code puzzle 16-1
 * Find the shortest path through the maze
 *
 * Advent of code puzzle 16-2
 * Find the amount of locations among all possible shortests paths through the maze
 */

// Define turn map as a global variable such that updates are easily accessible everywhere
vector<vector<int>> turnMap[4];

/*
 * Print the current maze map
 */
void printMap(vector<string> mazeMap){

  for(auto mapLine : mazeMap){
      cout << mapLine << endl;
  }

}

/*
 * Print the charred maze map
 */
void printCharredMap(vector<vector<char>> mazeMap){

  for(auto mapLine : mazeMap){
    for(auto mapChar : mapLine){
      cout << mapChar;
    }
    cout << endl;
  }

}

/*
 * Print the path taken by a reindeer
 *
 *  Arguments:
 *   vector<string> mazeMap = Map of the maze
 *   vector<pair<pair<int,int>,pair<int,int>>> reindeerPath = Path taken by the reindeer
 */
void printPath(vector<string> mazeMap, vector<pair<pair<int,int>,pair<int,int>>> reindeerPath){
 
  // To help printing the path, make transform map into double vector of chars
  vector<vector<char>> charredMap;
  for(auto mapLine : mazeMap){
  	vector<char> charLine;
  	for(char location : mapLine){
  		charLine.push_back(location);
  	}
  	charredMap.push_back(charLine);
  }

  // Use the reindeer path to show which path the reindeer took
  pair<int,int> location, direction;
  char mapUpdate;
  for(auto entry : reindeerPath){

  	// Get the location and direction of the reindeer from the reindeer path
    location = entry.first;
    direction = entry.second;

    // Find which character should be added to the map
    if(direction == make_pair(1,0)){
    	mapUpdate = '>';
    } else if(direction == make_pair(-1, 0)){
    	mapUpdate = '<';
    } else if (direction == make_pair(0, 1)){
    	mapUpdate = 'v';
    } else {
    	mapUpdate = '^';
    }

    // Update the charred map with the path sign
    charredMap.at(location.second).at(location.first) = mapUpdate;

  }

  // Print the map with the path the reindeer took
  printCharredMap(charredMap);

}

/*
 * Calculate path score for a specific path
 * Path score is calculated as 1 for each movement and 1000 for each turn
 *
 *  Arguments:
 *   vector<pair<pair<int,int>,pair<int,int>>> reindeerPath = The path the reindeer took inside the maze
 *
 *  Return:
 *   Path score for this path calculated as described above
 */
int findPathScore(vector<pair<pair<int,int>,pair<int,int>>> reindeerPath){
  
  // Find the number of turns for this path
  int nTurns = 0;
  pair<int,int> previousDirection, currentDirection;
  for(size_t timeStep = 1; timeStep < reindeerPath.size(); timeStep++){
    previousDirection = reindeerPath.at(timeStep-1).second;
    currentDirection = reindeerPath.at(timeStep).second;
    if(previousDirection != currentDirection) nTurns++;
  }

  // Return the path score
  return reindeerPath.size() - 1 + nTurns * 1000;

}

/*
 * Find all possible paths through a maze
 *
 *  Arguments:
 *   vector<string> mazeMap = Map of the maze
 *   vector<pair<pair<int,int>,pair<int,int>>> reindeerPath = The path taken by the reindeer thus far
 *   int nTurns = Number of turns in the current path
 *
 *  Return:
 *   vector<vector<pair<pair<int,int>,pair<int,int>>>> that has all possible paths through the maze
 */
vector<vector<pair<pair<int,int>,pair<int,int>>>> solveMaze(vector<string> mazeMap, vector<pair<pair<int,int>,pair<int,int>>> reindeerPath, int nTurns){

	// Optimization: keep updating each location of the map with the number of turns it takes to get there
	// If reaching a point with larger number of turns, kill the path

	// Define all possible paths that will be returned in the end
	vector<vector<pair<pair<int,int>,pair<int,int>>>> allPossiblePaths;
	vector<vector<pair<pair<int,int>,pair<int,int>>>> somePossiblePaths;

	// Find reindeer location on direction
	pair<int,int> reindeerLocation = reindeerPath.back().first;
	pair<int,int> reindeerDirection = reindeerPath.back().second;

	// First thing to do is the check which directions are possible. We should not turn 180 degrees, so never go back to where you come from
	pair<int,int> forbiddenDirection = make_pair(reindeerDirection.first * -1, reindeerDirection.second * -1);

	// Check if the reindeer can move in the three possible directions
	vector<pair<int,int>> possibleDirections = {make_pair(1,0), make_pair(0,-1), make_pair(0,1), make_pair(-1,0)};

  char mapFeature;
  pair<int,int> newLocation;
  int turnsInPath;
  int turnIndex = -1;
	for(pair<int,int> newDirection : possibleDirections){
		turnIndex++;
		if(newDirection == forbiddenDirection) continue;

		// Check what is in the map in the direction we are trying to go to
		newLocation = make_pair(reindeerLocation.first + newDirection.first, reindeerLocation.second + newDirection.second);
		mapFeature = mazeMap.at(newLocation.second).at(newLocation.first);

		// If there is a wall, we cannot move to that directiion
		if(mapFeature == '#') continue;

    // Check if the current location can be reached with less turns
		turnsInPath = nTurns;
		if(newDirection != reindeerDirection) turnsInPath++;
		if(turnMap[turnIndex].at(newLocation.second).at(newLocation.first) < turnsInPath){
			continue;
		} else {
			// Mark that the new location can be reached with this amount of turns, if it cannot be reached with less turns
			turnMap[turnIndex].at(newLocation.second).at(newLocation.first) = turnsInPath;
		}

		// If there is no wall, check if we have already been in the location. If we have, we are doing a loop and that cannot be the fastest route through the maze
		auto it = ranges::find(reindeerPath, newLocation, &decltype(reindeerPath)::value_type::first);
		if(it != reindeerPath.end()) continue;

		// Then move to a new location
		vector<pair<pair<int,int>,pair<int,int>>> possiblePath;
		for(auto location : reindeerPath){
			possiblePath.push_back(location);
		}
		possiblePath.push_back(make_pair(newLocation, newDirection));

		// If there is the goal, we are finished
		if(mapFeature == 'E'){
			allPossiblePaths.push_back(possiblePath);

			// Turns cost a lot. Update the turnmap such that there are no values larger this that found the goal in the map
			for(int iTurn = 0; iTurn < 4; iTurn++){
			  for(size_t yTurn = 0; yTurn < turnMap[iTurn].size(); yTurn++){
				  for(size_t xTurn = 0; xTurn < turnMap[iTurn].at(yTurn).size(); xTurn++){
					  if(turnMap[iTurn].at(yTurn).at(xTurn) > turnsInPath){
						  turnMap[iTurn].at(yTurn).at(xTurn) = turnsInPath;
					  }
				  }
			  }
		  }
		} else {
			somePossiblePaths = solveMaze(mazeMap, possiblePath, turnsInPath);
			for(auto path : somePossiblePaths){
				allPossiblePaths.push_back(path);
			}
		}

	}

	return allPossiblePaths;

}

/*
 * Find the reindeer from the map.
 *
 *  Arguments: 
 *   vector<string> mazeMap = Map of the maze
 *
 *  Return:
 *   pair<int,int> with x and y coordinates of the robot.
 */
pair<int,int> findReindeer(vector<string> warehouseMap){

  for(size_t yCoordinate = 1; yCoordinate < warehouseMap.size(); yCoordinate++){
    for(size_t xCoordinate = 1; xCoordinate < warehouseMap.at(yCoordinate).size(); xCoordinate++){
      if(warehouseMap.at(yCoordinate).at(xCoordinate) == 'S'){
        return make_pair(xCoordinate, yCoordinate);
      }
    }
  }

  // Return non-sensical value if we cannot find the robot
  return make_pair(-1,-1);

}

/*
 * Find the maze map from input file
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<string> of the map of the maze
 */
vector<string> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<string> mazeMap;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);
      
      // Create the map of the maze
      mazeMap.push_back(line);
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return mazeMap;

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

  // Find the maze map from the input file
  vector<string> mazeMap = readInputFile(argv[1]);

  // Find the original location of the reindeer in the maze
  pair<int,int> reindeerLocation = findReindeer(mazeMap);

  // Initialize the turn map to 1000000 everywhere
  for(int iTurn = 0; iTurn < 4; iTurn++){
    for(auto mapLine : mazeMap){
  	  vector<int> mapInitializer;
      for(auto mapChar : mapLine){
        mapInitializer.push_back(1000000);
      }
      turnMap[iTurn].push_back(mapInitializer);
    }
  }


  // Create the original location and direction vector
  pair<pair<int,int>,pair<int,int>> reindeerStart = make_pair(reindeerLocation, make_pair(1,0));
  vector<pair<pair<int,int>,pair<int,int>>> reindeerPath;
  reindeerPath.push_back(reindeerStart);

  // Find all possible paths through the maze
  vector<vector<pair<pair<int,int>,pair<int,int>>>> allPossiblePaths;
  allPossiblePaths = solveMaze(mazeMap, reindeerPath, 0);

  // Calculate the smallest path score of all the path we found from the maze
  int lowestPathScore = 10000000;
  vector<int> allPathScores;
  for(auto path : allPossiblePaths){
    allPathScores.push_back(findPathScore(path));
    if(allPathScores.back() < lowestPathScore){
    	lowestPathScore = allPathScores.back();
    }
  }

  // Next, check all the paths having the lowest path score and collect all unique locations to a vector
  vector<pair<int,int>> locationsInShortestPath;
  for(size_t iPath = 0; iPath < allPathScores.size(); iPath++){

  	// Only look at paths that have the lowest path score
  	if(allPathScores.at(iPath) > lowestPathScore) continue;

  	// Add all the locations that are not already in the shortest path location vector to that vector
  	for(auto location : allPossiblePaths.at(iPath)){
  		if(count(locationsInShortestPath.begin(), locationsInShortestPath.end(), location.first) == 0){
        locationsInShortestPath.push_back(location.first);
      }
  	}
  }

  // Print number of paths, lowest path score, and number of locations in shortest paths
  cout << "Found " << allPossiblePaths.size() << " different paths to goal" << endl;
  cout << "The lowest path score is " << lowestPathScore << endl;
  cout << "The shortest paths have a total of " << locationsInShortestPath.size() << " locations" << endl;

}