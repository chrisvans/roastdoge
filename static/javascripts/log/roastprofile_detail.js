// Callback called after line chart creation and update.  Responsible for creating/updating svg icons representing whether or not
// a point has comments on it.
// TODO: This should be part of one of the models.

var pointIconPreCall = function(visualization) {
  // Remove all previous comments icons within this visualization.
  d3.select(visualization.selectElement).selectAll('.svg-comment-icon').remove()
}
var pointIconCallback = function(visualization) {

  // Iterate over each element in data, where each element represents a line
  for (var dataIndex=0; dataIndex<visualization.data.length; dataIndex++) {

    // If the data has a hidden attribute set to true, that line is hidden, so we don't want to draw it's comment icons
    if (!visualization.data[dataIndex].hidden) {

      // Find the id on the data line, which is the id of the roastprofile associated with this line.
      var roastLineID = visualization.data[dataIndex].id.toString()

      // Construct the select string, we're looking for all of the circles ( points ) on a given roast profile's line
      var selectString = 'g.nv-group.nv-series-' + visualization.seriesMap[roastLineID] + ' > circle.nv-point'

      // Associate the data with each circle
      // TODO: Instead of attaching the whole data array to each circle, attach each corresponding value ( from data[x].values ) to the circle
      d3.selectAll(selectString).datum(visualization.data);

      // Iterate over each circle, that now has the associated data
      d3.selectAll(selectString).each(function(d, i) { 

        // Grab the value that should match the circle we're iterating over, since the circles are in the same order as the data[x].values array

        if (d[dataIndex].values[i].hasComments) { 
          var thisCircle = d3.select(this)

          var parentG = d3.select(thisCircle.node().parentNode)

          // Append the icon as an svg image to the parent g element, and set it to be near the point
          var iconSize = 16;
          parentG
            .append("image")
              .attr("xlink:href", URL.tempPoint.commentIcon)
              .attr("x", thisCircle.attr('cx'))
              .attr("y", (parseInt(thisCircle.attr('cy')) - iconSize).toString())
              .attr("width", iconSize)
              .attr("height", iconSize)
              // Give it a unique id that matched the temppoint's ID, so we can dynamically select it later
              // Used for when a temppoint has all of it's comments deleted, and needs to tell this node
              // to remove this comment icon.
              .attr("class", "svg-comment-icon temppoint_" + d[dataIndex].values[i].id);
        } 
      })
    }
  }
}

// Options to be passed into the lineChartVisualization model.
lineOptions = { 
  // selectElement is the element that the svg will be attached to when it is created.
  'selectElement': selectElement, 
  // data is an array of objects, and looks like this:
  // [
  //   {
  // ---> # Values is an array of objects, where each object is the x and y coordinate of the point,
  // ---> # the id of that object (temppoint), and a boolean noting whether or not is hasComments.
  //     "values": 
  //       [
  //         {"y": 80.0, "x": 0, "id": 62, "hasComments": false}, 
  //         {"y": 92.3, "x": 1, "id": 63, "hasComments": false}, 
  //         ...,
  //         ...,
  //         ...,
  //       ], 
  // ---> # The id of the roastprofile
  //     "id": 4,
  // ---> # The name of the roastprofile, used for the legend ( not implemented ) 
  //     "key": "Miiri - 4"
  //   }
  // ]
  // data also supports another key, 'hidden', which should be a boolean, and on chartUpdate this will
  // hide or show the corresponding line.
  'data': data, 
  'margin': margin, 
  'width': width, 
  'height': height,
  // Any functions put into this list will be called on createChart and updateChart.
  'storedCallbacks': [pointIconCallback],
  'preUpdateCalls': [pointIconPreCall],
  'seriesMap': seriesMap,
}

// Initialize Chart Model.
var lineChartVis = lineChartVisualization(lineOptions);

// Callback that sets all points in the graph to, once clicked, create a matching tempPoint model
// and create an empty comment form, with all previous comments of that tempPoint listed below it.
// This does not need to be updated, it will always run on any click of any point created within this chart.
var pointClickCallback = function(visualization) {
  visualization.nvchart.lines.dispatch.on('elementClick', null)
  visualization.nvchart.lines.dispatch.on('elementClick', function(element) {
    var pointOptions = {
      roastProfileID: element.series.id,
      id: element.point.id,
      URL: URL.tempPoint,
      visualization: visualization,
    }
    var tempPoint = tempPointModel(pointOptions);
    var ajaxCallCommentCreateForm = tempPoint.commentCreateForm();
    var callback = function(response) {

      $('#comments').html(response.data);

      // Setup click handler for the submit button
      $('#submit-pointcomment').click(function() {
        var ajaxCallCommentCreate = tempPoint.commentCreate('#id_comment');
        ajaxCallCommentCreate.done(function(){
          var ajaxCallCommentCreateFormInner = tempPoint.commentCreateForm();
          tempPoint.createPointIcon();
          ajaxCallCommentCreateFormInner.done(callback);
        })
      })

      // Setup click handler for the delete button.
      $('.comment-delete').click(function() {
        commentID = $(this).closest('div.comment').prop('id');
        var ajaxCallCommentDelete = tempPoint.commentDelete(commentID);
        ajaxCallCommentDelete.done(function(response) {
          $('#' + response.deletedCommentID).remove()

          if (!response.hasComments) {
            d3.select('.svg-comment-icon.temppoint_' + tempPoint.id).remove()
          }
        })
      })

      // Scroll the screen down to the comments div.
      var target= "div.comments";
      $('html, body').animate({
        scrollTop: $(target).offset().top
      }, 1000);
    }

    ajaxCallCommentCreateForm.done(callback)
  })
}

lineChartVis.createChart([pointClickCallback]);


var setRoastProfileGraphData = function(roastProfileID, callback) {

  var roastProfile = roastProfileModel({
    'id': roastProfileID,
    'URL': URL.roastProfile,
  })

  var ajaxCall = roastProfile.getGraphData();
  ajaxCall.done(callback)

}

var updateChartGraphData = function(roastProfileID) {

    var callback = function(response) {
      var graphData = response.graphData;
      var seriesCount = Object.keys(lineChartVis.seriesMap).length
      
      var dataAlreadyPresent = (roastProfileID in lineChartVis.seriesMap)

      if (dataAlreadyPresent) {
        lineChartVis.data[lineChartVis.seriesMap[roastProfileID]] = graphData
      } else {
        lineChartVis.seriesMap[roastProfileID] = seriesCount.toString()
        lineChartVis.data.push(graphData)
      }

      lineChartVis.updateChart();
    }
    setRoastProfileGraphData(roastProfileID, callback)

}
// Setup handler for roastprofile select form change, and loading data into chart.
$("#id_roastprofile_select").change(function() {

  var roastProfileID = $(this).val()

  if (!roastProfileID) { return }

  updateChartGraphData(roastProfileID)

})

// Setup handler for recording a new profile & stopping the recording process.
$("#listen-newprofile").click(function() {
  if (!$(this).data("listening")) {
    $(this).data("listening", true)
    $(this).val("Recording...  Click to stop recording.")

    var roastProfile = roastProfileModel({
      'roastProfileCreateURL': roastProfileCreateURL,
    })

    var callback = function(response) {
      var updateChart = function() {
        updateChartGraphData(roastProfile.id)
      }

      listenUpdatesID = setInterval(updateChart, 5000);
    }

    var ajaxCall = roastProfile.create();
    ajaxCall.done(callback)

  } else {
    clearInterval(listenUpdatesID)
    $(this).data("listening", false)
    $(this).val("Start Recording a New Profile")
  }
})
