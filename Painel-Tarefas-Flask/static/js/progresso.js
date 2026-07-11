const colors = ["#f2c94c", "#2f80ed", "#27ae60"];

const loadCharts = async () => {
  const res = await fetch("/api/stats");
  const data = await res.json();

  new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Tarefas",
          data: data.values,
          backgroundColor: colors,
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 },
        },
      },
    },
  });

  new Chart(document.getElementById("pieChart"), {
    type: "pie",
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.values,
          backgroundColor: colors,
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
};

loadCharts();
