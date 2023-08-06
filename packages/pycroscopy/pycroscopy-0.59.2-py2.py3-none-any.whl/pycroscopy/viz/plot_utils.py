# -*- coding: utf-8 -*-
"""
Created on Thu May 05 13:29:12 2016

@author: Suhas Somnath
"""
# TODO: All general plotting functions should support data with 1, 2, or 3 spatial dimensions.

from __future__ import division, print_function, absolute_import, unicode_literals

import inspect
from warnings import warn
import os
import sys
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.signal import blackman
import ipywidgets as widgets
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import ImageGrid
from ..io.hdf_utils import reshape_to_Ndims, get_formatted_labels, get_data_descriptor

# mpl.rcParams.keys()  # gets all allowable keys
mpl.rc('figure', figsize=(5,5))
mpl.rc('lines', linewidth=2)
mpl.rc('axes', labelsize=16, titlesize=16)
mpl.rc('figure', titlesize=20)
mpl.rc('font', size=14) # global font size
mpl.rc('legend', fontsize=16, fancybox=True)
mpl.rc('xtick.major', size=6)
mpl.rc('xtick.minor', size=4)
# mpl.rcParams['xtick.major.size'] = 6

if sys.version_info.major == 3:
    unicode = str

default_cmap = plt.cm.viridis

def set_tick_font_size(axes, font_size):
    """
    Sets the font size of the ticks in the provided axes

    Parameters
    ----------
    axes : matplotlib.pyplot.axis object or list of axis objects
        axes to set font sizes
    font_size : unigned int
        Font size
    """

    def __set_axis_tick(axis):
        """
        Sets the font sizes to the x and y axis in the given axis object

        Parameters
        ----------
        axis : matplotlib.pyplot.axis object
            axis to set font sizes
        """
        for tick in axis.xaxis.get_major_ticks():
            tick.label.set_fontsize(font_size)
        for tick in axis.yaxis.get_major_ticks():
            tick.label.set_fontsize(font_size)

    if hasattr(axes, '__iter__'):
        for axis in axes:
            __set_axis_tick(axis)
    else:
        __set_axis_tick(axes)


def make_scalar_mappable(vmin, vmax, cmap=None):
    """
    Creates a scalar mappable object that can be used to create a colorbar for non-image (e.g. - line) plots

    Parameters
    ----------
    vmin : float
        Minimum value for colorbar
    vmax : float
        Maximum value for colorbar
    cmap : colormap object
        Colormap object to use

    Returns
    -------
    sm : matplotlib.pyplot.cm.ScalarMappable object
        The object that can used to create a colorbar via plt.colorbar(sm)
    """
    if cmap is None:
        cmap = default_cmap

    sm = plt.cm.ScalarMappable(cmap=cmap,
                               norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # fake up the array of the scalar mappable
    sm._A = []
    return sm


def get_cmap_object(cmap):
    """
    Get the matplotlib.colors.LinearSegmentedColormap object regardless of the input

    Parameters
    ----------
    cmap : String, or matplotlib.colors.LinearSegmentedColormap object (Optional)
        Requested color map
    Returns
    -------
    cmap : matplotlib.colors.LinearSegmentedColormap object
        Requested / Default colormap object
    """
    if cmap is None:
        return default_cmap
    elif isinstance(cmap, str):
        return plt.get_cmap(cmap)
    return cmap


def cmap_jet_white_center():
    """
    Generates the jet colormap with a white center

    Returns
    -------
    white_jet : matplotlib.colors.LinearSegmentedColormap object
        color map object that can be used in place of the default colormap
    """
    # For red - central column is like brightness
    # For blue - last column is like brightness
    cdict = {'red': ((0.00, 0.0, 0.0),
                     (0.30, 0.0, 0.0),
                     (0.50, 1.0, 1.0),
                     (0.90, 1.0, 1.0),
                     (1.00, 0.5, 1.0)),
             'green': ((0.00, 0.0, 0.0),
                       (0.10, 0.0, 0.0),
                       (0.42, 1.0, 1.0),
                       (0.58, 1.0, 1.0),
                       (0.90, 0.0, 0.0),
                       (1.00, 0.0, 0.0)),
             'blue': ((0.00, 0.0, 0.5),
                      (0.10, 1.0, 1.0),
                      (0.50, 1.0, 1.0),
                      (0.70, 0.0, 0.0),
                      (1.00, 0.0, 0.0))
             }
    return LinearSegmentedColormap('white_jet', cdict)

def cmap_from_rgba(name, interp_vals, normalization_val):
    """
    Generates a colormap given a matlab-style interpolation table

    Parameters
    ----------
    name : String / Unicode
        Name of the desired colormap
    interp_vals : List of tuples
        Interpolation table that describes the desired color map. Each entry in the table should be described as:
        (position in the colorbar, (red, green, blue, alpha))
        The position in the color bar, red, green, blue, and alpha vary from 0 to the normalization value
    normalization_val : number
        The common maximum value for the position in the color bar, red, green, blue, and alpha

    Returns
    -------
    new_cmap : matplotlib.colors.LinearSegmentedColormap object
        desired color map
    """

    normalization_val = np.round(1.0 * normalization_val)

    cdict = {'red': tuple([(dist / normalization_val, colors[0] / normalization_val, colors[0] / normalization_val)
                           for (dist, colors) in interp_vals][::-1]),
             'green': tuple([(dist / normalization_val, colors[1] / normalization_val, colors[1] / normalization_val)
                             for (dist, colors) in interp_vals][::-1]),
             'blue': tuple([(dist / normalization_val, colors[2] / normalization_val, colors[2] / normalization_val)
                            for (dist, colors) in interp_vals][::-1]),
             'alpha': tuple([(dist / normalization_val, colors[3] / normalization_val, colors[3] / normalization_val)
                             for (dist, colors) in interp_vals][::-1])}

    return LinearSegmentedColormap(name, cdict)


def make_linear_alpha_cmap(name, solid_color, normalization_val, min_alpha=0, max_alpha=1):
    """
    Generates a transparent to opaque color map based on a single solid color

    Parameters
    ----------
    name : String / Unicode
        Name of the desired colormap
    solid_color : List of numbers
        red, green, blue, and alpha values for a specific color
    normalization_val : number
        The common maximum value for the red, green, blue, and alpha values. This is 1 in matplotlib
    min_alpha : float (optional. Default = 0 : ie- transparent)
        Lowest alpha value for the bottom of the color bar
    max_alpha : float (optional. Default = 1 : ie- opaque)
        Highest alpha value for the top of the color bar

    Returns
    -------
    new_cmap : matplotlib.colors.LinearSegmentedColormap object
        transparent to opaque color map based on the provided color
    """
    solid_color = np.array(solid_color) / normalization_val * 1.0
    interp_table = [(1.0, (solid_color[0], solid_color[1], solid_color[2], max_alpha)),
                    (0, (solid_color[0], solid_color[1], solid_color[2], min_alpha))]
    return cmap_from_rgba(name, interp_table, 1)


def cmap_hot_desaturated():
    """
    Returns a desaturated color map based on the hot colormap

    Returns
    -------
    new_cmap : matplotlib.colors.LinearSegmentedColormap object
        Desaturated version of the hot color map
    """
    hot_desaturated = [(255.0, (255, 76, 76, 255)),
                       (218.5, (107, 0, 0, 255)),
                       (182.1, (255, 96, 0, 255)),
                       (145.6, (255, 255, 0, 255)),
                       (109.4, (0, 127, 0, 255)),
                       (72.675, (0, 255, 255, 255)),
                       (36.5, (0, 0, 91, 255)),
                       (0, (71, 71, 219, 255))]

    return cmap_from_rgba('hot_desaturated', hot_desaturated, 255)


def discrete_cmap(num_bins, base_cmap=default_cmap):
    """
    Create an N-bin discrete colormap from the specified input map

    Parameters
    ----------
    num_bins : unsigned int
        Number of discrete bins
    base_cmap : matplotlib.colors.LinearSegmentedColormap object
        Base color map to discretize

    Returns
    -------
    new_cmap : String or matplotlib.colors.LinearSegmentedColormap object
        Discretized color map

    Notes
    -----
    Jake VanderPlas License: BSD-style
    https://gist.github.com/jakevdp/91077b0cae40f8f8244a

    """
    if base_cmap is None:
        base_cmap = default_cmap.name

    elif isinstance(base_cmap, type(default_cmap)):
        base_cmap = base_cmap.name

    if type(base_cmap) == str:
        return plt.get_cmap(base_cmap, num_bins)

    return base_cmap


def _add_loop_parameters(axes, switching_coef_vec):
    """
    Add the loop parameters for the given loop to a list of axes

    Parameters
    ----------
    axes : list of matplotlib.pyplo.axes
        Plot axes to add the coeffients to
    switching_coef_vec : 1D numpy.ndarray
        Array of loop parameters arranged by position

    Returns
    -------
    axes : list of matplotlib.pyplo.axes
    """
    positions = np.linspace(0, switching_coef_vec.shape[0] - 1, len(axes.flat), dtype=np.int)

    for ax, pos in zip(axes.flat, positions):
        ax.axvline(switching_coef_vec[pos]['V+'], c='k', label='V+')
        ax.axvline(switching_coef_vec[pos]['V-'], c='r', label='V-')
        ax.axvline(switching_coef_vec[pos]['Nucleation Bias 1'], c='k', ls=':', label='Nucleation Bias 1')
        ax.axvline(switching_coef_vec[pos]['Nucleation Bias 2'], c='r', ls=':', label='Nucleation Bias 2')
        ax.axhline(switching_coef_vec[pos]['R+'], c='k', ls='-.', label='R+')
        ax.axhline(switching_coef_vec[pos]['R-'], c='r', ls='-.', label='R-')

    return axes


def rainbow_plot(ax, ao_vec, ai_vec, num_steps=32, cmap=default_cmap, **kwargs):
    """
    Plots the input against the output waveform (typically loops).
    The color of the curve changes as a function of time using the jet colorscheme

    Parameters
    ----------
    ax : axis handle
        Axis to plot the curve
    ao_vec : 1D float numpy array
        vector that forms the X axis
    ai_vec : 1D float numpy array
        vector that forms the Y axis
    num_steps : unsigned int (Optional)
        Number of discrete color steps
    cmap : matplotlib.colors.LinearSegmentedColormap object
        Colormap to be used
    """
    cmap = get_cmap_object(cmap)

    pts_per_step = int(len(ai_vec) / num_steps)
    for step in range(num_steps - 1):
        ax.plot(ao_vec[step * pts_per_step:(step + 1) * pts_per_step],
                ai_vec[step * pts_per_step:(step + 1) * pts_per_step],
                color=cmap(255 * step / num_steps), **kwargs)
    # plot the remainder:
    ax.plot(ao_vec[(num_steps - 1) * pts_per_step:],
            ai_vec[(num_steps - 1) * pts_per_step:],
            color=cmap(255 * num_steps / num_steps), **kwargs)
    """
    CS3=plt.contourf([[0,0],[0,0]], range(0,310),cmap=plt.cm.viridis)
    fig.colorbar(CS3)"""


def plot_line_family(axis, x_axis, line_family, line_names=None, label_prefix='Line', label_suffix='',
                     cmap=default_cmap, y_offset=0, **kwargs):
    """
    Plots a family of lines with a sequence of colors

    Parameters
    ----------
    axis : axis handle
        Axis to plot the curve
    x_axis : array-like
        Values to plot against
    line_family : 2D numpy array
        family of curves arranged as [curve_index, features]
    line_names : array-like
        array of string or numbers that represent the identity of each curve in the family
    label_prefix : string / unicode
        prefix for the legend (before the index of the curve)
    label_suffix : string / unicode
        suffix for the legend (after the index of the curve)
    cmap : matplotlib.colors.LinearSegmentedColormap object
        Colormap to be used
    y_offset : (optional) number
        quantity by which the lines are offset from each other vertically (useful for spectra)
    """
    cmap = get_cmap_object(cmap)

    num_lines = line_family.shape[0]

    if line_names is None:
        line_names = ['{} {} {}'.format(label_prefix, line_ind, label_suffix) for line_ind in range(num_lines)]
    else:
        if len(line_names) != num_lines:
            warn('Line names of different length compared to provided dataset')
            line_names = ['{} {} {}'.format(label_prefix, line_ind, label_suffix) for line_ind in range(num_lines)]

    for line_ind in range(num_lines):
        axis.plot(x_axis, line_family[line_ind] + line_ind * y_offset,
                  label=line_names[line_ind],
                  color=cmap(int(255 * line_ind / (num_lines - 1))), **kwargs)


def plot_map(axis, data, stdevs=None, origin='lower', **kwargs):
    """
    Plots a 2d map with a tight z axis, with or without color bars.
    Note that the direction of the y axis is flipped if the color bar is required

    Parameters
    ----------
    axis : matplotlib.pyplot.axis object
        Axis to plot this map onto
    data : 2D real numpy array
        Data to be plotted
    stdevs : unsigned int (Optional. Default = None)
        Number of standard deviations to consider for plotting.  If None, full range is plotted.
    origin : str
        Where should the origin of the image data be located.  'lower' sets the origin to the
        bottom left, 'upper' sets it to the upper left.
        Default 'lower'

    Returns
    -------
    """
    if stdevs is not None:
        data_mean = np.mean(data)
        data_std = np.std(data)
        plt_min = data_mean - stdevs * data_std
        plt_max = data_mean + stdevs * data_std
    else:
        plt_min = np.min(data)
        plt_max = np.max(data)

    im = axis.imshow(data, interpolation='none',
                     vmin=plt_min,
                     vmax=plt_max,
                     origin=origin,
                     **kwargs)

    return im


def single_img_cbar_plot(axis, img, show_xy_ticks=True, show_cbar=True, x_size=1, y_size=1, num_ticks=4,
                         cbar_label=None, tick_font_size=14, **kwargs):
    """
    Plots an image within the given axis with a color bar + label and appropriate X, Y tick labels.
    This is particularly useful to get readily interpretable plots for papers

    Parameters
    ----------
    axis : matplotlib.axis object
        Axis to plot this image onto
    img : 2D numpy array with real values
        Data for the image plot
    show_xy_ticks : bool, Optional, default = None, shown unedited
        Whether or not to show X, Y ticks
    show_cbar : bool, optional, default = True
        Whether or not to show the colorbar
    x_size : float, optional, default = 1
        Extent of tick marks in the X axis. This could be something like 1.5 for 1.5 microns
    y_size : float, optional, default = 1
        Extent of tick marks in y axis
    num_ticks : unsigned int, optional, default = 4
        Number of tick marks on the X and Y axes
    cbar_label : str, optional, default = None
        Labels for the colorbar. Use this for something like quantity (units)
    tick_font_size : unsigned int, optional, default = 14
        Font size to apply to x, y, colorbar ticks and colorbar label
    kwargs : dictionary
        Anything else that will be passed on to plot_map or imshow

    Returns
    -------
    im_handle : handle to image plot
        handle to image plot
    cbar : handle to color bar
        handle to color bar
    """
    if 'clim' not in kwargs:
        im_handle = plot_map(axis, img, **kwargs)
    else:
        im_handle = axis.imshow(img, origin='lower', **kwargs)

    if show_xy_ticks is True:
        x_ticks = np.linspace(0, img.shape[1] - 1, num_ticks, dtype=int)
        y_ticks = np.linspace(0, img.shape[0] - 1, num_ticks, dtype=int)
        axis.set_xticks(x_ticks)
        axis.set_yticks(y_ticks)
        axis.set_xticklabels([str(np.round(ind * x_size / (img.shape[1] - 1), 2)) for ind in x_ticks])
        axis.set_yticklabels([str(np.round(ind * y_size / (img.shape[0] - 1), 2)) for ind in y_ticks])
        set_tick_font_size(axis, tick_font_size)
    elif show_xy_ticks is False:
        axis.set_xticks([])
        axis.set_yticks([])
    else:
        set_tick_font_size(axis, tick_font_size)

    cbar = None
    if show_cbar:
        # cbar = fig.colorbar(im_handle, ax=axis)
        # divider = make_axes_locatable(axis)
        # cax = divider.append_axes('right', size='5%', pad=0.05)
        # cbar = plt.colorbar(im_handle, cax=cax)
        cbar = plt.colorbar(im_handle, ax=axis, orientation='vertical',
                            fraction=0.046, pad=0.04, use_gridspec=True)
        if cbar_label is not None:
            cbar.set_label(cbar_label, fontsize=tick_font_size)
        """
        z_lims = cbar.get_clim()
        cbar.set_ticks(np.linspace(z_lims[0],z_lims[1], num_ticks))
        """
        cbar.ax.tick_params(labelsize=tick_font_size)
    return im_handle, cbar


def plot_loops(excit_wfm, datasets, line_colors=[], dataset_names=[], evenly_spaced=True,
               plots_on_side=5, x_label='', y_label='', subtitles='Position', title='',
               central_resp_size=None, use_rainbow_plots=False, h5_pos=None):
    # TODO: Allow multiple excitation waveforms
    """
    Plots loops from multiple datasets from up to 25 evenly spaced positions

    Parameters
    -----------
    excit_wfm : 1D numpy float array
        Excitation waveform in the time domain
    datasets : list of 2D numpy arrays or 2D hyp5.Dataset objects
        Datasets containing data arranged as (pixel, time)
    line_colors : list of strings
        Colors to be used for each of the datasets
    dataset_names : (Optional) list of strings
        Names of the different datasets to be compared
    h5_pos : HDF5 dataset reference or 2D numpy array
        Dataset containing position indices
    central_resp_size : (optional) unsigned integer
        Number of responce sample points from the center of the waveform to show in plots. Useful for SPORC
    evenly_spaced : boolean
        Evenly spaced positions or first N positions
    plots_on_side : unsigned int
        Number of plots on each side
    use_rainbow_plots : (optional) Boolean
        Plot the lines as a function of spectral index (eg. time)
    x_label : (optional) String
        X Label for all plots
    y_label : (optional) String
        Y label for all plots
    subtitles : (optional) String
        prefix for title over each plot
    title : (optional) String
        Main plot title

    Returns
    ---------
    fig, axes
    """
    if type(datasets) in [h5py.Dataset, np.ndarray]:
        # can be numpy array or h5py.dataset
        num_pos = datasets.shape[0]
        num_points = datasets.shape[1]
        datasets = [datasets]
        line_colors = ['b']
        dataset_names = ['Default']
    else:
        # First check if the datasets are correctly shaped:
        num_pos_es = list()
        num_points_es = list()
        for dataset in datasets:
            num_pos_es.append(dataset.shape[0])
            num_points_es.append(dataset.shape[1])
        num_pos_es = np.array(num_pos_es)
        num_points_es = np.array(num_points_es)
        if np.unique(num_pos_es).size > 1 or np.unique(num_points_es).size > 1:
            warn('Datasets of incompatible sizes')
            return
        num_pos = np.unique(num_pos_es)[0]
        num_points = np.unique(num_points_es)[0]

        # Next the identification of datasets:
        if len(dataset_names) > len(datasets):
            # remove additional titles
            dataset_names = dataset_names[:len(datasets)]
        elif len(dataset_names) < len(datasets):
            # add titles
            dataset_names = dataset_names + ['Dataset' + ' ' + str(x) for x in range(len(dataset_names), len(datasets))]
        if len(line_colors) != len(datasets):
            color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'pink', 'brown', 'orange']
            if len(datasets) < len(color_list):
                remaining_colors = [x for x in color_list if x not in line_colors]
                line_colors += remaining_colors[:len(datasets) - len(color_list)]
            else:
                warn('Insufficient number of line colors provided')
                return

    if excit_wfm.size != num_points:
        warn('Length of excitation waveform not compatible with second axis of datasets')
        return

    plots_on_side = min(abs(plots_on_side), 5)

    sq_num_plots = min(plots_on_side, int(round(num_pos ** 0.5)))
    if evenly_spaced:
        chosen_pos = np.linspace(0, num_pos - 1, sq_num_plots ** 2, dtype=int)
    else:
        chosen_pos = np.arange(sq_num_plots ** 2, dtype=int)

    fig, axes = plt.subplots(nrows=sq_num_plots, ncols=sq_num_plots, sharex=True, figsize=(12, 12))
    axes_lin = axes.flatten()

    cent_ind = int(0.5 * excit_wfm.size)
    if central_resp_size:
        sz = int(0.5 * central_resp_size)
        l_resp_ind = cent_ind - sz
        r_resp_ind = cent_ind + sz
    else:
        l_resp_ind = 0
        r_resp_ind = excit_wfm.size

    for count, posn in enumerate(chosen_pos):
        if use_rainbow_plots and len(datasets) == 1:
            rainbow_plot(axes_lin[count], excit_wfm[l_resp_ind:r_resp_ind], datasets[0][posn, l_resp_ind:r_resp_ind])
        else:
            for dataset, col_val in zip(datasets, line_colors):
                axes_lin[count].plot(excit_wfm[l_resp_ind:r_resp_ind], dataset[posn, l_resp_ind:r_resp_ind],
                                     color=col_val)
        if h5_pos is not None:
            # print('Row ' + str(h5_pos[posn,1]) + ' Col ' + str(h5_pos[posn,0]))
            axes_lin[count].set_title('Row ' + str(h5_pos[posn, 1]) + ' Col ' + str(h5_pos[posn, 0]), fontsize=12)
        else:
            axes_lin[count].set_title(subtitles + ' ' + str(posn), fontsize=12)

        if count % sq_num_plots == 0:
            axes_lin[count].set_ylabel(y_label, fontsize=12)
        if count >= (sq_num_plots - 1) * sq_num_plots:
            axes_lin[count].set_xlabel(x_label, fontsize=12)
        axes_lin[count].axis('tight')
        axes_lin[count].set_aspect('auto')
        axes_lin[count].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    if len(datasets) > 1:
        axes_lin[count].legend(dataset_names, loc='best')
    if title:
        fig.suptitle(title, fontsize=14, y=1.05)
    plt.tight_layout()
    return fig, axes


###############################################################################


def plot_complex_map_stack(map_stack, num_comps=4, title='Eigenvectors', xlabel='UDVS Step', stdevs=2,
                           cmap=default_cmap):
    """
    Plots the provided spectrograms from SVD V vector

    Parameters
    -------------
    map_stack : 3D numpy complex matrices
        Eigenvectors rearranged as - [row, col, component]
    num_comps : int
        Number of components to plot
    title : String
        Title to plot above everything else
    xlabel : String
        Label for x axis
    stdevs : int
        Number of standard deviations to consider for plotting
    cmap : String, or matplotlib.colors.LinearSegmentedColormap object (Optional)
        Requested color map

    Returns
    ---------
    fig, axes
    """
    cmap = get_cmap_object(cmap)

    fig201, axes201 = plt.subplots(2, num_comps, figsize=(4 * num_comps, 8))
    fig201.subplots_adjust(hspace=0.4, wspace=0.4)
    fig201.canvas.set_window_title(title)

    for index in range(num_comps):
        cur_map = np.transpose(map_stack[index, :, :])
        axes = [axes201.flat[index], axes201.flat[index + num_comps]]
        funcs = [np.abs, np.angle]
        labels = ['Amplitude', 'Phase']
        for func, lab, ax in zip(funcs, labels, axes):
            amp_mean = np.mean(func(cur_map))
            amp_std = np.std(func(cur_map))
            ax.imshow(func(cur_map), cmap=cmap,
                      vmin=amp_mean - stdevs * amp_std,
                      vmax=amp_mean + stdevs * amp_std)
            ax.set_title('Eigenvector: %d - %s' % (index + 1, lab))
            ax.set_aspect('auto')
        ax.set_xlabel(xlabel)

    return fig201, axes201


###############################################################################

def plot_complex_loop_stack(loop_stack, x_axis, heading='BE Loops', subtitle='Eigenvector', num_comps=4, x_label=''):
    """
    Plots the provided spectrograms from SVD V vector

    Parameters
    -------------
    loop_stack : 3D numpy complex matrices
        Loops rearranged as - [component, points]
    x_axis : 1D real numpy array
        The vector to plot against
    heading : str
        Title to plot above everything else
    subtitle : str
        Subtile to of Figure
    num_comps : int
        Number of components to plot
    x_label : str
        Label for x axis

    Returns
    ---------
    fig, axes
    """
    funcs = [np.abs, np.angle]
    labels = ['Amplitude', 'Phase']

    fig201, axes201 = plt.subplots(len(funcs), num_comps, figsize=(num_comps * 4, 4 * len(funcs)))
    fig201.subplots_adjust(hspace=0.4, wspace=0.4)
    fig201.canvas.set_window_title(heading)

    for index in range(num_comps):
        cur_map = loop_stack[index, :]
        axes = [axes201.flat[index], axes201.flat[index + num_comps]]
        for func, lab, ax in zip(funcs, labels, axes):
            ax.plot(x_axis, func(cur_map))
            ax.set_title('%s: %d - %s' % (subtitle, index + 1, lab))
        ax.set_xlabel(x_label)
    fig201.tight_layout()

    return fig201, axes201


###############################################################################


def plotScree(scree, title='Scree'):
    """
    Plots the scree or scree

    Parameters
    -------------
    scree : 1D real numpy array
        The scree vector from SVD
    title : str
        Figure title.  Default Scree

    Returns
    ---------
    fig, axes
    """
    fig203 = plt.figure(figsize=(6.5, 6))
    axes203 = fig203.add_axes([0.1, 0.1, .8, .8])  # left, bottom, width, height (range 0 to 1)
    axes203.loglog(np.arange(len(scree)) + 1, scree, 'b', marker='*')
    axes203.set_xlabel('Principal Component')
    axes203.set_ylabel('Variance')
    axes203.set_title(title)
    axes203.set_xlim(left=1, right=len(scree))
    axes203.set_ylim(bottom=np.min(scree), top=np.max(scree))
    fig203.canvas.set_window_title("Scree")

    return fig203, axes203


# ###############################################################################


def plot_map_stack(map_stack, num_comps=9, stdevs=2, color_bar_mode=None, evenly_spaced=False, reverse_dims=True,
                   title='Component', heading='Map Stack', colorbar_label='', fig_mult=(5, 5), pad_mult=(0.1, 0.07),
                   **kwargs):
    """
    Plots the provided stack of maps

    Parameters
    -------------
    map_stack : 3D real numpy array
        structured as [component, rows, cols]
    num_comps : unsigned int
        Number of components to plot
    stdevs : int
        Number of standard deviations to consider for plotting
    color_bar_mode : String, Optional
        Options are None, single or each. Default None
    evenly_spaced : bool
        Default False
    reverse_dims : Boolean (Optional)
        Set this to False to accept data structured as [component, rows, cols]
    title : String or list of strings
        The titles for each of the plots.
        If a single string is provided, the plot titles become ['title 01', title 02', ...].
        if a list of strings (equal to the number of components) are provided, these are used instead.
    heading : String
        ###Insert description here### Default 'Map Stack'
    colorbar_label : String
        label for colorbar. Default is an empty string.
    fig_mult : length 2 array_like of uints
        Size multipliers for the figure.  Figure size is calculated as (num_rows*`fig_mult[0]`, num_cols*`fig_mult[1]`).
        Default (4, 4)
    pad_mult : length 2 array_like of floats
        Multipliers for the axis padding between plots in the stack.  Padding is calculated as
        (pad_mult[0]*fig_mult[1], pad_mult[1]*fig_mult[0]) for the width and height padding respectively.
        Default (0.1, 0.07)
    kwargs : dictionary
        Keyword arguments to be passed to either matplotlib.pyplot.figure, mpl_toolkits.axes_grid1.ImageGrid, or
        pycroscopy.vis.plot_utils.plot_map.  See specific function documentation for the relavent options.

    Returns
    ---------
    fig, axes
    """
    if reverse_dims:
        map_stack = np.transpose(map_stack, (2, 0, 1))

    num_comps = abs(num_comps)
    num_comps = min(num_comps, map_stack.shape[0])

    if evenly_spaced:
        chosen_pos = np.linspace(0, map_stack.shape[0] - 1, num_comps, dtype=int)
    else:
        chosen_pos = np.arange(num_comps, dtype=int)

    if isinstance(title, list):
        if len(title) > num_comps:
            # remove additional titles
            title = title[:num_comps]
        elif len(title) < num_comps:
            # add titles
            title += ['Component' + ' ' + str(x) for x in range(len(title), num_comps)]
    else:
        if not isinstance(title, str):
            title = 'Component'
        title = [title + ' ' + str(x) for x in chosen_pos]

    fig_h, fig_w = fig_mult
    p_rows = int(np.floor(np.sqrt(num_comps)))
    p_cols = int(np.ceil(num_comps / p_rows))
    if p_rows * p_cols < num_comps:
        p_cols += 1

    pad_w, pad_h = pad_mult

    '''
    Set defaults for kwargs to the figure creation and extract any non-default values from current kwargs
    '''
    figkwargs = dict()

    if sys.version_info.major == 3:
        inspec_func = inspect.getfullargspec
    else:
        inspec_func = inspect.signature

    for key in inspec_func(plt.figure).args:
        if key in kwargs:
            figkwargs.update({key: kwargs.pop(key)})

    fig202 = plt.figure(figsize=(p_cols * fig_w, p_rows * fig_h), **figkwargs)

    '''
    Set defaults for kwargs to the ImageGrid and extract any non-default values from current kwargs
    '''
    igkwargs = {'cbar_pad': '1%',
                'cbar_size': '5%',
                'cbar_location': 'right',
                'direction': 'row',
                'add_all': True,
                'share_all': False,
                'aspect': True,
                'label_mode': 'L'}
    for key in igkwargs.keys():
        if key in kwargs:
            igkwargs.update({key: kwargs.pop(key)})

    axes202 = ImageGrid(fig202, 111, nrows_ncols=(p_rows, p_cols),
                        cbar_mode=color_bar_mode,
                        axes_pad=(pad_w * fig_w, pad_h * fig_h),
                        **igkwargs)
    fig202.canvas.set_window_title(heading)
    fig202.suptitle(heading, fontsize=16+(p_rows+ p_cols), y=0.9)

    for count, index, subtitle in zip(range(chosen_pos.size), chosen_pos, title):
        im = plot_map(axes202[count],
                      map_stack[index],
                      stdevs=stdevs, **kwargs)
        axes202[count].set_title(subtitle)
        if color_bar_mode is 'each':
            cb = axes202.cbar_axes[count].colorbar(im)
            cb.set_label_text(colorbar_label)
    if color_bar_mode is 'single':
        cb = axes202.cbar_axes[0].colorbar(im)
        cb.set_label_text(colorbar_label)
    return fig202, axes202


def plot_cluster_h5_group(h5_group, centroids_together=True, cmap=default_cmap):
    """
    Plots the cluster labels and mean response for each cluster

    Parameters
    ----------
    h5_group : h5py.Datagroup object
        H5 group containing the labels and mean response
    centroids_together : Boolean, optional - default = True
        Whether or nor to plot all centroids together on the same plot
    cmap : plt.cm object or str, optional
        Colormap to use for the labels map and the centroid.

    Returns
    -------
    fig : Figure
        Figure containing the plots
    axes : 1D array_like of axes objects
        Axes of the individual plots within `fig`
    """

    h5_labels = h5_group['Labels']
    try:
        h5_mean_resp = h5_group['Mean_Response']
    except KeyError:
        # old PySPM format:
        h5_mean_resp = h5_group['Centroids']

    # Reshape the mean response to N dimensions
    mean_response, success = reshape_to_Ndims(h5_mean_resp)

    # unfortunately, we cannot use the above function for the labels
    # However, we will assume that the position values are linked to the labels:
    h5_pos_vals = h5_labels.file[h5_labels.attrs['Position_Values']]
    h5_pos_inds = h5_labels.file[h5_labels.attrs['Position_Indices']]

    # Reshape the labels correctly:
    pos_dims = []
    for col in range(h5_pos_inds.shape[1]):
        pos_dims.append(np.unique(h5_pos_inds[:, col]).size)

    pos_ticks = [h5_pos_vals[:pos_dims[0], 0], h5_pos_vals[slice(0, None, pos_dims[0]), 1]]
    # prepare the axes ticks for the map

    pos_dims.reverse()  # go from slowest to fastest
    pos_dims = tuple(pos_dims)
    label_mat = np.reshape(h5_labels.value, pos_dims)

    # Figure out the correct units and labels for mean response:
    h5_spec_vals = h5_mean_resp.file[h5_mean_resp.attrs['Spectroscopic_Values']]
    x_spec_label = get_formatted_labels(h5_spec_vals)[0]

    # Figure out the correct axes labels for label map:
    pos_labels = get_formatted_labels(h5_pos_vals)

    y_spec_label = get_data_descriptor(h5_mean_resp)
    # TODO: cleaner x and y axes labels instead of 0.0000125 etc.

    if centroids_together:
        return plot_cluster_results_together(label_mat, mean_response, spec_val=np.squeeze(h5_spec_vals[0]),
                                             spec_label=x_spec_label, resp_label=y_spec_label,
                                             pos_labels=pos_labels, pos_ticks=pos_ticks, cmap=cmap)
    else:
        return plot_cluster_results_separate(label_mat, mean_response, max_centroids=4, x_label=x_spec_label,
                                             spec_val=np.squeeze(h5_spec_vals[0]), y_label=y_spec_label, cmap=cmap)


###############################################################################


def plot_cluster_results_together(label_mat, mean_response, spec_val=None, cmap=default_cmap,
                                  spec_label='Spectroscopic Value', resp_label='Response',
                                  pos_labels=('X', 'Y'), pos_ticks=None):
    """
    Plot the cluster labels and mean response for each cluster in separate plots

    Parameters
    ----------
    label_mat : 2D ndarray or h5py.Dataset of ints
        Spatial map of cluster labels structured as [rows, cols]
    mean_response : 2D array or h5py.Dataset
        Mean value of each cluster over all samples 
        arranged as [cluster number, features]
    spec_val :  1D array or h5py.Dataset of floats, optional
        X axis to plot the centroids against
        If no value is specified, the data is plotted against the index
    cmap : plt.cm object or str, optional
        Colormap to use for the labels map and the centroid.
        Advised to pick a map where the centroid plots show clearly.
        Default = matplotlib.pyplot.cm.jet
    spec_label : str, optional
        Label to use for X axis on cluster centroid plot
        Default = 'Spectroscopic Value'
    resp_label : str, optional
        Label to use for Y axis on cluster centroid plot
         Default = 'Response'
    pos_labels : array_like of str, optional
        Labels to use for the X and Y axes on the Label map
        Default = ('X', 'Y')
    pos_ticks : array_like of int

    Returns
    -------
    fig : Figure
        Figure containing the plots
    axes : 1D array_like of axes objects
        Axes of the individual plots within `fig`
    """
    cmap = get_cmap_object(cmap)

    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)

    def __plot_centroids(centroids, ax, spec_val, spec_label, y_label, cmap, title=None):
        plot_line_family(ax, spec_val, centroids, label_prefix='Cluster', cmap=cmap)
        ax.set_ylabel(y_label)
        # ax.legend(loc='best')
        if title:
            ax.set_title(title)
            ax.set_xlabel(spec_label)

    if spec_val is None:
        spec_val = np.arange(mean_response.shape[1])

    if mean_response.dtype in [np.complex64, np.complex128, np.complex]:
        fig = plt.figure(figsize=(12, 8))
        ax_map = plt.subplot2grid((2, 12), (0, 0), colspan=6, rowspan=2)
        ax_amp = plt.subplot2grid((2, 12), (0, 6), colspan=4)
        ax_phase = plt.subplot2grid((2, 12), (1, 6), colspan=4)
        axes = [ax_map, ax_amp, ax_phase]

        __plot_centroids(np.abs(mean_response), ax_amp, spec_val, spec_label,
                         resp_label + ' - Amplitude', cmap, 'Mean Response')
        __plot_centroids(np.angle(mean_response), ax_phase, spec_val, spec_label,
                         resp_label + ' - Phase', cmap)
        plot_handles, plot_labels = ax_amp.get_legend_handles_labels()

    else:
        fig = plt.figure(figsize=(12, 8))
        ax_map = plt.subplot2grid((1, 12), (0, 0), colspan=6)
        ax_resp = plt.subplot2grid((1, 12), (0, 6), colspan=4)
        axes = [ax_map, ax_resp]
        __plot_centroids(mean_response, ax_resp, spec_val, spec_label,
                         resp_label, cmap, 'Mean Response')
        plot_handles, plot_labels = ax_resp.get_legend_handles_labels()

    fleg = plt.figlegend(plot_handles, plot_labels, loc='center right',
                         borderaxespad=0.0)
    num_clusters = mean_response.shape[0]

    if isinstance(label_mat, h5py.Dataset):
        """
        Reshape label_mat based on linked positions
        """
        pos = label_mat.file[label_mat.attrs['Position_Indices']]
        nx = len(np.unique(pos[:, 0]))
        ny = len(np.unique(pos[:, 1]))
        label_mat = label_mat[()].reshape(nx, ny)

    # im = ax_map.imshow(label_mat, interpolation='none')
    ax_map.set_xlabel(pos_labels[0])
    ax_map.set_ylabel(pos_labels[1])

    if pos_ticks is not None:
        x_ticks = np.linspace(0, label_mat.shape[1] - 1, 5, dtype=np.uint16)
        y_ticks = np.linspace(0, label_mat.shape[0] - 1, 5, dtype=np.uint16)
        ax_map.set_xticks(x_ticks)
        ax_map.set_yticks(y_ticks)
        ax_map.set_xticklabels(pos_ticks[0][x_ticks])
        ax_map.set_yticklabels(pos_ticks[1][y_ticks])

    """divider = make_axes_locatable(ax_map)
    cax = divider.append_axes("right", size="5%", pad=0.05)  # space for colorbar
    fig.colorbar(im, cax=cax, ticks=np.arange(num_clusters),
                 cmap=discrete_cmap(num_clusters, base_cmap=plt.cm.viridis))
    ax_map.axis('tight')"""
    pcol0 = ax_map.pcolor(label_mat, cmap=discrete_cmap(num_clusters, base_cmap=cmap))
    fig.colorbar(pcol0, ax=ax_map, ticks=np.arange(num_clusters))
    ax_map.axis('tight')
    ax_map.set_aspect('auto')
    ax_map.set_title('Cluster Label Map')

    fig.tight_layout()
    fig.canvas.set_window_title('Cluster results')

    return fig, axes


###############################################################################


def plot_cluster_results_separate(label_mat, cluster_centroids, max_centroids=4, cmap=default_cmap,
                                  spec_val=None, x_label='Excitation (a.u.)', y_label='Response (a.u.)'):
    """
    Plots the provided labels mat and centroids from clustering

    Parameters
    ----------
    label_mat : 2D int numpy array
                structured as [rows, cols]
    cluster_centroids: 2D real numpy array
                       structured as [cluster,features]
    max_centroids : unsigned int
                    Number of centroids to plot
    cmap : plt.cm object or str, optional
        Colormap to use for the labels map and the centroids
    spec_val :  array-like
        X axis to plot the centroids against
        If no value is specified, the data is plotted against the index
    x_label : String / unicode
              X label for centroid plots
    y_label : String / unicode
              Y label for centroid plots

    Returns
    -------
    fig
    """

    cmap = get_cmap_object(cmap)

    if max_centroids < 5:

        fig501 = plt.figure(figsize=(20, 10))
        fax1 = plt.subplot2grid((2, 4), (0, 0), colspan=2, rowspan=2)
        fax2 = plt.subplot2grid((2, 4), (0, 2))
        fax3 = plt.subplot2grid((2, 4), (0, 3))
        fax4 = plt.subplot2grid((2, 4), (1, 2))
        fax5 = plt.subplot2grid((2, 4), (1, 3))
        fig501.tight_layout()
        axes_handles = [fax1, fax2, fax3, fax4, fax5]

    else:
        fig501 = plt.figure(figsize=(20, 10))
        # make subplot for cluster map
        fax1 = plt.subplot2grid((3, 6), (0, 0), colspan=3, rowspan=3)  # For cluster map
        fax1.set_xmargin(0.50)
        # make subplot for cluster centers
        fax2 = plt.subplot2grid((3, 6), (0, 3))
        fax3 = plt.subplot2grid((3, 6), (0, 4))
        fax4 = plt.subplot2grid((3, 6), (0, 5))
        fax5 = plt.subplot2grid((3, 6), (1, 3))
        fax6 = plt.subplot2grid((3, 6), (1, 4))
        fax7 = plt.subplot2grid((3, 6), (1, 5))
        fax8 = plt.subplot2grid((3, 6), (2, 3))
        fax9 = plt.subplot2grid((3, 6), (2, 4))
        fax10 = plt.subplot2grid((3, 6), (2, 5))
        fig501.tight_layout()
        axes_handles = [fax1, fax2, fax3, fax4, fax5, fax6, fax7, fax8, fax9, fax10]

    # First plot the labels map:
    pcol0 = fax1.pcolor(label_mat, cmap=discrete_cmap(cluster_centroids.shape[0], base_cmap=cmap))
    fig501.colorbar(pcol0, ax=fax1, ticks=np.arange(cluster_centroids.shape[0]))
    fax1.axis('tight')
    fax1.set_aspect('auto')
    fax1.set_title('Cluster Label Map')
    """im = fax1.imshow(label_mat, interpolation='none')
    divider = make_axes_locatable(fax1)
    cax = divider.append_axes("right", size="5%", pad=0.05)  # space for colorbar
    plt.colorbar(im, cax=cax)"""

    if spec_val is None and cluster_centroids.ndim == 2:
        spec_val = np.arange(cluster_centroids.shape[1])

    # Plot results
    for ax, index in zip(axes_handles[1: max_centroids + 1], np.arange(max_centroids)):
        if cluster_centroids.ndim == 2:
            ax.plot(spec_val, cluster_centroids[index, :],
                    color=cmap(int(255 * index / (cluster_centroids.shape[0] - 1))))
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
        elif cluster_centroids.ndim == 3:
            plot_map(ax, cluster_centroids[index])
        ax.set_title('Centroid: %d' % index)

    fig501.subplots_adjust(hspace=0.60, wspace=0.60)
    fig501.tight_layout()

    return fig501


###############################################################################

def plot_cluster_dendrogram(label_mat, e_vals, num_comp, num_cluster, mode='Full', last=None,
                            sort_type='distance', sort_mode=True):
    """
    Creates and plots the dendrograms for the given label_mat and
    eigenvalues

    Parameters
    -------------
    label_mat : 2D real numpy array
        structured as [rows, cols], from KMeans clustering
    e_vals: 3D real numpy array of eigenvalues
        structured as [component, rows, cols]
    num_comp : int
        Number of components used to make eigenvalues
    num_cluster : int
        Number of cluster used to make the label_mat
    mode: str, optional
        How should the dendrograms be created.
        "Full" -- use all clusters when creating the dendrograms
        "Truncated" -- stop showing clusters after 'last'
    last: int, optional - should be provided when using "Truncated"
        How many merged clusters should be shown when using
        "Truncated" mode
    sort_type: {'count', 'distance'}, optional
        What type of sorting should be used when plotting the
        dendrograms.  Options are:
        count - Uses the count_sort from scipy.cluster.hierachy.dendrogram
        distance - Uses the distance_sort from scipy.cluster.hierachy.dendrogram
    sort_mode: {False, True, 'ascending', 'descending'}, optional
        For the chosen sort_type, which mode should be used.
        False - Does no sorting
        'ascending' or True - The child with the minimum of the chosen sort
        parameter is plotted first
        'descending' - The child with the maximum of the chosen sort parameter is
        plotted first

    Returns
    ---------
    fig : matplotlib.pyplot Figure object
        Figure containing the dendrogram
    """
    if mode == 'Truncated' and not last:
        warn('Warning: Truncated dendrograms requested, but no last cluster given.  Reverting to full dendrograms.')
        mode = 'Full'

    if mode == 'Full':
        print('Creating full dendrogram from clusters')
        mode = None
    elif mode == 'Truncated':
        print('Creating truncated dendrogram from clusters.  Will stop at {}.'.format(last))
        mode = 'lastp'
    else:
        raise ValueError('Error: Unknown mode requested for plotting dendrograms. mode={}'.format(mode))

    c_sort = False
    d_sort = False
    if sort_type == 'count':
        c_sort = sort_mode
        if c_sort == 'descending':
            c_sort = 'descendent'
    elif sort_type == 'distance':
        d_sort = sort_mode

    centroid_mat = np.zeros([num_cluster, num_comp])
    for k1 in range(num_cluster):
        [i_x, i_y] = np.where(label_mat == k1)
        u_stack = np.zeros([len(i_x), num_comp])
        for k2 in range(len(i_x)):
            u_stack[k2, :] = np.abs(e_vals[i_x[k2], i_y[k2], :num_comp])

        centroid_mat[k1, :] = np.mean(u_stack, 0)

    # Get the distrance between cluster means
    distance_mat = scipy.spatial.distance.pdist(centroid_mat)

    # get hierachical pairings of clusters
    linkage_pairing = scipy.cluster.hierarchy.linkage(distance_mat, 'weighted')
    linkage_pairing[:, 3] = linkage_pairing[:, 3] / max(linkage_pairing[:, 3])

    fig = plt.figure()
    scipy.cluster.hierarchy.dendrogram(linkage_pairing, p=last, truncate_mode=mode,
                                       count_sort=c_sort, distance_sort=d_sort,
                                       leaf_rotation=90)

    fig.axes[0].set_title('Dendrogram')
    fig.axes[0].set_xlabel('Index or (cluster size)')
    fig.axes[0].set_ylabel('Distance')

    return fig


def plot_1d_spectrum(data_vec, freq, title, figure_path=None):
    """
    Plots the Step averaged BE response

    Parameters
    ------------
    data_vec : 1D numpy array
        Response of one BE pulse
    freq : 1D numpy array
        BE frequency that serves as the X axis of the plot
    title : String
        Plot group name
    figure_path : String / Unicode
        Absolute path of the file to write the figure to

    Returns
    ---------
    fig : Matplotlib.pyplot figure
        Figure handle
    ax : Matplotlib.pyplot axis
        Axis handle
    """
    if len(data_vec) != len(freq):
        warn('plot_1d_spectrum: Incompatible data sizes!!!!')
        print('1D:', data_vec.shape, freq.shape)
        return
    freq *= 1E-3  # to kHz
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax[0].plot(freq, np.abs(data_vec) * 1E+3)
    ax[0].set_title('Amplitude (mV)')
    ax[1].plot(freq, np.angle(data_vec) * 180 / np.pi)
    ax[1].set_title('Phase (deg)')
    ax[1].set_xlabel('Frequency (kHz)')
    fig.suptitle(title + ': mean UDVS, mean spatial response')
    if figure_path:
        plt.savefig(figure_path, format='png', dpi=300)
    return


###############################################################################

def plot_2d_spectrogram(mean_spectrogram, freq, title, figure_path=None, **kwargs):
    """
    Plots the position averaged spectrogram

    Parameters
    ------------
    mean_spectrogram : 2D numpy complex array
        Means spectrogram arranged as [frequency, UDVS step]
    freq : 1D numpy float array
        BE frequency that serves as the X axis of the plot
    title : String
        Plot group name
    figure_path : String / Unicode
        Absolute path of the file to write the figure to

    Returns
    ---------
    fig : Matplotlib.pyplot figure
        Figure handle
    ax : Matplotlib.pyplot axis
        Axis handle
    """
    if mean_spectrogram.shape[1] != len(freq):
        warn('plot_2d_spectrogram: Incompatible data sizes!!!!')
        print('2D:', mean_spectrogram.shape, freq.shape)
        return

    freq *= 1E-3  # to kHz
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    # print(mean_spectrogram.shape)
    # print(freq.shape)
    ax[0].imshow(np.abs(mean_spectrogram), interpolation='nearest',
                 extent=[freq[0], freq[-1], mean_spectrogram.shape[0], 0], **kwargs)
    ax[0].set_title('Amplitude')
    # ax[0].set_xticks(freq)
    # ax[0].set_ylabel('UDVS Step')
    ax[0].axis('tight')
    ax[1].imshow(np.angle(mean_spectrogram), interpolation='nearest',
                 extent=[freq[0], freq[-1], mean_spectrogram.shape[0], 0], **kwargs)
    ax[1].set_title('Phase')
    ax[1].set_xlabel('Frequency (kHz)')
    # ax[0].set_ylabel('UDVS Step')
    ax[1].axis('tight')
    fig.suptitle(title)
    if figure_path:
        plt.savefig(figure_path, format='png', dpi=300)
    return fig, ax


###############################################################################


def plot_histgrams(p_hist, p_hbins, title, figure_path=None):
    """
    Plots the position averaged spectrogram

    Parameters
    ------------
    p_hist : 2D numpy array
        histogram data arranged as [physical quantity, frequency bin]
    p_hbins : 1D numpy array
        BE frequency that serves as the X axis of the plot
    title : String
        Plot group name
    figure_path : String / Unicode
        Absolute path of the file to write the figure to

    Returns
    ---------
    fig : Matplotlib.pyplot figure
        Figure handle
    """

    base_fig_size = 7
    h_fig = base_fig_size
    w_fig = base_fig_size * 4

    fig = plt.figure(figsize=(w_fig, h_fig))
    fig.suptitle(title)
    iplot = 0

    p_Nx, p_Ny = np.amax(p_hbins, axis=1) + 1

    p_hist = np.reshape(p_hist, (4, p_Ny, p_Nx))

    iplot += 1
    p_plot_title = 'Spectral BEHistogram Amp (log10 of counts)'
    p_plot = fig.add_subplot(1, 4, iplot, title=p_plot_title)
    p_im = p_plot.imshow(np.rot90(np.log10(p_hist[0])), interpolation='nearest')
    p_plot.axis('tight')
    fig.colorbar(p_im, fraction=0.1)

    iplot += 1
    p_plot_title = 'Spectral BEHistogram Phase (log10 of counts)'
    p_plot = fig.add_subplot(1, 4, iplot, title=p_plot_title)
    p_im = p_plot.imshow(np.rot90(np.log10(p_hist[1])), interpolation='nearest')
    p_plot.axis('tight')
    fig.colorbar(p_im, fraction=0.1)

    iplot += 1
    p_plot_title = 'Spectral BEHistogram Real (log10 of counts)'
    p_plot = fig.add_subplot(1, 4, iplot, title=p_plot_title)
    p_im = p_plot.imshow(np.rot90(np.log10(p_hist[2])), interpolation='nearest')
    p_plot.axis('tight')
    fig.colorbar(p_im, fraction=0.1)

    iplot += 1
    p_plot_title = 'Spectral BEHistogram Imag (log10 of counts)'
    p_plot = fig.add_subplot(1, 4, iplot, title=p_plot_title)
    p_im = p_plot.imshow(np.rot90(np.log10(p_hist[3])), interpolation='nearest')
    p_plot.axis('tight')
    fig.colorbar(p_im, fraction=0.1)

    if figure_path:
        plt.savefig(figure_path, format='png')

    return fig


def plot_image_cleaning_results(raw_image, clean_image, stdevs=2, heading='Image Cleaning Results',
                                fig_mult=(4, 4), fig_args={}, **kwargs):
    """
    
    Parameters
    ----------
    raw_image
    clean_image
    stdevs
    fig_mult
    fig_args
    heading

    Returns
    -------

    """
    plot_args = {'cbar_pad': '2.0%', 'cbar_size': '4%', 'hor_axis_pad': 0.115, 'vert_axis_pad': 0.1,
                 'sup_title_size': 26, 'sub_title_size': 22, 'show_x_y_ticks': False, 'show_tick_marks': False,
                 'x_y_tick_font_size': 18, 'cbar_tick_font_size': 18}

    plot_args.update(fig_args)

    fig_h, fig_w = fig_mult
    p_rows = 2
    p_cols = 3

    fig_clean = plt.figure(figsize=(p_cols * fig_w, p_rows * fig_h))
    axes_clean = ImageGrid(fig_clean, 111, nrows_ncols=(p_rows, p_cols), cbar_mode='each',
                           cbar_pad=plot_args['cbar_pad'], cbar_size=plot_args['cbar_size'],
                           axes_pad=(plot_args['hor_axis_pad'] * fig_w, plot_args['vert_axis_pad'] * fig_h))
    fig_clean.canvas.set_window_title(heading)
    fig_clean.suptitle(heading, fontsize=plot_args['sup_title_size'])

    '''
    Calculate the removed noise and the FFT's of the raw, clean, and noise
    '''
    removed_noise = raw_image - clean_image
    blackman_window_rows = scipy.signal.blackman(clean_image.shape[0])
    blackman_window_cols = scipy.signal.blackman(clean_image.shape[1])

    FFT_raw = np.abs(np.fft.fftshift(
        np.fft.fft2(blackman_window_rows[:, np.newaxis] * raw_image * blackman_window_cols[np.newaxis, :]),
        axes=(0, 1)))
    FFT_clean = np.abs(np.fft.fftshift(
        np.fft.fft2(blackman_window_rows[:, np.newaxis] * clean_image * blackman_window_cols[np.newaxis, :]),
        axes=(0, 1)))
    FFT_noise = np.abs(np.fft.fftshift(
        np.fft.fft2(blackman_window_rows[:, np.newaxis] * removed_noise * blackman_window_cols[np.newaxis, :]),
        axes=(0, 1)))

    '''
    Now find the mean and standard deviation of the images
    '''
    raw_mean = np.mean(raw_image)
    clean_mean = np.mean(clean_image)
    noise_mean = np.mean(removed_noise)

    raw_std = np.std(raw_image)
    clean_std = np.std(clean_image)
    noise_std = np.std(removed_noise)
    fft_clean_std = np.std(FFT_clean)

    '''
    Make lists of everything needed to plot
    '''
    plot_names = ['Original Image', 'Cleaned Image', 'Removed Noise',
                  'FFT Original Image', 'FFT Cleaned Image', 'FFT Removed Noise']
    plot_data = [raw_image, clean_image, removed_noise, FFT_raw, FFT_clean, FFT_noise]
    plot_mins = [raw_mean - stdevs * raw_std, clean_mean - stdevs * clean_std, noise_mean - stdevs * noise_std, 0, 0, 0]
    plot_maxes = [raw_mean + stdevs * raw_std, clean_mean + stdevs * clean_std, noise_mean + stdevs * noise_std,
                  2 * stdevs * fft_clean_std, 2 * stdevs * fft_clean_std, 2 * stdevs * fft_clean_std]

    for count, ax, image, title, plot_min, plot_max in zip(range(6), axes_clean, plot_data,
                                                           plot_names, plot_mins, plot_maxes):
        im = plot_map(ax, image, stdevs, **kwargs)
        im.set_clim(vmin=plot_min, vmax=plot_max)
        axes_clean[count].set_title(title, fontsize=plot_args['sub_title_size'])
        cbar = axes_clean.cbar_axes[count].colorbar(im)
        cbar.ax.tick_params(labelsize=plot_args['cbar_tick_font_size'])

        if not plot_args['show_x_y_ticks']:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        if not plot_args['show_tick_marks']:
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)

    return fig_clean, axes_clean


def save_fig_filebox_button(fig, filename):
    """
    Create ipython widgets to allow the user to save a figure to the
    specified file.

    Parameters
    ----------
    fig : matplotlib.Figure
        The figure to be saved.
    filename : str
        The filename the figure should be saved to

    Returns
    -------
    widget_box : ipywidgets.HBox
        Widget box holding the text entry and save button

    """
    filename = os.path.abspath(filename)
    file_dir, filename = os.path.split(filename)

    name_box = widgets.Text(value=filename,
                            placeholder='Type something',
                            description='Output Filename:',
                            disabled=False,
                            layout={'width': '50%'})
    save_button = widgets.Button(description='Save figure')

    def _save_fig():
        save_path = os.path.join(file_dir, filename)
        fig.save_fig(save_path, dpi='figure')
        print('Figure saved to "{}".'.format(save_path))

    widget_box = widgets.HBox([name_box, save_button])

    save_button.on_click(_save_fig)

    return widget_box


def export_fig_data(fig, filename, include_images=False):
    """
    Export the data of all plots in the figure `fig` to a plain text file.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure containing the data to be exported
    filename : str
        The filename of the output text file
    include_images : bool
        Should images in the figure also be exported

    Returns
    -------

    """
    # Get the data from the figure
    axes = fig.get_axes()
    axes_dict = dict()
    for ax in axes:
        ax_dict = dict()

        ims = ax.get_images()
        if len(ims) != 0 and include_images:
            im_dict = dict()

            for im in ims:
                # Image data
                im_lab = im.get_label()
                im_dict[im_lab] = im.get_array().data

                # X-Axis
                x_ax = ax.get_xaxis()
                x_lab = x_ax.label.get_label()
                if x_lab == '':
                    x_lab = 'X'

                im_dict[im_lab + x_lab] = x_ax.get_data_interval()

                # Y-Axis
                y_ax = ax.get_yaxis()
                y_lab = y_ax.label.get_label()
                if y_lab == '':
                    y_lab = 'Y'

                im_dict[im_lab + y_lab] = y_ax.get_data_interval()

            ax_dict['Images'] = im_dict

        lines = ax.get_lines()
        if len(lines) != 0:
            line_dict = dict()

            xlab = ax.get_xlabel()
            ylab = ax.get_ylabel()

            if xlab == '':
                xlab = 'X Data'
            if ylab == '':
                ylab = 'Y Data'

            for line in lines:
                line_dict[line.get_label()] = {xlab: line.get_xdata(),
                                               ylab: line.get_ydata()}

            ax_dict['Lines'] = line_dict

        if ax_dict != dict():
            axes_dict[ax.get_title()] = ax_dict

    '''
    Now that we have the data from the figure, we need to write it to file.
    '''

    filename = os.path.abspath(filename)
    basename, ext = os.path.splitext(filename)
    folder, _ = os.path.split(basename)

    spacer = r'**********************************************\n'

    data_file = open(filename, 'w')

    data_file.write(fig.get_label() + '\n')
    data_file.write('\n')

    for ax_lab, ax in axes_dict.items():
        data_file.write('Axis: {} \n'.format(ax_lab))

        for im_lab, im in ax['Images'].items():
            data_file.write('Image: {} \n'.format(im_lab))
            data_file.write('\n')
            im_data = im.pop('data')
            for row in im_data:
                row.tofile(data_file, sep='\t', format='%s')
                data_file.write('\n')
            data_file.write('\n')

            for key, val in im.items():
                data_file.write(key + '\n')

                val.tofile(data_file, sep='\n', format='%s')
                data_file.write('\n')

            data_file.write(spacer)

        for line_lab, line_dict in ax['Lines'].items():
            data_file.write('Line: {} \n'.format(line_lab))
            data_file.write('\n')

            dim1, dim2 = line_dict.keys()

            data_file.write('{} \t {} \n'.format(dim1, dim2))
            for val1, val2 in zip(line_dict[dim1], line_dict[dim2]):
                data_file.write('{} \t {} \n'.format(str(val1), str(val2)))

            data_file.write(spacer)

        data_file.write(spacer)

    data_file.close()

    return
