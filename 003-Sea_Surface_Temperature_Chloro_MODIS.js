//Menentukan ID Citra, waktu perekaman, Composite Band, dan geomer 
var modis_klor = ee.ImageCollection("NASA/OCEANDATA/MODIS-Aqua/L3SMI")
.filterDate('2020-08-01', '2021-09-01')
.select('chlor_a')
.mean()
.clip(geometry);
var modis_sst = ee.ImageCollection("NASA/OCEANDATA/MODIS-Aqua/L3SMI")
.filterDate('2020-08-01', '2020-09-01')
.select('sst')
.mean()
.clip(geometry);

//Menentukan range nilai band dan mode
var vis_suhu = {min: 25, max: 30, palette: ['blue','green','yellow','orange','red']};
var vis_klor = {min: 0, max: 1, palette: ['blue', 'yellow','green']};

//Visualisasi Citra
Map.addLayer(modis_sst, vis_suhu, 'Suhu Laut');
Map.addLayer(modis_klor, vis_klor, 'Klorofil');
