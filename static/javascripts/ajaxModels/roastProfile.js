// Depends on setupAjax.js, baseAjaxModel.js, jQuery

function RoastProfile(options) {
  // This model is intended to control the CRUD interactions between the roastProfile model and it's child
  // relation, tempPoint.

  // Inherit from BaseAjaxModel
  BaseAjaxModel.apply(this, arguments)

  options = (typeof(options) === 'undefined') ? {} : options

  // The variable 'self' is used to represent this, as we want to reference the object within
  // it's own functions, where the variable 'this' would no longer represent the object.
  var self = this;

  // Initialize own attributes based off of the object passed into the creation function

  self.modelName = 'RoastProfile'
  self.coffeeID = self.setAttrOrNull(options.coffeeID)
  self.graphData = null

  // Overwrites BaseAjaxModel's create, as we want to pass in the related model as a parent.
  self.create = function() {

    self._validateCreate()

    return $.ajax({
      url: self.crudURL.list,
      type: 'POST',
      data: {
        'name': 'New Profile',
        'coffee': self.coffeeID,
      },
      dataType: 'json',
      success: function(response) {
        
        self.id = response.id;
        self.graphData = response.temp_graph_data;

      },
      error: function(jqXHR, textStatus, errorThrown ) {

        console.log(textStatus + ' ' + errorThrown)

      }
    })
  }

  self.getGraphData = function() {

    self._validateCRUD('getGraphData')
    
    return $.ajax({
      url: self.crudURL.list + self.id,
      type: 'GET',
      data: {},
      dataType: 'json',
      success: function(response) {

        self.graphData = response.temp_graph_data

      },
      error: function(jqXHR, textStatus, errorThrown ) {

        console.log(textStatus + ' ' + errorThrown)

      }
    })

  }

  self.getGraphDataSlice = function(sliceStart) {

    self._validateCRUD('getGraphDataSlice')

    return $.ajax({
      url: self.crudURL.getGraphDataSlice,
      type: 'GET',
      data: {
        'id': self.id,
        'sliceStart': sliceStart,
      },
      dataType: 'json',
      success: function(response) {

        // self.graphData.values.push(response.graphDataValues)

        // response = {
        //   'graphDataValues': roastprofile.get_temp_graph_data_slice(sliceStart)
        // }
        
      },
      error: function(jqXHR, textStatus, errorThrown) {

        console.log(textStatus + ' ' + errorThrown)

      }
    })

  }

  var parent_validateCreate = self._validateCreate
  self._validateCreate = function() {
    // We want our own custom validator, but also want to call the BaseAjaxModel's validator

    // RoastProfiles must be created as a child of a coffee.
    if (typeof(self.coffeeID) === 'undefined') {
      throw self.validationError('create', 'Attempted to run with no coffeeID attribute set.')
    }

    // Run parent validator
    parent_validateCreate.apply(self)
  }

}