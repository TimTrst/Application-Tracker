import {
  getApplications,
  getApplicationPhases,
  getApplicationStatuses,
  postApplication,
  deleteApplication,
  updateApplication,
} from "./api.js";
import { renderApplicationKanban } from "./ui/applicationsKanaban.js";
import { createApplicationForm } from "./ui/createApplicationForm.js";
import { responseNotification } from "./ui/responseNotification.js";

let _statuses = [];
let _phases = [];

async function createFormCallback(new_application) {
  const response = await postApplication(new_application);
  responseNotification(response);
  refreshKanban(_phases, _statuses);
}

async function deleteApplicationCallback(application_id) {
  const response = await deleteApplication(application_id);
  responseNotification(response);
  refreshKanban(_phases, _statuses);
}

async function updateFormCallback(updatedApplication, id) {
  const response = await updateApplication(updatedApplication, id);
  responseNotification(response);
  refreshKanban(_phases, _statuses);
}

async function refreshKanban(phases, statuses) {
  const applications = await getApplications();

  renderApplicationKanban(
    applications,
    phases,
    statuses,
    createFormCallback,
    deleteApplicationCallback,
    updateFormCallback,
  );
}

async function init() {
  _phases = await getApplicationPhases();
  _statuses = await getApplicationStatuses();

  refreshKanban(_phases, _statuses);
}

init();
