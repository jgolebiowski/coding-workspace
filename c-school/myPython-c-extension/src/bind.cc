#include "libmypy.h"

char hellofunc_docs[] = "hello()\n"
                        "Hello world description.";
char heymanfunc_docs[] = "heyman(number, name)\n"
                         "Echo your name and passed number.";
char addfunc_docs[] = "add(number1, number2)\n"
                      "Add two numbers.";

PyMethodDef helloworld_funcs[] = {
    {   "hello", (PyCFunction)hello, METH_NOARGS, hellofunc_docs},
    {   "heyman", (PyCFunction)heyman, METH_VARARGS, heymanfunc_docs},
    {   "add", (PyCFunction)add, METH_VARARGS, addfunc_docs},
    {   NULL, NULL}     /* Sentinel - marks the end of this structure */
};

char helloworldmod_docs[] = "This is hello world module.";

PyModuleDef helloworld_mod = {
    PyModuleDef_HEAD_INIT,
    "helloworld",                   /* name of module */
    helloworldmod_docs,             /* module documentation, may be NULL */
    -1,                             /* size of per-interpreter state of the module,
                                       or -1 if the module keeps state in global variables. */
    helloworld_funcs,               /* module functions */
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_helloworld(void) {
    return PyModule_Create(&helloworld_mod);
}