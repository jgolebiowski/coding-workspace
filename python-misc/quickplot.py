import unittest
from typing import Union, List
from math import floor, ceil

import numpy as np


def quickplot(x: Union[List, np.ndarray], y: Union[List, np.ndarray],
              xmin: float = None, xmax: float = None, ymin: float = None, ymax: float = None,
              display_width: int = 100, display_heigth: int = 32):
    """
    Quickly plot a given function ( y = f(x) ) in a terminal window vertically.

    :param x: function arguments in shape (n_points, )
    :param y: function values in shape (n_points, )
    :param xmin: If specified, only arguments above xmin will be plotted
    :param xmax: If specified, only arguments below xmax will be plotted
    :param ymin: If specified, only values above ymin will be plotted
    :param ymax: If specified, only values below ymax will be plotted
    :param display_width: Width of the display
    :param display_heigth: Heigth of the display
    """
    if display_width < 30:
        raise ValueError("Plase use display width > 40")
    if len(x) != len(y):
        raise ValueError(f"Lengths of x and y not equal {len(x)} != {len(y)}")
    if isinstance(x, np.ndarray):
        if x.ndim != 1:
            raise ValueError("x must be a list or a 1-D array")
    if isinstance(y, np.ndarray):
        if y.ndim != 1:
            raise ValueError("y must be a list or a 1-D array")

    if xmin is None:
        xmin = min(x)
    if xmax is None:
        xmax = max(x)
    if ymin is None:
        ymin = min(y)
    if ymax is None:
        ymax = max(y)

    plotwidth = display_width - 11
    plotheigth = display_heigth - 2
    xbins = np.linspace(xmin, xmax, num=plotwidth)
    ybins = np.linspace(ymin, ymax, num=plotheigth)

    # ------ Make plot central panel
    plot = np.chararray((plotheigth, plotwidth), itemsize=1, unicode=True)
    plot[:] = "."
    for xval, yval in zip(x, y):
        if (xval > xmax) or (xval < xmin) or (yval > ymax) or (yval < ymin):
            continue

        xposition = (plotwidth - 1) * (xval - xmin) / (xmax - xmin)
        xposition = floor(xposition)

        yposition = (plotheigth - 1) * (yval - ymin) / (ymax - ymin)
        yposition = plotheigth - 1 - floor(yposition)
        plot[yposition, xposition] = "o"

    plotlines = []
    # ------ Make vertical ticks
    tickmask = [False for idx in range(plotheigth)]
    tickmask[0] = True
    tickmask[-1] = True
    find_vertical_ticks(1, len(tickmask) - 1, tickmask)
    for idx in range(plotheigth):
        if tickmask[idx]:
            line = f"{ybins[idx]:+8.2e} |" + "".join(plot[idx, :])
        else:
            line = f"          |" + "".join(plot[idx, :])
        plotlines.append(line)
    plotlines.append("=" * display_width)

    # ------ Make horizontal ticks
    tickwidth = 10
    finalline = [" " for idx in range(plotwidth)]
    finalline[0: tickwidth] = f"{xbins[0]:+9.3e}"
    finalline[-tickwidth:] = f"{xbins[-1]:+9.3e}"
    find_horizontal_ticks(tickwidth, len(finalline) - tickwidth, finalline, xbins)
    finalline = " " * 10 + "".join(finalline)
    plotlines.append(finalline)

    plotstring = "\n".join(plotlines)
    print(plotstring)

def find_vertical_ticks(start: int, stop: int, tickmask: List[bool]):
    """
    Recursive routine to fill in tick mask
    :param start: beggining of the fragment to fill
    :param stop: end of the fragment to fill
    :param tickmask: tick mask itself
    """
    tickwidth = 6
    if (stop - start) < tickwidth:
        return

    midpoint = floor((start + stop) / 2)
    tickmask[midpoint] = True
    find_vertical_ticks(start, midpoint, tickmask)
    find_vertical_ticks(midpoint, stop, tickmask)


def find_horizontal_ticks(start: int, stop: int, finalline: List[str], xbins: np.ndarray):
    """
    Recursive routine for filling in ticks in the final line
    :param start: begigning of the final line fragment to fill
    :param stop: finish of the final line fragment to fill
    :param finalline: the line itself
    :param xbins: bins for x
    """
    tickwidth = 10
    if (stop - start) < 2 * tickwidth:
        return

    midpoint = floor((start + stop) / 2)
    finalline[int(midpoint - tickwidth / 2):
              int(midpoint + tickwidth / 2)] = f"{xbins[int(midpoint)]:+9.3e}"
    find_horizontal_ticks(start, int(midpoint - tickwidth / 2), finalline, xbins)
    find_horizontal_ticks(int(midpoint + tickwidth / 2), stop, finalline, xbins)


class TestUtilities(unittest.TestCase):
    @staticmethod
    def get_bin(bins: np.ndarray, value) -> int:
        """
        Get index of the bin for that value
        :param bins: bins, monotonically increasing, each given by its lower bound
        :param value: value to be placed
        :return: index of the bin. -1 if value is smaller than lower bound of the first bin.
        """
        idx = 0
        while (idx < len(bins)):
            if value >= bins[idx]:
                idx += 1
            else:
                break
        return idx - 1

    def test_quickplot(self):
        x = np.linspace(-10, 10, num=100, endpoint=True)
        y = x ** 2
        print("")
        quickplot(x, y)

    def test_gen_bin(self):
        bins = np.linspace(0, 9, num=10)
        self.assertEqual(self.get_bin(bins, 2), 2)
        self.assertEqual(self.get_bin(bins, 1.5), 1)
        self.assertEqual(self.get_bin(bins, 10), 9)

    def test_gen_bins2(self):
        xmin = 0
        xmax = 10
        nbins = 25
        bins = np.linspace(xmin, xmax, num=nbins)

        for value in np.linspace(xmin, xmax, num=13):
            position = floor((nbins - 1) * (value - xmin) / (xmax - xmin))
            targetposition = self.get_bin(bins, value)
            self.assertEqual(position, targetposition)


if (__name__ == "__main__"):
    unittest.main()

