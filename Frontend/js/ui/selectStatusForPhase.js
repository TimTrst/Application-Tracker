import { buildApplicationObject } from "../helper.js";

export function selectStatusForPhase(
  application_object,
  statuses_for_phase,
  updateApplicationCallback,
) {
  const selectStatusForPhaseContainer = document.createElement("div");

  selectStatusForPhaseContainer.className = "dialog-background";

  document.body.appendChild(selectStatusForPhaseContainer);

  const confirmDialog = confirmDialogHtml(statuses_for_phase);

  selectStatusForPhaseContainer.appendChild(confirmDialog);

  const confirm_button = selectStatusForPhaseContainer.querySelector(
    ".confirm-select-status-button",
  );
  const cancel_button = selectStatusForPhaseContainer.querySelector(
    ".cancel-select-status-button",
  );

  confirm_button.addEventListener("click", async (e) => {
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

  cancel_button.addEventListener("click", (e) => {
    document.body.removeChild(selectStatusForPhaseContainer);
  });
}

function confirmDialogHtml(statuses_for_phase) {
  const dialog = document.createElement("div");

  dialog.className = "dialog";

  dialog.innerHTML = `
    <p>Select a statuse for the new application_object phase</p>
    <select class="astatus" name="status">
        ${statuses_for_phase
          .map((status) => {
            return `<option value="${status["id"]}">${status["name"]}</option>`;
          })
          .join("")}
    </select>
    <button class="confirm-select-status-button">Submit</button>
    <button class="cancel-select-status-button">Cancel</button>
  `;

  return dialog;
}
