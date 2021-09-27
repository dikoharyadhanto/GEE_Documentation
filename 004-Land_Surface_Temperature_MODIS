//Menentukan ID Citra, waktu perekaman, Composite Band,fungsi reducer dan geomer 
var modis_sst_dataset21 = ee.ImageCollection("MODIS/006/MOD11A2") //id citra
.filterDate('2020-09-25','2021-09-25') //filter waktu
.select('LST_Day_1km') //composite band
.mean() //reducer
.clip(geometry); //clip geomer

var modis_sst_dataset20 = ee.ImageCollection("MODIS/006/MOD11A2") //id citra
.filterDate('2019-09-25','2020-09-25') //filter waktu
.select('LST_Day_1km') //composite band
.mean() //reducer
.clip(geometry); //clip geomer

var modis_sst_dataset19 = ee.ImageCollection("MODIS/006/MOD11A2") //id citra
.filterDate('2018-09-25','2019-09-25') //filter waktu
.select('LST_Day_1km') //composite band
.mean() //reducer
.clip(geometry); //clip geomer

//Kalkulasi nilai Modis menjadi nilai celcius
var dki_celcius21 = modis_sst_dataset21.multiply(0.02).subtract(273.15);
var dki_celcius20 = modis_sst_dataset20.multiply(0.02).subtract(273.15);
var dki_celcius19 = modis_sst_dataset19.multiply(0.02).subtract(273.15);

//Menentukan range nilai band dan mode
var suhu_param = {min: 20, max: 40, palette: ['blue','green','yellow','orange','red']};

//Visualisasi Citra
Map.addLayer(dki_celcius21, suhu_param, 'Rata-Rata Suhu Permukaan DKI Jakarta 2020-2021');
Map.addLayer(dki_celcius20, suhu_param, 'Rata-Rata Suhu Permukaan DKI Jakarta 2019-2020');
Map.addLayer(dki_celcius19, suhu_param, 'Rata-Rata Suhu Permukaan DKI Jakarta 2018-2019');
                                   
