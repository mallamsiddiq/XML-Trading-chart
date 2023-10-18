document.addEventListener('DOMContentLoaded', function () {
  Chart.helpers.each(Chart.instances, function (instance) {
    instance.data.options.moment = {
      format: 'MMM YYYY', // Your desired date format
    };
  });

  var ctx = document.getElementById('mixedChart').getContext('2d');
  var mixedChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: labels,
          datasets: [
            {
                label: 'Balance Track',
                data: profits_losses,
                type: 'line', // Use a line chart for this dataset
                backgroundColor: "rgba(87, 121, 234, 0.6)",
                borderColor: "rgba(87, 121, 234, 0.6)",
                
                borderWidth: 3,
                tension: 0.5,
                fill: false
            },
            {
                label: 'Current Balance',
                data: PrevBalance,
                type: 'bar', // Use a bar chart for this dataset
                
                

                backgroundColor: "rgba(18, 200, 150, 0.6)",
                borderColor: "rgba(18, 200, 150, 0.6)",
                stack: 'stack'
            },
            {
              label: 'Profit/Loss',
              data: barData,
              type: 'bar', // Use a bar chart for this dataset
              backgroundColor: "rgba(234, 87, 102, 0.6)",
              borderColor: "rgba(234, 87, 102, 0.6)",
              stack: 'stack'
          },
            
        ],
      },
      options: {
        scales: {
          xAxis: { // Use 'xAxis' instead of 'x'
            type: 'time',
            position: 'bottom',
            beginAtZero: true,
            time: {
              unit: 'minute',
              displayFormats: {
                minute: 'HH:mm',
              },
              min: labels[0],  // Set the minimum timestamp from your data
              max: labels[labels.length - 1]
            },
            grid: {
              offset: true
            }
          },
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value, index, values) {
                return '$' + value;
              }
            }
          }
        }
      }
      
  });
});