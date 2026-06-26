export function selectStatusForPhase(
  application,
  statuses_for_phase,
  updateApplicationCallback,
) {
  const selectStatusContainer = document.createElement("div");

  selectStatusContainer.className = "dialog-background";

  document.body.appendChild(selectStatusContainer);

  const confirmDialog = confirmDialogHtml(statuses_for_phase);

  selectStatusContainer.appendChild(confirmDialog);

  const confirm_button = document.querySelector(
    ".confirm-select-status-button",
  );
  const cancel_button = document.querySelector(".cancel-select-status-button");

  confirm_button.addEventListener("click", async (e) => {
    const selectElement = selectStatusContainer.querySelector(".astatus");
    const selectedStatus = selectElement.value;

    let new_application = {
      company_name: "",
      job_title: "",
      url: null,
      status_id: 1,
      date_appointment: "",
    };

    new_application.company_name = application.company_name;
    new_application.job_title = application.job_title;
    new_application.url = application.url;
    new_application.status_id = parseInt(selectedStatus);
    new_application.date_appointment =
      application.date_appointment !== "" ? application.date_appointment : null;

    updateApplicationCallback(new_application, application.id);

    document.body.removeChild(selectStatusContainer);
  });

  cancel_button.addEventListener("click", (e) => {
    document.body.removeChild(selectStatusContainer);
  });
}

function confirmDialogHtml(statuses_for_phase) {
  const dialog = document.createElement("div");

  dialog.className = "dialog";

  dialog.innerHTML = `
    <p>Select a statuse for the new application phase</p>
    <select class="astatus" name="status">
        ${statuses_for_phase
          .map((status) => {
            return `<option value="${status["id"]}"}>${status["name"]}</option>`;
          })
          .join("")}
    </select>
    <button class="confirm-select-status-button">Submit</button>
    <button class="cancel-select-status-button">Cancel</button>
  `;

  return dialog;
}
