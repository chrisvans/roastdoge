function roastProfileModel(options) {
  var self = {};

  // Initialize own attributes based off of the object passed into the creation function

  // This model is intended to control the CRUD interactions between the roastProfile model and it's child
  // relation, tempPoint.

  // Each ajax method returns itself, and it is expected that you should use the returned object's '.done', '.fail', and '.always'
  // methods to control what happens in regard to responses and changes to the HTML structure.
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

        // response = {
        //     'roastProfileID': roastprofile.id,
        //     'roastProfileGraphData': roastprofile.get_temp_graph_data(),
        // }

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

        // response = {
        //     'deletedRoastProfileID': roastProfileID
        // }

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

        // response = {
        //     'graphData': roastprofile.get_temp_graph_data()
        // }

      }
    })

  }

  return self
}