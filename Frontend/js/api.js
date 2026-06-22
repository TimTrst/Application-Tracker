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

export async function postApplication(application, timeoutMs = 8000) {
  console.log(application);
  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}/api/applications/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Guardrail 2: Explicitly ask for JSON back to prevent HTML error pages
        Accept: "application/json",
      },
      body: JSON.stringify(application),
    });

    // Guardrail 3: Handle HTTP error statuses (fetch does NOT reject on 4xx/5xx)
    if (!response.ok) {
      let errorDetails;
      try {
        errorDetails = await response.json();
      } catch {
        errorDetails = { message: `HTTP error status ${response.status}` };
      }
      throw new Error(
        errorDetails.message || `Server responded with ${response.status}`,
      );
    }

    // Guardrail 4: Guard against empty or non-JSON payloads (e.g., 204 No Content)
    if (response.status === 204) {
      return { success: true };
    }

    // Guardrail 5: Safely parse JSON to prevent app crashes on malformed data
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      throw new TypeError(
        "Expected JSON response from server but received something else.",
      );
    }

    return await response.json();
  } catch (error) {
    if (error.name === "AbortError") {
      console.error("[API Error]: Request timed out.");
      throw new Error("The server took too long to respond. Please try again.");
    }

    console.error("[API Error]: postApplication failed:", error.message);
    throw error; // Re-throw to let your UI component handle the error state
  }
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

export async function updateApplication(updatedApplication, id) {
  console.log(id);
  const response = await fetch(
    `${CONFIG.API_BASE_URL}/api/applications/${id}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        // Guardrail 2: Explicitly ask for JSON back to prevent HTML error pages
        Accept: "application/json",
      },
      body: JSON.stringify(updatedApplication),
    },
  );
}
