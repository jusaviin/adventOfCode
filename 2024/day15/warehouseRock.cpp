#include<iostream> // For cout and stuff
#include<fstream>  // File stream
#include<tuple>    // Return several parameters from function via tuple

// Always use std namespace, avoid repeatedly typing std
using namespace std;

/*
 * Advent of code puzzle 15-1
 * Move the robot around pushing boxes and see what happens
 *
 * Advent of code puzzle 15-2
 * The same as before, but now boxes are wider making pushing even more fun!
 */

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
 * Make the map wider by extending all boxes to have width of 2
 *
 *  Arguments:
 *   vector<vector<char>> warehouseMap = Original warehouse map
 *
 *  Return:
 *   vector<vector<char>> giving the new map that is twice as wide as the original
 */
vector<vector<char>> widenMap(vector<vector<char>> warehouseMap){

  // Make variables needed to construct the new map
  vector<vector<char>> wideMap;
  vector<char> wideMapLine;

  for(auto mapLine : warehouseMap){
    wideMapLine.clear();
    for(auto mapChar : mapLine){
      switch(mapChar){
        case '#':
          wideMapLine.push_back('#');
          wideMapLine.push_back('#');
          break;
        case 'O':
          wideMapLine.push_back('[');
          wideMapLine.push_back(']');
          break;
        case '.':
          wideMapLine.push_back('.');
          wideMapLine.push_back('.');
          break;
        case '@':
          wideMapLine.push_back('@');
          wideMapLine.push_back('.');
          break;
        default:
          cout << "Error! Invalid character in the map!" << endl;
          exit(1);
      }
    }
    wideMap.push_back(wideMapLine);
  }

  // Return the widened map
  return wideMap;

}

/*
 * Calculate the Goods Positioning System value from the current map state
 *
 *  Arguments: 
 *   vector<vector<char>> warehouseMap = Map of the warehouse
 *
 *  Return:
 *   GPS value of the current map state
 */
int calculateGPSvalue(vector<vector<char>> warehouseMap){

  // Loop over all the locations in the map. If we find a box, increment the GPS value
  int gpsValue = 0;
  for(size_t yCoordinate = 1; yCoordinate < warehouseMap.size(); yCoordinate++){
    for(size_t xCoordinate = 1; xCoordinate < warehouseMap.at(yCoordinate).size(); xCoordinate++){
      if(warehouseMap.at(yCoordinate).at(xCoordinate) == 'O' || warehouseMap.at(yCoordinate).at(xCoordinate) == '['){
        gpsValue += xCoordinate + 100 * yCoordinate;
      }
    }
  }

  return gpsValue;

}

/*
 * Find the robot from the map.
 *
 *  Arguments: 
 *   vector<vector<char>> warehouseMap = Map of the warehouse
 *
 *  Return:
 *   pair<int,int> with x and y coordinates of the robot.
 */
pair<int,int> findRobot(vector<vector<char>> warehouseMap){

  for(size_t yCoordinate = 1; yCoordinate < warehouseMap.size(); yCoordinate++){
    for(size_t xCoordinate = 1; xCoordinate < warehouseMap.at(yCoordinate).size(); xCoordinate++){
      if(warehouseMap.at(yCoordinate).at(xCoordinate) == '@'){
        return make_pair(xCoordinate, yCoordinate);
      }
    }
  }

  // Return non-sensical value if we cannot find the robot
  return make_pair(-1,-1);

}

/*
 * Find the direction of robot movement based on instruction character
 *
 *  Arguments:
 *   char robotMovement = Character giving instruction for robot movement
 *
 *  Return:
 *   pair<int,int> = Pair giving the movement direction in x-y coordinate space
 */
pair<int,int> decodeMovementChar(char robotMovement){

  pair<int,int> movementInstruction;
  switch(robotMovement){
    case '<':
      movementInstruction = make_pair(-1, 0);
      break;
    case '>':
      movementInstruction = make_pair(1, 0);
      break;
    case '^':
      movementInstruction = make_pair(0, -1);
      break;
    case 'v':
      movementInstruction = make_pair(0, 1);
      break;
    default:
      cout << "Error! Invalid movement instruction for the robot!" << endl;
      exit(1);
  }

  return movementInstruction;

}

/*
 * Move the robot and update the warehouse map accordingly
 *
 *  Arguments:
 *   vector<vector<char>>& warehouseMap = Map of the warehouse. Will be updated if the robot moves
 *   pair<int,int>& robotLocation = Location of the robot in the map. Will be updated if the robot moves
 *   char robotMovement = Character describing the direction the robot attempts to move
 */
void moveRobot(vector<vector<char>>& warehouseMap, pair<int,int>& robotLocation, char robotMovement){
  
  // First, decode the movement direction from the char giving the robot movement instruction
  pair<int,int> movementInstruction = decodeMovementChar(robotMovement);

  // After the movement instruction is decoded, check if the robot can move to the chosen direction
  int movingThings = 1;
  int yCoordinate, xCoordinate;
  bool robotCanMove = false;
  while(true){

    // Find the coordinate in the map we need to check for empty space
    xCoordinate = robotLocation.first + movingThings * movementInstruction.first;
    yCoordinate = robotLocation.second + movingThings * movementInstruction.second;

    // If there is empty space, the robot can move and we can proceed in updating the map and robot location
    if(warehouseMap.at(yCoordinate).at(xCoordinate) == '.'){
      robotCanMove = true;
      break;
    }

    // If there is a wall, robot cannot move and we do not need to update anything
    if(warehouseMap.at(yCoordinate).at(xCoordinate) == '#') break;

    // If there is no empty space or wall, there is a box that might move with the robot. We need to check the next coordinate to know for sure.
    movingThings++;
  }

  // If the robot can move, we need to update the robot location and the warehouse map accordingly
  if(robotCanMove){

    // Move the robot and all the boxes the robot can push one space
    while(movingThings > 0){

      // Find the coordinate in the map we want to update
      xCoordinate = robotLocation.first + movingThings * movementInstruction.first;
      yCoordinate = robotLocation.second + movingThings * movementInstruction.second;

      // Update the coordinate in the map
      warehouseMap.at(yCoordinate).at(xCoordinate) = warehouseMap.at(yCoordinate - movementInstruction.second).at(xCoordinate - movementInstruction.first);

      // Update the tracker telling how many more things we need to move
      movingThings--;
      
    }

    // After everything has been moved, replace the original location of the robot with empty space
    warehouseMap.at(robotLocation.second).at(robotLocation.first) = '.';

    // Then update the robot location
    robotLocation = make_pair(robotLocation.first + movementInstruction.first, robotLocation.second + movementInstruction.second);
  }

}

/*
 * Move the robot and update the warehouse map accordingly assuming wide boxes
 *
 *  Arguments:
 *   vector<vector<char>>& warehouseMap = Map of the warehouse. Will be updated if the robot moves
 *   pair<int,int>& robotLocation = Location of the robot in the map. Will be updated if the robot moves
 *   char robotMovement = Character describing the direction the robot attempts to move
 *   int boxWidth = Width of the boxes in the warehouse
 */
void moveRobotWideBox(vector<vector<char>>& warehouseMap, pair<int,int>& robotLocation, char robotMovement, int boxWidth){
  
  // First, decode the movement direction from the char giving the robot movement instruction
  pair<int,int> movementInstruction = decodeMovementChar(robotMovement);

  // Wide boxes are an issue only if moving things up or down. When moving left or right same algorithm as for narrow boxes will work.
  if(movementInstruction.second == 0 || boxWidth == 1){
    moveRobot(warehouseMap, robotLocation, robotMovement);
    return;
  }

  // For wide boxes, we need to be more careful when moving up or down
  // Instead of just relying on straigh line from the robot, we should remember all box coordinates they try to move
  vector<pair<int,int>> movingObjects;
  pair<int,int> thisObject;
  int locationCheck = 0;
  int movingObjectCount = 0;
  movingObjects.push_back(robotLocation);
  int yCoordinate, xCoordinate;
  bool robotCanMove = true;
  bool breakWhile = false;

  while(true){

    robotCanMove = true;

    // Update the size of the vector of objects that need to be moved
    locationCheck = movingObjectCount;
    movingObjectCount = movingObjects.size();

    // Check that all objects that need to move can move
    for(int checkedObject = locationCheck; checkedObject < movingObjectCount; checkedObject++){

      // Find the coordinate in the map we need to check for empty space
      xCoordinate = movingObjects.at(checkedObject).first + movementInstruction.first;
      yCoordinate = movingObjects.at(checkedObject).second + movementInstruction.second;

      // If there is empty space, this robot or box can move
      if(warehouseMap.at(yCoordinate).at(xCoordinate) == '.'){
        continue;
      } else { 
        robotCanMove = false;
      }

      // If there is a wall, the robot or box cannot move. No movements should be done
      if(warehouseMap.at(yCoordinate).at(xCoordinate) == '#') {
        robotCanMove = false;
        breakWhile = true;
        break;
      }

      // If we are here for the checked object, we know we need to move a box. Since box has width of two, both of these must be able to move.
      if(warehouseMap.at(yCoordinate).at(xCoordinate) == '['){

        // Add the coordinates for the box if they are not already in the moving objects vector
        thisObject = make_pair(xCoordinate, yCoordinate);
        if(count(movingObjects.begin(), movingObjects.end(), thisObject) == 0){
          movingObjects.push_back(thisObject);
        }

        thisObject = make_pair(xCoordinate+1, yCoordinate);
        if(count(movingObjects.begin(), movingObjects.end(), thisObject) == 0){
          movingObjects.push_back(thisObject);
        }

      } else {
        // Here the only remaining option is that the object is right side of the box ']'

        // Add the coordinates for the box if they are not already in the moving objects vector
        thisObject = make_pair(xCoordinate, yCoordinate);
        if(count(movingObjects.begin(), movingObjects.end(), thisObject) == 0){
          movingObjects.push_back(thisObject);
        }

        thisObject = make_pair(xCoordinate-1, yCoordinate);
        if(count(movingObjects.begin(), movingObjects.end(), thisObject) == 0){
          movingObjects.push_back(thisObject);
        }
      }

    }

    // If we have determined that the robot can move, we can break from the loop
    if(robotCanMove) break;

    // If we hit a wall, break the while loop
    if(breakWhile) break;
  }

  // If the robot can move, we need to update the location of all the objects that move
  if(robotCanMove){

    // Move the robot and all the boxes the robot can push one space
    for(int iObject = movingObjects.size()-1; iObject >= 0; iObject--){

      // Find the coordinate in the map we want to update
      xCoordinate = movingObjects.at(iObject).first;
      yCoordinate = movingObjects.at(iObject).second;

      // Update the coordinate in the map
      warehouseMap.at(yCoordinate + movementInstruction.second).at(xCoordinate + movementInstruction.first) = warehouseMap.at(yCoordinate).at(xCoordinate);
      warehouseMap.at(yCoordinate).at(xCoordinate) = '.';
      
    }

    // Then update the robot location
    robotLocation = make_pair(robotLocation.first + movementInstruction.first, robotLocation.second + movementInstruction.second);
  }

}

/*
 * Find the warehouse map and robot instructions from the input file
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   Warehouse map and robot instruction in a tuple
 */
tuple<vector<vector<char>>, string> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<vector<char>> warehouseMap;
  string robotInstructions;
  bool mapPart = true;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  vector<char> mapLine;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);
      
      // If we find an empty line, that marks the change from warehouse map to robot instructions
      if(line.compare("") == 0) {
        mapPart = false;
        continue;
      }

      // Determine if we are in the map part or the instructions part
      if(mapPart){
        // If we are reading map part, make a char vector from the current line
        mapLine.clear();
        for(char thisChar : line){
          mapLine.push_back(thisChar);
        }
        warehouseMap.push_back(mapLine);
      } else {
        // If we are reading robot instructions, just save them into string
        robotInstructions = line;
      }
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return make_tuple(warehouseMap, robotInstructions);

}


/*
 * Main program
 */
int main(int argc, char** argv){

  //==== Read arguments =====
  if ( argc<3 ) {
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout<<"+ Usage of the macro: " << endl;
    cout<<"+  "<<argv[0]<<" [puzzleInput] [boxWidth]"<<endl;
    cout<<"+  puzzleInput: Text file containing the puzzle input" <<endl;
    cout<<"+  boxWidth: Box width in the warehouse. Either 1 or 2" << endl;
    cout<<"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl;
    cout << endl << endl;
    exit(1);
  }

  // Find the warehouse map and robot instructions from the input file
  vector<vector<char>> warehouseMap;
  string robotInstructions;
  tie(warehouseMap, robotInstructions) = readInputFile(argv[1]);
  const int boxWidth = atoi(argv[2]);

  // Check that the box width is 1 or 2
  if(boxWidth != 1 && boxWidth != 2){
    cout << "Error! Invalid box width argument. Please give either 1 or 2 for box width." << endl;
    exit(1);
  }

  // If we are doing the study for wide boxes, we need to update the original warehouse map read from the file
  if(boxWidth == 2){
    warehouseMap = widenMap(warehouseMap);
  }

  // Find the location of the robot. Better to keep track of it than find it again in each iteration
  pair<int,int> robotLocation = findRobot(warehouseMap);

  // Algorithms need to change a bit depending on the box width on the map
  // Once we have the map and the instructions ready, loop over the instructions and update the map in each step
  for(char robotMovement : robotInstructions){
    moveRobotWideBox(warehouseMap, robotLocation, robotMovement, boxWidth);
  }

  // After the robot stops moving, calculate the Goods Positioning System value
  int gpsValue = calculateGPSvalue(warehouseMap);

  // Print the GPS value after the robot stops moving
  cout << "Final GPS value is: " << gpsValue << endl;

}