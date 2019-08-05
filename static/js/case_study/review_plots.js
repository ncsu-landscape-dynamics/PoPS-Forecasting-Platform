//Polynomial plot for temp and precip reclass
function reclass_plot(min,max,reclass=0,color) {
     var trace = {
    x: [min,max],
    y: [reclass,reclass],
    mode: 'lines+markers',
    type: 'scatter',
    marker: {
            size: 8,
            color: ['#16181b',color],
            line: {
                width: 1,
                color:color,
            }
        },
    line: {
        color:color,
        width: 3,
    },
    };
    return trace;
}

function polynomial_plot(div_id,x_range,x_label,a0=0,a1=0,x1=0,a2=0,x2=0,a3=0,x3=0) {
    var x_values = [];
    var y_values = [];
    for (var i = x_range[0]; i <= x_range[1]; i++) {
        x_values.push(i);
        reclass=a0+a1*(i+x1)+a2*(i+x2)**2+a3*(i+x3)**3;
        if (reclass < 0){
            y_values.push(0);
        } else if (reclass > 1) {
            y_values.push(1);
        } else {
            y_values.push(reclass);
        };
    }
    var data = [{
    x: x_values,
    y: y_values,
    mode: 'lines',
    type: 'scatter',
    line: {
        color:'cyan',
        width: 3,
    },
    }];
    var layout = dark_layout(x_label=x_label,x_range=x_range)
    return Plotly.newPlot(div_id, data, layout, {responsive: true});
}

function dark_layout(x_label='',x_range=[0,100]) {
    var axis_template={
        showgrid:true,
        zeroline:true,
        gridcolor: '#16181b',
        gridwidth: 1,
        zerolinecolor: '#969696',
        zerolinewidth: 1,
        //linecolor: 'black',
        //mirror: true,
        //linewidth: 1,
        nticks:20,
        titlefont: {
        family: 'Arial, sans-serif',
        size: 14,
        color: '#909294'
        },
        showticklabels: true,
        tickangle: 'auto',
        tickfont: {
        family: 'Arial, sans-serif',
        size: 12,
        color: '#909294'
        },
    };

    var xaxis={title: x_label, range: x_range};
    var yaxis={title: 'Reclass', range: [-0.02, 1.02]};
    var layout={
        showlegend:false,
        paper_bgcolor:'rgba(0,0,0,0)',
        plot_bgcolor:'rgba(0,0,0,0)',//'#16181b',
        margin: {
            l: 50,
            r: 20,
            b: 40,
            t: 20,
            pad: 4
        },
        xaxis: $.extend({}, axis_template, xaxis),
        yaxis: $.extend({}, axis_template, yaxis),
    };
    return layout;
}