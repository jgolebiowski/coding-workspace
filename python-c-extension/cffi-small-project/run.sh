gcc -Wall -Wextra -fdiagnostics-color -Xpreprocessor -fopenmp -I/usr/local  source.c -o test.out -L/usr/local/lib -lm -liomp5 -lgsl -lcblas
./test.out