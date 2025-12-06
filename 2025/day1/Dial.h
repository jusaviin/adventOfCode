#ifndef DIAL_H
#define DIAL_H

// Includes
#include <iostream>
#include <string>

/*
 * Dial class
 *
 * The dial hold certain values and can be rotated
 */
class Dial {

public:

	Dial(); // Default constructor
	Dial(const int minValue, const int maxValue, const int startValue); // Custom constructor
	~Dial() = default;      // Destructor

	// Functions manipulating the dial
  void SetMinimumValue(const int minValue);
  void SetMaximumValue(const int minValue);
  int TurnDial(std::string instruction);

	// Getter for dial state
	int GetDialValue() const;

private:

  // Variables defining the state of the dial
	int minimumDialValue_;
	int maximumDialValue_;
	int nDialValues_;
	int currentDialValue_;

	// Sanity checkers
	void MinMaxSanityCheck();
	int RotateDialToAllowedRange();

};

#endif