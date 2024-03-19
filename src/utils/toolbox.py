import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def combine_outlier_booleans(*arg_bool):
    """gets any number of outlier_bool from different methods and 
    combines them. It is ment to be used to combine outliers found 
    from different methods to make a list of final outliers. 

    Returns:
        _type_: np.array(booleans)
    """
    combined_outlier_bool = np.array([False]*len(arg_bool[0]))
    for bool in arg_bool:
        combined_outlier_bool[bool]=True

    return combined_outlier_bool

##Helper functions for plots:
def get_initial_1d_graphs(np_data):
    "data: np.array"
    fig, [ax1, ax2] = plt.subplots(2,1)
    ax2.hist(np_data, bins='fd')
    ax1.plot(np_data)
    return fig

def scatter_hist_for_2d_data(x, y, ax, ax_histx, ax_histy, x_label, y_label, outlier_bool = None):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    colors = None
    if outlier_bool is not None:
        colors_ = np.array(['blue']*len(x))
        colors_[outlier_bool]='red'
        colors= colors_.tolist()
  
    ax.scatter(x, y, color=colors )
    
    
    
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    
    

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')
    
    

def get_2d_distrib_plots(x, y, x_label, y_label, outlier_bool = None):
    # Start with a square Figure.
    fig = plt.figure(figsize=(6, 6))
    # Add a gridspec with two rows and two columns and a ratio of 1 to 4 between
    # the size of the marginal axes and the main axes in both directions.
    # Also adjust the subplot parameters for a square plot.
    gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(1, 4),
                        left=0.1, right=0.9, bottom=0.1, top=0.9,
                        wspace=0.05, hspace=0.05)
    # Create the Axes.
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
    # Draw the scatter plot and marginals.
    return scatter_hist_for_2d_data(x, y, ax, ax_histx, ax_histy, x_label, y_label, outlier_bool = outlier_bool)

### End of helper functions