function gaugePlot(div_id, host_removal_dollars, pesticide_dollars, max_amount) {

  var max_level = max_amount/1000000;
  var host_removal_cost = host_removal_dollars/1000000;
  var pesticide_cost = pesticide_dollars/1000000;
  var total_cost = host_removal_cost + pesticide_cost;

  if (total_cost >= max_level) {
    main_color = "#f55949";
    drawn_level = max_level;
    var overbudget = total_cost - max_level;
    warning_msg = "Budget exceeded by:<br>$" + round(overbudget, 2) + " million";
    warning_color = "#f55949";
  var data = [{
    values: [max_level,(0.98 * max_level - total_cost), (max_level / 50), (max_level / 3)],
    rotation: -135,
    direction: "clockwise",
    sort: false,
    textinfo: 'text',
    textposition: 'inside',
    marker: {
      colors: [main_color, '#676b73', '#f55949', 'rgba(255, 255, 255, 0)']
    },
    labels: ['Total <br> cost:<br>$' + round(total_cost, 3) + ' million', '', 'Budget: $' + max_level +
      ' million', ''
    ],
    hoverinfo: 'label',
    hole: 0.8,
    type: 'pie',
    showlegend: false
  }];
        } else {
    main_color = "#7ba83d";
    drawn_level = total_cost;
    warning_msg = 'spent on<br>management';
    warning_color = 'white';
  var data = [{
    values: [host_removal_cost, pesticide_cost,(0.98 * max_level - total_cost), (max_level / 50), (max_level / 3)],
    rotation: -135,
    direction: "clockwise",
    sort: false,
    textinfo: 'text',
    textposition: 'inside',
    marker: {
      colors: [main_color, main_color, '#676b73', '#f55949', 'rgba(255, 255, 255, 0)']
    },
    labels: ['Host removal <br> cost:<br>$' + round(host_removal_cost, 3) + ' million',
    'Pesticide <br> cost:<br>$' + round(pesticide_cost, 3) + ' million', '', 'Budget: $' + max_level +
      ' million', ''
    ],
    hoverinfo: 'label',
    hole: 0.8,
    type: 'pie',
    showlegend: false
  }];
        };

  var layout = {
    annotations: [{
        xref: 'paper',
        yref: 'paper',
        x: 0.5,
        xanchor: 'middle',
        y: 0.5,
        yanchor: 'middle',
        text: '$' + round(total_cost, 1),
        font: {
          family: 'Helvetica',
          size: 30,
          color: '#ffffff'
        },
        align: 'center',

        showarrow: false,
      },
      {
        xref: 'paper',
        yref: 'paper',
        x: 0.5,
        xanchor: 'center',
        y: 0.3,
        yanchor: 'middle',
        text: 'million',
        font: {
          family: 'Helvetica',
          size: 20,
          color: '#ffffff'
        },
        align: 'center',

        showarrow: false,
      },
      {
        xref: 'paper',
        yref: 'paper',
        x: 0.5,
        xanchor: 'center',
        y: 0.0,
        yanchor: 'middle',
        text: warning_msg,
        font: {
          family: 'Helvetica',
          size: 14,
          color: warning_color,
        },
        align: 'center',

        showarrow: false,
      }

    ],
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)', //'#16181b',
    margin: {
      l: 30,
      r: 30,
      b: 20,
      t: 0,
      pad: 0
    },



    title: {
      text: '',
      font: {
        color: 'white',
      },
    },


    xaxis: {
      zeroline: false,
      showticklabels: false,
      showgrid: false,
    },
    yaxis: {
      zeroline: false,
      showticklabels: false,
      showgrid: false,
    }
  };

  return Plotly.newPlot(div_id, data, layout, {
    displayModeBar: false,
    responsive: true
  });
}