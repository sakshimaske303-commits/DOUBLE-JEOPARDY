var wms_layers = [];


        var lyr_GoogleHybrid_0 = new ol.layer.Tile({
            'title': 'Google Hybrid',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
            attributions: '<a href="https://www.google.at/permissions/geoguidelines/attr-guide.html">Map data ©2015 Google</a>',
                url: 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
            })
        });
var format_fiji_mangroves_2020_1 = new ol.format.GeoJSON();
var features_fiji_mangroves_2020_1 = format_fiji_mangroves_2020_1.readFeatures(json_fiji_mangroves_2020_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_fiji_mangroves_2020_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_fiji_mangroves_2020_1.addFeatures(features_fiji_mangroves_2020_1);
var lyr_fiji_mangroves_2020_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_fiji_mangroves_2020_1, 
                style: style_fiji_mangroves_2020_1,
                popuplayertitle: 'fiji_mangroves_2020',
                interactive: false,
                title: '<img src="styles/legend/fiji_mangroves_2020_1.png" /> fiji_mangroves_2020'
            });
var format_fiji_mangroves_1996_2 = new ol.format.GeoJSON();
var features_fiji_mangroves_1996_2 = format_fiji_mangroves_1996_2.readFeatures(json_fiji_mangroves_1996_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_fiji_mangroves_1996_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_fiji_mangroves_1996_2.addFeatures(features_fiji_mangroves_1996_2);
var lyr_fiji_mangroves_1996_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_fiji_mangroves_1996_2, 
                style: style_fiji_mangroves_1996_2,
                popuplayertitle: 'fiji_mangroves_1996',
                interactive: false,
                title: '<img src="styles/legend/fiji_mangroves_1996_2.png" /> fiji_mangroves_1996'
            });
var format_fiji_mangroves_2010_3 = new ol.format.GeoJSON();
var features_fiji_mangroves_2010_3 = format_fiji_mangroves_2010_3.readFeatures(json_fiji_mangroves_2010_3, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_fiji_mangroves_2010_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_fiji_mangroves_2010_3.addFeatures(features_fiji_mangroves_2010_3);
var lyr_fiji_mangroves_2010_3 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_fiji_mangroves_2010_3, 
                style: style_fiji_mangroves_2010_3,
                popuplayertitle: 'fiji_mangroves_2010',
                interactive: false,
                title: '<img src="styles/legend/fiji_mangroves_2010_3.png" /> fiji_mangroves_2010'
            });

lyr_GoogleHybrid_0.setVisible(true);lyr_fiji_mangroves_2020_1.setVisible(true);lyr_fiji_mangroves_1996_2.setVisible(true);lyr_fiji_mangroves_2010_3.setVisible(true);
var layersList = [lyr_GoogleHybrid_0,lyr_fiji_mangroves_2020_1,lyr_fiji_mangroves_1996_2,lyr_fiji_mangroves_2010_3];
lyr_fiji_mangroves_2020_1.set('fieldAliases', {'fid': 'fid', 'PXLVAL': 'PXLVAL', });
lyr_fiji_mangroves_1996_2.set('fieldAliases', {'fid': 'fid', 'PXLVAL': 'PXLVAL', });
lyr_fiji_mangroves_2010_3.set('fieldAliases', {'fid': 'fid', 'PXLVAL': 'PXLVAL', });
lyr_fiji_mangroves_2020_1.set('fieldImages', {'fid': 'TextEdit', 'PXLVAL': 'Range', });
lyr_fiji_mangroves_1996_2.set('fieldImages', {'fid': 'TextEdit', 'PXLVAL': 'Range', });
lyr_fiji_mangroves_2010_3.set('fieldImages', {'fid': 'TextEdit', 'PXLVAL': 'Range', });
lyr_fiji_mangroves_2020_1.set('fieldLabels', {'fid': 'no label', 'PXLVAL': 'no label', });
lyr_fiji_mangroves_1996_2.set('fieldLabels', {'fid': 'no label', 'PXLVAL': 'no label', });
lyr_fiji_mangroves_2010_3.set('fieldLabels', {'fid': 'no label', 'PXLVAL': 'no label', });
lyr_fiji_mangroves_2010_3.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});