// Click handler for deletion of roast profiles.

$('.roastprofile-delete').click(function() {
  var answer = confirm("Are you sure you want to delete this profile?");
  if (answer) {
    roastProfile = roastProfileModel({
        'id': $(this).attr("id"),
        'URL': URL.roastProfile
    })
    var ajaxCallRoastProfileDelete = roastProfile.delete()
    ajaxCallRoastProfileDelete.done(function (response){
        $('li#id_roastprofile_' + response.deletedRoastProfileID).remove()
    })
  }
})