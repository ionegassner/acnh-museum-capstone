$("#cat_name").change(function() {
  $("#secondary_form").hide()
  $('#fish').hide()
  $('#sea_creature').hide();
  $('#fossil').hide();
  $('#bug').hide();
  $('#secondary').hide();
});
$("#cat_name").trigger("change")

$("#cat_name").change(function() {
  $("#secondary_form").show()
  if ($(this).val() == "fish") {
    $("#secondary").show()
    $('#fish').show();
  }
  if ($(this).val() == "sea_creature") {
    $("#secondary").show()
    $('#sea_creature').show();
  }
  if ($(this).val() == "fossil") {
    $("#secondary").show()
    $('#fossil').show();
  }
  if ($(this).val() == "bug") {
    $("#secondary").show()
    $('#bug').show();
  } 
});
$("#cat_name").trigger("change")


