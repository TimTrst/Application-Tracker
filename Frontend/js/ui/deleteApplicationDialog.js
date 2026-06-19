export function deleteApplicationDialog(
  application_id,
  deleteApplicationCallback,
) {
  const confirmDialogBackground = document.createElement("div");

  confirmDialogBackground.className = "delete-application-dialog-background";

  document.body.appendChild(confirmDialogBackground);

  const confirmDialog = confirmDialogHtml();

  confirmDialogBackground.appendChild(confirmDialog);

  const confirm_button = document.querySelector(
    ".confirm-delete-application-button",
  );
  const cancel_button = document.querySelector(
    ".cancel-delete-application-button",
  );

  confirm_button.addEventListener("click", async (e) => {
    deleteApplicationCallback(application_id);

    document.body.removeChild(confirmDialogBackground);
  });

  cancel_button.addEventListener("click", (e) => {
    document.body.removeChild(confirmDialogBackground);
  });
}

function confirmDialogHtml() {
  const dialog = document.createElement("div");

  dialog.className = "delete-application-dialog";

  dialog.innerHTML = `
    <p>Do you want to delete this Application?</p>
    <button class="cancel-delete-application-button">Cancel</button>
    <button class="confirm-delete-application-button">Delete</button>
  `;

  return dialog;
}
