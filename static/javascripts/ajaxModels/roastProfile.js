function roastProfileModel(options) {
    var roastProfile = {};

    // Initialize own attributes based off of the object passed into the creation function
    // You could consider 'roastProfile' to be 'self'

    // This model is intended to control the CRUD interactions between the roastProfile model and it's child
    // relation, tempPoint, as well as responses and changes to the HTML structure to display changes.
    roastProfile.__init__ = function(options) {
        roastProfile.id = options.id
        roastProfile.roastProfileCreateURL = options.roastProfileCreateURL
        roastProfile.tempPointCreateURL = options.tempPointCreateURL
        roastProfile.graphData = null
    }

    roastProfile.__init__(options)

    roastProfile.create = function() {
      
      // thisCoffeeID is a 'global' variable defining the coffee that this roastprofile ( detail page ) is a child of.

      return $.ajax({
        url: roastProfile.roastProfileCreateURL,
        type: 'POST',
        data: {
          'coffeeID': thisCoffeeID,
        },
        dataType: 'json',
        success: function(response) {
          
          roastProfile.id = response.roastProfileID;

        }
      })
    }

    roastProfile.getGraphData = function() {
      
      return $.ajax({
        url: getRoastProfileGraphDataURL,
        type: 'GET',
        data: {
          'roastProfileID': roastProfile.id,
        },
        dataType: 'json',
        success: function(response) {

          roastProfile.graphData = response.graphData

        }
      })

    }

    return roastProfile
}