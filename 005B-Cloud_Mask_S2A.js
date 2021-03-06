// --------------Sentinel 2A ------------------------------------

// Membuat fungsi cloud mask
function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  
    // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
      
  return image.updateMask(mask).divide(10000);
}


//Menentukan ID Citra, waktu perekaman, fungsi cloud masking, fungsi reducer dan geomer 
var S2A_dataset = ee.ImageCollection('COPERNICUS/S2_SR')
                    .filterDate('2021-01-01','2021-09-28')
                    // Pre-filter to get less cloudy granules.
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',90))
                    .map(maskS2clouds)
                    .median()
                    .clip(geometry);

//Menentukan Composite Band dan range nilai band yang Digunakan
var senRGBTrue = {
  min: 0.0,
  max: 0.3,
  bands: ['B4', 'B3', 'B2'],
};

//Visualisasi Citra
Map.addLayer(S2A_dataset, senRGBTrue, 'Data Sentinel 2A Jawa 2021');

//----------Export Citra---------------
Export.image.toDrive({
  image: S2A_dataset,
  description: 'Data_Sentinel_2A_Jawa_2021',
  scale: 10,
  maxPixels: 600000000,
  region: geometry
});
