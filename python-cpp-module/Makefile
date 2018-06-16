# define the C compiler to use
CXX = g++-8

# define any compile-time flags
#CFLAGS = -std=c++11 -Wall -Wextra -pedantic -O3 -fopenmp -fdiagnostics-color
CFLAGS = -std=c++11 -Wall -Wextra -pedantic -fdiagnostics-color -fopenmp -fPIC -shared

# define any directories containing header files other than /usr/include
#
INCLUDES = -I./cpp/src -I/Users/golejace/Documents/eigen-git-mirror

# define library paths in addition to /usr/lib
#   if I wanted to include libraries not in /usr/lib I'd specify
#   their path using -Lpath, something like:
# LFLAGS = -L/home/lib  -L./lib
LFLAGS= -L./cpp/lib

# define any libraries to link into executable:
#   if I want to link in libraries (libx.so or libx.a) I use the -llibname
#   option, something like (this will link in libmylib.so and libm.so:
# LDFLAGS = -lmylib -lm
LDFLAGS=

# define the Cpp source files
# SRCS = emitter.cpp error.cpp init.cpp lexer.cpp main.cpp symbol.cpp parser.cpp
SRCS = $(wildcard cpp/src/*.cpp)

# define the Cpp object files
#
# This uses Suffix Replacement within a macro:
#   $(name:string1=string2)
#         For each word in 'name' replace 'string1' with 'string2'
# Below we are replacing the suffix .c of all words in the macro SRCS
# with the .o suffix
#
OBJS = $(SRCS:.cpp=.o)

# define the executable file
#MAIN = myprogram.out
#destination = .

MAIN = mylibrary.so
destination = integration_tools/extensions

rebuild: clean $(MAIN)
	mv $(MAIN) $(destination)/$(MAIN)
	@echo $(MAIN) has been re-compiled!

build: $(MAIN)
	mv $(MAIN) $(destination)/$(MAIN)
	@echo  $(MAIN) has been compiled!


# Rule to build the main object, it needs all the objects first and
# will be compiled using necessary flags
$(MAIN): $(OBJS)
	$(CXX) $(CFLAGS) $(INCLUDES) -o $(MAIN) $(OBJS) $(LFLAGS) $(LDFLAGS)

# Rule to build all the targets ending with .c or .o - objects essensitlly
# It will add necessary flags and uses -c flag to only compile objects
# See link below for explanation of automatic variables ($^ and $@)
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html#Automatic-Variables

# Example, consider:
# all: library.cpp main.cpp
# In this case:
#
# $@ evaluates to all
# $< evaluates to library.c
# $^ evaluates to library.c main.c
.cpp.o:
	$(CXX) $(CFLAGS) $(INCLUDES) -c $^ -o $@


clean:
	$(RM) ./cpp/src/*.o *~ $(MAIN)

depend: $(SRCS)
	makedepend $(INCLUDES) $^

# DO NOT DELETE THIS LINE -- make depend needs it
# ONLY WORKS WHEN makedepend is present