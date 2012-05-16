d3.csv("data/yelp.csv", function handleCSV(csv) {
    var data = csv.filter(function(el){return el});
    var restaurants = data.map(function(el){
        return el.restaurant
        });
    var words = data.map(function(el){
        return el.word
        });
    var times = data.map(function(el){
        return parseInt(el.times)
        });
    // console.log(restaurants);
    // console.log(times);
    // console.log(d3.max(times))

  var w = 800,
      h = 620,
      p = 40,
      x = d3.scale.linear()
                  .domain([0, d3.max(times) * 1.01])
                  .range([0, w]),
      //domain has to be states, but then how do you deal with range?
      y = d3.scale.ordinal()
                  .domain(restaurants)
                  .rangePoints([0,610]);
    // console.log(d3.max(times))
  var vis = d3.select("div #yelpBarChart")
              .append("svg")
              .attr("width", w + p * 2)
              .attr("height", h + p * 2)
              .append("g")
              .attr("transform", "translate(" + p*5 + "," + p + ")");

  // axes
  var xAxis = d3.svg
                .axis()
                .scale(x)
                .ticks(5)
                .tickPadding(5);

  var yAxis = d3.svg
                .axis()
                .scale(y)
                .orient("left"); 
  // x axis
  vis.append("g")
    .attr("class", "x")
    .attr("transform", "translate(0," + h + ")")
    .call(xAxis);
  // y axis
  vis.append("g")
    .attr("class", "y")
    .call(yAxis);
    
  d3.select("div#yelpBarChart")
    .append("text")
    .attr("id", "tip")
    .attr("text-anchor", "start")
    .attr("font-size", "20")
    .text("Word:Frequency");   
    
  vis.selectAll("rect")
     .data(data)
     .enter()
     .append("rect")
     .attr("x", 0)
     .attr("y", function(d){
                    return y(d.restaurant)})
     .attr("width", function(d) { return x(d.times); })
     .attr("height", function(d) { return 10; })
     .attr("fill", "steelblue")
     .on("mouseover", function(d, i){
                                    d3.select("#tip").remove(); 
                                    d3.select(this).attr("fill", "steelblue")
     
                                    d3.select("div#yelpBarChart")
                                        .append("text")
                                        .attr("id", "tip")
                                        .attr("x", x(d.times))
                                        .attr("y",y(d.restaurant)+7)
                                        .attr("text-anchor", "start")
                                        .attr("font-size", "20")
                                        .text(d.word+":"+d.times)
                                        .attr("fill", "red"); 
                                    d3.select(this).attr("fill", "blue")})
     .on("mouseout", function(d, i){d3.select(this).attr("fill", "steelblue")
                                    d3.select("#tip").remove();
                                    d3.select("div#yelpBarChart")
                                        .append("text")
                                        .attr("id", "tip")
                                        .attr("text-anchor", "start")
                                        .attr("font-size", "20")
                                        .text("Word:Frequency")});
});



