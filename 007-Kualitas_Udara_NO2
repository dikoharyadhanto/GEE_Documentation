//Sentinel-5p untuk memonitoring atmosfer permukaan bumi
//Diluncurkan  3 Okt 2017
// Fungsi ngukur kualitas udara, ozon, dan UV
// Resolusi spasial 10km
// Resolusi temporal 1 hari


//Ambil citranya dengan periode tertentu dirata2kan
var periode2018 = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_NO2")
.select('NO2_column_number_density')
.filterDate('2018-01-01','2018-12-31')
.mean();

var periode2019 = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_NO2")
.select('NO2_column_number_density')
.filterDate('2019-01-01','2019-12-31')
.mean();

var periode2020 = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_NO2")
.select('NO2_column_number_density')
.filterDate('2020-01-01','2020-12-31')
.mean();

var periode2021 = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_NO2")
.select('NO2_column_number_density')
.filterDate('2021-01-01','2021-12-31')
.mean();

var periode2022 = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_NO2")
.select('NO2_column_number_density')
.filterDate('2022-01-01','2022-04-30')
.mean();

//variabel stacked_composite fungsinya itu untuk menggabungkan (stacking)
//variabel periode2019 - periode2022 digabung jadi satu layer
var stacked_composite = periode2018.addBands(periode2019).addBands(periode2020)
.addBands(periode2021).addBands(periode2022);

print('NO2_2018-2022', stacked_composite.bandNames());

//parameter grafik
var options = {
  title: 'Grafik Kadar NO2 Tahunan',
  hAxis: {title: 'Periode Waktu'},
  vAxis: {title: 'Kadar NO2'},
  linedWidth: 3,
  pointSize: 4,
};

var waktu = ['2018', '2019', '2020', '2021', '2022'];

//Script Memunculkan Grafik
var grafik = ui.Chart.image.regions(
  stacked_composite, geometry, ee.Reducer.mean(), 30, 'label', waktu)
  .setChartType('ColumnChart')
  .setOptions(options);

//Display Grafik
print(grafik);

//visualisasi citra
var band_viz = {
  min: 0.00004,
  max: 0.00007,
  palette: ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
};

//filter pixel diatas 0,0001
//hanya memfilter yg kadar NO2 nya diatas 0,0001 saja. Dibawah itu gak dimunculkan
var subset2018 = periode2018.gt(0.00004)
var subset2019 = periode2019.gt(0.00004)
var subset2020 = periode2020.gt(0.00004)
var subset2021 = periode2021.gt(0.00004)
var subset2022 = periode2022.gt(0.00004)

//mask hanya pixel diatas 0,0001
var af2018 = periode2018.mask(subset2019).clip(geometry)
var af2019 = periode2019.mask(subset2019).clip(geometry)
var af2020 = periode2020.mask(subset2020).clip(geometry)
var af2021 = periode2021.mask(subset2021).clip(geometry)
var af2022 = periode2022.mask(subset2022).clip(geometry)

//Menampilkan visualisasi citra per tahun
Map.addLayer(af2018, band_viz, 'NO2 2018')
Map.addLayer(af2019, band_viz, 'NO2 2019')
Map.addLayer(af2020, band_viz, 'NO2 2020')
Map.addLayer(af2021, band_viz, 'NO2 2021')
Map.addLayer(af2022, band_viz, 'NO2 2022')

//Export to Drive
Export.image.toDrive({
  image: af2022,
  description: 'NO2_Lembang2022',
  scale: 10000,
  maxPixels: 600000000,
  region: geometry
});
