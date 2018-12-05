/**
 * Ad Ruigrok van der Werve
 * 11323760
 * Javascript file
 */


var womenInScience = "http://stats.oecd.org/SDMX-JSON/data/MSTI_PUB/TH_WRXRS.FRA+DEU+KOR+NLD+PRT+GBR/all?startTime=2007&endTime=2015"
var consConf = "http://stats.oecd.org/SDMX-JSON/data/HH_DASH/FRA+DEU+KOR+NLD+PRT+GBR.COCONF.A/all?startTime=2007&endTime=2015"

window.onload = function() {

  var requests = [d3.json(womenInScience), d3.json(consConf)];
  Promise.all(requests).then(function(response) {

    var data_women = transformResponse(response[0])
    var data_customer = transformResponse(response[1])

    const margin = {
      top: 40,
      right: 250,
      bottom: 30,
      left: 250
    };

    const width = 1300 - margin.left - margin.right;
    const height = 550 - margin.top - margin.bottom;

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // solution to the lack that both lists are not equal in length
    var combined_data = [];
    counter = 0;

    for (i in data_customer){
        if (data_customer[i].time == data_women[i - counter].time) {
            combined_data.push([data_women[i - counter].datapoint, data_customer[i].datapoint, data_customer[i].time])
        }
        else {
            counter += 1;
        }

    };

    var xScale = d3.scaleLinear()
        .domain([14, d3.max(data_women, function(d){
            return d.datapoint
        })])
        .range([0, width]);

    var yScale = d3.scaleLinear()
        .domain([96, d3.max(data_customer, function(d){
            return d.datapoint
        })])
        .range([height, 0]);

    var xAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale));

    var yAxis = svg.append("g")
        .call(d3.axisLeft(yScale));

    var color = d3.scaleOrdinal(d3.schemeCategory10)

    // draw circles and change radius
    svg.selectAll("circle")
        .data(combined_data)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
            return xScale(d[0]);
        })
        .attr("cy", function(d) {
            return yScale(d[1]);
        })
        .attr("r", function(d) {
            return Math.sqrt(400 - yScale(d[1]));
        })
        .transition()
            .delay(function(d, i){
                return(i * 25)
            })
            .style("fill", function(d){
                return color(d[2])
        });

    svg.selectAll("text")
        .data(combined_data)
        .enter()
        .append("text")
        .text(function(d) {
            return d[2];
        })
        .attr("x", function(d) {
            return xScale(d[0]);
        })
        .attr("y", function(d) {
            return yScale(d[1]);
        })
        .attr("font-family", "sans-serif")
            .attr("font-size", "11px")
            .attr("fill", "black");

    // a list of years to use as data in the legend
    counters = 0
    years_list = []
    for (i in data_customer){
        if (data_customer[i].time == data_women[i - counters].time) {
            years_list.push([data_customer[i].time])
        }
        else {
            counters += 1;
        }
    };

    var legend = svg.selectAll(".legend")
        .data([2007,2008,2009,2010,2011,2012,2013,2014,2015])
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform",
            function(d, i) {
                return "translate(0," + i * 20 + ")";
        });


    legend.append("rect")
        .attr("x", width + 130)
        .attr("y", 200)
        .attr("width", 18)
        .attr("height", 18)
        .attr("fill", "whitesmoke")
        .transition()
            .duration(1800)
            .attr("fill", function(d){
                return color(d)
        });

    legend.append("text")
        .data(years_list)
        .attr("class", "legend-text")
        .attr("x", width + 200)
        .attr("y", 200 + 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .attr("fill", "whitesmoke")
        .text(function(d) {
            return (d);
        })
        .transition()
          .duration(1800)
          .attr("fill", "black");

  }).catch(function(e){
      throw(e);
  });

  function transformResponse(data){

    // access data property of the response
    let dataHere = data.dataSets[0].series;

    // access variables in the response and save length for later
    let series = data.structure.dimensions.series;
    let seriesLength = series.length;

    // set up array of variables and array of lengths
    let varArray = [];
    let lenArray = [];

    series.forEach(function(serie){
        varArray.push(serie);
        lenArray.push(serie.values.length);
    });

    // get the time periods in the dataset
    let observation = data.structure.dimensions.observation[0];

    // add time periods to the variables, but since it's not included in the
    // 0:0:0 format it's not included in the array of lengths
    varArray.push(observation);

    // create array with all possible combinations of the 0:0:0 format
    let strings = Object.keys(dataHere);

    // set up output array, an array of objects, each containing a single datapoint
    // and the descriptors for that datapoint
    let dataArray = [];

    // for each string that we created
    strings.forEach(function(string){
        // for each observation and its index
        observation.values.forEach(function(obs, index){
            let data = dataHere[string].observations[index];
            if (data != undefined){

                // set up temporary object
                let tempObj = {};

                let tempString = string.split(":").slice(0, -1);
                tempString.forEach(function(s, indexi){
                    tempObj[varArray[indexi].name] = varArray[indexi].values[s].name;
                });

                // every datapoint has a time and ofcourse a datapoint
                tempObj["time"] = obs.name;
                tempObj["datapoint"] = data[0];
                dataArray.push(tempObj);
            }
        });
    });
    // return the finished product!
    return dataArray;
}

};
