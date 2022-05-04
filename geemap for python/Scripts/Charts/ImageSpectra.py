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
# Plot band values at points in an image.
landsat8Toa = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')

COLOR = {
  'PARK': 'ff0000',
  'FARM': '0000ff',
  'URBAN': '00ff00'
}

# Three known locations.
park = ee.Feature(
    ee.Geometry.Point(-99.25260, 19.32235), {'label': 'park'})
farm = ee.Feature(
    ee.Geometry.Point(-99.08992, 19.27868), {'label': 'farm'})
urban = ee.Feature(
    ee.Geometry.Point(-99.21135, 19.31860), {'label': 'urban'})

mexicoPoints = ee.FeatureCollection([park, farm, urban])
landsat8Toa = landsat8Toa.filterBounds(mexicoPoints)

mexicoImage = ee.Image(landsat8Toa.first())

# Select bands B1 to B7.
mexicoImage = mexicoImage.select(['B[1-7]'])

bandChart = ui.Chart.image.regions({
  'image': mexicoImage,
  'regions': mexicoPoints,
  'scale': 30,
  'seriesProperty': 'label'
})
bandChart.setChartType('LineChart')
bandChart.setOptions({
  'title': 'Landsat 8 TOA band values at three points near Mexico City',
  'hAxis': {
    'title': 'Band'
  },
  'vAxis': {
    'title': 'Reflectance'
  },
  'lineWidth': 1,
  'pointSize': 4,
  'series': {
    '0': '{color': COLOR.PARK},
    '1': '{color': COLOR.FARM},
    '2': '{color': COLOR.URBAN}
  }
})

# From: https:#landsat.usgs.gov/what-are-best-spectral-bands-use-my-study
wavelengths = [.44, .48, .56, .65, .86, 1.61, 2.2]

spectraChart = ui.Chart.image.regions({
  'image': mexicoImage,
  'regions': mexicoPoints,
  'scale': 30,
  'seriesProperty': 'label',
  'xLabels': wavelengths
})
spectraChart.setChartType('LineChart')
spectraChart.setOptions({
  'title': 'Landsat 8 TOA spectra at three points near Mexico City',
  'hAxis': {
    'title': 'Wavelength (micrometers)'
  },
  'vAxis': {
    'title': 'Reflectance'
  },
  'lineWidth': 1,
  'pointSize': 4,
  'series': {
    '0': '{color': COLOR.PARK},
    '1': '{color': COLOR.FARM},
    '2': '{color': COLOR.URBAN}
  }
})

print(bandChart)
print(spectraChart)

Map.addLayer(park, {'color': COLOR.PARK})
Map.addLayer(farm, {'color': COLOR.FARM})
Map.addLayer(urban, {'color': COLOR.URBAN})
Map.setCenter(-99.25260, 19.32235, 11)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl()  # This line is not needed for ipyleaflet-based Map.
Map
