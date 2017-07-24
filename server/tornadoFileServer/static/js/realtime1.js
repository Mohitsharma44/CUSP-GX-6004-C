var cpu_load = document.getElementById("cpu_load");
var cpu_cur_freq = document.getElementById("cpu_cur_freq");
var mem_available = document.getElementById("mem_available");
var mem_percent = document.getElementById("mem_percent");
var net_en0 = document.getElementById("net_en0");
var storage_root = document.getElementById("storage_root");
var net_tx_packets = document.getElementById("net_tx_packets");
var net_rx_packets = document.getElementById("net_rx_packets");

var limit = 60 * 1,
    duration = 750,
    now = new Date(Date.now() - duration);

var width = document.getElementById('graphdata1').clientWidth,
    height = 250;


var groups = {
    cpu_util: {
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
    console.log(json_data);
    cpu_load.innerHTML = "CPU Load: " + parseInt(json_data.cpu_load) + " %";
    cpu_cur_freq.innerHTML = "CPU Frequency: " + parseInt(json_data.cpu_cur_freq) + " GHz";
    mem_available.innerHTML = "RAM Available: " + parseFloat(json_data.mem_available)/1024/1024 + " MB";
    mem_percent.innerHTML = "RAM Percent: " + parseFloat(json_data.mem_percent) + " %";
    net_en0.innerHTML = "IP Address: " + json_data.net_en0;
    net_tx_packets.innerHTML = "Transmitted Packets: " + parseFloat(json_data.net_tx_packets);
    net_rx_packets.innerHTML = "Received Packets: " + parseFloat(json_data.net_rx_packets);
    storage_root.innerHTML = "Total Storage Used: " + parseFloat(json_data.storage_root) + " %";
    //for (var name in groups) {
    //    var group = groups[name];
    groups['cpu_util'].value = parseInt(json_data.cpu_load);
    //}
    setTimeout(function(){
        //for (var name in groups){
        //    var group = groups[name];
        groups['cpu_util'].value = 0;
        //}
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

var svg = d3.select(".graph").append('svg')
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
