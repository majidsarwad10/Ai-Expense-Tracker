document.addEventListener("DOMContentLoaded", () => {
  const data = window.expenseDashboard;
  if (!data || typeof Chart === "undefined") return;

  const categoryCanvas = document.getElementById("categoryChart");
  if (categoryCanvas) {
    new Chart(categoryCanvas, {
      type: "doughnut",
      data: {
        labels: data.categoryLabels,
        datasets: [{ data: data.categoryValues }]
      },
      options: { responsive: true, plugins: { legend: { position: "bottom" } } }
    });
  }

  const monthCanvas = document.getElementById("monthChart");
  if (monthCanvas) {
    new Chart(monthCanvas, {
      type: "bar",
      data: {
        labels: data.monthLabels,
        datasets: [{ label: "Expenses (₹)", data: data.monthValues }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
  }
});
