const applyTheme = (theme) => {
  document.documentElement.setAttribute("data-bs-theme", theme);
  const icon = document.querySelector("#themeToggle i");
  if (icon) {
    icon.className = theme === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
  }
};

const savedTheme = localStorage.getItem("task-theme") || "light";
applyTheme(savedTheme);

document.getElementById("themeToggle")?.addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-bs-theme") || "light";
  const next = current === "dark" ? "light" : "dark";
  localStorage.setItem("task-theme", next);
  applyTheme(next);
});
