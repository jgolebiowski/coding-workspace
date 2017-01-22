def power(n,pow_ix=2,float_ix='no'):
	result=1
	for i in range(0,pow_ix):
		result=result*n
	if float_ix=='yes':
		result=float(result)
	return result

def _sqroot(n,epsilon=10**(-10),iter_max=1000,int_epsilon=10**(-7)):
        x0=float(n)
        x1=2*float(n)+10
        for i in range(iter_max):
                x1=x0-(x0**2-n)/(2*x0)
                if abs(x1-x0)<=epsilon:
                        result=x1
                        break
                x0=x1
        else:
                raise Exception("Iteration limit reached, current limit:", iter_max)

        if abs(float(result)-int(result))<=int_epsilon:
                result=int(result)
        return result

class number:
	"""My class documentation string"""
	
	def __init__(self,n):
		self.value=n	
	def hello(self):
		"""Print out an introductory sentenc"""
		print 'Hello my class! The value is:',self.value
	def add(self,n):
		"""Increases the value by a certian amount"""
		self.value=self.value+n
	def sqroot(self, **kwargs):
		"""using sqroot function to find the square root"""
		#------ the arguments (in a list format) given when the number.sqroot() functiona is called are transferred to the _sqroot function via the **kwargs - a generic list.
		self.sqrt=_sqroot(self.value, **kwargs)
		return _sqroot(self.value, **kwargs)

class test:
	def __init__(mako,n):
		mako.var=n
	def hello(mako2):
		print 'Elo',mako2.var
