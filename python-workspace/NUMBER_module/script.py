#!/usr/bin/python
import module
from module import number 

#------ Introducing my class
print '#------ My class'
#------ Define the new member of a class an dprint the value
myobject = number(4)
print myobject.value

#------ Call class functions
myobject.add(3)
myobject.hello()


print myobject.sqroot()
print 'from class:',myobject.sqrt

#------ testing the updated values inside the function
secobject = number(16)
x=secobject.sqroot(epsilon=10, iter_max=2)
print secobject.sqrt
print secobject.sqroot(epsilon=10, iter_max=2) 
