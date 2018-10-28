# Example project for cpp + python integration

* There are two cmake-list files in the cmake-list directory that are used with setup.py to shell out to cmake and install appropriate versions
* See setup.py for exact details and to set some constants.
* The test compilation runs with -g and -O0 flags for debugging and uses catch2 library.
    * Two versions of compile are recommended, either compile all tests or just a simple main.cpp program to test a function


## Misc
In order to run gdb on OSX:
* install gdb 8.0.1 from
    * brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/c3128a5c335bd2fa75ffba9d721e9910134e4644/Formula/gdb.rb
* Setup shell start by
    * echo "set startup-with-shell off" >> ~/.gdbinit
run gdb as a superuser as
    * sudo gdb xxxxx 

PYBIND11:
* Can be found at https://github.com/pybind/pybind11.git