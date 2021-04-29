# hagerstrand


[![image](https://img.shields.io/pypi/v/hagerstrand.svg)](https://pypi.python.org/pypi/hagerstrand)
[![image](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![image](https://pepy.tech/badge/hagerstrand)](https://pepy.tech/project/hagerstrand)
[![image](https://img.shields.io/conda/vn/conda-forge/hagerstrand.svg)](https://anaconda.org/conda-forge/hagerstrand)

**A Python package for an interactive space-time Geographic Information System (GIS)**


- GitHub repo: [https://github.com/jimmy-feng/hagerstrand](https://github.com/jimmy-feng/hagerstrand)
- Documentation: [https://jimmy-feng.github.io/hagerstrand](https://jimmy-feng.github.io/hagerstrand)
- PyPI: [https://pypi.org/project/hagerstrand](https://pypi.org/project/hagerstrand)
- Conda-forge: [https://anaconda.org/conda-forge/hagerstrand](https://anaconda.org/conda-forge/hagerstrand)
- Free software: MIT license
    

## Introduction
**Hagerstrand** is a Python package for a space-time GIS for individual-level human phenomena based on [Torsten Hägerstrand's](https://en.wikipedia.org/wiki/Torsten_H%C3%A4gerstrand) time geographic framework. Investigation of individual activity patterns in a geographic information system (GIS) has been an interest for many geographers and geographic information scientists since Hägerstrand's seminal article, [*What about people in regional science?*](https://doi.org/10.1007/BF01936872) in 1970. However, there lacks a uniform implementation of the concepts in the time geographic framework in a GIS across the academic research community. Esri's ArcGIS platforms have various functions for analysis, visualization, and querying of space-time data but are rather limited and only commercially available. This package is continually developed to enable for more comprehensive space-time GIS processes in an open-source Python environment, and can also be used to explore individual human dynamics (e.g. accessibility to various human needs and services.)

## Installation

**Pip**

`pip install hagerstrand`

**Conda**

Installing `hagerstrand` from the `conda-forge` channel can be achieved by adding `conda-forge` to your channels with:

```
conda config --add channels conda-forge
```

Once the `conda-forge` channel has been enabled, `hagerstrand` can be installed with:

```
conda install hagerstrand
```

It is possible to list all of the versions of `hagerstrand` available on your platform with:

```
conda search hagerstrand --channel conda-forge
```
## Features

- Create an interactive map
- Add local datasets (e.g. GeoJSON, JSON, Shapefile) to the map either through code or GUI
- Add pandas DataFrames and GeoPandas GeoDataFrames to the map
- Use a widget for quick viewing of filtered results of a pd.DataFrame
- Filter any non-TileLayer in the map by a unique value in a field/column
- Process SafeGraph data and unpack json columns into an existing or a new DataFrame 

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
