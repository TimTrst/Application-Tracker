import { fillApplicationCardHTML } from "./applicationCard.js";
import { deleteApplicationDialog } from "./deleteApplicationDialog.js";
import { selectStatusForPhase } from "./selectStatusForPhase.js";
import { createApplicationForm } from "./createApplicationForm.js";

function createHTMLPhaseColumn(phase) {
  let phaseColumnHtml = `<div class="kanban-column-flex-container" data-phase-id="${phase["id"]}">`;

  let phaseHeader = `<div class="kanban-column-header">`;

  let phaseName = `<p>${phase["name"]}</p></div>`;

  phaseColumnHtml += phaseHeader + phaseName;

  let phaseColumnInner = (phase["applications"] ?? [])
    .map((application) => fillApplicationCardHTML(application))
    .join("");

  phaseColumnHtml = phaseColumnHtml + phaseColumnInner;

  let addApplicationDiv = `<div class="kanban-card" data-phase-id="${phase["id"]}">
   <button class="application-button-create">Create new Application</button>
  </div>`;

  phaseColumnHtml = phaseColumnHtml + addApplicationDiv + `</div>`;

  return phaseColumnHtml;
}

export function renderApplicationKanban(
  applications,
  phases,
  statuses,
  createApplicationCallback,
  deleteApplicationCallback,
  updateApplicationCallback,
) {
  const container = document.getElementById("applications-list");
  const phasesWithApplications = new Map();
  let draggedApplicationElement;
  let sourceColumnOfDraggedElement;

  phases.forEach((phase) => {
    phasesWithApplications.set(phase["name"], {
      ...phase,
      applications: [],
    });
  });

  applications.forEach((application) => {
    let applicationPhase = application["status"]["phase"];
    let applicationPhaseName = applicationPhase["name"];

    phasesWithApplications
      .get(applicationPhaseName)
      .applications.push(application);
  });

  container.innerHTML = `
    ${[...phasesWithApplications.values()]
      .map((phase) => createHTMLPhaseColumn(phase))
      .join("")}
  `;

  function getStatusesByPhaseId(phaseId) {
    return statuses.filter((state) => {
      return state["phase"]["id"].toString() === phaseId;
    });
  }

  function getApplicationById(appId) {
    return applications.find((application) => {
      return application["id"].toString() === appId;
    });
  }

  /*
  Eventlistener for application cards (create, update, delete)
  ------------------------------------------------------------------------------
  */
  // DELETE
  document
    .querySelectorAll(".application-card-button-delete")
    .forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const applicationCard = e.target.closest(".application-card");
        const applicationId = applicationCard.dataset.appId;

        if (!document.querySelector(".delete-application-dialog")) {
          deleteApplicationDialog(applicationId, deleteApplicationCallback);
        }
      });
    });

  // UPDATE
  document
    .querySelectorAll(".application-card-button-change")
    .forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const kanbanCard = e.target.closest(".kanban-card");
        const applicationCard = e.target.closest(".application-card");
        const applicationId = applicationCard.dataset.appId;
        const applicationObject = applications.find(
          (application) => application.id == applicationId,
        );
        const phaseColumn = e.target.closest(".kanban-column-flex-container");
        const phaseId = phaseColumn.dataset.phaseId;
        const statusesForPhase = getStatusesByPhaseId(phaseId);

        // hidden, not removed, so it can be restored if the edit is cancelled
        applicationCard.classList.add("hidden");

        createApplicationForm(
          kanbanCard,
          statusesForPhase,
          applicationCard,
          updateApplicationCallback,
          // passing an applicationObject switches the form into "update" mode;
          // the create flow calls this with it omitted
          applicationObject,
        );
      });
    });

  // CREATE
  document.querySelectorAll(".application-button-create").forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      const kanbanCard = e.currentTarget.parentNode;
      const phaseId = kanbanCard.dataset.phaseId;
      const createButton = e.currentTarget;
      const statusesForPhase = getStatusesByPhaseId(phaseId);

      createButton.classList.add("hidden");

      createApplicationForm(
        kanbanCard,
        statusesForPhase,
        createButton,
        createApplicationCallback, // create callback
        // application object missing here: we do not need an existing object for creating a new one
      );
    }),
  );

  // UPDATE: DRAGSTART EVENT
  // dragging starts with a specific application card
  document.querySelectorAll(".application-card").forEach((card) =>
    card.addEventListener("dragstart", async (e) => {
      const applicationCard = e.currentTarget;
      draggedApplicationElement = applicationCard.parentNode; // grab whole kanban-card which holds an application card
      sourceColumnOfDraggedElement = draggedApplicationElement.parentNode;
      const applicationId = applicationCard.dataset.appId;
      e.dataTransfer.setData("text/plain", applicationId);
    }),
  );

  // UPDATE: DRAGOVER
  // the card can be dropped anywhere in a kanban column
  // todo: visualizing the drop in a column (before releasing and updating the board)
  document
    .querySelectorAll(".kanban-column-flex-container")
    .forEach((column) => {
      column.addEventListener("dragover", (e) => {
        e.preventDefault();
        const buttonCard = column.querySelector(
          ".application-button-create",
        ).parentNode;

        column.insertBefore(draggedApplicationElement, buttonCard);
      });

      column.addEventListener("drop", async (e) => {
        e.preventDefault();

        const phaseColumn = e.currentTarget;
        const newPhaseId = phaseColumn.dataset.phaseId;
        const statusesForPhase = getStatusesByPhaseId(newPhaseId);
        const applicationId = e.dataTransfer.getData("text/plain");
        const application = getApplicationById(applicationId);
        const previousPhaseId = application.status.phase.id;

        if (previousPhaseId != newPhaseId) {
          selectStatusForPhase(
            application,
            statusesForPhase,
            updateApplicationCallback,
            draggedApplicationElement,
            sourceColumnOfDraggedElement,
          );
        } else {
          console.log("Cannot place application into the same phase as before");
        }
      });
    });
}
