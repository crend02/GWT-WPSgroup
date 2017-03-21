# GWT-WPSgroup
# Installation
### Frontend
This WPS is implemented for [this](https://github.com/tonja26/CrowdDensityMapper) frontend.

### Database
Install the database as described [here](https://github.com/LEinfeldt/AdvancedGeoWeb).

### pyWPS configuration
Please install [pyWPS](http://pywps.org) on your system. Include the file [coordinates.py](https://github.com/crend02/GWT-WPSgroup/blob/master/coordinates.py) in your pyWPS `processes` folder. In our case this folder is located at `/usr/local/lib/python2.7/dist-packages/pywps-3.2.5-py2.7.egg/pywps/processes`. You need to modify the `__init__.py` file which is located at `/usr/local/lib/python2.7/dist-packages/pywps-3.2.5-py2.7.egg/pywps` and change the `__all__` variable to `__all__ = ["coordinates"]`. 

### Python libraries
You will need to install some python libraries. Please install them with `sudo -H pip install [library...]`. Please install the following libraries:
- requests
- json
- matplotlib
- geopandas
- fiona
- scipy
- numpy

# Run
You can call the WPS Process by the following URL: `http://localhost/cgi-bin/pywps.cgi?service=wps&version=1.0.0&request=execute&identifier=coordinates`
