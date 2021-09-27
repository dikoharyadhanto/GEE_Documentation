var dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1') // buat nentuin image-nya. Kode image dicatet dulu di menu pencarian citra
                  .filterBounds(geometry) //fungsi untuk memfilter pencarian geomer atas sebuah dataset
                  .filterDate('2021-06-01', '2021-09-27'); // fungsi untuk pencarian berdasarkan waktu
print(dataset); //fungsi memunculkan dataset layer

var single = ee.Image('LANDSAT/LC08/C01/T1/LC08_122064_20210916') //buat nampilin image-nya
            
var RGBTrue = single.select(['B4', 'B3', 'B2']); //buat nampilin composite band True color

//memunculkan citra
var RGBparam = { min: 0, max: 20000,}; //mau nampilin citra dengan nilai pixel rentang berapa sampe berapa
Map.addLayer(RGBTrue, RGBparam, 'Nama_Citra-nya');



