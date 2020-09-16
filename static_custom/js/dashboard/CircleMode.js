// CUSTOM CIRCLE DRAWING MODE 
// to draw management buffers of given radius.
// Info on custom modes: https://github.com/mapbox/mapbox-gl-draw/blob/main/docs/MODES.md
const CircleMode = {};

CircleMode.onSetup = function (opts) {
  var state = {};
  return state;
};
//On click, a circle of radius, management_circle_radius, is drawn and added to the management JSON.
CircleMode.onClick = function (state, e) {
  console.log('Drawing circle...')
  var center = [e.lngLat.lng, e.lngLat.lat]; 
  var radius = management_circle_radius;
  var management_properties = getManagementProperties();
  for (var n = 0; n < management_properties.length; n++) {
    var circle = createCircle(center, radius, management_properties[n]);
    var featureID = draw.add(circle);
    findAndCombineOverlappingPolygons(featureID);
  }
};
//Creates a JSON circle of given radius and number of steps. Includes management and efficacy properties.
function createCircle(center, radius, management_properties) {
  var options = {
    steps: 32,
    units: 'kilometers',
    properties: {
      management_type: management_properties[0],
      efficacy: management_properties[1],
      cost: management_properties[2]
    }
  };
  var circle = turf.circle(center, radius, options);
  return circle
}

CircleMode.onStop = function (state, e) {
  //this.map.fire("draw.create");
};

//toDisplayFeatures is a required function to show the polygon. Triggered anytime a feature is rendered.
CircleMode.toDisplayFeatures = function (state, geojson, display) {
  display(geojson);
};