function updateDrawColor (year_count) {
  disableDrawTools();
  enableDrawTools();
  console.log('Removing draw control.');
  console.log('Adding draw color for year: ' + year_count);
  map.removeControl(draw);
  if (year_count) {
    var draw_color = colors[year_count-1];
    var host_removal_pattern = host_removal_patterns[year_count-1];
    var pesticide_application_pattern = pesticide_application_patterns[year_count-1];
  }
  else {
    var draw_color = '#000';
    var host_removal_pattern = '';
    var pesticide_application_pattern = '';
  }
  console.log('Draw color:' + draw_color);
  draw = set_draw_color(draw_color,host_removal_pattern,pesticide_application_pattern);
  map.addControl(draw);
  return;
};