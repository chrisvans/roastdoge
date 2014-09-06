function BaseAjaxModel(options) {
  options = (typeof(options) === 'undefined') ? {} : options

  // The variable 'self' is used to represent this, as we want to reference the object within
  // it's own functions, where the variable 'this' would no longer represent the object.
  var self = this;

  // This model is intended to control the CRUD interactions on a basic model.

  // Each ajax method returns itself, and it is expected that you should use the returned object's '.done', '.fail', and '.always'
  // methods to control what happens in regard to responses and changes to the HTML structure.
  // ref - http://api.jquery.com/category/deferred-object/

  // UTILITY METHODS

  // Any methods not defined should be set to null, because undefined is evil.
  self.setAttrOrNull = function (attr) {
    return (typeof(attr) === 'undefined') ? null : attr
  }

  // ATTR ASSIGNMENTS

  // Always overwrite the modelName with an appropriate name.
  self.modelName = 'BaseAjaxModel'

  // ID should match the ID of the represented model in the DB.  If this is a new model, An id will be attached upon 
  // successful run of the 'create' method.
  // The response to the create AJAX call must return a modelID as 'self.modelName+"ID"'
  self.id = self.setAttrOrNull(options.id)
  // All CRUD methods are reliant on a set of URLs, which should at least have the following:
  // {
  // 'create':url,
  // 'delete':url,
  // 'read':url, # Not Implemented
  // 'update':url # Not Implemented
  // }
  self.crudURL = self.setAttrOrNull(options.crudURL)

  // AJAX METHODS

  // Each ajax method returns itself, and it is expected that you should use the returned object's '.done', '.fail', and '.always'
  // methods to control what happens in regard to responses and changes to the HTML structure.

  // If you overwrite the create method, you should also run the _validateCreate method.

  self.create = function() {

    self._validateCreate()

    return $.ajax({
      url: self.crudURL.create,
      type: 'POST',
      data: {
      },
      dataType: 'json',
      success: function(response) {

      	self.id = response[self.modelName+'ID']

      },
      error: function(jqXHR, textStatus, errorThrown ) {

        console.log(textStatus + ' ' + errorThrown)

      }
    })
  }

  // If you overwrite the delete method, you should also run the _validateDelete method.
  self.delete = function() {

    self._validateDelete()

    return $.ajax({
      url: self.crudURL.delete,
      type: 'DELETE',
      data: {'id':self.id},
      dataType: 'json',
      success: function(response) {

      },
      error: function(jqXHR, textStatus, errorThrown ) {

        console.log(textStatus + ' ' + errorThrown)

      }
    })
  }

  // VALIDATION

  self.validationError = function(methodString, error) {
  	return self.modelName + '.' + methodString + ' : ' + error
  }

  // Any methods that use an Ajax call should run _validateCRUD, with the name of that method 
  // as the first argument.
  self._validateCRUD = function(methodString) {
    // methodString should be a CRUD method, or the method that is being called.
    // 'create', 'read', 'update', and 'delete' are the identified strings
    // used to auto-detect what level of validation is needed.

    // CRUD Validators

    // All CRUD Methods require that a crudURL be set.
    if (self.crudURL === null) {
      throw self.validationError(methodString, 'Method was attempted with no crudURL attribute set.')
    }

    if ((methodString !== 'create') && (self.id === null)) {
      throw self.validationError(methodString, 'Attempted to access data with no id attribute set.')
    }

  }

  self._validateCreate = function() {
    // 'create' Validators

    self._validateCRUD('create')

    if (typeof(self.crudURL.create) === 'undefined') {
      throw self.validationError('create', 'Method was attempted with no crudURL.create attribute set.')
    }
  }

  self._validateDelete = function() {
    // 'delete' Validators

    self._validateCRUD('delete')

    if (typeof(self.crudURL.delete) === 'undefined') {
      throw self.validationError('delete', 'Method was attempted with no crudURL.delete attribute set.')
    }

    if (typeof(self.id) === 'undefined') {
      throw self.validationError('delete', 'Attempted to run with no id attribute set.')
    }
  }

}