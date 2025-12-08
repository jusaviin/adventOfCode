PROGRAM       = tachyonSplitter

version       = development
CXX           = g++
CXXFLAGS      = -g -Wall -D$(version)
LDFLAGS       = -O2 
        
#HDRS += Dial.h

#SRCS = $(HDRS:.h=.cpp)
#OBJS = $(HDRS:.h=.o)

all:            $(PROGRAM)

$(PROGRAM):     $(PROGRAM).cpp
		@echo "Linking $(PROGRAM) ..."
		$(CXX) -L$(PWD) $(PROGRAM).cpp $(CXXFLAGS) --std=c++20 $(LDFLAGS) -o $(PROGRAM)
		@echo "done"

%.cpp:

%: %.cpp
#  commands to execute (built-in):
	$(LINK.cc) $^ $(CXXFLAGS) $(LOADLIBES) $(LDLIBS) -o $@

%.o: %.cpp %.h
#  commands to execute (built-in):
	$(COMPILE.cc) $(OUTPUT_OPTION) $<

# If dictionaries built, need to clean also them: *Dict*
clean:
		rm -rf $(PROGRAM).o *.dSYM $(PROGRAM)

cl:  clean $(PROGRAM)
