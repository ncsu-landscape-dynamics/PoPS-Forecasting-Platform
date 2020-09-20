function gaugePlot(div_id, host_removal_dollars, pesticide_dollars, max_amount) {

  var total_cost_dollars = host_removal_dollars + pesticide_dollars;

  function divideCost(amount,divide_by) {
    new_cost = round(amount/divide_by,1);
    return new_cost
  }

    var divide_by = 1;
    var display_unit = '';

  if (total_cost_dollars >= 1e9) {
    divide_by = 1e9;
    display_unit = 'billion';
  }
  else if (total_cost_dollars >= 1e6) {
    divide_by = 1e6;
    display_unit = 'million';
  }
  else if (total_cost_dollars >= 1e3) {
    divide_by = 1000;
    display_unit = 'thousand';
  }

  var max_level = divideCost(max_amount,divide_by);
  var host_removal_cost = divideCost(host_removal_dollars,divide_by);
  var pesticide_cost = divideCost(pesticide_dollars,divide_by);
  var total_cost = divideCost(total_cost_dollars,divide_by);


  if (total_cost_dollars >= max_amount) {
    main_color = "#f55949";
    drawn_level = max_amount;
    var overbudget = total_cost_dollars - max_amount;
    var displayed_overbudget = overbudget.toLocaleString("en");
    warning_msg = "Budget exceeded by:<br>$" + displayed_overbudget + " " ;
    warning_color = "#f55949";
  var data = [{
    values: [max_amount,0, (max_amount / 50), (max_amount / 3)],
    rotation: -135,
    direction: "clockwise",
    sort: false,
    textinfo: 'text',
    textposition: 'inside',
    marker: {
      colors: [main_color, '#676b73', '#f55949', 'rgba(255, 255, 255, 0)']
    },
    labels: ['Total <br> cost:<br>$' + total_cost + ' ' + display_unit, '', 'Budget: $' + max_level +
      ' '+ display_unit, ''
    ],
    hoverinfo: 'label',
    hole: 0.8,
    type: 'pie',
    showlegend: false
  }];
        } else {
    main_color = "#7ba83d";
    drawn_level = total_cost_dollars;
    warning_msg = 'spent on<br>management';
    warning_color = 'white';
  var data = [{
    values: [host_removal_dollars, pesticide_dollars,(0.98 * max_amount - total_cost_dollars), (max_amount / 50), (max_amount / 3)],
    rotation: -135,
    direction: "clockwise",
    sort: false,
    textinfo: 'text',
    textposition: 'inside',
    marker: {
      colors: [main_color, "a3e04f", '#676b73', '#f55949', 'rgba(255, 255, 255, 0)']
    },
    labels: ['Host removal <br> cost:<br>$' + host_removal_cost + ' ' + display_unit,
    'Pesticide <br> cost:<br>$' + pesticide_cost + ' ' + display_unit, '', 'Budget: $' + max_level +
      ' ' + display_unit, ''
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
        y: 0.55,
        yanchor: 'middle',
        text: '$' + total_cost,
        font: {
          family: 'Helvetica',
          size: 28,
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
        y: 0.35,
        yanchor: 'middle',
        text: display_unit,
        font: {
          family: 'Helvetica',
          size: 18,
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
          size: 12,
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
};
