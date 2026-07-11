const grid = document.getElementById("tasksGrid");
const emptyState = document.getElementById("emptyState");
const filter = document.getElementById("statusFilter");

const statusClasses = {
  pendente: "status-pendente",
  andamento: "status-andamento",
  concluida: "status-concluida",
};

const escapeHtml = (value) =>
  String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

const loadStats = async () => {
  const res = await fetch("/api/stats");
  const stats = await res.json();
  document.getElementById("countPendente").textContent = stats.raw.pendente || 0;
  document.getElementById("countAndamento").textContent = stats.raw.andamento || 0;
  document.getElementById("countConcluida").textContent = stats.raw.concluida || 0;
};

const renderTask = (task) => {
  const badgeClass = statusClasses[task.status] || "status-pendente";
  const concluidaButton =
    task.status === "concluida"
      ? ""
      : `<button class="btn btn-sm btn-success" data-complete="${task.id}" title="Concluir">
           <i class="bi bi-check2"></i>
         </button>`;

  return `
    <article class="card task-card ${task.status === "andamento" ? "status-andamento" : ""} ${task.status === "concluida" ? "status-concluida" : ""}">
      <div class="card-body gap-3">
        <span class="badge rounded-pill status-badge ${badgeClass}">${escapeHtml(task.status_label)}</span>
        <div>
          <h2 class="h5 mb-2">${escapeHtml(task.titulo)}</h2>
          <p class="task-desc mb-0">${escapeHtml(task.descricao || "Sem descricao.")}</p>
        </div>
        <div class="task-actions">
          <a class="btn btn-sm btn-outline-primary" href="/editar/${task.id}" title="Editar">
            <i class="bi bi-pencil"></i>
          </a>
          ${concluidaButton}
          <button class="btn btn-sm btn-outline-danger" data-delete="${task.id}" title="Excluir">
            <i class="bi bi-trash"></i>
          </button>
        </div>
      </div>
    </article>
  `;
};

const loadTasks = async () => {
  const status = filter?.value || "todas";
  const res = await fetch(`/api/tasks?status=${encodeURIComponent(status)}`);
  const tasks = await res.json();
  grid.innerHTML = tasks.map(renderTask).join("");
  emptyState.classList.toggle("d-none", tasks.length > 0);
  await loadStats();
};

filter?.addEventListener("change", loadTasks);

grid?.addEventListener("click", async (event) => {
  const deleteButton = event.target.closest("[data-delete]");
  const completeButton = event.target.closest("[data-complete]");

  if (deleteButton) {
    await fetch(`/api/tasks/${deleteButton.dataset.delete}`, { method: "DELETE" });
    await loadTasks();
  }

  if (completeButton) {
    await fetch(`/api/tasks/${completeButton.dataset.complete}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: "concluida" }),
    });
    await loadTasks();
  }
});

loadTasks();
