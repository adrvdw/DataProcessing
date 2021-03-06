// Ad Ruigrok van der Werve
// 11323760

var fileName = "data.json";
var txtFile = new XMLHttpRequest();
txtFile.onreadystatechange = function() {

  if (txtFile.readyState === 4 && txtFile.status == 200) {
    data = JSON.parse(txtFile.responseText);

    var range = [];

    keys = Object.keys(data);
    // obtain max and min values of date, represented as YYYYMMDD
    var keys_length = keys.length;
    var domain_max_ = Math.max.apply(null, keys);
    var domain_max_ = domain_max_.toString();
    var domain_min_ = Math.min.apply(null, keys);
    var domain_min_ = domain_min_.toString();

    range.push(domain_min_, domain_max_);

    values = Object.values(data);

    // strip YYYYMMDD to another date notation
    var dateString = domain_max_;
    var year = dateString.substring(0,4);
    var month = dateString.substring(4,6);
    var day = dateString.substring(6,8);

    var date_max = new Date(year, month-1, day);

    var dateString1 = domain_min_;
    var year1 = dateString1.substring(0,4);
    var month1 = dateString1.substring(4,6);
    var day1 = dateString1.substring(6,8);

    var date_min = new Date(year1, month1-1, day1);

    var list = [];

    var domain = [];
    // get value of TX that belongs to key(YYYYMMDD)
    keys.forEach(function(key)  {
      value = (data[key]["TX"]);
      list.push(value);
    });

    // obtain max and min values of TX

    range_max_ = Math.max.apply(null, list);
    range_min_ = Math.min.apply(null, list);

    domain.push(range_min_, range_max_);

    // scale both x and y directions of plot
    transformY = createTransform(domain, [700, 0]);
    transformX = createTransform(range, [0, 500]);
    list.forEach(function(element){
      transformY(element);
    })

    let lines = document.querySelector("canvas").getContext("2d");

    lines.moveTo(100, transformY(list[0]));

    // draw keys_length(18) connected points
    for (i = 1; i < keys_length; i++){
      lines.lineTo(100 + i * 45, transformY(list[i]))
      lines.moveTo(100 + i * 45, transformY(list[i]))
    }

    lines.stroke()
  }
}

txtFile.open("GET", fileName);
txtFile.send();

function createTransform(domain, range){
    var domain_min = domain[0];
    var domain_max = domain[1];
    var range_min = range[0];
    var range_max = range[1];

    // formulas to calculate the alpha and the beta
   	var alpha = (range_max - range_min) / (domain_max - domain_min)
    var beta = range_max - alpha * domain_max

    // returns the function for the linear transformation (y= a * x + b)
    return function(x){
      return alpha * x + beta;
    }
}

// draw x, y plane
let cy = document.querySelector("canvas").getContext("2d");
cy.beginPath();
for (let y = 100; y < 910; y += 100) {
   cy.lineTo(y, 800);
 }
 cy.stroke();

 let cx = document.querySelector("canvas").getContext("2d");
 cx.beginPath();
 for (let x = 0; x < 810; x += 100) {
   cx.lineTo(100, x);
  }
 cx.stroke();

// loop to place values of x,y values at the axes

      var x_coordinaat = 60;
      var y_coordinaat = 14;
      var y = 189
      var canvas = document.getElementById("canvas");
      var ctx = canvas.getContext("2d");
      for (var i = 0; i < 8; i++){
          ctx.font = "15px Arial";
          ctx.strokeText(y,x_coordinaat,y_coordinaat);
          y_coordinaat += 101
          y -= 20
        };

      var x_coordinaat = 100;
      var y_coordinaat = 830;
      var x = 1
      var canvas = document.getElementById("canvas");
      var ctx = canvas.getContext("2d");
      // months =
      for (var i = 0; i < 18; i++){
          ctx.font = "15px Arial";
          ctx.strokeText(x,x_coordinaat,y_coordinaat);
          x_coordinaat += 45
          x += 1
        };


        ctx.font = '20px arial';
        ctx.fillText('Datum (november)', 435, 865);

        ctx.font = '20px arial';
        ctx.fillText('Max. Temp. /0.1 graad', 865, 475);

        ctx.font = '40px arial';
        ctx.fillText('Ad Ruigrok van der Werve', 100, 950);
        ctx.fillText('Javascript week3', 100, 1050);
