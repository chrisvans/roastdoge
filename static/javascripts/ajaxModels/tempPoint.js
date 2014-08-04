function tempPointModel(options) {
    tempPoint = {};

    tempPoint.__init__ = function(options) {
        tempPoint.id = options.id
        tempPoint.createURL = options.createURL
        tempPoint.commentCreateURL = options.commentCreateURL
        tempPoint.commentDeleteURL = options.commentDeleteURL
        tempPoint.commentCreateFormURL = options.commentCreateFormURL
        tempPoint.commentIconURL = options.commentIconURL
    }

    tempPoint.__init__(options)

    tempPoint.updatePointIcons = function() {
      d3.selectAll('circle.nv-point').datum(lineChartVis.data);
      d3.selectAll('circle.nv-point').each(function(d, i) { 
        if (d[0].values[i].id == tempPoint.id) { 
          var commentIcon = d3.select('.svg-comment-icon.temppoint_' + tempPoint.id);

          if (commentIcon.node() == null) {
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
          tempPoint.updatePointIcons();

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

          $('#submit-pointcomment').click(function() {tempPoint.commentCreate()})

          $('.comment-delete').click(function() {
            commentID = $(this).closest('div.comment').prop('id');
            tempPoint.commentDelete(commentID);
          })

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