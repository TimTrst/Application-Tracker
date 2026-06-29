import { fillApplicationCardHTML } from "./applicationCard.js";
import { deleteApplicationDialog } from "./deleteApplicationDialog.js";
import { selectStatusForPhase } from "./selectStatusForPhase.js";
import { createApplicationForm } from "./createApplicationForm.js";

function createHTMLPhaseColumn(phase) {
  let phase_column_html = `<div class="kanban-column-flex-container" data-phase-id="${phase["id"]}">`;

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
  createApplicationCallback,
  deleteApplicationCallback,
  updateApplicationCallback,
) {
  console.log(applications);

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

  function getStatusesByPhaseId(phase_id) {
    return statuses.filter((state) => {
      return state["phase"]["id"].toString() === phase_id;
    });
  }

  function getApplicationById(app_id) {
    return applications.find((application) => {
      return application["id"].toString() === app_id;
    });
  }

  document
    .querySelectorAll(".application-card-button-delete")
    .forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const application_card = e.target.closest(".application-card");
        const application_id = application_card.dataset.appId;

        if (!document.querySelector(".delete-application-dialog")) {
          deleteApplicationDialog(application_id, deleteApplicationCallback);
        }
      });
    });

  document
    .querySelectorAll(".application-card-button-change")
    .forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const kanban_card = e.target.closest(".kanban-card");
        const application_card = e.target.closest(".application-card");
        const application_id = application_card.dataset.appId;
        const application_object = applications.find(
          (application) => application.id == application_id,
        );
        const phase_column = e.target.closest(".kanban-column-flex-container");
        const phase_id = phase_column.dataset.phaseId;
        const statuses_for_phase = getStatusesByPhaseId(phase_id);

        application_card.classList.add("hidden");

        createApplicationForm(
          kanban_card,
          statuses_for_phase,
          application_card,
          updateApplicationCallback,
          application_object,
        );
      });
    });

  document.querySelectorAll(".application-button-create").forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      const application_card = e.currentTarget.parentNode;
      const phase_id = application_card.dataset.phaseId;
      const create_button = e.currentTarget;
      const statuses_for_phase = getStatusesByPhaseId(phase_id);

      create_button.classList.add("hidden");

      createApplicationForm(
        application_card,
        statuses_for_phase,
        create_button,
        createApplicationCallback,
      );
    }),
  );

  document.querySelectorAll(".application-card").forEach((card) =>
    card.addEventListener("dragstart", async (e) => {
      const application_card = e.currentTarget;
      const application_id = application_card.dataset.appId;
      e.dataTransfer.setData("text/plain", application_id);
    }),
  );

  document
    .querySelectorAll(".kanban-column-flex-container")
    .forEach((column) => {
      column.addEventListener("dragover", (e) => e.preventDefault());

      column.addEventListener("drop", async (e) => {
        e.preventDefault();

        const phase_column = e.currentTarget;
        const new_phase_id = phase_column.dataset.phaseId;
        const statuses_for_phase = getStatusesByPhaseId(new_phase_id);
        const application_id = e.dataTransfer.getData("text/plain");
        const application = getApplicationById(application_id);
        const previous_phase_id = application.status.phase.id;

        if (previous_phase_id != new_phase_id) {
          selectStatusForPhase(
            application,
            statuses_for_phase,
            updateApplicationCallback,
          );
        } else {
          console.log("Cannot place application into the same phase as before");
        }
      });
    });
}
