// Click handler for deletion of roast profiles.

$('.roastprofile-delete').click(function() {
  var answer = confirm("Are you sure you want to delete this profile?");
  if (answer) {
    var roastProfileID = $(this).attr("id")
    var roastProfile = new RoastProfile({
        'id': roastProfileID,
        'URL': URL.roastProfile
    })
    roastProfile.delete()
      .done(function (response){
        $('li#id_roastprofile_' + roastProfileID).remove()
      })
  }
})