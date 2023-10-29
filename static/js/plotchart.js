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
          labels: timeStamp,
          datasets: [
            {
                label: 'Balance Track',
                data: currBalance,
                type: 'line', // Use a line chart for this dataset
                backgroundColor: "#EEE8AA",
                borderColor: "#EEE8AA",
                borderWidth: 4,
                tension: 0.5,
                fill: false
            },
            {
                label: 'Balance Bars',
                data: balanceBars,
                type: 'bar', // Use a bar chart for this dataset
                backgroundColor: "rgba(87, 121, 234, 0.6)",
                borderColor: "rgba(87, 121, 234, 0.6)",
                stack: 'stack'
            },
            {
              label: 'Credit Transactions',
              data: Credits,
              type: 'bar', // Use a bar chart for this dataset
              backgroundColor: "rgba(18, 200, 150, 0.6)",
              borderColor: "rgba(18, 200, 150, 0.6)",
              stack: 'stack'
            },
            {
              label: 'Debit Transaction',
              data: Debits,
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
              min: timeStamp[0],  // Set the minimum timestamp from  data
              max: timeStamp[timeStamp.length - 1]
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