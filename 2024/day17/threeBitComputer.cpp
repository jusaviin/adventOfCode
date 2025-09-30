#include <iostream>
#include <fstream>
#include <sstream>
#include <tuple>
#include <cmath>

using namespace std;

/*
 * Advent of code puzzle 17-1
 * Run the three bit computer and see the program output
 *
 * Advent of code puzzle 17-2
 * Find input registry value such that the program output is a copy of the program
 */

/*
 * For a length of sequence, find a number of steps required to change the last number
 *
 *  Arguments: 
 *   int sequenceLength = Length of the sequence we have
 *
 *  Return: 
 *   long int with a number of steps we need to take forward for the last number to change
 */
long stepsToChangeLastNumber(int sequenceLength){

	long stepsToTake = 0;
	for(int i = 1; i < sequenceLength; i++){
  	stepsToTake += 7*pow(8,i-1);
  }

  return stepsToTake;

}

/*
 * Find the value of a combo operand
 *
 * Combo operands 0 through 3 represent literal values 0 through 3.
 * Combo operand 4 represents the value of register A.
 * Combo operand 5 represents the value of register B.
 * Combo operand 6 represents the value of register C.
 * Combo operand 7 is reserved and will not appear in valid programs.
 */
long getComboValue(int operand, vector<long> registers){
  
  // Check that there are no illegal operands
  if(operand < 0 || operand > 6){
  	cout << "ERROR! Illegal operand! This caused a crash in the computer!" << endl;
  	exit(1);
  }

  // Below 4 just return the operand value
  if(operand < 4) return operand;

  // Otherwise return the value in the corresponding register
  return registers.at(operand-4);
}

/*
 * Find the program that is run by the three bit computer
 *
 *  Arguments:
 *   string inputFileName = Name of the input file
 *
 *  Return:
 *   pair<vector<int>, vector<int>> where the first vector gives the initial register values and the second vector the program commands
 */
pair<vector<long>, vector<int>> readInputFile(string inputFileName){

  // Define variables that will be filled
  vector<long> registers;
  vector<int> program;
  bool readingRegisters = true;

  // Set up the file names file for reading
  ifstream file_stream(inputFileName);
  string line;
  vector<string> lineTokens;
  string currentToken;
  
  // Open the file names file for reading
  if( file_stream.is_open() ) {
    
    // Loop over the lines in the file
    while( !file_stream.eof() ) {
      getline(file_stream, line);
      
      // If we find an empty line, that marks the change from registers to actual program
      if(line.compare("") == 0) {
        readingRegisters = false;
        continue;
      }

      // Clear the helper vector
      lineTokens.clear();

      // Both for registers and program, first tokenize the string using spaces
      stringstream likeTokenizer(line);
      while(getline(likeTokenizer, currentToken, ' ')){
        lineTokens.push_back(currentToken);
      }

      // Determine if we are reading registers or the program
      if(readingRegisters){
      	// For registers, the initial value in the register is given in the third token of the string
        registers.push_back(atoi(lineTokens.at(2).c_str()));

      } else {
        // For main program, we still need to tokenize the second token by commas. These are the program commands
        stringstream likeTokenizer(lineTokens.at(1));
        while(getline(likeTokenizer, currentToken, ',')){
          program.push_back(atoi(currentToken.c_str()));
        }
        
      }
      
    } // Loop over lines in the file
    
  // If cannot read the file, give error and end program
  } else {
    std::cout << "Error, could not open " << inputFileName << " for reading" << std::endl;
    exit(1);
  }

  return make_pair(registers, program);

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

  // Find the register values and program commands from the input file
  vector<long> registers;
  vector<int> program;
  tie(registers, program) = readInputFile(argv[1]);
  int executionPointer = 0;
  int programLength = program.size();

  // Print the information to the console
  cout << "Register A: " << registers.at(0) << endl;
  cout << "Register B: " << registers.at(1) << endl;
  cout << "Register C: " << registers.at(2) << endl;
  for(int command : program){
  	cout << command << " ";
  }
  cout << endl;

  /*
   * Based on testing with two different test programs, the foolowing is true on the output of the program when the value of the A-register is incremented by 1.
   *
   *  1) The first sequence has a length of 7, and always repeats as the last numbers of the output
   *  2) The other sequences have a length of 8
   *  4) The other sequences depend change based on numbers and are not fixed
   *  5) The later numbers only change after the first numbers have gone through their sequence
   *
   * In order to find a copy of the program, we the following alrogitm will give us the answer quickly:
   *  1) Calculate the index that gives the same number of output values as in the input program instructions
   *  2) Start checking numbers from the end of the sequence
   *    3) If the number does not match the one in the original program, increment the counter to a value that changes the last number
   *    4) If the last number matches, go to the second last number and back to step 2
   */

  // To find the output that matches the initial program, start by finding an A-registry value that produces the correct number of output digits
  long initialA = stepsToChangeLastNumber(programLength);

  // Run the program
  int command;
  int operand;
  long numerator;
  long denominator;
  bool copyDone = false;
  
  long aValue = initialA;
  vector<int> testOutput;

  // Check which value of register A will produce a copy of the program
  while(!copyDone){

  	// Clear the output vector
  	testOutput.clear();

  	// Increase the value of the A-register
  	aValue++;
  	registers.at(0) = aValue;

  	// Reset the values of other registers
  	registers.at(1) = 0;
  	registers.at(2) = 0;

  	// Reset the execution pointer to the start of the program
  	executionPointer = 0;

    while(executionPointer < programLength){

      // Read the command and the operant to execute next
      command = program.at(executionPointer);
      operand = program.at(executionPointer+1);

      // Based on the the command, do different operations
      switch(command){
        case 0:
      	  // The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

      	  numerator = registers.at(0);
      	  denominator = pow(2,getComboValue(operand, registers));
      	  registers.at(0) = numerator / denominator;
      	
          break;

        case 1:
      	  // The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

      	  registers.at(1) = registers.at(1) ^ operand;
        
          break;

        case 2:
          // The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

          registers.at(1) = getComboValue(operand, registers) % 8;

          break;

        case 3:
          // The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

          if(registers.at(0) == 0) break;

          executionPointer = operand - 2;

          break;

        case 4:
          // The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

          registers.at(1) = registers.at(1) ^ registers.at(2);

          break;

        case 5:
          // The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

          // Calculate the value that the program outputs
          testOutput.push_back(getComboValue(operand, registers) % 8);

          break;

        case 6:
      	  // The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

          numerator = registers.at(0);
      	  denominator = pow(2,getComboValue(operand, registers));
      	  registers.at(1) = numerator / denominator;

          break;

        case 7:
          // The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

          numerator = registers.at(0);
      	  denominator = pow(2,getComboValue(operand, registers));
      	  registers.at(2) = numerator / denominator;

          break;

        default:
          cout << "Error! Invalid command! Cannot execute!" << endl;
          exit(1);

      }

      // After the command has been executed, move the execution pointer to the next value
      executionPointer += 2;

    }

    /*cout << "aValue: " << aValue << " ";
    for(int command : testOutput){
    	cout << command << " ";
    }
    cout << endl;*/


    // Check from the end of the output to see if the numbers match what is in the program
    copyDone = true;
    for(int i = programLength - 1; i >= 0; i--){

    	// If the numbers do not match, move the A-value such that the last non-matching number changes
    	if(program.at(i) != testOutput.at(i)){
        copyDone = false;
        aValue += stepsToChangeLastNumber(i+1);
        break;
    	}
    }

  }

  // Print the register values after the execution of the program
  cout << endl;
  cout << endl;
  cout << "After the program has been executed" << endl;
  cout << "Register A: " << registers.at(0) << endl;
  cout << "Register B: " << registers.at(1) << endl;
  cout << "Register C: " << registers.at(2) << endl;
  cout << endl;
  cout << "Copy produced with A value: " << aValue << endl;
  for(int command : testOutput){
  	cout << command << " ";
  }
  cout << endl;

}