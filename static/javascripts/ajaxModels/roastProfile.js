function roastProfileModel(options) {
  var self = {};

  // Initialize own attributes based off of the object passed into the creation function

  // This model is intended to control the CRUD interactions between the roastProfile model and it's child
  // relation, tempPoint, as well as responses and changes to the HTML structure to display changes.
  self.__init__ = function(options) {
      self.id = options.id
      self.URL = options.URL
      self.graphData = null
  }

  self.__init__(options)

  self.create = function() {
    
    // thisCoffeeID is a 'global' variable defining the coffee that this roastprofile ( detail page ) is a child of.

    return $.ajax({
      url: self.URL.create,
      type: 'POST',
      data: {
        'coffeeID': thisCoffeeID,
      },
      dataType: 'json',
      success: function(response) {
        
        self.id = response.roastProfileID;

      }
    })
  }

  self.delete = function() {
    return $.ajax({
      url: self.URL.delete,
      type: 'POST',
      data: {
        'roastProfileID': self.id,
      },
      dataType: 'json',
      success: function(response) {

      }
    })
  }

  self.getGraphData = function() {
    
    return $.ajax({
      url: self.URL.getRoastProfileGraphData,
      type: 'GET',
      data: {
        'roastProfileID': self.id,
      },
      dataType: 'json',
      success: function(response) {

        self.graphData = response.graphData

      }
    })

  }

  return self
}