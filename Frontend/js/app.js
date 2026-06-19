import {
  getApplications,
  getApplicationPhases,
  getApplicationStatuses,
  postApplication,
  deleteApplication,
} from "./api.js";
import { renderApplicationKanban } from "./ui/applicationsKanaban.js";
import { createApplicationForm } from "./ui/createApplicationForm.js";

async function createFormCallback(new_application) {
  try {
    const response = await postApplication(new_application);
    refreshKanban();
  } catch (error) {
    console.log(error);
  }
}

async function deleteApplicationCallback(application_id) {
  const response = await deleteApplication(application_id);
  refreshKanban();
}

async function getApplicationStatusesCallback() {
  const response = await getApplicationStatuses();
  return response;
}

async function refreshKanban() {
  const applications = await getApplications();
  const phases = await getApplicationPhases();

  renderApplicationKanban(
    applications,
    phases,
    createFormCallback,
    deleteApplicationCallback,
    getApplicationStatusesCallback,
  );
}

async function init() {
  refreshKanban();
}

init();
