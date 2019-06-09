![image](https://user-images.githubusercontent.com/5902974/59154328-fe0c6300-8a67-11e9-9261-4d79fcf8ee94.png)
<img alt="OCEAN_AREA" align="right" src="https://user-images.githubusercontent.com/5902974/59154328-fe0c6300-8a67-11e9-9261-4d79fcf8ee94.png">
                
# OCEAN_AREA

Development code for calculation of the latitudinal variation of ocean + sea ice area.

## Contents

* `ocean_area.py` - main script to be run with Python 3.6
* `landsea_mask.nc` - NAVOCEANO_landmask_v1.0 EUMETSAT_OSI-SAF_icemask ARCLake_lakemask
* `ocean_area.png` - example output figure

The first step is to clone latest OCEAN_AREA code and step into the check out directory: 

    $ git clone https://github.com/patternizer/OCEAN_AREA.git
    $ cd OCEAN_AREA
    
### Using Standard Python 

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and
was tested in a conda virtual environment running a 64-bit version of Python 3.6+.

OCEAN_AREA can be run from sources directly, once the following module requirements are resolved:

* `numpy`
* `xarray`
* `matplotlib`
* `seaborn`

Run with:

    $ python3 ocean_area.py
        
### Landsea_mask.nc

This is an OSTIA L4 product from the ESA SST CCI project produced using OSTIA reanalysis sytem v3.0.

## License

The code is distributed under terms and conditions of the [MIT license](https://opensource.org/licenses/MIT).

## Contact information

* Michael Taylor (michael.taylor@reading.ac.uk)
