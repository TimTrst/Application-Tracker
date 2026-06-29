export function deleteApplicationDialog(
  application_id,
  deleteApplicationCallback,
) {
  const deleteApplicationContainer = document.createElement("div");

  deleteApplicationContainer.className = "dialog-background";

  document.body.appendChild(deleteApplicationContainer);

  const confirmDialog = confirmDialogHtml();

  deleteApplicationContainer.appendChild(confirmDialog);

  const confirm_button = deleteApplicationContainer.querySelector(
    ".confirm-delete-application-button",
  );
  const cancel_button = deleteApplicationContainer.querySelector(
    ".cancel-delete-application-button",
  );

  confirm_button.addEventListener("click", async (e) => {
    deleteApplicationCallback(application_id);

    document.body.removeChild(deleteApplicationContainer);
  });

  cancel_button.addEventListener("click", (e) => {
    document.body.removeChild(deleteApplicationContainer);
  });
}

function confirmDialogHtml() {
  const dialog = document.createElement("div");

  dialog.className = "dialog";

  dialog.innerHTML = `
    <p>Do you want to delete this Application?</p>
    <button class="cancel-delete-application-button">Cancel</button>
    <button class="confirm-delete-application-button">Delete</button>
  `;

  return dialog;
}
