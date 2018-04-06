import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from pcl_helper import *


def rgb_to_hsv(rgb_list):
    rgb_normalized = [1.0*rgb_list[0]/255, 1.0*rgb_list[1]/255, 1.0*rgb_list[2]/255]
    hsv_normalized = matplotlib.colors.rgb_to_hsv([[rgb_normalized]])[0][0]
    return hsv_normalized

def histograms(color_list, bins, value_range):
    color_list = np.array(color_list)
    r_hist = np.histogram(color_list[:,0], bins=bins, range=value_range)
    g_hist = np.histogram(color_list[:,1], bins=bins, range=value_range)
    b_hist = np.histogram(color_list[:,2], bins=bins, range=value_range)

    rgb_hist = np.concatenate((r_hist[0], g_hist[0], b_hist[0])).astype(np.float64)
    norm_features = rgb_hist/( np.sum(rgb_hist)+ 0.001)

    return norm_features

def compute_color_histograms(cloud, bins, using_hsv=False):

    # Compute histograms for the clusters
    point_colors_list = []

    # Step through each point in the point cloud
    for point in pc2.read_points(cloud, skip_nans=True):
        rgb_list = float_to_rgb(point[3])
        if using_hsv:
            point_colors_list.append(rgb_to_hsv(rgb_list) * 255)
        else:
            point_colors_list.append(rgb_list)

    normed_features = histograms(point_colors_list, bins, (0, 256))

    return normed_features 


def compute_normal_histograms(normal_cloud, bins):

    norm_x_vals = []
    norm_y_vals = []
    norm_z_vals = []

    for norm_component in pc2.read_points(normal_cloud,
                                          field_names = ('normal_x', 'normal_y', 'normal_z'),
                                          skip_nans=True):
        norm_x_vals.append(norm_component[0])
        norm_y_vals.append(norm_component[1])
        norm_z_vals.append(norm_component[2])
 
    normed_features = histograms((norm_x_vals, norm_y_vals, norm_z_vals), bins, (-1, 1))

    return []
