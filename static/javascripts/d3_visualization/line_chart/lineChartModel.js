// Create an object to handle data storage, chart creation and update
function lineChartVisualization(options) {

  var visualization = {}

  // Create object with parameters required for chart creation
  // You can set these attributes manually, and then call visualization.updateChart();
  visualization.__init__ = function(options) {

    visualization.selectElement = options.selectElement;

    // each object within the data attr now supports an extra boolean key "hidden", which will upon update, hide or unhide the line
    visualization.data = options.data;

    visualization.margin = options.margin;
    visualization.width = options.width;
    visualization.height = options.height;
    visualization.xAxisLabel = options.xAxisLabel || 'Time in Minutes';
    visualization.yAxisLabel = options.yAxisLabel || 'Temperature';
    visualization.nvchart = '';
    visualization.tempMeasurement = options.tempMeasurement || 'C';  
    visualization.storedCallbacks = options.storedCallbacks || [];
    visualization.preUpdateCalls = options.preUpdateCalls || [];

  }

  // Run the init method
  visualization.__init__(options);

  visualization.callPreUpdateCalls = function() {
    for (var i=0; i<visualization.preUpdateCalls.length; i++) {
      visualization.preUpdateCalls[i]();
    }    
  }

  visualization.callStoredCallbacks = function() {
    for (var i=0; i<visualization.storedCallbacks.length; i++) {
      visualization.storedCallbacks[i]();
    }
  }

  // Known issue: Chart does not scale based on visible lines, but on all lines regardless.
  visualization.setLinesVisibility = function() {
    for (var i=0; i<visualization.data.length; i++) {
      lineG = d3.select(visualization.selectElement + ' svg g g g.nv-linesWrap g.nvd3.nv-wrap.nv-line g g.nv-groups > g.nv-group.nv-series-' + i)
      if (visualization.data[i].hidden) {
        lineG.style('visibility', 'hidden')
      } else {
        lineG.style('visibility', 'visible')
      }
    }
  }

  visualization.createChart = function (callbacks) {

    visualization.xScale = d3.scale.linear()
      .domain([0, d3.max(visualization.data, function(d) { return d.values; })])
      .range([0, d3.max(visualization.data, function(d) { return d.values; })]);

    nv.addGraph(function() {
      visualization.nvchart = nv.models.lineChart()
        .color(d3.scale.category10().range())
        .showLegend(false);

      visualization.nvchart.x(function(d,i) { 
        var time = new Date(d.x)
        return time; 
      })

      visualization.nvchart.xAxis // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
        .axisLabel(visualization.xAxisLabel)
        .tickFormat(d3.format(',.0f'))
      //.tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); })
        .scale(visualization.xScale);

      visualization.nvchart.yAxis
        .axisLabel(visualization.yAxisLabel)
        .tickFormat( function(d) {
          formatted_tick = d3.format(',.1f')(d);
          return formatted_tick + ' ' + visualization.tempMeasurement;
        });

      d3.select(visualization.selectElement)
        .attr("style", "height:" + (visualization.height + visualization.margin.top + visualization.margin.bottom).toString() )

      d3.select(visualization.selectElement)
        .append('svg')
          .attr("height", visualization.height + visualization.margin.top + visualization.margin.bottom)
          .datum(visualization.data)
          .call(visualization.nvchart);

      nv.utils.windowResize( function() {
        d3.select(visualization.selectElement + ' svg')
        .transition()
          .call(visualization.nvchart);
        visualization.nvchart.update();
      });
      
      function callCallbacks() {
        if ((callbacks) && (callbacks.length > 0)) {
          for (var i=0; i<callbacks.length; i++) {
            callbacks[i]()
          }
        }
      }

      callCallbacks();

      visualization.callStoredCallbacks()

      nv.utils.windowResize(function() {
        visualization.callPreUpdateCalls();
        visualization.nvchart.update;
        setTimeout(visualization.callStoredCallbacks, 1000);
      })

      return visualization.nvchart;

    });

    visualization.setLinesVisibility()

  }

  visualization.updateChart = function(callbacks) {

    visualization.callPreUpdateCalls()

    visualization.xScale = d3.scale.linear()
      .domain([0, d3.max(visualization.data, function(d) { return d.values; })])
      .range([0, d3.max(visualization.data, function(d) { return d.values; })]);

    visualization.nvchart.x(function(d,i) { 
      var time = new Date(d.x)
      return time; 
    })

    visualization.nvchart.xAxis // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
      .axisLabel(visualization.xAxisLabel)
      .tickFormat(d3.format(',.0f'))
    //.tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); })
      .scale(visualization.xScale);

    visualization.nvchart.yAxis
      .axisLabel(visualization.xAxisLabel)
      .tickFormat( function(d) {
        formatted_tick = d3.format(',.1f')(d);
        return formatted_tick + ' ' + visualization.tempMeasurement;
      });

    d3.select(visualization.selectElement)
      .attr("style", "height:" + (visualization.height + visualization.margin.top + visualization.margin.bottom).toString() )

    d3.select(visualization.selectElement + ' svg')
      .attr("height", visualization.height + visualization.margin.top + visualization.margin.bottom)
      .datum(visualization.data)
      .transition()
      .call(visualization.nvchart);

    visualization.nvchart.update();

    if ((callbacks) && (callbacks.length > 0)) {
      for (var i=0; i<callbacks.length; i++) {
        callbacks[i]()
      }
    }

    visualization.setLinesVisibility()

    setTimeout(visualization.callStoredCallbacks, 1000)

  }

  return visualization;

}