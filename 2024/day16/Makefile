PROGRAM       = mazeNavigator

version       = development
CXX           = g++
CXXFLAGS      = -g -Wall -D$(version)
LDFLAGS       = -O2 
        
all:            $(PROGRAM)

$(PROGRAM):     $(PROGRAM).cpp
		@echo "Linking $(PROGRAM) ..."
		$(CXX) -L$(PWD) $(PROGRAM).cpp $(CXXFLAGS) --std=c++20 $(LDFLAGS) -o $(PROGRAM)
		@echo "done"

%.cxx:

%: %.cxx
#  commands to execute (built-in):
	$(LINK.cc) $^ $(CXXFLAGS) $(LOADLIBES) $(LDLIBS) -o $@

%.o: %.cxx %.h
#  commands to execute (built-in):
	$(COMPILE.cc) $(OUTPUT_OPTION) $<

# If dictionaries built, need to clean also them: *Dict*
clean:
		rm -rf $(PROGRAM).o *.dSYM $(PROGRAM)

cl:  clean $(PROGRAM)
