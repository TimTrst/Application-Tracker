import { buildApplicationObject } from "../helper.js";

export function selectStatusForPhase(
  application_object,
  statuses_for_phase,
  updateApplicationCallback,
  draggedApplicationElement,
  sourceColumnOfDraggedElement,
) {
  const selectStatusForPhaseContainer = document.createElement("div");

  selectStatusForPhaseContainer.className = "dialog-background";

  document.body.appendChild(selectStatusForPhaseContainer);

  const confirmDialog = confirmDialogHtml(statuses_for_phase);

  selectStatusForPhaseContainer.appendChild(confirmDialog);

  const confirmButton = selectStatusForPhaseContainer.querySelector(
    ".confirm-select-status-button",
  );
  const cancelButton = selectStatusForPhaseContainer.querySelector(
    ".cancel-select-status-button",
  );

  confirmButton.addEventListener("click", async (e) => {
    const selectElement =
      selectStatusForPhaseContainer.querySelector(".astatus");
    const selectedStatus = selectElement.value;

    const newApplication = buildApplicationObject({
      ...application_object,
      status_id: selectedStatus,
    });

    updateApplicationCallback(newApplication, application_object.id);

    document.body.removeChild(selectStatusForPhaseContainer);
  });

  cancelButton.addEventListener("click", (e) => {
    document.body.removeChild(selectStatusForPhaseContainer);

    const buttonCard = sourceColumnOfDraggedElement.querySelector(
      ".application-button-create",
    ).parentNode;

    const column = buttonCard.parentNode;

    column.insertBefore(draggedApplicationElement, buttonCard);
  });
}

function confirmDialogHtml(statuses_for_phase) {
  const dialog = document.createElement("div");

  console.log(statuses_for_phase);

  dialog.className = "dialog";

  dialog.innerHTML = `
    <p>Select a status for the new phase: ${statuses_for_phase[0].phase.name}</p>
    <select class="astatus" name="status">
        ${statuses_for_phase
          .map((status) => {
            return `<option value="${status["id"]}">${status["name"]}</option>`;
          })
          .join("")}
    </select>
    <div class="dialog-footer">      
      <button class="confirm-select-status-button">Submit</button>
      <button class="cancel-select-status-button">Cancel</button>
    </div>
  `;

  return dialog;
}
