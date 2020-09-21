function newFireLayer(map_data, year, max_legend_value) {
  console.log("Adding new layer for year " + year);
  map.addSource(year, {
    'type': 'geojson',
    /*many types of data can be added, such as geojson, vector tiles or raster data*/
    'data': map_data
  });
  map.addLayer({
    "id": year,
    "type": 'fill',
    "source": year,
    "layout": {
      'visibility': 'none',
    },
    'paint': {
      'fill-color': [
        'interpolate',
        ['linear'],
        ['get', 'outputs'],
        0.0 * max_legend_value, '#CC0000',
        0.1 * max_legend_value, '#D61900',
        0.2 * max_legend_value, '#E03300',
        0.3 * max_legend_value, '#EA4C00',
        0.4 * max_legend_value, '#F46600',
        0.5 * max_legend_value, '#FF8000',
        0.6 * max_legend_value, '#FF9F19',
        0.7 * max_legend_value, '#FFBF33',
        0.8 * max_legend_value, '#FFDF4C',
        0.9 * max_legend_value, '#FFFF66',
        1.0 * max_legend_value, '#FFFFCC'
      ],
      'fill-outline-color': [
        'interpolate',
        ['linear'],
        ['get', 'outputs'],
        0.0 * max_legend_value, '#CC0000',
        0.1 * max_legend_value, '#D61900',
        0.2 * max_legend_value, '#E03300',
        0.3 * max_legend_value, '#EA4C00',
        0.4 * max_legend_value, '#F46600',
        0.5 * max_legend_value, '#FF8000',
        0.6 * max_legend_value, '#FF9F19',
        0.7 * max_legend_value, '#FFBF33',
        0.8 * max_legend_value, '#FFDF4C',
        0.9 * max_legend_value, '#FFFF66',
        1.0 * max_legend_value, '#FFFFCC'
      ],
      'fill-opacity': [
        'interpolate',
        ['linear'],
        ['get', 'outputs'],
        0.0 * max_legend_value, 0.0,
        0.001 * max_legend_value, map_fill_opacity,
        0.2 * max_legend_value, map_fill_opacity,
        0.3 * max_legend_value, map_fill_opacity,
        0.4 * max_legend_value, map_fill_opacity,
        0.5 * max_legend_value, map_fill_opacity,
        0.6 * max_legend_value, map_fill_opacity,
        0.7 * max_legend_value, map_fill_opacity,
        0.8 * max_legend_value, map_fill_opacity,
        0.9 * max_legend_value, map_fill_opacity,
        1.0 * max_legend_value, map_fill_opacity
      ]
    }
  }, 'waterway-label');
};

function newMagmaLayer(map_data, year, max_legend_value) {
  console.log("Adding new magma layer for year " + year);
  map.addSource(year, {
    'type': 'geojson',
    /*many types of data can be added, such as geojson, vector tiles or raster data*/
    'data': map_data
  });
  map.addLayer({
    "id": year,
    "type": 'fill',
    "source": year,
    "layout": {
      'visibility': 'none',
    },
    'paint': {
      'fill-color': [
        'interpolate',
        ['linear'],
        ['get', 'outputs'],
        0.0 * max_legend_value, '#000005',
        0.1 * max_legend_value, '#080616',
        0.2 * max_legend_value, '#1E0848',
        0.3 * max_legend_value, '#43006A',
        0.4 * max_legend_value, '#6B116F',
        0.5 * max_legend_value, '#981D69',
        0.6 * max_legend_value, '#C92D59',
        0.7 * max_legend_value, '#ED504A',
        0.8 * max_legend_value, '#FA8657',
        0.9 * max_legend_value, '#FBC17D',
        1.0 * max_legend_value, '#FCFFB2'
      ],
      'fill-outline-color': [
        'interpolate',
        ['linear'],
        ['get', 'outputs'],
        0.0 * max_legend_value, '#000005',
        0.1 * max_legend_value, '#080616',
        0.2 * max_legend_value, '#1E0848',
        0.3 * max_legend_value, '#43006A',
        0.4 * max_legend_value, '#6B116F',
        0.5 * max_legend_value, '#981D69',
        0.6 * max_legend_value, '#C92D59',
        0.7 * max_legend_value, '#ED504A',
        0.8 * max_legend_value, '#FA8657',
        0.9 * max_legend_value, '#FBC17D',
        1.0 * max_legend_value, '#FCFFB2'
      ],
      'fill-opacity': [
        'interpolate',
        ['linear'],
        ['get', 'outputs'],
        0.0 * max_legend_value, 0.0,
        0.001 * max_legend_value, map_fill_opacity,
        0.2 * max_legend_value, map_fill_opacity,
        0.3 * max_legend_value, map_fill_opacity,
        0.4 * max_legend_value, map_fill_opacity,
        0.5 * max_legend_value, map_fill_opacity,
        0.6 * max_legend_value, map_fill_opacity,
        0.7 * max_legend_value, map_fill_opacity,
        0.8 * max_legend_value, map_fill_opacity,
        0.9 * max_legend_value, map_fill_opacity,
        1.0 * max_legend_value, map_fill_opacity
      ]
    }
  }, 'waterway-label');
};

function hostmapLayer(data) {
  console.log("Adding host map layer");
  map.addSource('host_map', {
      'type': 'geojson',
      'data': data
  });
  map.addLayer({
                    "id": 'host_map',
                    "type": 'fill',
                    "source": 'host_map',
                    'paint': {
                    'fill-color': [
                    'interpolate',
                    ['linear'],
                    ['get', 'outputs'],
                    1, '#63f542'
                    ],
                        'fill-opacity': [
                            'interpolate',
                            ['linear'],
                            ['get', 'outputs'],
                            0, 0.00,
                            100, 0.4,
                        ]
                    }
                  }, 'waterway-label'); 
};

    /*
    console.log("Adding APHIS Perimeter Zone.");
    map.addSource('perimeter_zone', {
      'type': 'geojson',
      'data': '{% static "map_data/slf_aphis_treatment.geojson" %}'
    });
    map.addLayer({
          "id": 'perimeter_zone_layer',
          "type": 'fill',
          "source": 'perimeter_zone',
          'paint': {
          'fill-color': [
          'interpolate',
          ['linear'],
          ['get', 'Dis_KB'],
          1, '#41dff4'
          ],
          'fill-opacity': 0.1
          }
          }, 'waterway-label');  */
          