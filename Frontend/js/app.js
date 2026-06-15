import {
  getApplications,
  getApplicationPhases,
  getApplicationStatuses,
  postApplication,
} from "./api.js";
import { renderApplicationKanban } from "./ui/applicationsKanaban.js";
import { renderCreateApplicationForm } from "./ui/createApplicationForm.js";

async function createFormCallback(new_application) {
  console.log(new_application);
  const response = await postApplication(new_application);
  refreshKanban();
}

async function refreshKanban() {
  const applications = await getApplications();
  const phases = await getApplicationPhases();
  renderApplicationKanban(applications, phases);
}

async function init() {
  refreshKanban();

  const create_application_button = document.getElementById(
    "application-create-button",
  );

  create_application_button.addEventListener("click", async () => {
    const statuses = await getApplicationStatuses();
    renderCreateApplicationForm(statuses, createFormCallback);
  });
}

init();
