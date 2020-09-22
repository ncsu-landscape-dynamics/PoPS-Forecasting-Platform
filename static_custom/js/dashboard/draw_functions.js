function createPolygon (e) {
  var polygon = grabPolygon(e); 
  var area = getArea(polygon);
  var management_properties = getManagementProperties();
  var number_of_management_types = management_properties.length;
  for (var n = 0; n < number_of_management_types; n++) {
    featureID = drawPolygon(polygon, management_properties[n],area);
    findAndCombineOverlappingPolygons(featureID);
  }
  updateJSON();
}
//Get the currently drawn polygon, so we can add management properties to the JSON.
function grabPolygon(e) {
  polygon = draw.get(e.features[0].id); //Get the polygon
  delete polygon['id']; //Delete the ID, so we can duplicate it if there are more than 1 management type.
  draw.delete(e.features[0].id); //delete the original polygon.
  return polygon; 
};
function getArea(polygon) {
  var area = turf.area(polygon);
  return Math.round(area);
}
//Get array of management properties structured as [['Type1',efficacy,cost],['Type2',efficacy,cost],...]
function getManagementProperties() {
  management = [];
  if ($('#host_removal_status').prop('checked')) {
    host_removal_management = ['Host removal',
      $("#default_host_removal_efficacy").val(),
      $("#default_host_removal_cost").val(),
      $("#default_host_removal_date").val()];
    management.push(host_removal_management);
  } 
  if ($('#pesticide_status').prop('checked')) {
    pesticide_management = ['Pesticide',
      $("#default_pesticide_efficacy").val(),
      $("#default_pesticide_cost").val(),
      $("#default_pesticide_date").val()];
    management.push(pesticide_management);  
  } 
  return management;
}
//Add the polygon to draw. Set management properties. Perform findAndCombineOverlappingPolyogns.
function drawPolygon(polygon, management_properties,area) {
  featureID = draw.add(polygon);
  draw.setFeatureProperty(featureID, 'management_type', management_properties[0]);
  draw.setFeatureProperty(featureID, 'efficacy', management_properties[1]);
  draw.setFeatureProperty(featureID, 'cost', management_properties[2]);
  draw.setFeatureProperty(featureID, 'date', management_properties[3]);
  draw.setFeatureProperty(featureID, 'area', area);
  //draw.add(draw.get(featureID)); //This line makes the new change draw on the map and appear.    
  return featureID;
};
//Check if the most recently drawn polygon overlaps any existing polygons
//of the same type and combine.
function findAndCombineOverlappingPolygons(newPolygonID) {
  var allPolygons = draw.getAll();
  newPolygon = draw.get(newPolygonID);
  //Check that there are more than one polygon
  if (allPolygons.features.length > 1) {
    //Loop through all of the existing polygons
    for (var n = 0; n < allPolygons.features.length - 1; n++) {
      var existingPolygon = allPolygons.features[n];
      //Check to see if the new polygon intersects the existing polygon
      var intersection = turf.intersect(newPolygon, existingPolygon);
      if (intersection) {
        //If they are the same management type, combine the two polygons.
        if ((newPolygon.properties.management_type == existingPolygon.properties.management_type)) {
          if ((newPolygon.properties.efficacy == existingPolygon.properties.efficacy) && 
          (newPolygon.properties.cost == existingPolygon.properties.cost) &&
          (newPolygon.properties.date == existingPolygon.properties.date)) {
            union = combineTwoPolygons(newPolygonID, existingPolygon.id);
            if (union) {
              newPolygonID = union;
              polygon =  draw.get(newPolygonID);
              var area=Math.round(getArea(polygon));
              draw.setFeatureProperty(newPolygonID, 'area', area);
            }
          }
          else if ((newPolygon.properties.management_type != 'Pesticide') || (newPolygon.properties.date == existingPolygon.properties.date)
          ) {
            difference = turf.difference(existingPolygon,newPolygon);//remove newpolygon from existing polygon
            var newPolygonID = draw.add(difference); //add new polygon to draw
            draw.delete(existingPolygon.id); //remove original overlapping polygons
            var area=Math.round(getArea(difference));
            draw.setFeatureProperty(newPolygonID, 'area', area);          }
        }
        else {
        }
      }
    }
  }
}
//Check if polygon1 and polygon 2 intersect and are of the same type.
//If yes, combine them into a single polygon and delete the original 2.
function combineTwoPolygons(polygonID1, polygonID2) {
  polygon1 = draw.get(polygonID1);
  polygon2 = draw.get(polygonID2);
  //if polygons intersect AND management type is the same, perform union of two polygons
  if ((turf.intersect(polygon1, polygon2)) && (polygon1.properties.management_type == polygon2.properties.management_type)) {
    union = turf.union(polygon1, polygon2); //create new union polygon
    var featureIds = draw.add(union); //add new polygon to draw
    draw.delete(polygonID1) //remove original overlapping polygons
    draw.delete(polygonID2) //remove original overlapping polygons
    return (featureIds); //return the ID of the new polygon
  }
}
function updatePolygons(e) {
  selection = draw.getSelectedIds();
  for (var n = 0; n < selection.length; n++) {
    findAndCombineOverlappingPolygons(selection[n]);
  }
  updateJSON();
}
    //When selection changes, show box to edit the selected polygons.
    function displaySelectionChange() {
      selection = draw.getSelected();
      //display ability to edit if 1 or more polygons are selected
      if (selection.features.length > 0) {
        //Get the management type of the first feature, to pre-check that as the type
        selected_management_type = selection.features[0].properties.management_type;
        $("input[type=radio][name='editManagementOptions']").prop("checked", false);
        $("input[type=radio][value='" + selected_management_type + "']").prop("checked", true);
        $("input[id='edit_efficacy']").val(selection.features[0].properties.efficacy);
        var area_modifier = $("select#edit_area_unit").val();
        $("input[id='edit_display_cost']").val(selection.features[0].properties.cost/area_modifier);
        $("input[id='edit_date']").val(selection.features[0].properties.date);
        //Show edit polygons box.
        $('#editPolygons').show();
      } else {
        $('#editPolygons').hide();
      }
    }

function changePolygonProperties() {
      selectionIDs = draw.getSelectedIds();
      var editManagementTypeValue = $("input[name='editManagementOptions']:checked").val();
      var editEfficacy = $("input[id='edit_efficacy']").val();
      var editCost = $("input[id='edit_cost']").val();
      var editDate = $("input[id='edit_date']").val();
      for (var n = 0; n < selectionIDs.length; n++) {
        draw.setFeatureProperty(selectionIDs[n], 'management_type', editManagementTypeValue);
        draw.setFeatureProperty(selectionIDs[n], 'efficacy', editEfficacy);
        draw.setFeatureProperty(selectionIDs[n], 'cost', editCost);
        draw.setFeatureProperty(selectionIDs[n], 'date', editDate);
        draw.add(draw.get(selectionIDs[n])); //This line makes the new change draw on the map and appear.
      }
      updateJSON(selectionIDs);
};

//This function updates the GeoJSON management field 
function updateJSON() {
  var data = draw.getAll();
  console.log("Updating management polygons:");
  //console.log(data);
  var answer = document.getElementById('displayed-management-area');
  var budget = $("input#id_budget").val();
  var area_unit = $("select#id_area_unit").children("option:selected").text();
  var abbreviated_unit_display = $("select#id_area_unit").children("option:selected").attr('data-text');
  var area_modifier = $("select#id_area_unit").children("option:selected").val();
  if (data.features.length > 0) {
    // Stringify the GeoJson
    var convertedData = JSON.stringify(data);
    [host_removal_area, pesticide_area, host_removal_cost,pesticide_cost] = calculateTotalDrawnManagement(data);
    console.log('host_removal_area = ' + host_removal_area);
    console.log('pesticide_area = ' + pesticide_area);
    console.log('convertedData = ' + convertedData);
    var total_area = host_removal_area + pesticide_area;
    var rounded_area = Math.round(total_area);
    var displayed_area = Math.round(total_area*area_modifier);
    // round cost to 2 decimal places
    var total_cost = host_removal_cost + pesticide_cost;
    console.log('Cost is = ' + total_cost)
  } else {
    var rounded_area=0;
    var convertedData = 0;
    var host_removal_cost=0, pesticide_cost = 0;
    var total_cost = 0;
    var displayed_area = 0;
    console.log("updateJSON: There is no management.")
  }
  answer.innerHTML =  displayed_area.toLocaleString("en") + ' ' + abbreviated_unit_display;  
  $('#id_management_polygons').val(convertedData);
  $('#id_management_area').val(rounded_area);
  $('#id_management_cost').val(total_cost);
  gaugePlot("current-budget-plot", host_removal_cost, pesticide_cost, budget);
}

function calculateTotalDrawnManagement(data) {
  var host_removal_area = 0;
  var pesticide_area = 0;  
  var host_removal_cost = 0;
  var pesticide_cost = 0;
  var length = data.features.length;
  for (var n = 0; n < length; n++) {
    if (data.features[n].properties.management_type == 'Host removal') {
      host_removal_area += data.features[n].properties.area;
      host_removal_cost += data.features[n].properties.area * data.features[n].properties.cost;
    } 
    else if (data.features[n].properties.management_type == 'Pesticide') {
      pesticide_area += data.features[n].properties.area;
      pesticide_cost += data.features[n].properties.area * data.features[n].properties.cost;
    }
  }
  return [host_removal_area, pesticide_area, host_removal_cost, pesticide_cost];
}

function updateCircleRadiusInMeters() {
    console.log("Circle radius changed")
    var displayed_management_circle_radius = $("input#displayed_circle_radius").val();
    console.log('Displayed radius = ' + displayed_management_circle_radius);
    var convert_to_meters_modifier = $("select#circle_distance_unit").children("option:selected").val();
    console.log('Modifier = ' + convert_to_meters_modifier);
    var management_circle_radius_meters = displayed_management_circle_radius*convert_to_meters_modifier;
    console.log("Radius in hidden field = " + management_circle_radius_meters);
    $("input#circle_radius_in_meters").val(management_circle_radius_meters);
};

function updateDefaultManagementCost(element) {
  var displayed_cost = $(element).find("input.displayed_cost").val();
  console.log("DISPLAYED COST: " + displayed_cost);
  var cost_modifier =  $(element).find("option:selected").val();
  console.log("COST MODIFIER: " + cost_modifier);
  var actual_cost_per_meter_squared = Math.round(displayed_cost*cost_modifier*100000000)/100000000;
  console.log("ACTUAL COST: " + actual_cost_per_meter_squared);
  $(element).find("input.default_cost").val(actual_cost_per_meter_squared);
};

function disableDrawTools(){
  if ($("#draw-controls").is(":visible")){
    console.log('Disabling draw tools.')
    draw.changeMode('simple_select');
    map.removeControl(draw);
    map.getContainer().classList.remove("mouse-add");
    $('.drawing-tool').removeClass('active');
    $('#select-tool').addClass('active');
    $( "#draw-controls" ).hide();
  }
  else {
    console.log("Draw tools already disabled.")
  }
};

function enableDrawTools(){
  if ($("#draw-controls").is(":hidden")){
    if (!$('input#id_tangible_landscape').prop('checked') && $('#map-tab').hasClass('active')){
      map.addControl(draw);
      $( "#draw-controls" ).show();
      var treatment = JSON.parse($('#id_management_polygons').val());
      console.log('Currently drawn treatment JSON:');
      console.log(treatment);
      if (treatment != 0) {
        var ids = draw.set(treatment);
      };
      console.log('Added draw tools.')
      updateJSON();
    }  
    else  {
    console.log('Did not add draw tools because TL is checked')
      updateJSON();
    }
  }
  else {
    console.log("Draw tools already enabled.")
  }
};
