#!/usr/bin/env python

# PROGRAM: ocean_area.py
# ----------------------------------------------------------------------------------
# Version 0.2
# 8 June, 2019
# michael.taylor AT reading DOT ac DOT uk 

import numpy as np
import xarray
import seaborn as sns; sns.set(style="darkgrid")
import matplotlib
import matplotlib.pyplot as plt; plt.close("all")

def calc_land_frac(landsea_mask):
    '''
    Calc lat_fraction of  non-land [0.05 degree resolution] from landsea_mask:
    mask:source = "NAVOCEANO_landmask_v1.0 EUMETSAT_OSI-SAF_icemask ARCLake_\
lakemask"
    mask:comment = "water land lake ice"
    mask:flag_masks = 1b, 2b, 4b, 8b, 16b
    mask:summary = "OSTIA L4 product from the ESA SST CCI project, produced \
using OSTIA reanalysis sytem v3.0"
    '''

    ds = xarray.open_dataset('landsea_mask.nc')
    x = ds.lon
    y = ds.lat
    z = ds.mask

    ocean = z==1
    land = z==2
    sea_ice = z==9

    f = 1 - (np.sum(land[0,:,:],axis=1) / len(x)*1.)
    lat_fraction = np.array(f)

    lat_vec = np.array(y)
    dlat = 0.05

    return lat_vec, lat_fraction, dlat

def calc_water_frac(lat_vec, lat_fraction, dlat):
    '''
    Calc Earth surface area and ocean + sea ice vectors (latitudinal slices)
    
    The equation for the area of the Earth between a line of latitude and the north pole (the area of a spherical cap): A = 2*pi*R*h where R is the radius of the earth and h is the perpendicular distance from the plane containing the line of latitude to the pole. We can calculate h using trigonometry: h = R*(1-sin(lat)). The area north of a line of latitude is therefore: A = 2*pi*R^2(1-sin(lat)) with angles in radians (i.e. degrees * 2pi/360). The area between two lines of latitude is the difference between the area north of one latitude and the area north of the other latitude: A = |2*pi*R^2(1-sin(lat2)) - 2*pi*R^2(1-sin(lat1)) = 2*pi*R^2 |sin(lat1) - sin(lat2)
    '''

    R = 6371.0088 # Mean Earth radius [km]

    A = []
    N = len(lat_vec)
    for i in range(N):

        dA = 2. * np.pi * R**2.0 * np.absolute( np.sin(2*np.pi/360 * (lat_vec[i]+dlat/2)) - np.sin(2*np.pi/360 * (lat_vec[i]-dlat/2)))
        A.append(dA)

    surface_vec = np.array(A)
    ocean_vec = surface_vec * lat_fraction

    return surface_vec, ocean_vec

def plot(lat_vec, surface_vec, ocean_vec):

    ocean_area = 361900000.0 # Total ocean area from ETOPO1: https://ngdc.noaa.gov/mgg/global/etopo1_ocean_volumes.html
    FPE = 100. * (1.0 - np.sum(ocean_vec) / ocean_area)
    ocean_percent = 100. * (np.sum(ocean_vec) / np.sum(surface_vec))

    fig, ax = plt.subplots()
    plt.fill_between(surface_vec, lat_vec,  color='g', step="post", alpha=0.4)
    plt.fill_between(ocean_vec, lat_vec, color='b', step="post", alpha=0.4)
    plt.plot(surface_vec, lat_vec, color='g', drawstyle='steps-post', label='Earth surface area')
    plt.plot(ocean_vec, lat_vec, color='b', drawstyle='steps-post', label='Ocean + sea ice')
    ax = plt.gca()
    ax.set_xlim([-1000,250000])
    ax.set_ylim([-91,90])
    ticks = ax.get_yticks()
    ax.set_yticks(np.linspace(-90, 90, 7))
    plt.legend()
    plt.xlabel(r'Area / $km^{2}$')
    plt.ylabel(r'Latitude / $degrees$, N')
#    title_str = "NOAA ETOPO1: " + "{0:.3e}".format(ocean_area) + " L4 OSTIA: " + "{0:.3e}".format(np.sum(ocean_vec)) + " FPE=" + "{0:.3f}".format(FPE) + "%" + " Ocean+Ice=:" + "{0:.3f}".format(ocean_percent) + "%"
    title_str = "Ocean+sea ice=" + "{0:.3f}".format(ocean_percent) + "%"
    file_str = "ocean_area.png"
    plt.title(title_str, fontsize=12)
    fig.tight_layout()
    plt.savefig(file_str)

    return FPE, ocean_percent

if __name__ == "__main__":

    lat_vec, lat_fraction, dlat = calc_land_frac('landsea_mask.nc')
    surface_vec, ocean_vec = calc_water_frac(lat_vec, lat_fraction, dlat)    
    FPE, ocean_percent = plot(lat_vec, surface_vec, ocean_vec)

    print('FPE=', FPE, '%')
    print('% Ocean + Sea Ice=', ocean_percent, '%')
    print('** END')


