#include <iostream>
#include <Python.h>
#include "libmypy.h"

PyObject * hello(PyObject * self)
{
    return PyUnicode_FromFormat("Hello C++ extension!");
}

PyObject * heyman(PyObject *self, PyObject *args)
{
    int num;
    char *name;

    if(!PyArg_ParseTuple(args, "is", &num, &name))
        return NULL;

    return PyUnicode_FromFormat("Hay %s!  You gave me %d.", name, num);
}

PyObject * add(PyObject *self, PyObject *args)
{
    int num1, num2;
    std::string eq;

    if(!PyArg_ParseTuple(args, "ii", &num1, &num2))
        return NULL;

    eq = std::to_string(num1) + " plus " + std::to_string(num2);

    return Py_BuildValue("is", num1 + num2, eq.c_str());
}
