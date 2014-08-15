// Depends on setupAjax.js, baseAjaxModel.js, jQuery

function TempPointModel(options) {
  // This model is intended to control the CRUD interactions between the tempPoint model and it's child
  // relation, pointComment
  var self = this;

  // Inherit from BaseAjaxModel
  BaseAjaxModel.apply(this, arguments)

  options = (typeof(options) === 'undefined') ? {} : options

  // Initialize own attributes based off of the object passed into the creation function
  self.modelName = 'TempPoint'
  self.roastProfileID = self.setAttrOrNull(options.roastProfileID)
  self.visualization = self.setAttrOrNull(options.visualization)

  // TODO: Some way to signify that this function is not an ajax call, and modifies only the DOM
  self.createPointIcon = function() {

    // if (self.visualization === null) {
    //   throw self.
    // }

    // Find the index of the roastprofile line in visualization.data, based off of it's id
    // seriesMap must be updated every time a new line is added, so this model knows which 
    // data set it belongs to.
    var roastProfileIndex = self.visualization.seriesMap[self.roastProfileID]

    // If the line is not set to hidden, then we need to create comment icons on each point that has comments.
    if (!self.visualization.data[roastProfileIndex].hidden) {

      var roastLineID = self.visualization.data[roastProfileIndex].id.toString()
      // Grab all the circles within our line's g group.
      var selectString = 'g.nv-group.nv-series-' + self.visualization.seriesMap[roastLineID] + ' > circle.nv-point'
      // Attach the data to each circle.
      d3.selectAll(selectString).datum(self.visualization.data);
      // Iterate over each circle, passing in the data set.
      // TODO: Attach each circle's own data to itself, rather than passing in the whole data array.
      d3.selectAll(selectString).each(function(d, i) { 

        // Find the data value that corresponds to THIS tempPoint.
        if (d[roastProfileIndex].values[i].id == self.id) { 

          // Update the data to reflect that this point has at least one comment.
          d[roastProfileIndex].values[i].hasComments = true;

          var commentIcon = d3.select('.svg-comment-icon.temppoint_' + self.id);

          // If the node is null, we know that there was no icon previously.
          if (commentIcon.node() == null) {

            // Create the icon, and attach it to the parent g with similiar x and y attributes to the circle it belongs to.
            var thisCircle = d3.select(this)

            var parentG = d3.select(thisCircle.node().parentNode)
            var iconSize = 16;
            parentG
              .append("image")
                .attr("xlink:href", self.URL.commentIcon)
                .attr("x", thisCircle.attr('cx'))
                .attr("y", (parseInt(thisCircle.attr('cy')) - iconSize).toString())
                .attr("width", iconSize)
                .attr("height", iconSize)
                .attr("class", "svg-comment-icon temppoint_" + self.id);
          }
        } 
      })
    }
  }

  // Creates a PointComment with the TempPoint as it's parent.
  self.commentCreate = function(inputElementSelector) {
    
    var comment = $(inputElementSelector).val();

    return $.ajax({
      url: self.URL.commentCreate,
      type: 'POST',
      data: {
        'TempPointID': self.id,
        'comment': comment,
      },
      dataType: 'json',
      success: function(response) {

        // response = {}

      },
      error: function(jqXHR, textStatus, errorThrown ) {

        console.log(textStatus + ' ' + errorThrown)

      }
    })
  }

  // Deletes a comment
  self.commentDelete = function(commentID) {
    
    return $.ajax({
      url: self.URL.commentDelete,
      type: 'POST',
      data: {
        'TempPointID': self.id,
        'commentID': commentID,
      },
      dataType: 'json',
      success: function(response) {

        // response = {
        //     'deletedCommentID': commentID,
        //     'hasComments': Boolean,
        // }

      },
      error: function(jqXHR, textStatus, errorThrown ) {

        console.log(textStatus + ' ' + errorThrown)

      }
    })
  }

  // Instantiates a new comment form, and displays all previous comments.
  self.commentCreateForm = function() {
    return $.ajax({
      url: self.URL.commentCreateForm,
      type: 'GET',
      data: { 
        'TempPointID': self.id,
      },
      dataType: 'json',
      statusCode: {
        403: function() {
          alert( "Permission was denied.  It is possible that your session has timed out.  Please reload the page." );
        }
      },
      success: function(response) {

        // response = {
        //   data: "Formatted HTML of comment input form & previous comments for this tempPoint" 
        // }

      },
      error: function(jqXHR, textStatus, errorThrown ) {

        console.log(textStatus + ' ' + errorThrown)

      }
    });
  }

  return self
}