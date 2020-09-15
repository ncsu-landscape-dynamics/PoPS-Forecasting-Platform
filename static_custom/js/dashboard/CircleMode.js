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
  var management = getManagementType();
  var management_type = management[0];
  var host_removal_efficacy = management[1];
  var pesticide_application_efficacy = management[2];
  var host_removal_cost = management[3];
  var pesticide_application_cost = management[4];
  if (management_type == 'Host removal and Pesticide') {
    var circle1 = createCircle(center, radius, 'Host removal', host_removal_efficacy,host_removal_cost);
    addCircle(circle1);
    var circle2 = createCircle(center, radius, 'Pesticide', pesticide_application_efficacy,pesticide_application_cost);
    addCircle(circle2);
  } else if (management_type == 'Host removal') {
    var circle = createCircle(center, radius, 'Host removal', host_removal_efficacy, host_removal_cost);
    addCircle(circle);
  } else if (management_type == 'Pesticide') {
    var circle = createCircle(center, radius, 'Pesticide', pesticide_application_efficacy,pesticide_application_cost);
    addCircle(circle);
  } else {
    console.log('No management type selected.')
  }
};
//Creates a JSON circle of given radius and number of steps. Includes management and efficacy properties.
function createCircle(center, radius, management_type, efficacy, cost) {
  var options = {
    steps: 32,
    units: 'kilometers',
    properties: {
      management_type: management_type,
      efficacy: efficacy,
      cost: cost
    }
  };
  var circle = turf.circle(center, radius, options);
  return circle
}
//Adds the circle JSON to Draw, finds and combines polygons, adds to management JSON.
function addCircle(circle) {
  featureID = draw.add(circle);
  new_circle = draw.get(featureID);
  findAndCombineOverlappingPolygons(featureID);
}

CircleMode.onStop = function (state, e) {
  //this.map.fire("draw.create");
};

//toDisplayFeatures is a required function to show the polygon. Triggered anytime a feature is rendered.
CircleMode.toDisplayFeatures = function (state, geojson, display) {
  display(geojson);
};