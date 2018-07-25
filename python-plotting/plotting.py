from __future__ import absolute_import, division, print_function, unicode_literals

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np

def plot_data_1d(x, y, plot_name, xlim=None):
    """Generate a matplotlib plot for 1D data
    Parameters
    ----------
    x : np.array
        input points given as (npoints, ndimensions)
    y : np.array
        function values given in (1, npoints)
    plot_name : str
        Name of the output file
    xlim : tuple of floats
        (x min, x max)
    """

    plt.plot(x[:, 0], y[:, 0], linestyle='none', linewidth=0.5, marker='o', markersize=5)

    if xlim is not None:
        plt.xlim(xlim)

    dpi = 175
    plot_format = "png"
    file_name = "{}.{}".format(plot_name, plot_format)
    plt.savefig(file_name, format=plot_format, bbox_inches='tight', dpi=dpi)
    plt.clf()


def plot_data_function_1d(x, y, function, plot_name, xlim=None, ylim=None):
    """Generate a matplotlib plot for 1D data
    Parameters
    ----------
    x : np.array
        input points given as (npoints, ndimensions)
    y : np.array
        function values given in (1, npoints)
    function : function
        Function to be ploted alongside the points
    plot_name : str
        Name of the output file
    xlim : tuple of floats
        (x min, x max)
    ylim : tuple of floats
        (y min, y max)
    """

    plt.plot(x[:, 0], y[:, 0], linestyle='none', linewidth=0.5, marker='o', markersize=5)
    x_plot = x[:, 0].copy()
    x_plot.sort()
    plt.plot(x_plot, function(x_plot), linestyle='solid', linewidth=0.5)

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    dpi = 175
    plot_format = "png"
    file_name = "{}.{}".format(plot_name, plot_format)
    plt.savefig(file_name, format=plot_format, bbox_inches='tight', dpi=dpi)
    plt.clf()


def plot_gp_predictions(x_pred, pred_mean, pred_error, x_train, y_train, plot_name, xlim=None, ylim=None):
    """Generate a plot for GP regression
    Parameters
    ----------
    x_pred : np.array
        input points given as (npoints, ndimensions)
    pred_mean : np.array
        Values of the mean at prediction points dims in (1, npoints)
    pred_error : np.array
        Uncertianty sigma given as (npoints, )
    x_train : np.array
        Training points given as (npoints, ndimensions)
    y_train : np.array
        Training values given in (1, npoints)
    plot_name : str
        Name of the output file
    xlim : tuple of floats
        (x min, x max)
    ylim : tuple of floats
        (y min, y max)
    """

    plt.gca().fill_between(x_pred[:, 0],
                           pred_mean[:, 0] - pred_error[:, 0],
                           pred_mean[:, 0] + pred_error[:, 0], color="#dddddd")
    plt.plot(x_pred[:, 0], pred_mean[:, 0], 'r--', lw=1)
    plt.plot(x_train[:, 0], y_train[:, 0], "bo", markersize=3)
    # plt.errorbar(x_pred[:, 0], pred_mean[:, 0], yerr=pred_error.flatten(), capsize=0)

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

    dpi = 175
    plot_format = "png"
    file_name = "{}.{}".format(plot_name, plot_format)
    plt.savefig(file_name, format=plot_format, bbox_inches='tight', dpi=dpi)
    plt.clf()



def plot_data_scatter(data, plot_name,
                       xlabel=None, ylabel=None, title=None, fontsize=12,
                       xlim=None, ylim=None, logplot=False, save_plot=True):
    """Generate a matplotlib plot for multiple datasets
    
    Parameters
    ----------
    data : list of dictionaries with 3 elements
        x : np.array
            input points given as (npoints, )
        y : np.array
            function values given in (npoints, )
        yerror : np.array
            Errors of y  in shape (npoints, )
        data_label : str
            Labels for the data
    plot_name : str
            Name of the output file
    xlabel : str
        Optional, name of the xaxis
    ylabel : None
        Optional, name of the yaxis
    title : None
        Optional, title plot
    fontsize : int
        Plot fontsize
    xlim : tuple of floats
        (x min, x max)
    ylim : tuple of floats
        (y min, y max)
    logplot : bool
        If true, x axis is in logarithmic units
    save_plot : bool
        If true, Save plot to file
    
    Returns
    -------
    matplotlib.pyplot
        PyPlot object   
    """
    plt.clf()
    matplotlib.rcParams.update({'font.size': fontsize})

    for dataitem in data:
        x = dataitem["x"]
        y = dataitem["y"]
        yerr = dataitem["yerror"]
        data_label = dataitem["data_label"]
        plt.errorbar(x, y, yerr=yerr,
                     linestyle='none', linewidth=0.5, marker='o', markersize=5, label=data_label)

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)

    # ------ Set a logscale
    if logplot:
        plt.xscale('log')
        # plt.yscale('log')

    # # ------ Set scientific axis and larger fontsize
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    # ax = plt.gca()
    # ax.xaxis.major.locator.set_params(nbins=10)
    # ax.yaxis.major.locator.set_params(nbins=10)


    # # Plot the legend and finish the plot
    plt.legend(loc="upper right")

    if save_plot:
        # ------ Do the actual plot
        dpi = 150
        plot_format = "png"
        file_name = "{}.{}".format(plot_name, plot_format)
        plt.savefig(file_name, format=plot_format, bbox_inches='tight', dpi=dpi)
    
    return plt

def plot_data_lines(data, plot_name,
                       xlabel=None, ylabel=None, title=None, fontsize=12,
                       xlim=None, ylim=None, logplot=False, save_plot=True):
    """Generate a matplotlib plot for multiple datasets
    
    Parameters
    ----------
    data : list of dictionaries with 3 elements
        x : np.array
            input points given as (npoints, )
        y : np.array
            function values given in (npoints, )
        data_label : str
            Labels for the data
    plot_name : str
            Name of the output file
    xlabel : str
        Optional, name of the xaxis
    ylabel : None
        Optional, name of the yaxis
    title : None
        Optional, title plot
    fontsize : int
        Plot fontsize
    xlim : tuple of floats
        (x min, x max)
    ylim : tuple of floats
        (y min, y max)
    logplot : bool
        If true, x axis is in logarithmic units
    save_plot : bool
        If true, Save plot to file
    
    Returns
    -------
    matplotlib.pyplot
        PyPlot object   
    """
    plt.clf()
    matplotlib.rcParams.update({'font.size': fontsize})

    for dataitem in data:
        x = dataitem["x"]
        y = dataitem["y"]
        data_label = dataitem["data_label"]
        plt.plot(x, y, linestyle='solid', linewidth=0.5, marker='o', markersize=5, label=data_label)

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    # ------ Set a logscale
    if logplot:
        plt.xscale('log')
        # plt.yscale('log')

    # # ------ Set scientific axis and larger fontsize
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    # ax = plt.gca()
    # ax.xaxis.major.locator.set_params(nbins=10)
    # ax.yaxis.major.locator.set_params(nbins=10)


    # # Plot the legend and finish the plot
    plt.legend(loc="upper right")

    if save_plot:
        # ------ Do the actual plot
        dpi = 150
        plot_format = "png"
        file_name = "{}.{}".format(plot_name, plot_format)
        plt.savefig(file_name, format=plot_format, bbox_inches='tight', dpi=dpi)
    
    return plt