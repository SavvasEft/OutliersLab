import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


##################################



###################################


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

def get_initial_1d_graphs(data_np):
    "data: np.array"
    fig, axs = plt.subplots(2,1)
    axs[0].plot(data_np)
    axs[1].hist(data_np, bins='fd')

    axs[0].title.set_text('Values Overview')
    axs[0].set_xlabel('Numbered labels')
    axs[0].set_ylabel('Point Values')
    
    axs[1].title.set_text('Values histogram')
    axs[1].set_xlabel('Point Values')
    axs[1].set_ylabel('Counts')
    plt.subplots_adjust(hspace=0.5)
    return fig

def get_joint_plot_for_2d_data(data_df:pd.DataFrame = None, x_label = None, y_label = None):
    fig = sns.jointplot(data = data_df,
            x = data_df.columns[0],
            y = data_df.columns[1], 
            marker = "o")
    if x_label is not None:
        fig.ax_joint.set_xlabel(x_label)

    if y_label is not None:
        fig.ax_joint.set_ylabel(y_label)


    fig.fig.suptitle('2d data distributions', fontsize=16)
    fig.fig.subplots_adjust(top=0.95)

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
  
    ax.scatter(x, y, color=colors)
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



def draw_scatter_plot_2d(data, outlier_bool=None, title = None, 
                         x_label = None, y_label = None):

    if title is None:
        title = 'Outliers Found'
    if x_label is None:
        x_label = 'Axes 1 Values'
    if y_label is None:
        y_label = 'Axes 2 Values'
        

    fig, ax = plt.subplots(1,1)
    ax.scatter(x=data[:,0], y=data[:,1], zorder=1)
    outlier_data = data[outlier_bool]
    ax.scatter(x=outlier_data[:,0],y=outlier_data[:,1], color = 'red', zorder=2)
    
    ax.title.set_text(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    
    ax.legend(["Point Values", "Outliers"], loc="lower right", prop={'size': 6})

    return fig

def draw_line_or_point_plot_1d(data, outlier_bool, line_plot = False, title = None):
    if title == None:
        title = 'Outliers Found'
    index = np.arange(len(data)).reshape(len(data),1)
    fig, ax = plt.subplots(1,1)

    if not line_plot:
        ax.scatter(x = index, y=data, zorder=1)
    else:
        ax.plot(data, zorder=1)
    ax.scatter(x = index[outlier_bool], y=data[outlier_bool], color  = 'red', zorder=2)
    
    ax.title.set_text(title)
    ax.set_xlabel('Numbered labels')
    ax.set_ylabel('Point Values')
    ax.legend(["Point Values", "Outliers"], loc="lower right", prop={'size': 6})
    
    return fig


def get_all_methods_outlier_array(data, methods_list):
    methods_outlier_masks_list = []
    for method in methods_list: 
        method_mask = method(data)
        methods_outlier_masks_list.append(method_mask)

    all_methods_outlier_masks_array = np.copy(methods_outlier_masks_list[0])
    if len(methods_list)>1:
        for i in range(1, len(methods_list)):
            all_methods_outlier_masks_array  = np.c_[all_methods_outlier_masks_array, \
                                               methods_outlier_masks_list[i]]

    return all_methods_outlier_masks_array




def get_outliers_report_and_global_outliers_mask(data, outlier_masks_list):
    # all_methods_outlier_masks_array = get_all_methods_outlier_array(data=data, \
    #                                             methods_list=methods_list)
    all_methods_outlier_masks_array = np.copy(outlier_masks_list[0])
    if len(outlier_masks_list)>1:
        for i in range(1, len(outlier_masks_list)):
            all_methods_outlier_masks_array  = np.c_[all_methods_outlier_masks_array, \
                                                     outlier_masks_list[i]]

    
    
    data_index = np.arange(len(data))       
    all_points_report_array = np.copy(data_index)

    if len(outlier_masks_list)>1:
        points_outlier_score = all_methods_outlier_masks_array.sum(axis=1) 
        global_outlier_mask = points_outlier_score>0   
        all_points_report_array = np.c_[all_points_report_array, points_outlier_score]
        all_points_report_array = np.c_[all_points_report_array, all_methods_outlier_masks_array]
        outlier_report_array = all_points_report_array[global_outlier_mask]
        return outlier_report_array, global_outlier_mask
    
    elif len(outlier_masks_list)==1:
        points_outlier_score = all_methods_outlier_masks_array
        global_outlier_mask = all_methods_outlier_masks_array>0
        all_points_report_array = np.c_[all_points_report_array, points_outlier_score]
        all_points_report_array = np.c_[all_points_report_array, all_methods_outlier_masks_array]
        outlier_report_array = all_points_report_array[global_outlier_mask]
        return outlier_report_array, global_outlier_mask
 
 
 
def describe_function(description):
    #decorator used in methods for attaching a string to each method
    def decorator(func):
        # Attach the description to the function
        func.description = description
        return func
    return decorator


def get_before_vs_after_plot(data, clean_data, data_dim):
    fig, axs = plt.subplots(2,1, sharex=True, sharey=True)
    if data_dim == 1:
        axs[0].plot(data)
        axs[1].plot(clean_data)

        axs[0].set_xlabel('Numbered labels')
        axs[1].set_xlabel('Numbered labels')
        axs[0].set_ylabel('Point Values')
        axs[1].set_ylabel('Point Values')

    elif data_dim == 2: 
        axs[0].scatter(data[:,0],data[:,1])
        axs[1].scatter(clean_data[:,0], clean_data[:,1])
        axs[0].set_xlabel('Axes 1 Values')
        axs[1].set_xlabel('Axes 1 Values')
        axs[0].set_ylabel('Axes 2 Values')
        axs[1].set_ylabel('Axes 2 Values')
    

    axs[0].title.set_text('Dirty data')
    axs[1].title.set_text('Clean data')
    
    plt.subplots_adjust(hspace=0.5)
    return fig   

def get_plot_with_1d_or_2d_data_with_mask(data, outliers_mask, title = None, line_plot=True):
    
    if data is None:
        print('eeeeeee')
 
    data_dimensions = data.shape[1]
    
    if data_dimensions is None: 
        data_dimensions=1

    if data_dimensions == 1:    
        plot = draw_line_or_point_plot_1d(data = data, outlier_bool = outliers_mask, \
                                            line_plot = line_plot,  \
                                            title = title)

    elif data_dimensions == 2:
        plot = draw_scatter_plot_2d(data = data, outlier_bool = outliers_mask, title = title )

    else:
        raise ValueError('Dimensions of data passed in graphs should be 1 or 2.')

    return plot