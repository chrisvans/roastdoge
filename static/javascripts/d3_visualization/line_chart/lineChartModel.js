// Create an object to handle data storage, chart creation and update
function lineChartVisualization(options) {

  var visualization = {}

  // Create object with parameters required for chart creation
  // You can set these attributes manually, and then call visualization.updateChart();
  visualization.__init__ = function(options) {

    visualization.selectElement = options.selectElement;
    visualization.data = options.data;
    visualization.margin = options.margin;
    visualization.width = options.width;
    visualization.height = options.height;
    visualization.xAxisLabel = options.xAxisLabel;
    visualization.yAxisLabel = options.yAxisLabel;
    visualization.nvchart = '';
    
  }

  // Run the init method
  visualization.__init__(options);

  visualization.createChart = function () {

    visualization.xScale = d3.scale.linear()
      .domain([0, d3.max(visualization.data, function(d) { return d.values; })])
      .range([0, d3.max(visualization.data, function(d) { return d.values; })]);

    nv.addGraph(function() {
      visualization.nvchart = nv.models.lineChart()
        .color(d3.scale.category10().range());

      visualization.nvchart.x(function(d,i) { 
        var time = new Date(d.x)
        return time; 
      })

      visualization.nvchart.xAxis // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
        .axisLabel(visualization.xAxisLabel || 'Time in Minutes')
        .tickFormat(d3.format(',.0f'))
      //.tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); })
        .scale(visualization.xScale);

      visualization.nvchart.yAxis
        .axisLabel(visualization.yAxisLabel || 'Temperature')
        .tickFormat( function(d) {
            formatted_tick = d3.format(',.1f')(d);
            return formatted_tick + ' F';
        });

      d3.select(visualization.selectElement)
        .append('svg')
          .attr("height", visualization.height + visualization.margin.top + visualization.margin.bottom)
          .datum(visualization.data)
          .call(visualization.nvchart);

      nv.utils.windowResize( function() {
        d3.select(visualization.selectElement + ' svg')
        .transition().duration(500)
          .call(visualization.nvchart);
        visualization.nvchart.update();
      });

      return visualization.nvchart;

    });

  }

  visualization.updateChart = function() {

    visualization.xScale = d3.scale.linear()
      .domain([0, d3.max(visualization.data, function(d) { return d.values; })])
      .range([0, d3.max(visualization.data, function(d) { return d.values; })]);

    visualization.nvchart.x(function(d,i) { 
      var time = new Date(d.x)
      return time; 
    })

    visualization.nvchart.xAxis // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
      .axisLabel(visualization.xAxisLabel || 'Time in Minutes')
      .tickFormat(d3.format(',.0f'))
    //.tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); })
      .scale(visualization.xScale);

    visualization.nvchart.yAxis
      .axisLabel(visualization.xAxisLabel || 'Temperature')
      .tickFormat( function(d) {
        formatted_tick = d3.format(',.1f')(d);
        return formatted_tick + ' F';
      });

    d3.select(visualization.selectElement + ' svg')
      .attr("height", visualization.height + visualization.margin.top + visualization.margin.bottom)
      .datum(visualization.data)
      .transition().duration(500)
      .call(visualization.nvchart);

    visualization.nvchart.update();

  }

  return visualization;

}