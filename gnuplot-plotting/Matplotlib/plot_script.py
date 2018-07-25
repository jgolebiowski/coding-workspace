import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import sys

###############################################################################
# This script loads in the data from a file and plots them 
###############################################################################

#------ Read in the filename
filename = str(sys.argv[1])

#------ Read in the data using np.genfromtxt command
# The first row will be read as names of the columns
# The type will be assigned as floats, if there is a different type
# it will be stored as NaN.
# The outout is a Structured array (use data["colname"] to access a column
data = np.genfromtxt(filename, autostrip=True, dtype=None, names=True)

#------ Set data for the plot
# Potentially use the data.dtype.names[] as a list of cols
# ydata_names = data.dtype.names[2:]
ydata_names = ["abs_MAX_FE", "rel_MAX_FE"]
xdata_name = "time"

#------ Set the plot labels
#plot_labels = ydata_names
plot_labels = ["MAX force error",
                "relative MAX force error"]

#------  Set the axis
xmin = 0
xmax = 10
ymin = 0
ymax = 10
#plt.axis([xmin, xmax, ymin, ymax])

#------ Set the label and titles (can use LaTeX with $$)
xlabel = r"Time [fs]"
ylabel = r"Force [eV/ $\mathrm{\AA}$]"
title = "Super plot"

plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)

#------ Set a logscale
# plt.xscale('log')
# plt.yscale('log')


for i, y_name in enumerate(ydata_names):
    ydata = data[y_name]
    xdata = data[xdata_name]
    label = plot_labels[i]
    
    #------ Data operations, as a regular 1D numpy array
    # Can be done at any stage 
    # xdata = xdata * 2
    
    # Plot the xdata vs ydata with the label, basic visual keywords
    # linestyle='solid', linewidth=0.5, marker='o',  markersize=5
 
    plt.plot(xdata, ydata, label=label, linestyle='solid', linewidth=0.5, marker='o',  markersize=5)

# Plot the legend and finish the plot
plt.legend()

#------ Show the figure or save to file 
# Show to screen
plt.show()

# Save as an eps
# outname = "plot-"+filename
# outname = outname.replace(".", "-")
# outname = outname+".eps"
# plt.savefig(outname, format="eps")
