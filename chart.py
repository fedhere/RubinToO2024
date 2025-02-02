# author: Igor Andreoni <igor.andreoni@gmail.com>

import numpy as np
import math
import matplotlib.pyplot as plt
from collections import OrderedDict


def makeChart(results, event="BNS merger",
              filters_color_dict={'u': 'b', 'g': 'g', 'r': 'r',
                                  'i': 'yellow', 'z': 'k', 'y': 'orange'},
              exptimes_marker_list=["o", "s", "p", "h", "8"],
              ):

    # Initialize the figure
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)
    marker_size = 50

    # Assign variables to the y labels, length of table
    ylabels = list(results.keys())
    ilen = len(ylabels)

    # Markers piechart. First define the ratios
    ratio = 1./6   # same for 6 filters
    xy_list_pie = get_pie(ratio)

    for i in range(len(ylabels)):
        timeline = results[ylabels[i]]["cadence_hr"]
        filters = results[ylabels[i]]["filters"]
        # Iterate over combination of filters
        for xy, f in zip(xy_list_pie, filters_color_dict.keys()):
            # Iterate over individual filters
            for t, filters_epoch in zip(timeline, filters):
                if f in filters_epoch:
                    ax.plot(t, (i*0.5) + 0.5, marker=(xy),
                            ms=marker_size,
                            markerfacecolor=filters_color_dict[f],
                            markeredgecolor='k', linestyle='none', label=f)
    # y axis labels
    pos = np.arange(0.5, ilen*0.5+0.5, 0.5)
    locsy, labelsy = plt.yticks(pos, ylabels)
    plt.setp(labelsy, fontsize=16)

    # Add a grid to guide the eye
    ax.grid(which='both', color='grey', linestyle=':')
    ax.set_xlabel(f"Hours from {event}", fontsize=30)

    # plot edges based on median exptimes
    plot_edges(results, ax, marker_size=60,
               exptimes_marker_list=exptimes_marker_list)

    # Legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    # Organize number of rows
    if len(by_label.values()) <= 8:
        bbox_to_anchor = (0.5, 1.39)
    else:
        bbox_to_anchor = (0.5, 1.43)
    ax.legend(by_label.values(), by_label.keys(), loc='upper center',
              bbox_to_anchor=bbox_to_anchor, ncol=8, fancybox=True, shadow=False,
              fontsize=20, framealpha=0.8, borderpad=1.5)
    # Logscale
    ax.set_xscale("log")

    # Fix the y axis limits
    ax.tick_params(labelsize=30, width=1, length=5)
    ax.set_ylim(ymin=0.3, ymax=ilen*0.5+0.2)
    ax.invert_yaxis()
    # Fix the x axis limits
    xlim = ax.get_xlim()  # get existing x limits
    ax.set_xlim(xlim)

    # Secondary axis (days)
    ax2 = ax.twiny()  # instantiate a second axes that shares the same y-axis
    xlim2 = [np.log10(xlim[0]), np.log10(xlim[1])]
    ax2.set_xlim(xlim2)
    x2ticks = [0.2, 1, 2]
    ax2.set_xticks([np.log10(24*x) for x in x2ticks])
    ax2.set_xticklabels(x2ticks)
    ax2.tick_params(labelsize=30, width=1, length=5)
    ax2.set_xlabel(f"Days from {event}", fontsize=30)

    # If needed, plot an horizontal line
    # ax.plot([xlim[0], xlim[1]],
    #          2*[np.mean(np.arange(len(results))) - 0.25],
    #          color='grey')

    # Adjust the plot
    plt.subplots_adjust(left=0.2)

    return fig, ax


def plot_edges(results, ax, marker_size=50,
               exptimes_marker_list=["o", "s", "p", "h", "8"],
               ):
    # Plot marker edges for exposure times
    ylabels = list(results.keys())
    # create a dictionary for the markers
    exptimes_marker_dict = {}
    # Check that there are enough markers for the exptimes
    exptimes_all = set(np.concatenate([results[k]["exptimes_median"]
                                       for k in results.keys()]))
    if len(exptimes_marker_list) < len(set(exptimes_all)):
        print("STOP! Add markers to your exptimes_marker_list, \n\
there are not enough")
        return
    for et, marker in zip(sorted(set(exptimes_all)), exptimes_marker_list):
        exptimes_marker_dict[et] = marker
    for i in range(len(ylabels)):
        timeline = np.array(results[ylabels[i]]["cadence_hr"])
        exptimes = np.array(results[ylabels[i]]["exptimes_median"])
        # Plot the edges by iterating over epochs and exp. times
        for t, exptime in zip(timeline, exptimes):
            ax.plot(t, (i*0.5)+0.5,
                    marker=exptimes_marker_dict[exptime],
                    markerfacecolor='none',
                    markeredgecolor='k',
                    markeredgewidth=1,
                    markersize=marker_size,
                    label=f"{exptime}s")


def get_pie(ratio0):
    # Disclaimer: code found at
    # https://matplotlib.org/2.0.1/mpl_examples/api/scatter_piecharts.py
    # calculate the points of the first pie marker;
    # these are just the origin (0,0) + some points on a circle cos,sin
    xy_list = []
    r1 = ratio0
    r2 = r1 + ratio0
    r3 = r2 + ratio0
    r4 = r3 + ratio0
    r5 = r4 + ratio0

    x = [0] + np.cos(np.linspace(0, 2*math.pi*r1, 10)).tolist()
    y = [0] + np.sin(np.linspace(0, 2*math.pi*r1, 10)).tolist()
    xy_list.append(list(zip(x, y)))

    x = [0] + np.cos(np.linspace(2*math.pi*r1, 2*math.pi*r2, 10)).tolist()
    y = [0] + np.sin(np.linspace(2*math.pi*r1, 2*math.pi*r2, 10)).tolist()
    xy_list.append(list(zip(x, y)))

    x = [0] + np.cos(np.linspace(2*math.pi*r2, 2*math.pi*r3, 10)).tolist()
    y = [0] + np.sin(np.linspace(2*math.pi*r2, 2*math.pi*r3, 10)).tolist()
    xy_list.append(list(zip(x, y)))

    x = [0] + np.cos(np.linspace(2*math.pi*r3, 2*math.pi*r4, 10)).tolist()
    y = [0] + np.sin(np.linspace(2*math.pi*r3, 2*math.pi*r4, 10)).tolist()
    xy_list.append(list(zip(x, y)))

    x = [0] + np.cos(np.linspace(2*math.pi*r4, 2*math.pi*r5, 10)).tolist()
    y = [0] + np.sin(np.linspace(2*math.pi*r4, 2*math.pi*r5, 10)).tolist()
    xy_list.append(list(zip(x, y)))

    x = [0] + np.cos(np.linspace(2*math.pi*r5, 2*math.pi, 10)).tolist()
    y = [0] + np.sin(np.linspace(2*math.pi*r5, 2*math.pi, 10)).tolist()
    xy_list.append(list(zip(x, y)))

    return xy_list
