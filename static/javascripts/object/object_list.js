// Click handler for deletion of objects in a generic listview.
// Requires that a variable objectInfo be defined, which is an object that looks like
// objectInfo = {
//   name: {{ object.__class__.__name__ }},
//   module: {{ object.__class__.__module__ }},
//   deleteURL: "{% url 'ajax-generic-object-delete' %}",
// }
// The icon to be clicked on should be classed "object-delete"
// The listing li's should be given an id attribute "id_object_{{object.id}}"

$('.object-delete').click(function() {
  var answer = confirm("Are you sure you want to delete this " + objectInfo.name + "?");
  if (answer) {
    var objectID = $(this).attr("id")

    $.ajax({
      url: objectInfo.deleteURL,
      type: 'POST',
      data: {
        'objectName': objectInfo.name,
        'objectModule': objectInfo.module, 
        'objectID': objectID},
      dataType: 'JSON',
    })
      .done(function (response){
        $('li#id_object_' + objectID).remove()
      })
  }
})