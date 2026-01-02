function weeklyViews() {
  const canvasElement = document.querySelector("canvas#weekly-views");
  let ctx = canvasElement.getContext("2d");

  let get = canvasElement.dataset.get;

  fetch(get, { method: "GET" })
    .then((response) => {
      try {
        return response.json();
      } catch (error) {
        throw new Error(error);
      }
    })
    .catch((e) => {
      console.log(e);
    })
    .then((data) => {
      let obj = new Object({ ...data });
      let cols = [];
      let vals = [];

      for (const [key, value] of Object.entries(obj)) {
        cols.push(key);
        vals.push(value);
      }

      if (document.ctx.views) {
        let chart = document.ctx.views;
        chart.data.labels = cols;
        chart.data.datasets[0].data = vals;

        chart.update();
        return;
      }

      document.ctx.views = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [...cols],
          datasets: [
            {
              label: "Views",
              tension: 0.4,
              borderWidth: 0,
              borderRadius: 4,
              borderSkipped: false,
              backgroundColor: "#43A047",
              data: [...vals],
              barThickness: "flex",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false,
            },
          },
          interaction: {
            intersect: false,
            mode: "index",
          },
          scales: {
            y: {
              grid: {
                drawBorder: false,
                display: true,
                drawOnChartArea: true,
                drawTicks: false,
                borderDash: [5, 5],
                color: "#e5e5e5",
              },
              ticks: {
                suggestedMin: 0,
                suggestedMax: 500,
                beginAtZero: true,
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
                color: "#737373",
              },
            },
            x: {
              grid: {
                drawBorder: false,
                display: false,
                drawOnChartArea: false,
                drawTicks: false,
                borderDash: [5, 5],
              },
              ticks: {
                display: true,
                color: "#737373",
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
              },
            },
          },
        },
      });

      setInterval(weeklyViews, 10000);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  document.ctx = {};

  weeklyViews();
});
