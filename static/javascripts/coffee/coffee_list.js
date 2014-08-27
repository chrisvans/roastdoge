$('.coffee-delete').click(function() {
  var answer = confirm("Are you sure you want to delete this coffee?");
  if (answer) {
    var coffeeID = $(this).attr("id")
    $.ajax({
      url: coffeeDeleteURL,
      type: 'POST',
      data: {'coffeeID': coffeeID},
      dataType: 'JSON',
    })
      .done(function (response){
        $('li#id_coffee_' + coffeeID).remove()
      })
  }
})