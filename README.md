# Processing Scintillometry Data in Complex Terrain

A suite of tools for computing sensible heat fluxes from the BLS450 scintillometer and working with 2D flux footprints.

This project formed part of a scintillometry field course. Due to licensing constraints, some dependencies are not satisfied by this repository alone. These are indicated below.


## 1. Features

### 1.1 Scintillometry

- Parses scintillometry data from BLS450 scintillometer.
- Processes this data and computes sensible heat fluxes.
- Processes topographical data.
- Processes InnFlux and HATPRO data.
- Produces plots of scintillometer data, path topography, and weather data.

### 1.2 Footprint Climatology 

- Processes 2D flux footprints generated by Natascha Kljun's online model, available [here](http://footprint.kljun.net/).
- Makes individual topographical adjustments and stitches footprints together.
- Overlays stitched footprints onto map.

## 2. Workflow

Running scripts directly from the console will cause errors. Not all data and dependences are available in this repository, and some of the scripts must be tailored to each individual project, notably station parameters and the times when the boundary layer switches from stable to unstable regimes.

The results of working examples are found in `Scintillometry Processing.ipynb` and `Footprint Rasters.ipynb`. The field course report and analysis is not available.

Before beginning, run Manuela Lehner's `read_tirol_dgm.m` (not included) on DGM 5m data to generate topographical data for the scintillometer's path coordinates. Then, use `core_path_calculator.m` to generate path transects. These are also necessary for calibrating the scintillometer.


**Scintillometer path coordinates must be accurate. Incorrectly generated topographical data leads to poor calibration and nonsense results!**

### 2.1 Scintillometry

An example of scintillometry processing can be found in `Scintillometry Processing.ipynb`.
1. Use `data_parser.py` to parse scintillometer and weather data.
2. Use `cn_derivations.data_processor()` to derive $Cn^{2}$. Make sure to enter the correct regime switch time.
3. Use `r_function_port.ward_method()`, a Python port of Helen Ward's code, to compute the Obukhov length and sensible heat flux.
4. Use the functions in `prettyplot.py` to visualise data.
### 2.2 Path Footprint Climatology
 
 Some example code is given in `Footprint Rasters.ipynb`, but individual adjustments are necessary.
 
 1. Generate footprints for entire path length either by using the online 2D FFP tool, or the FFP_clim function provided by Natascha Kljun.
 2. Generate xllcenter, yllcenter coordinates for each footprint.
 2. Determine the resolution and cell size of each generated footprint via the MATLAB engine for Python.
 3. Calculate xllcorner,yllcorner coordinates:
 
    > `xllcorner = xllcenter - (nrow * cellsize)/2`

4. Generate ASCII raster files, inserting correct coordinates.
5. Generate TIFF files, apply weighting functions to each TIFF.
6. Mosaic and average TIFF files in R, generate final contour.
7. Layer contour plot over map (e.g. with QGIS).