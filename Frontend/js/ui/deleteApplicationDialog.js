export function deleteApplicationDialog(
  applicationId,
  deleteApplicationCallback,
) {
  const deleteApplicationContainer = document.createElement("div");

  deleteApplicationContainer.className = "dialog-background";

  document.body.appendChild(deleteApplicationContainer);

  const confirmDialog = confirmDialogHtml();

  deleteApplicationContainer.appendChild(confirmDialog);

  const confirmButton = deleteApplicationContainer.querySelector(
    ".confirm-delete-application-button",
  );
  const cancelButton = deleteApplicationContainer.querySelector(
    ".cancel-delete-application-button",
  );

  confirmButton.addEventListener("click", async (e) => {
    deleteApplicationCallback(applicationId);

    document.body.removeChild(deleteApplicationContainer);
  });

  cancelButton.addEventListener("click", (e) => {
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
