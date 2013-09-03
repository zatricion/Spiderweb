;(function(exports) {
    var bubbles = {};

    var diameter = 960,
    format = d3.format(",d"),
    color = d3.scale.category20c();

    var bubble = d3.layout.pack()
	.sort(null)
	.size([diameter, diameter])
	.padding(1.5);

    var svg = d3.select("body").append("svg")
	.attr("width", diameter)
	.attr("height", diameter)
	.attr("class", "bubble");

    bubbles.showGraph = function (nodes) {
	var tree = {children: nodes};
	console.log(tree);

	var node = svg.selectAll(".node")
	    .data(bubble.nodes(tree).filter(function(d) { return !d.children; }))
	    .enter().append("g")
	    .attr("class", "node")
	    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
            .on("click", function(d) { window.open(d.name, '_blank'); });

	node.append("title")
	    .text(function(d) { return d.name + ": " + format(d.value); });

	node.append("circle")
	    .attr("r", function(d) { return d.r; })
	    .style("fill", function(d) { return color(d.name); });

	node.append("text")
	    .attr("dy", ".3em")
	    .style("text-anchor", "middle")
	    .text(function(d) { return getDomain(d.name).substring(0, d.r / 4); });

	d3.select(self.frameElement).style("height", diameter + "px");
    };

    var getDomain = function (url) {
      // Parse url
      var a = document.createElement('a');
      a.href = url;
      return a.hostname.replace('^www.', '');
    };

    exports.bubbles = bubbles;
}(this));
