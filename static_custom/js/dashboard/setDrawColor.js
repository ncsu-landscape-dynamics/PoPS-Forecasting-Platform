function setDrawColor(draw_color,host_removal_pattern,pesticide_application_pattern) {
  var draw = new MapboxDraw({
    keybindings: true,
    displayControlsDefault: false,
    userProperties: true,
    modes: Object.assign({
      draw_circle: CircleMode,
    }, MapboxDraw.modes),
    controls: {
      //polygon: true,
      //trash: true
    },
styles: [
{
  'id': 'circle-active',
  'type': 'circle',
  'filter': ['all',
    ['==', '$type', 'Point'],
    ['==', 'meta', 'feature'],
    ['==', 'active', 'true']],
  'paint': {
    'circle-radius': 7,
    'circle-color': draw_color,
  }
},        
{
  'id': 'circle-static',
  'type': 'circle',
  'filter': ['all',
    ['==', '$type', 'Point'],
    ['==', 'meta', 'feature'],
    ['==', 'active', 'false']],
  'paint': {
    'circle-radius': 7,
    'circle-color': draw_color,
  }
},    
{
  'id': 'highlight-active-points',
  'type': 'circle',
  'filter': ['all',
    ['==', '$type', 'Point'],
    ['==', 'meta', 'feature'],
    ['==', 'active', 'true']],
  'paint': {
    'circle-radius': 7,
    'circle-color': draw_color,
  }
},

  // ACTIVE (being drawn)
  // line stroke
  {
    "id": "gl-draw-line",
    "type": "line",
    "filter": ["all", ["==", "$type", "LineString"],
      ["!=", "mode", "static"]
    ],
    "layout": {
      "line-cap": "round",
      "line-join": "round"
    },
    "paint": {
      "line-color": draw_color,
      "line-dasharray": [0.2, 2],
      "line-width": 3
    }
  },
  // polygon fill
  {
    "id": "gl-draw-polygon-fill",
    "type": "fill",
    "filter": ["all", ["==", "$type", "Polygon"],
      ["!=", "mode", "static"]
    ],
        "paint": {
          'fill-pattern': [
            "case",
            ['==', ['get', "user_management_type"], "Host removal"], host_removal_pattern,
            ['==', ['get', "user_management_type"], "Pesticide"], pesticide_application_pattern,
            ''
          ],      
          "fill-outline-color": draw_color,
          "fill-opacity": 1.0
        }
      },
  // polygon outline stroke
  // This doesn't style the first edge of the polygon, which uses the line stroke styling instead
  {
    "id": "gl-draw-polygon-stroke-active",
    "type": "line",
    "filter": ["all", ["==", "$type", "Polygon"],
      ["!=", "mode", "static"]
    ],
    "layout": {
      "line-cap": "round",
      "line-join": "round"
    },
    "paint": {
      "line-color": draw_color,
      "line-width": 3
    }
  },
  // vertex point halos
  {
    "id": "gl-draw-polygon-and-line-vertex-halo-active",
    "type": "circle",
    "filter": ["all", ["==", "meta", "vertex"],
      ["==", "$type", "Point"],
      ["!=", "mode", "static"]
    ],
    "paint": {
      "circle-radius": 7,
      "circle-color": "#FFF"
    }
  },
  // vertex points
  {
    "id": "gl-draw-polygon-and-line-vertex-active",
    "type": "circle",
    "filter": ["all", ["==", "meta", "vertex"],
      ["==", "$type", "Point"],
      ["!=", "mode", "static"]
    ],
    "paint": {
      "circle-radius": 5,
      "circle-color": draw_color,
    }
  },

  // INACTIVE (static, already drawn)
  // line stroke
  {
    "id": "gl-draw-line-static",
    "type": "line",
    "filter": ["all", ["==", "$type", "LineString"],
      ["==", "mode", "static"]
    ],
    "layout": {
      "line-cap": "round",
      "line-join": "round"
    },
    "paint": {
      "line-color": "#000",
      "line-width": 3
    }
  },
  // polygon fill
  {
    "id": "gl-draw-polygon-fill-static",
    "type": "fill",
    "filter": ["all", ["==", "$type", "Polygon"],
      ["==", "mode", "static"]
    ],
    "paint": {
      "fill-color": "#000",
      "fill-outline-color": "#000",
      "fill-opacity": 0.3
    }
  },
  // polygon outline
  {
    "id": "gl-draw-polygon-stroke-static",
    "type": "line",
    "filter": ["all", ["==", "$type", "Polygon"],
      ["==", "mode", "static"]
    ],
    "layout": {
      "line-cap": "round",
      "line-join": "round"
    },
    "paint": {
      "line-color": "#000",
      "line-width": 3
    }
  }
]
});
return draw;
};
