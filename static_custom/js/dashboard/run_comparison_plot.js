function run_comparison_plot(run_comparison_div,run_name,infected, area, money) {

  var max_a=1;
  var max_b=1;
  
  if (infected == 'None') {
    infected=0;
  };
  if (area == 'None') {
    area=0;
  }
  if (money == 'None') {
    money=0;
  }
  var trace1 = {
    x: ['# Occurences'],
    y: [infected],
    type: 'bar',
    text: ['Additional info'],
    hoverinfo: ['x+y+text'],
    marker: {
      color: ['#2598b8'],
      opacity: 1,
    }
  }; 
  var trace2 = {
    x: ['Occurence area'],
    y: [area*acre_to_meter_ratio],
    type: 'bar',
    text: ['Additional info'],
    hoverinfo: ['x+y+text'],
    yaxis:'y2',
    marker: {
      color: ['#5fc2c2'],
      opacity: 1,
    }
  }; 
  var trace3 = {
    x: ['Money spent'],
    y: [money],
    type: 'bar',
    text: ['Additional info'],
    hoverinfo: ['x+y+text'],
    yaxis:'y3',
    marker: {
      color: ['#7ba83d'],
      opacity: 1,
    }
  }; 
  
  var data = [trace1,trace2,trace3];
      var axis_template={
          showgrid:false,
          zeroline:false,
          showticklabels: false,
      };
  
  var xaxis ={
      tickfont: {
        size: 9,
        color: 'white',
        },
        title: run_name,
        titlefont: {
        size: 12,
        color: 'white',
        },
  };
  var yaxis = {
          range: [0,max_number],
    };
  var yaxis2= {
    ticksuffix:' acres',
    overlaying: 'y',
    range: [0,max_area*acre_to_meter_ratio],
    };
  var yaxis3= {
    tickprefix:'$',
    overlaying: 'y',
    range: [0,max_cost],
    };
  var yaxis4= {
    overlaying: 'y',
    range: [0,max_a],
    };
  var yaxis5= {
    overlaying: 'y',
    range: [0,max_b],
    };
   
  var layout = {
      xaxis: $.extend({}, axis_template, xaxis),
      yaxis: $.extend({}, axis_template, yaxis),
      yaxis2: $.extend({}, axis_template, yaxis2),
      yaxis3: $.extend({}, axis_template, yaxis3),
          showlegend:false,
          paper_bgcolor:'rgba(0,0,0,0)',
          plot_bgcolor:'rgba(0,0,0,0)',//'#16181b',
          margin: {
              l: 10,
              r: 10,
              b: 30,
              t: 5,
              pad: 0
          },
          bargap: 0.1,
          barmode: 'group',
      };
  return Plotly.newPlot(run_comparison_div, data, layout, {displayModeBar: false, responsive: true});
  };