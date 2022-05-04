# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/geemap/tree/master/examples/template/template.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/geemap/blob/master/examples/template/template.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/geemap/blob/master/examples/template/template.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://geemap.org). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print("Installing geemap ...")
    subprocess.check_call(["python", "-m", "pip", "install", "geemap"])

# %%
import ee
import geemap

# %%
"""
## Create an interactive map 
The default basemap is `Google Maps`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
"""

# %%
Map = geemap.Map(center=[40, -100], zoom=4)
Map

# %%
"""
## Add Earth Engine Python script 
"""

# %%
# Add Earth Engine dataset
# Generate day-of-year charts from Landsat 8 images.

city = ee.Feature(    # San Francisco.
    ee.Geometry.Rectangle(-122.42, 37.78, -122.4, 37.8),
    {'label': 'City'})
forest = ee.Feature(  # Tahoe National Forest.
    ee.Geometry.Rectangle(-121, 39.4, -120.99, 39.45),
    {'label': 'Forest'})
desert = ee.Feature(  # Black Rock Desert.
    ee.Geometry.Rectangle(-119.02, 40.95, -119, 41),
    {'label': 'Desert'})
westernRegions = ee.FeatureCollection([city, forest, desert])

landsat8Toa = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(westernRegions)
landsat8Toa = landsat8Toa.select('B[1-7]')

# Create a chart using a sequence of arguments.
bands = ui.Chart.image.doySeries(landsat8Toa, forest, None, 200)
print(bands)

# Create a chart using a dictionary of named arguments.
years = ui.Chart.image.doySeriesByYear({
  'imageCollection': landsat8Toa,
  'bandName': 'B1',
  'region': forest,
  'scale': 200
})
print(years)

regions = ui.Chart.image.doySeriesByRegion({
  'imageCollection': landsat8Toa,
  'bandName': 'B1',
  'regions': westernRegions,
  'scale': 500,
  'seriesProperty': 'label'
})
print(regions)

Map.addLayer(westernRegions)
Map.setCenter(-121, 39.4, 6)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl()  # This line is not needed for ipyleaflet-based Map.
Map
