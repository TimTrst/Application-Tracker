import { CONFIG } from "./config.js";

export async function getApplications() {
  const response = await fetch(`${CONFIG.API_BASE_URL}/api/applications/`);
  return await response.json();
}

export async function getApplicationPhases() {
  const response = await fetch(`${CONFIG.API_BASE_URL}/api/phases/`);
  return await response.json();
}

export async function getApplicationStatuses() {
  const response = await fetch(`${CONFIG.API_BASE_URL}/api/statuses/`);
  return await response.json();
}

export async function postApplication(application) {
  const response = await fetch(`${CONFIG.API_BASE_URL}/api/applications/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(application),
  });
  return await response.json();
}

export async function deleteApplication(id) {
  const response = await fetch(
    `${CONFIG.API_BASE_URL}/api/applications/${id}`,
    {
      method: "DELETE",
    },
  );
  return await response.json();
}
