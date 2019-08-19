function toggleVisibilityOnOff(toggle_id, visibility_id) {
    if ($(toggle_id).is(':checked')){
        $(visibility_id).show();}
      else {$(visibility_id).hide();}   
}

function togglePolynomialVisibility(toggle_id_1, toggle_id_2, toggle_id_3, visibility_id_1, visibility_id_2, visibility_id_3) {
    if ($(toggle_id_3).is(':checked')){
        $(visibility_id_2).show();
        $(visibility_id_3).show();}
    else if ($(toggle_id_2).is(':checked')){
        $(visibility_id_2).show();   
        $(visibility_id_3).hide();}
    else {
        $(visibility_id_2).hide();   
        $(visibility_id_3).hide();}
}
  
