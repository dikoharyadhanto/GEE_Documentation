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
# Plot average seasonal temperatures in US States.

# Import US state boundaries.
states = ee.FeatureCollection('TIGER/2018/States')

# Import temperature normals and convert month features to bands.
normClim = ee.ImageCollection('OREGONSTATE/PRISM/Norm81m') \
  .select(['tmean']) \
  .toBands()

# Calculate mean monthly temperature per state.
states = normClim.reduceRegions({
  'collection': states,
  'reducer': ee.Reducer.mean(),
  'scale': 5e4}) \
  .filter(ee.Filter.NotNull(['01_tmean']))

# Calculate Jan to Jul temperature difference per state and set as a property.

def func_kda(state):
  julyTemp = ee.Number(state.get('06_tmean'))
  janTemp = ee.Number(state.get('01_tmean'))
  return state.set('seasonal_delta', julyTemp.subtract(janTemp))

states = states.map(func_kda)






# Select the extreme states.
extremeStates =
  states.limit(1, '01_tmean')                 # Coldest. \
  .merge(states.limit(1, '07_tmean', False)) \
  .merge(states.limit(1, 'seasonal_delta'));  

# Define properties to chart.
months = {
  '01_tmean': 1,
  '04_tmean': 4,
  '07_tmean': 7,
  '10_tmean': 10
}

# Prepare the chart.
extremeTempsChart =
  ui.Chart.feature.byProperty(extremeStates, months, 'NAME') \
    .setChartType('LineChart') \
    .setOptions({
      'title': 'Average Temperatures in U.S. States',
      'hAxis': {
        'title': 'Month',
        'ticks': '[{v': months['01_tmean'], 'f': 'January'},
                {'v': months['04_tmean'], 'f': 'April'},
                {'v': months['07_tmean'], 'f': 'July'},
                {'v': months['10_tmean'], 'f': 'October'}]
      },
      'vAxis': {
        'title': 'Temperature (Celsius)'
      },
      'lineWidth': 1,
      'pointSize': 3
    })

print(extremeTempsChart)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl()  # This line is not needed for ipyleaflet-based Map.
Map
