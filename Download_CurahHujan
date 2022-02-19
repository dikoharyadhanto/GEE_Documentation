// Cara Download data curah hujan ==> TRMM (28 -30 km), GSamP, CHIRPS
// Resolusi TRMM 0.25 ==> 28 - 30 km
// Resolusi GSamp 0.1 ==. 10 km
// Resolusi CHIRPS 0.05 ==> 5 km

//CHIRPS (mm/day)
var dataset = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
                  .filter(ee.Filter.date('2022-01-01', '2022-02-19'));
var precipitation = dataset.select('precipitation');
var precipitationVis = {
  min: 1.0,
  max: 17.0,
  palette: ['001137', '0aab1e', 'e7eb05', 'ff4a2d', 'e90000'],
};
var ch = dataset.mean().clip(geometry)
Map.addLayer(ch, precipitationVis, 'chirps');

//kalo gak muncul berarti tidak ada datanya

//TRMM (bisa perjam atau bulanan) (suka delayy goblok banget dah)
var dataset2 = ee.ImageCollection('TRMM/3B42')
                  .filter(ee.Filter.date('2019-01-01', '2019-01-02'));
var precipitation2 =
    dataset2.select(['precipitation', 'HQprecipitation', 'IRprecipitation']);
var precipitationVis2 = {
  min: 0.0,
  max: 12.0,
  gamma: 5.0,
};
var ch2 = precipitation2.sum().clip(geometry)
Map.addLayer(ch2, precipitationVis2, 'TRMM');

//GSMap (mm/hours)
var dataset3 = ee.ImageCollection('JAXA/GPM_L3/GSMaP/v6/operational')
                  .filter(ee.Filter.date('2022-02-17', '2022-02-18'));
var precipitation3 = dataset3.select('hourlyPrecipRate');
var precipitationVis3 = {
  min: 0.0,
  max: 30.0,
  palette:
      ['1621a2', 'ffffff', '03ffff', '13ff03', 'efff00', 'ffb103', 'ff2300'],
};
var ch3 = precipitation3.sum().clip(geometry)
// kalo mau liat grafik per jamnya, jangan pake sum sama clipnya
Map.addLayer(ch3, precipitationVis3, 'GSMap');

//Export to Drive
Export.image.toDrive({
  image: ch3,
  description: 'CH_GSMAP',
  scale: 10000,
  maxPixels: 600000000,
  region: geometry
});
