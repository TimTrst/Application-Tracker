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

let _statuses = [];
let _phases = [];

async function createFormCallback(new_application) {
  try {
    const response = await postApplication(new_application);
    refreshKanban(_phases, _statuses);
  } catch (error) {
    console.log(error);
  }
}

async function deleteApplicationCallback(application_id) {
  const response = await deleteApplication(application_id);
  console.log(response);
  refreshKanban(_phases, _statuses);
}

async function updateFormCallback(updatedApplication, id) {
  try {
    const response = await updateApplication(updatedApplication, id);
    refreshKanban(_phases, _statuses);
  } catch (error) {
    console.log(error);
  }
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
