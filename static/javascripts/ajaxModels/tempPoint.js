function tempPointModel(options) {
    var tempPoint = {};

    // Initialize own attributes based off of the object passed into the creation function
    // You could consider 'tempPoint' to be 'self'

    // This model is intended to control the CRUD interactions between the tempPoint model and it's child
    // relation, pointComments, as well as responses and changes to the HTML structure to display changes.
    tempPoint.__init__ = function(options) {
        tempPoint.roastProfileID = options.roastProfileID
        tempPoint.id = options.id
        tempPoint.commentCreateURL = options.commentCreateURL
        tempPoint.commentDeleteURL = options.commentDeleteURL
        tempPoint.commentCreateFormURL = options.commentCreateFormURL
        tempPoint.commentIconURL = options.commentIconURL
        tempPoint.visualization = options.visualization
    }

    tempPoint.__init__(options)

    tempPoint.createPointIcon = function() {

      // Find the index of the roastprofile line in visualization.data, based off of it's id
      // seriesMap must be updated every time a new line is added, so this model knows which 
      // data set it belongs to.
      var roastProfileIndex = tempPoint.visualization.seriesMap[tempPoint.roastProfileID]

      // If the line is not set to hidden, then we need to create comment icons on each point that has comments.
      if (!tempPoint.visualization.data[roastProfileIndex].hidden) {

        var roastLineID = tempPoint.visualization.data[roastProfileIndex].id.toString()
        // Grab all the circles within our line's g group.
        var selectString = 'g.nv-group.nv-series-' + tempPoint.visualization.seriesMap[roastLineID] + ' > circle.nv-point'
        // Attach the data to each circle.
        d3.selectAll(selectString).datum(tempPoint.visualization.data);
        // Iterate over each circle, passing in the data set.
        // TODO: Attach each circle's own data to itself, rather than passing in the whole data array.
        d3.selectAll(selectString).each(function(d, i) { 

          // Find the data value that corresponds to THIS tempPoint.
          if (d[roastProfileIndex].values[i].id == tempPoint.id) { 

            // Update the data to reflect that this point has at least one comment.
            d[roastProfileIndex].values[i].hasComments = true;

            var commentIcon = d3.select('.svg-comment-icon.temppoint_' + tempPoint.id);

            // If the node is null, we know that there was no icon previously.
            if (commentIcon.node() == null) {

              // Create the icon, and attach it to the parent g with similiar x and y attributes to the circle it belongs to.
              var thisCircle = d3.select(this)

              var parentG = d3.select(thisCircle.node().parentNode)
              var iconSize = 16;
              parentG
                .append("image")
                  .attr("xlink:href", tempPoint.commentIconURL)
                  .attr("x", thisCircle.attr('cx'))
                  .attr("y", (parseInt(thisCircle.attr('cy')) - iconSize).toString())
                  .attr("width", iconSize)
                  .attr("height", iconSize)
                  .attr("class", "svg-comment-icon temppoint_" + tempPoint.id);
            }
          } 
        })
      }
    }

    // Creates a PointComment with the TempPoint as it's parent.
    tempPoint.commentCreate = function(inputElementSelector) {
      
      var comment = $(inputElementSelector).val();

      return $.ajax({
        url: tempPoint.commentCreateURL,
        type: 'POST',
        data: {
          'tempPointID': tempPoint.id,
          'comment': comment,
        },
        dataType: 'json',
        success: function(response) {

        }
      })
    }

    // Deletes a comment
    tempPoint.commentDelete = function(commentID) {
      
      return $.ajax({
        url: tempPoint.commentDeleteURL,
        type: 'POST',
        data: {
          'tempPointID': tempPoint.id,
          'commentID': commentID,
        },
        dataType: 'json',
        success: function(response) {

        }
      })
    }

    // Instantiates a new comment form, and displays all previous comments.
    tempPoint.commentCreateForm = function() {
      return $.ajax({
        url: tempPoint.commentCreateFormURL,
        type: 'GET',
        data: { 
          'tempPointID': tempPoint.id,
        },
        dataType: 'json',
        statusCode: {
          403: function() {
            alert( "Permission was denied.  It is possible that your session has timed out.  Please reload the page." );
          }
        },
        success: function(response) {

        },
        error: function(jqXHR, textStatus, errorThrown ) {

          // log the error

        }
      });
    }

    return tempPoint
}