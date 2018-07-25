#-------------------------------------------------------------------------------
#	SET TERMINAL
# QT - standard
# eps and latex - see two scrips
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#	PLOT CUSTOMIZATION	
#-------------------------------------------------------------------------------
set title "Mytitle"		#setting the plot title
set xlabel "My X label"		#Put a label on the x-axis
set ylabel "My Y label"		#Put a label on the y-axis

set xrange [0:12]		#Change the x-axis range
set yrange [0:12]		#Change the y-axis range
set autoscale			#Have Gnuplot determine ranges

set key at 1,0.2		#Move the legend box manually
set key bottom right		#Move the legend to a corner
set key default			#Default position - top left 
#WARNING - after fixing the key manually it is necessary to run 'set key default' before the corner command can be used 
unset key			#Delete the legends box

set label "My Label" at 1,0.2	#Put a label on a plot 
unset label			#Delete all labels

set logscale			#Use log scale for both axis
set logscale y			#Use log scale for y axis
set logscale x			#Use log scale for x axis
unset logscale			#Not use logscale

set ytics 1			# set y axis tics to appear every 1
set ytics (1,2,3)		# manually set the position of y axis tics
set xtics 1			# set x axis tics to appear every 1
set xtics (1,2,3)		# manually set the position of x axis tics

set mytics 5			# Set the minor tics for y axis - here 5 between a single major tick
set mxtics 5			# Set the minor tics for x axis - here 5 between a single major tick

unset ytics			# Delete tics on Y
set ytics auto			# Return to default on Y
unset xtics			# Delete tics on X
set xtics auto			# Return to default on X

#-------------------------------------------------------------------------------
#	FUNCTIONS
#-------------------------------------------------------------------------------
function1(x,y)=abs(x)+x*y	#Standard way to define a function

abs(x)            absolute value of x, |x|
acos(x)           arc-cosine  of x
asin(x)           arc-sine    of x  
atan(x)           arc-tangent of x
cos(x)            cosine      of x,  x is in radians.
cosh(x)           hyperbolic cosine of x, x is in radians
erf(x)            error function of x
exp(x)            exponential function of x, base e
inverf(x)         inverse error function of x
invnorm(x)        inverse normal distribution of x
log(x)            log of x, base e
log10(x)          log of x, base 10
norm(x)           normal Gaussian distribution function
rand(x)           pseudo-random number generator      
sgn(x)            1 if x > 0, -1 if x < 0, 0 if x=0
sin(x)            sine      of x, x is in radians
sinh(x)           hyperbolic sine of x, x is in radians
sqrt(x)           the square root of x
tan(x)            tangent of x, x is in radians
tanh(x)           hyperbolic tangent of x, x is in radians

#-------------------------------------------------------------------------------
#	DATA PLOTTING
#-------------------------------------------------------------------------------
plot 'path-to-file' using 1:2		#Plots the data with the 1st column as X and the 2nd as Y(x) - 0 is the line no
plot 'path-to-file' u 1:2 [arguments] 	#u = using, then the arguments 
DATAPOINTS
	-				#default using datapoints 
	with line (w l)			#Using lines co connect datapoints 
	with linepoints (w lp)		#Using points connected with a line 
LINES
	ps [number]			#Different colors depending on a number 
TITLE
	title 'my title'		#The legend will show my title
	columnheaders			#The plot resulting from the column of data will be named after the first row of Y values 
	columnheader(i)			#The plot resulting from the column of data will be named after the first row of the column i
ERRORBARS
	using 1:2:3 with yerrorbars	#The 3rd column will contain the errorbars for y values

#-------------------------------------------------------------------------------
#	DATA OPERATIONS
#-------------------------------------------------------------------------------
plot 'file' using (function1($i)):(function2($j))	#Plot the results of function1 acting on ith column as X and function2 acting on jth column as Y
plot 'file' using 1:(function3($i,$j)	#Plot the result of function3 acting on ith and jth columns as Y with the 1st column as X
plot 'file' using 1:($i*10+2)		#Plot the values from ith column x10 and +2 vs the first column

#-------------------------------------------------------------------------------
#	MULTIPLE PLOTS
#-------------------------------------------------------------------------------
plot for [i=1:10] 'file' using 1:i w l title columnheader	# Plot columns from 1 to 10 as a function of 1st column with the titles from the first cell from the appropriate column
# Also
plot for [i=1:10] 'file' using 1:($i+10) w l titile columnheader 	#Similar but with some data operations on every one of the plots 

#MULTILINE SCRIPTS

plot 'file' u 1:2 title 'plot1', \ 
	'' u 1:3 title 'plot2'		#Plot 1:2 from file with the label plot1 and 1:3 from the same file labelled plot 2
# MULTILINE - '\' means integrate the two lines (remember, NO SPACE after '/')

#-------------------------------------------------------------------------------
#	CURVE FITTING
#-------------------------------------------------------------------------------
f1(x) = a1*tanh(x/b1)			 	# define the function to be fit
a1 = 300
b1 = 0.01					# initial guess for a1 and b1
fit f1(x) 'force.dat' using 1:2 via a1, b1	#fit the function f1(x) to the 2nd column as a function of 1st column from 'force.dat' file varying a1 and b1 as parameters

# ------ Fit parameters
FIT_LIMIT = 1e-5			#the parameter for convergence, default is 1e-5
FIT_MAXITER = 0 			#mac interations 0 is limitless

FIT_START_LAMBDA
FIT_LAMBDA_FACTOR			#Parameters for the Marquardt-Levenberg algorithm, starting lambda and the factor that lambda is changed when the fit is way off
