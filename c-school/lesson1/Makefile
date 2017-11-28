# define the C compiler to use
CC = gcc

# define any compile-time flags
# CFLAGS = -std=c90 -Wall -Wextra -O3 -fopenmp -fdiagnostics-color -fPIC -shared
CFLAGS = -std=c90 -Wextra -O3 -fopenmp -fdiagnostics-color

# define any directories containing header files other than /usr/include
#
INCLUDES = -I./include

# define library paths in addition to /usr/lib
#   if I wanted to include libraries not in /usr/lib I'd specify
#   their path using -Lpath, something like:
# LFLAGS = -L/home/lib  -L./lib
LFLAGS=

# define any libraries to link into executable:
#   if I want to link in libraries (libx.so or libx.a) I use the -llibname 
#   option, something like (this will link in libmylib.so and libm.so:
# LDFLAGS = -lmylib -lm
LDFLAGS=

# define the C source files
# SRCS = emitter.c error.c init.c lexer.c main.c symbol.c parser.c
SRCS = $(wildcard src/*.c)

# define the C object files 
#
# This uses Suffix Replacement within a macro:
#   $(name:string1=string2)
#         For each word in 'name' replace 'string1' with 'string2'
# Below we are replacing the suffix .c of all words in the macro SRCS
# with the .o suffix
#
OBJS = $(SRCS:.c=.o)

# define the executable file 
MAIN = myprogram.out
# MAIN = mylibrary.so

rebuild: clean $(MAIN)
	@echo $(MAIN) has been re-compiled

build: $(MAIN)
	@echo  $(MAIN) has been compiled


# Rule to build the main object, it needs all the objects first and 
# will be compiled using necessary flags 
$(MAIN): $(OBJS) 
	$(CC) $(CFLAGS) $(INCLUDES) -o $(MAIN) $(OBJS) $(LFLAGS) $(LDFLAGS)

# Rule to build all the targets ending with .cpp or .o - objects essensitlly
# It will add necessary flags and uses -c flag to only compile objects 
# See link below for explanation of automatic variables ($^ and $@)
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html#Automatic-Variables

# Example, consider:
# all: library.cpp main.cpp
# In this case:
# 
# $@ evaluates to all
# $< evaluates to library.cpp
# $^ evaluates to library.cpp main.cpp
.c.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $^ -o $@


clean:
	$(RM) ./src/*.o *~ $(MAIN)

depend: $(SRCS)
	makedepend $(INCLUDES) $^

# DO NOT DELETE THIS LINE -- make depend needs it
# ONLY WORKS WHEN makedepend is present