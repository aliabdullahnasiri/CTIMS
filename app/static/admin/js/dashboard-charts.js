function fetchChartData(canvas) {
  let get = canvas.dataset.get;

  return fetch(get, { method: "GET" })
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
      return [cols, vals];
    });
}

function weeklyUsers() {
  const canvasElement = document.querySelector("canvas#weekly-users");

  let ctx = canvasElement?.getContext("2d");

  if (!ctx) {
    return;
  }

  fetchChartData(canvasElement).then((data) => {
    const [cols, vals] = data;

    if (document.ctx.users) {
      let chart = document.ctx.users;
      chart.data.labels = cols;
      chart.data.datasets[0].data = vals;

      chart.update();
      return;
    }

    document.ctx.users = new Chart(ctx, {
      type: "bar",
      data: {
        labels: [...cols],
        datasets: [
          {
            label: "Users",
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

    setInterval(weeklyUsers, 10000);
  });
}
function weeklyViews() {
  const canvasElement = document.querySelector("canvas#weekly-views");

  let ctx = canvasElement.getContext("2d");

  fetchChartData(canvasElement).then((data) => {
    const [cols, vals] = data;

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

function yearlyStudents() {
  const canvasElement = document.querySelector("canvas#yearly-students");

  let ctx = canvasElement?.getContext("2d");

  if (!ctx) return;

  fetchChartData(canvasElement).then((data) => {
    const [cols, vals] = data;

    if (document.ctx.students) {
      let chart = document.ctx.students;
      chart.data.labels = cols;
      chart.data.datasets[0].data = vals;

      chart.update();
      return;
    }

    document.ctx.students = new Chart(ctx, {
      type: "line",
      data: {
        labels: [...cols],
        datasets: [
          {
            label: "Students",
            tension: 0,
            borderWidth: 2,
            pointRadius: 3,
            pointBackgroundColor: "#43A047",
            pointBorderColor: "transparent",
            borderColor: "#43A047",
            backgroundColor: "transparent",
            fill: true,
            data: [...vals],
            maxBarThickness: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                const value = context.parsed.y;
                return value.toLocaleString();
              },
            },
          },
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
              callback: function (value) {
                return value.toLocaleString();
              },
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

    setInterval(yearlyStudents, 10000);
  });
}

function yearlyClasses() {
  const canvasElement = document.querySelector("canvas#yearly-classes");

  let ctx = canvasElement.getContext("2d");

  if (!ctx) return;
  fetchChartData(canvasElement).then((data) => {
    const [cols, vals] = data;

    if (document.ctx.classes) {
      let chart = document.ctx.classes;
      chart.data.labels = cols;
      chart.data.datasets[0].data = vals;

      chart.update();
      return;
    }

    document.ctx.classes = new Chart(ctx, {
      type: "line",
      data: {
        labels: [...cols],
        datasets: [
          {
            label: "Class",
            tension: 0,
            borderWidth: 2,
            pointRadius: 3,
            pointBackgroundColor: "#43A047",
            pointBorderColor: "transparent",
            borderColor: "#43A047",
            backgroundColor: "transparent",
            fill: true,
            data: [...vals],
            maxBarThickness: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                const value = context.parsed.y;
                return value.toLocaleString();
              },
            },
          },
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
              callback: function (value) {
                return value.toLocaleString();
              },
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

    setInterval(yearlyClasses, 10000);
  });
}
document.addEventListener("DOMContentLoaded", () => {
  document.ctx = {};

  weeklyViews();
  weeklyUsers();
  yearlyStudents();
  yearlyClasses();
});
