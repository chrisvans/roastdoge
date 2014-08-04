function tempPointModel(options) {
    var tempPoint = {};

    // Initialize own attributes based off of the object passed into the creation function
    // You could consider 'tempPoint' to be 'self'
    tempPoint.__init__ = function(options) {
        tempPoint.roastProfileID = options.roastProfileID
        tempPoint.id = options.id
        tempPoint.createURL = options.createURL
        tempPoint.commentCreateURL = options.commentCreateURL
        tempPoint.commentDeleteURL = options.commentDeleteURL
        tempPoint.commentCreateFormURL = options.commentCreateFormURL
        tempPoint.commentIconURL = options.commentIconURL
    }

    tempPoint.__init__(options)

    tempPoint.createPointIcon = function() {

      // Find the index of the roastprofile line in visualization.data, based off of it's id
      // seriesMap must be updated every time a new line is added, so this model knows which 
      // data set it belongs to.
      var roastProfileIndex = seriesMap[tempPoint.roastProfileID]

      // If the line is not set to hidden, then we need to create comment icons on each point that has comments.
      if (!lineChartVis.data[roastProfileIndex].hidden) {

        var roastLineID = lineChartVis.data[roastProfileIndex].id.toString()
        // Grab all the circles within our line's g group.
        var selectString = 'g.nv-group.nv-series-' + seriesMap[roastLineID] + ' > circle.nv-point'
        // Attach the data to each circle.
        d3.selectAll(selectString).datum(lineChartVis.data);
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
                  .attr("x", thisCircle.attr('cx') + iconSize/2)
                  .attr("y", thisCircle.attr('cy') - iconSize)
                  .attr("width", iconSize)
                  .attr("height", iconSize)
                  .attr("class", "svg-comment-icon temppoint_" + tempPoint.id);
            }
          } 
        })
      }
    }

    // Creates a PointComment with the TempPoint as it's parent.
    tempPoint.commentCreate = function() {
      
      var comment = $('#id_comment').val();

      $.ajax({
        url: tempPoint.commentCreateURL,
        type: 'POST',
        data: {
          'tempPointID': tempPoint.id,
          'comment': comment,
        },
        dataType: 'json',
        success: function(response) {
          tempPoint.commentCreateForm();
          tempPoint.createPointIcon();

        }
      })
    }

    // Deletes a comment
    tempPoint.commentDelete = function(commentID) {
      
      $.ajax({
        url: tempPoint.commentDeleteURL,
        type: 'POST',
        data: {
          'tempPointID': tempPoint.id,
          'commentID': commentID,
        },
        dataType: 'json',
        success: function(response) {
          $('#' + commentID).remove()

          if (!response.hasComments) {
            d3.select('.svg-comment-icon.temppoint_' + tempPoint.id).remove()
          }
        }
      })
    }

    // Instantiates a new comment form, and displays all previous comments.
    tempPoint.commentCreateForm = function() {
      $.ajax({
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

          $('#comments').html(response.data);

          // Setup click handler for the submit button
          $('#submit-pointcomment').click(function() {tempPoint.commentCreate()})

          // Setup click handler for the delete button.
          $('.comment-delete').click(function() {
            commentID = $(this).closest('div.comment').prop('id');
            tempPoint.commentDelete(commentID);
          })

          // Scroll the screen down to the comments div.
          var target= "div.comments";
          $('html, body').animate({
            scrollTop: $(target).offset().top
          }, 1000);

        },
        error: function(jqXHR, textStatus, errorThrown ) {

          // log the error

        }
      });
    }

    // Not Implemented - intended to be used to create your own data points.
    tempPoint.create = function() {
      $.ajax({
        url: tempPoint.createURL,
        type: 'POST',
        data: { 
          // tempPoint create data
        },
        dataType: 'json',
        statusCode: {
          403: function() {
            alert( "Permission was denied.  It is possible that your session has timed out.  Please reload the page." );
          }
        },
        success: function(response) {

          // create a new point

        },
        error: function(jqXHR, textStatus, errorThrown ) {

          // log the error

        }
      });
    }

    return tempPoint
}