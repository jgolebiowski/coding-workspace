# Example project for c + python integration with CFFI


## Misc
In order to run gdb on OSX:
* install gdb 8.0.1 from
    * brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/c3128a5c335bd2fa75ffba9d721e9910134e4644/Formula/gdb.rb
* Setup shell start by
    * echo "set startup-with-shell off" >> ~/.gdbinit
run gdb as a superuser as
    * sudo gdb xxxxx 