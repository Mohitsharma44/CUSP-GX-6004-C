var limit = 60 * 1,
    duration = 750,
    now = new Date(Date.now() - duration);

var width = 750,
    height = 200;

var groups = {
    current: {
        value: 0,
        color: 'orange',
        data: d3.range(limit).map(function() {
            return 0;
        })
    },
    /*    target: {
          value: 0,
          color: 'green',
          data: d3.range(limit).map(function() {
          return 0;
          })
          },
          output: {
          value: 0,
          color: 'grey',
          data: d3.range(limit).map(function() {
          return 0;
          })
          }
    */
}

var ws = new WebSocket("ws://localhost:8888/realtime");
ws.onopen = function(){
    console.log("Connection Established");
};

ws.onmessage = function(ev){
    console.log("Got a message!");
    var json_data = JSON.parse(ev.data);
    console.log(json_data.cpu_load);
    for (var name in groups) {
        var group = groups[name];
        group.value = parseInt(json_data.cpu_load);
    } setTimeout(function(){
        for (var name in groups){
            var group = groups[name];
            group.value = 0;
        }
    }, 10000);
};

ws.onclose = function(ev){
    console.log("connection was closed");
};

ws.onerror = function(ev){
    console.log("Error creating socket setup");
};

var x = d3.time.scale()
    .domain([now - (limit - 2), now - duration])
    .range([0, width]);

var y = d3.scale.linear()
    .domain([0, 100])
    .range([height, 0]);

var line = d3.svg.line()
    .interpolate('basis')
    .x(function(d, i) {
        return x(now - (limit - 1 - i) * duration);
    })
    .y(function(d) {
        return y(d);
    });


var svg = d3.select('.graph').append('svg')
    .attr('class', 'chart')
    .attr('width', width)
    .attr('height', height + 50);

var axis = svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', 'translate(0,' + height + ')')
    .call(x.axis = d3.svg.axis().scale(x).orient('bottom'));

svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width)
    .attr("y", height - 6)
    .text("Time");

svg.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("y", 6)
    .attr("dy", ".75em")
    .attr("transform", "rotate(-90)")
    .text("Percent");

var paths = svg.append('g');

for (var name in groups) {
    var group = groups[name];
    group.path = paths.append('path')
        .data([group.data])
        .attr('class', name + ' group')
        .style('stroke', group.color);
}

function createGraph() {
    now = new Date();

    // Add new values
    for (var name in groups) {
        var group = groups[name];
        //group.data.push(group.value) // Real values arrive at irregular intervals
        //group.data.push(20 + Math.random() * 100);
        group.data.push(group.value);
        group.path.attr('d', line);
    }

    // Shift domain
    x.domain([now - (limit - 2) * duration, now - duration]);

    // Slide x-axis left
    axis.transition()
        .duration(duration)
        .ease('linear')
        .call(x.axis);

    // Slide paths left
    paths.attr('transform', null)
        .transition()
        .duration(duration)
        .ease('linear')
        .attr('transform', 'translate(' + x(now - (limit - 1) * duration) + ')')
        .each('end', createGraph);

    // Remove oldest data point from each group
    for (var name in groups) {
        var group = groups[name];
        group.data.shift();
    }
}

createGraph();
