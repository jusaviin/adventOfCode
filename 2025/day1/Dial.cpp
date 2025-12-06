// Implementation of the Dial class

// Include the header file
#include "Dial.h"

/*
 * Default constructor
 */ 
Dial::Dial() :
  minimumDialValue_(0),
  maximumDialValue_(0),
  nDialValues_(1),
  currentDialValue_(0)
{}

/*
 * Custom constructor
 */
Dial::Dial(const int minValue, const int maxValue, const int startValue) :
  minimumDialValue_(minValue),
  maximumDialValue_(maxValue),
  currentDialValue_(startValue)
{
  
  // Do a sanity check for the minimum and maximum dial values
  MinMaxSanityCheck();

  // Make sure that the start value is in allowed range
  RotateDialToAllowedRange();

}

/*
 * Perform a sanity check for the current minimum and maximum dial values
 */
void Dial::MinMaxSanityCheck(){
	if(maximumDialValue_ < minimumDialValue_){
    int tempValue = maximumDialValue_;
    maximumDialValue_ = minimumDialValue_;
    minimumDialValue_ = tempValue;
  }

  // Set the total number of available dial values
  nDialValues_ = maximumDialValue_ - minimumDialValue_ + 1;
}

/*
 * If the current value is outside of the alowed range in the dial, rotate it back to the allowed range
 */
int Dial::RotateDialToAllowedRange(){
	int zeroClicks = 0;
  while(currentDialValue_ > maximumDialValue_){
  	currentDialValue_ -= nDialValues_;
  	zeroClicks++;
  }
  while(currentDialValue_ < minimumDialValue_){
  	currentDialValue_ += nDialValues_;
  	zeroClicks++;
  }
  return zeroClicks;
}

/*
 * Set a new minimum value for the dial
 */
void Dial::SetMinimumValue(const int minValue){
	minimumDialValue_ = minValue;

	// Do a sanity check for the minimum and maximum dial values
  MinMaxSanityCheck();
}

/*
 * Set a new maximum value for the dial
 */
void Dial::SetMaximumValue(const int maxValue){
	maximumDialValue_ = maxValue;

	// Do a sanity check for the minimum and maximum dial values
  MinMaxSanityCheck();
}

/*
 * Getter for dial state
 */
int Dial::GetDialValue() const{
	return currentDialValue_;
}

/*
 * Turn the dial based on instruction string
 *
 *  return = Number of times zero is obtained with the clicks
 */
int Dial::TurnDial(std::string instruction){

	// The string needs to be at least 2 characters long
	if(instruction.size() < 2){
		std::cout << "Dial::Error! Cannot turn dial!" << std::endl;
		std::cout << "The string " << instruction << " is too short!" << std::endl;
		return currentDialValue_;
	}

  // The first character in the instruction string must be L or R
  int turnSign = 0;
  if(instruction[0] == 'L') turnSign = -1;
  if(instruction[0] == 'R') turnSign = 1;

  // If turnSign is still 0, the instructyion is faulty
  if(turnSign == 0){
  	std::cout << "Dial::Error! Cannot turn dial!" << std::endl;
		std::cout << "The string " << instruction << " does not start with L or R!" << std::endl;
		return currentDialValue_;
  }

  // Find the integer part of the rest of the string
  int turnClicks = atoi(instruction.substr(1).c_str());

  // Get the number of times number zero is clicked while turning the dial
  int zeroClicks = 0;
  while(turnClicks > nDialValues_){
  	turnClicks -= nDialValues_;
  	zeroClicks++;
  }

  // Remember if initial dial value is 0
  int initialDialValue = currentDialValue_;

  // Turn the dial with the given instructions
  currentDialValue_ += turnSign * turnClicks;

  // If we are exactly at 0, we need to add 1 zero click to the counter
  // Note that this needs to be done before 100 is rotated to 0 for example to avoid double counting
  if(currentDialValue_ == 0) zeroClicks++;

  // Make sure that we stay on the allowed range. Note that if we start from zero, we do not pass zero while rotating to allowed range
  if(initialDialValue == 0){
    RotateDialToAllowedRange();
  } else {
    zeroClicks += RotateDialToAllowedRange();
  }

  // Return the number of times zero is obtained when doing the dial turning
  return zeroClicks;

}