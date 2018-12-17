// width and height
var width = 1300;
var height = 1200;

// map projection
var projection = d3.geoMercator()
					   .center([ 13, 52 ])
					   .translate([ width/1.8, height/1.5 ])
					   .scale([ width/1.1 ]);

// path generator
var path = d3.geoPath()
				 		.projection(projection);

var svg = d3.select("#container")
						.append("svg")
						.attr("width", width)
						.attr("height", height);

// load data
var requests = [d3.json("countries.json"), d3.json("data.json")];

Promise.all(requests).then(function(res) {
    makeMap(res[0], res[1])
		})
						.catch(function(e){
    						throw(e);
    });

function makeMap(json, data){
	var tooltip = d3.tip()
	      		.attr("class", "d3-tip")
	      		.offset([10, 0])
	      		.html(function(d) {
								return d.properties.admin + "<br>" + data[d.properties.admin]["Quality of Life Index"];
							});
	    			svg.call(tooltip);

	// bind data and create one path per GeoJSON feature
	svg.selectAll("path")
		   			.data(json.features)
		   			.enter()
		   			.append("path")
		   			.attr("d", path)
		   			.attr("stroke", "rgba(10, 400, 156, 0.5)")
		   			.attr("fill", "rgba(8, 400, 156, 0.1)")
			 			.on('mouseover', tooltip.show)
	     			.on('mouseout', tooltip.hide)
			 			.on("click", function(d){
				 		makeBarchart(d.properties.admin, data)
			});
};

function makeBarchart(country, data){
						d3.select("#barchart").select("svg").remove();
						d3.select("#titlebars").select("svg").remove();
						keys = Object.keys(data[country])

	values = [];

	for (i in keys){
						values.push(data[country][keys[i]]);
			}

	// remove specific values
	keys.splice(0, 1)
	keys.splice(5, 1)
	values.splice(0, 1)
	values.splice(5, 1)

	for (i in keys){
						keys[i] = keys[i].replace(" Index", "");
						console.log(keys[i])
	}

	// width and height
	var margin = {top: 20, right: 20, bottom: 50, left: 40},
						width = 1000 - margin.left - margin.right;
						height = 900 - margin.top - margin.bottom;

	// create SVG
	var svg = d3.select("#barchart")
						.append("svg")
						.attr("id", "bars")
						.attr("width", width + margin.left + margin.right)
						.attr("height", height + margin.top + margin.bottom)
						.append("g")
    				.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// configure ranges
	var x = d3.scaleBand()
	          .range([0, width])
	          .padding(0.5);
	var y = d3.scaleLinear()
	          .range([height, 0]);

	// scale ranges
	x.domain(keys);
	y.domain([0, d3.max(values, function(d) {
		 				return d;
	 })]);

 var tooltip = d3.tip()
     				.attr("class", "d3-tip")
     				.offset([-8, 0])
     				.html(function(d) { return d; });
   					svg.call(tooltip);

	// create bars
	svg.selectAll(".bar")
						.data(values)
						.enter().append("rect")
						.attr("class", "bar")
						.attr("x", function(d, i) { return x(keys[i]); })
						.attr("width", x.bandwidth())
						.attr("y", function(d) { return y(d); })
						.attr("height", function(d) { return height - y(d) })
						.on('mouseover', tooltip.show)
						.on('mouseout', tooltip.hide);


	// add x axis
	svg.append("g")
						.attr("transform", "translate(0," + height + ")")
						.call(d3.axisBottom(x))
						.style("font-size", "8px");

	// add y axis
	svg.append("g")
						.call(d3.axisLeft(y));

	// text label for the y axis
  svg.append("text")
					  .attr("transform", "rotate(-90)")
					  .attr("y", 0 - margin.left)
					  .attr("x", -60)
					  .attr("dy", "1em")
					  .style("text-anchor", "middle")
						.style("font-size", "12px")
					  .text("Index value -->");

}
