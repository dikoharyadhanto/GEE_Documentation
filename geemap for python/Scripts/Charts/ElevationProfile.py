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
# Plot elevation at waypoints along the Mt. Rainier summit trail.

elevation = ee.Image('CGIAR/SRTM90_V4')
waypoints = [
  ee.Feature(
      ee.Geometry.Point([-121.7353, 46.78622]),
      {'name': 'Paradise Ranger Station'}),
  ee.Feature(
      ee.Geometry.Point([-121.72529, 46.8093]), {'name': 'Pebble Creek'}),
  ee.Feature(
      ee.Geometry.Point([-121.72585, 46.8102899]),
      {'name': 'Start of Glacier'}),
  ee.Feature(
      ee.Geometry.Point([-121.7252699, 46.81202]), {'name': 'Glacier Point 1'}),
  ee.Feature(
      ee.Geometry.Point([-121.72453, 46.81661]), {'name': 'Glacier Point 2'}),
  ee.Feature(
      ee.Geometry.Point([-121.72508, 46.82262]), {'name': 'Little Africa'}),
  ee.Feature(
      ee.Geometry.Point([-121.7278699, 46.82648]), {'name': 'Moon Rocks'}),
  ee.Feature(ee.Geometry.Point([-121.73281, 46.8354]), {'name': 'Camp Muir'}),
  ee.Feature(ee.Geometry.Point([-121.75976, 46.85257]), {'name': 'Summit'})
]

rainierWaypoints = ee.FeatureCollection(waypoints)

chart = ui.Chart.image.byRegion({
  'image': elevation,
  'regions': rainierWaypoints,
  'scale': 200,
  'xProperty': 'name'
})
chart.setOptions({
  'title': 'Mt. Rainier Summit Trail Elevation',
  'vAxis': {
    'title': 'Elevation (meters)'
  },
  'legend': 'none',
  'lineWidth': 1,
  'pointSize': 4
})

print(chart)

Map.addLayer(elevation, {'min': 500, 'max': 4500})
Map.addLayer(rainierWaypoints, {'color': 'FF0000'})
Map.setCenter(-121.75976, 46.85257, 11)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl()  # This line is not needed for ipyleaflet-based Map.
Map
