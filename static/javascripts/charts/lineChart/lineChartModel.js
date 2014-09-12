// Create an object to handle data storage, chart creation and update
function lineChartVisualization(options) {

  var self = {}

  // Create object with parameters required for chart creation
  // You can set these attributes manually, and then call visualization.updateChart();
  self.__init__ = function(options) {

    self.selectElement = options.selectElement;

    // each object within the data attr now supports an extra boolean key "hidden", which will upon update, hide or unhide the line
    self.data = options.data;

    self.margin = options.margin;
    self.width = options.width;
    self.height = options.height;
    self.xAxisLabel = options.xAxisLabel || 'Time in Seconds';
    self.yAxisLabel = options.yAxisLabel || 'Temperature';
    self.nvchart = '';
    self.tempMeasurement = options.tempMeasurement || 'C';  
    self.storedCallbacks = options.storedCallbacks || [];
    self.preUpdateCalls = options.preUpdateCalls || [];
    self.seriesMap = options.seriesMap || {};

  }

  // Run the init method
  self.__init__(options);

  self.callPreUpdateCalls = function() {
    for (var i=0; i<self.preUpdateCalls.length; i++) {
      self.preUpdateCalls[i](self);
    }    
  }

  self.callStoredCallbacks = function() {
    for (var i=0; i<self.storedCallbacks.length; i++) {
      self.storedCallbacks[i](self);
    }
  }

  // Known issue: Chart does not scale based on visible lines, but on all lines regardless.
  self.setLinesVisibility = function() {
    for (var i=0; i<self.data.length; i++) {
      var lineG = d3.select(self.selectElement + ' svg g g g.nv-linesWrap g.nvd3.nv-wrap.nv-line g g.nv-groups > g.nv-group.nv-series-' + i)
      if (self.data[i].hidden) {
        lineG.style('visibility', 'hidden')
      } else {
        lineG.style('visibility', 'visible')
      }
    }
  }

  self.createChart = function (callbacks) {

    self.xScale = d3.scale.linear()
      .domain([0, d3.max(self.data, function(d) { return d.values; })])
      .range([0, d3.max(self.data, function(d) { return d.values; })]);

    nv.addGraph(function() {
      self.nvchart = nv.models.lineChart()
        .color(d3.scale.category10().range())
        .showLegend(false)
        .interpolate('monotone');

      self.nvchart.x(function(d,i) { 
        var time = new Date(d.x)
        return time; 
      })

      self.nvchart.xAxis // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
        .axisLabel(self.xAxisLabel)
        .tickFormat(d3.format(',.0f'))
      //.tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); })
        .scale(self.xScale);

      self.nvchart.yAxis
        .axisLabel(self.yAxisLabel)
        .tickFormat( function(d) {
          if (self.tempMeasurement == 'F') {
            function c2f(value) {
              return value * 1.8 + 32;
            }
            var formatted_tick = d3.format(',.1f')(c2f(d));
          } else {
            var formatted_tick = d3.format(',.1f')(d);
          }
          return formatted_tick + ' ' + self.tempMeasurement;
        });

      d3.select(self.selectElement)
        .attr("style", "height:" + (self.height + self.margin.top + self.margin.bottom).toString() )

      d3.select(self.selectElement)
        .append('svg')
          .attr("height", self.height + self.margin.top + self.margin.bottom)
          .datum(self.data)
          .call(self.nvchart);

      nv.utils.windowResize( function() {
        d3.select(self.selectElement + ' svg')
        .transition()
          .call(self.nvchart);
        self.nvchart.update();
      });
      
      function callCallbacks() {
        if ((callbacks) && (callbacks.length > 0)) {
          for (var i=0; i<callbacks.length; i++) {
            callbacks[i](self)
          }
        }
      }

      callCallbacks();

      self.callStoredCallbacks()

      nv.utils.windowResize(function() {
        self.callPreUpdateCalls();
        self.nvchart.update;
        setTimeout(self.callStoredCallbacks, 1000);
      })

      return self.nvchart;

    });

    self.setLinesVisibility()

  }

  self.updateChart = function(callbacks) {

    self.callPreUpdateCalls()

    self.xScale = d3.scale.linear()
      .domain([0, d3.max(self.data, function(d) { return d.values; })])
      .range([0, d3.max(self.data, function(d) { return d.values; })]);

    self.nvchart.x(function(d,i) { 
      var time = new Date(d.x)
      return time; 
    })

    self.nvchart.xAxis // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
      .axisLabel(self.xAxisLabel)
      .tickFormat(d3.format(',.0f'))
    //.tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); })
      .scale(self.xScale);

    self.nvchart.yAxis
      .axisLabel(self.yAxisLabel)
      .tickFormat( function(d) {
        if (self.tempMeasurement == 'F') {
          function c2f(value) {
            return value * 1.8 + 32;
          }
          var formatted_tick = d3.format(',.1f')(c2f(d));
        } else {
          var formatted_tick = d3.format(',.1f')(d);
        }
        return formatted_tick + ' ' + self.tempMeasurement;
      });

    d3.select(self.selectElement)
      .attr("style", "height:" + (self.height + self.margin.top + self.margin.bottom).toString() )

    d3.select(self.selectElement + ' svg')
      .attr("height", self.height + self.margin.top + self.margin.bottom)
      .datum(self.data)
      .transition()
      .call(self.nvchart);

    self.nvchart.update();

    if ((callbacks) && (callbacks.length > 0)) {
      for (var i=0; i<callbacks.length; i++) {
        callbacks[i](self)
      }
    }

    self.setLinesVisibility()

    // TODO: Set this up as an actual callback, rather than just doing it one second later
    setTimeout(self.callStoredCallbacks, 1000)

  }

  return self;

}