#include <iostream>
#include <fstream>
#include <sstream>
#include <tuple>
#include <map>

using namespace std;

/*
 * Advent of code puzzle 9-1
 * Determine the largest rectangle where opposite corner coordinates are read from the file
 *
 * Advent of code puzzle 9-2
 * Same as 1, but rectangles can only contain red and green tiles
 */

/*
 * Print the current tile map
 */
void printMap(vector<vector<bool>> tileMap){

  for(auto mapLine : tileMap){
    for(auto mapTile : mapLine){
      cout << mapTile;
    }
    cout << endl;
  }

}

/*
 * Find all the red and green tiles based on tile outline
 * This is done by counting how many times the outline boundary is crossed
 * Every time we cross the boundary we are moving from outside to inside or inside to outside
 * We can use this information to determine if the rectangle is red or green
 *
 *  Arguments: 
 *   vector<vector<bool>> outlineTiles = List of all outline tiles
 *   vector<long long> coordinateLimits = Region in coordinate space in which all tiles are located
 *  
 */
vector<vector<bool>> findRedAndGreenTiles(vector<vector<bool>> outlineTiles, vector<long long> coordinateLimits){

  // Note this implementation takes too much time, it is slow to keep searching for indices from the tile list
  // Instead, we should make a vector<vector<bool>> telling if a tile in a specific index is green or red
  // The outline tiles should follow this format and and then also redAndGreenTiles should be this instead of a map
  // We can use the coordinate limits to shift the indices such that there are no huge amount of falses in the beginning

  // First, determine the range of x and y coordinates to study
  long long minX = coordinateLimits.at(0);
  long long maxX = coordinateLimits.at(1);
  long long minY = coordinateLimits.at(2);
  long long maxY = coordinateLimits.at(3);

  // For the minimum Y-coordinate, determine if the next crossing in X will be outside or inside
  bool insideRedGreenRegion = false;
  bool upperSideBoundary = false;
  bool lowerSideBoundary = false;

  vector<vector<bool>> redAndGreenTiles;
  vector<bool> redAndGreenStripe;

  for(int yCoordinate = minY; yCoordinate <= maxY; yCoordinate++){
    redAndGreenStripe.clear();
    for(int xCoordinate = minX; xCoordinate <= maxX; xCoordinate++){

      // Check if the current tile is part of the outline
      if(outlineTiles.at(yCoordinate - minY).at(xCoordinate - minX)){

        // If the line is part of outline, it is either red or green
        redAndGreenStripe.push_back(true);

        // Then we need to determine if we are crossing the boundary from outside to inside or inside to outside
        // For this, we need to know if the tiles directly above and below the current tile are also part of the boundary
        // Note that if we encounter two upper or lower boundaries in a row, we are not crossing a boundary.
        // 
        //                                                      -X....X-
        // In these cases, the map looks something like this:   -X....X-
        //                                                      -XXXXXX-
        //
        //                                                                      -X.........
        // Notice that we need to do the check separately for cases like this:  -XXXXXX....
        //                                                                      ------X....
        //
        if(outlineTiles.at(yCoordinate - 1 - minY).at(xCoordinate - minX)){
          if(upperSideBoundary){
            upperSideBoundary = false;
          } else {
            upperSideBoundary = true;
          }

        }
        if(outlineTiles.at(yCoordinate + 1 - minY).at(xCoordinate - minX)){
          if(lowerSideBoundary){
            lowerSideBoundary = false;
          } else {
            lowerSideBoundary = true;
          }
        }

        // We are crossing a boundary if we have found both upper and lower side of a boundary
        if(upperSideBoundary && lowerSideBoundary){
          upperSideBoundary = false;
          lowerSideBoundary = false;
          insideRedGreenRegion = !insideRedGreenRegion;
        }

      } else if(insideRedGreenRegion) {
        // If the current tile is not part of the boundary we either stay outside or inside of the red/green area
        // If we are inside of such a region, put the tile to red and green tile map
        redAndGreenStripe.push_back(true);

      } else {
        // If we are outside of the area, the tile is not red or green
        redAndGreenStripe.push_back(false);
      }

    }

    // Remember the red and green tiles corresponding to this y-coordinate in the map
    redAndGreenTiles.push_back(redAndGreenStripe);
  }

  return redAndGreenTiles;
  

}

/*
 * Outline tiles connect each adjacent red tile with straight line
 * Find all red and green outline tiles based on the location of red tiles
 */
vector<vector<bool>>findOutlineTiles(vector<pair<long long, long long>> redTiles, vector<long long> coordinateLimits){

  // First, use the coordinate limits to create and empty map
  vector<vector<bool>> outlineTiles;
  vector<bool> outlineRow;
  for(int xCoordinate = coordinateLimits.at(0); xCoordinate <= coordinateLimits.at(1); xCoordinate++){
    outlineRow.push_back(false);
  }
  for(int yCoordinate = coordinateLimits.at(2); yCoordinate <= coordinateLimits.at(3); yCoordinate++){
    outlineTiles.push_back(outlineRow);
  }
  
  // Check the pairs of tiles and fill the outline to the map
  pair<long long, long long> currentTile;
  pair<long long, long long> nextTile;
  for(int iTile = 0; iTile < redTiles.size(); iTile++){

    // In the end the list loops for the purposes of determining the outline
    if(iTile == redTiles.size() - 1){
      currentTile = redTiles.at(iTile);
      nextTile = redTiles.at(0);
    } else {
      currentTile = redTiles.at(iTile);
      nextTile = redTiles.at(iTile+1);
    }

    // Start by adding the current tile to the outline map
    outlineTiles.at(currentTile.second - coordinateLimits.at(2)).at(currentTile.first - coordinateLimits.at(0)) = true;

    // Add all the tiles in between the current tile and the next tile to the outline
    if(currentTile.first == nextTile.first){
      if(currentTile.second > nextTile.second){
        for(long long yCoordinate = currentTile.second-1; yCoordinate > nextTile.second; yCoordinate--){
          outlineTiles.at(yCoordinate - coordinateLimits.at(2)).at(currentTile.first - coordinateLimits.at(0)) = true;
        }
      } else {
        for(long long yCoordinate = currentTile.second+1; yCoordinate < nextTile.second; yCoordinate++){
          outlineTiles.at(yCoordinate - coordinateLimits.at(2)).at(currentTile.first - coordinateLimits.at(0)) = true;
        }
      }
    } else {
      if(currentTile.first > nextTile.first){
        for(long long xCoordinate = currentTile.first-1; xCoordinate > nextTile.first; xCoordinate--){
          outlineTiles.at(currentTile.second - coordinateLimits.at(2)).at(xCoordinate - coordinateLimits.at(0)) = true;
        }
      } else {
        for(long long xCoordinate = currentTile.first+1; xCoordinate < nextTile.first; xCoordinate++){
          outlineTiles.at(currentTile.second - coordinateLimits.at(2)).at(xCoordinate - coordinateLimits.at(0)) = true;
        }
      }
    }
  }

  // In the end, return the outline tile list
  return outlineTiles;

}

/*
 * Read all the lines in the input file to a vector of strings
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   vector<pair<long long, long long>> of the red tile coordinates in the movie theater
 *   the second vector in the tuple has the maximum and minimum x and y coordinates
 */
tuple<vector<pair<long long, long long>>, vector<long long>> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<pair<long long, long long>> redTiles;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  vector<string> bothRanges;
  string currentToken;
  vector<long long> minMaxXY;
  long long currentX, currentY;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);

      // Skip empty lines
      if(line == "") continue;
      
      // Determine the tile coordinated from the input string
      stringstream rangeTokenizer(line);
      bothRanges.clear();
      while(getline(rangeTokenizer, currentToken, ',')){
        bothRanges.push_back(currentToken);
      }

      currentX = atoll(bothRanges.at(0).c_str());
      currentY = atoll(bothRanges.at(1).c_str());

      redTiles.push_back(make_pair(currentX, currentY));

      if(minMaxXY.size() < 4){
        minMaxXY.push_back(currentX);
        minMaxXY.push_back(currentX);
        minMaxXY.push_back(currentY);
        minMaxXY.push_back(currentY);
      } else {
        if(currentX < minMaxXY.at(0)){
          minMaxXY.at(0) = currentX;
        }
        if(currentX > minMaxXY.at(1)){
          minMaxXY.at(1) = currentX;
        }
        if(currentY < minMaxXY.at(2)){
          minMaxXY.at(2) = currentY;
        }
        if(currentY > minMaxXY.at(3)){
          minMaxXY.at(3) = currentY;
        }
      }
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  // Add padding of one in coordinate space to each direction for tile region vector
  minMaxXY.at(0)--;
  minMaxXY.at(1)++;
  minMaxXY.at(2)--;
  minMaxXY.at(3)++;

  // Return the locations of red tiles and corners of the rectangle each of these are located
  return make_tuple(redTiles, minMaxXY);

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
  vector<pair<long long, long long>> redTiles;
  vector<long long> coordinateLimits;
  tie(redTiles, coordinateLimits) = readInputFile(argv[1]);

  // Now we need to include green tiles. All the tiles connecting adjacent red tiles are green
  // In addition, all the tiles enclosed inside the green and red outline are green
  cout << "File opened" << endl;
  vector<vector<bool>> outlineTiles = findOutlineTiles(redTiles, coordinateLimits);
  cout << "Outline tiles ready" << endl;
  vector<vector<bool>> redAndGreenTiles = findRedAndGreenTiles(outlineTiles, coordinateLimits);
  cout << "Red and green tiles ready" << endl;

  // Calculate all possible areas and choose the largest
  long long largestArea = 0;
  long long largestAreaWithinAllowedRegion = 0;
  long long currentArea;
  long long minX, maxX, minY, maxY;
  vector<int> rowValidator;
  bool areaValid = true;
  for(int iTile = 0; iTile < redTiles.size(); iTile++){
    cout << "Doing tile loop " << iTile << "/" << redTiles.size() << endl;
    for(int jTile = iTile+1; jTile < redTiles.size(); jTile++){
      currentArea = (abs(redTiles.at(iTile).first - redTiles.at(jTile).first) + 1) * (abs(redTiles.at(iTile).second - redTiles.at(jTile).second) + 1);
      areaValid = true;
      if(currentArea > largestArea){
        largestArea = currentArea;
      }

      // We can use the map of red and green tiles to validate the area is in the allowed region
      // First, determine the coordinates spanned by the rectangle
      // This needs to be done only if the current area would be larger than the largest already found valid area

      if(currentArea < largestAreaWithinAllowedRegion) continue;

      minX = redTiles.at(iTile).first - coordinateLimits.at(0);
      maxX = redTiles.at(jTile).first - coordinateLimits.at(0);
      minY = redTiles.at(iTile).second - coordinateLimits.at(2);
      maxY = redTiles.at(jTile).second - coordinateLimits.at(2);

      if(minX > maxX){
        minX = redTiles.at(jTile).first - coordinateLimits.at(0);
        maxX = redTiles.at(iTile).first - coordinateLimits.at(0);
      }

      if(minY > maxY){
        minY = redTiles.at(jTile).second - coordinateLimits.at(2);
        maxY = redTiles.at(iTile).second - coordinateLimits.at(2);
      }

      // Loop over the outline of the rectangle whose area we are examining
      // If the whole outline is good, the interior also must be good
      for(int yCoordinate = minY; yCoordinate <= maxY; yCoordinate++){
        for(int xCoordinate = minX; xCoordinate <= maxX; xCoordinate++){
          if(!redAndGreenTiles.at(yCoordinate).at(xCoordinate)){
            areaValid = false;
            break;
          }
          if(yCoordinate != minY && yCoordinate != maxY && xCoordinate != maxX){
            xCoordinate += (maxX - minX - 1);
          }
        }
        if(!areaValid) break;
      }

      // If the area is valid, remember it as the largest valid area
      if(areaValid){
        largestAreaWithinAllowedRegion = currentArea;
      }

    } // Inner tile loop
  } // Outer tile loop

  // In the end, print the largest area to the console:
  cout << "Largest area is: " << largestArea << endl;
  cout << "Largest valid area: " << largestAreaWithinAllowedRegion << endl; 

}