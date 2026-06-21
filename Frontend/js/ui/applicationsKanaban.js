import { fillApplicationCardHTML } from "./applicationCard.js";
import { deleteApplicationDialog } from "./deleteApplicationDialog.js";
import { createApplicationForm } from "./createApplicationForm.js";

function createHTMLPhaseColumn(phase) {
  let phase_column_html = `<div class="kanban-column-flex-container">`;

  let phase_header = `<div class="kanban-column-header">`;

  let phase_name = `<p>${phase["name"]}</p></div>`;

  phase_column_html += phase_header + phase_name;

  let phase_column_inner = (phase["applications"] ?? [])
    .map((application) => fillApplicationCardHTML(application))
    .join("");

  phase_column_html = phase_column_html + phase_column_inner;

  let add_application_div = `<div class="kanban-card" data-phase-id="${phase["id"]}">
   <button class="application-button-create">Create new Application</button>
  </div>`;

  phase_column_html = phase_column_html + add_application_div + `</div>`;

  return phase_column_html;
}

export function renderApplicationKanban(
  applications,
  phases,
  statuses,
  createFormCallback,
  deleteApplicationCallback,
  getApplicationStatusesCallback,
) {
  const container = document.getElementById("applications-list");

  const phases_with_applications = new Map();

  phases.forEach((phase) => {
    phases_with_applications.set(phase["name"], {
      ...phase,
      applications: [],
    });
  });

  applications.forEach((application) => {
    let application_phase = application["status"]["phase"];
    let application_phase_name = application_phase["name"];

    phases_with_applications
      .get(application_phase_name)
      .applications.push(application);
  });

  container.innerHTML = `
    ${[...phases_with_applications.values()]
      .map((phase) => createHTMLPhaseColumn(phase))
      .join("")}
  `;

  document
    .querySelectorAll(".application-card-button-delete")
    .forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const application_id = e.target.dataset.appId;

        if (!document.querySelector(".delete-application-dialog")) {
          deleteApplicationDialog(application_id, deleteApplicationCallback);
        }
      });
    });

  document.querySelectorAll(".application-button-create").forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      const phase_id = e.currentTarget.parentNode.dataset.phaseId;
      const create_button = e.currentTarget;
      create_button.classList.add("hidden");

      // const statuses = await getApplicationStatusesCallback();

      const statuses_for_phase = statuses.filter((state) => {
        return state["phase"]["id"].toString() === phase_id;
      });

      const kanban_phase_column_container = document.querySelector(
        `[data-phase-id="${phase_id}"]`,
      );

      createApplicationForm(
        kanban_phase_column_container,
        statuses_for_phase,
        createFormCallback,
      );
    }),
  );
}
