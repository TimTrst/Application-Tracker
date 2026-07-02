import { CONFIG } from "./config.js";

const REQUEST_TYPE = {
  POST: "post",
  PATCH: "patch",
  GET: "get",
  DELETE: "delete",
};

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
  const response = await fetch(`${CONFIG.API_BASE_URL}/api/applications/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(application),
  });

  return await handleRequestReponse(response, REQUEST_TYPE.POST);
}

export async function deleteApplication(id) {
  const response = await fetch(
    `${CONFIG.API_BASE_URL}/api/applications/${id}`,
    {
      method: "DELETE",
    },
  );
  return await handleRequestReponse(response, REQUEST_TYPE.DELETE);
}

export async function updateApplication(updatedApplication, id) {
  const response = await fetch(
    `${CONFIG.API_BASE_URL}/api/applications/${id}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(updatedApplication),
    },
  );
  return await handleRequestReponse(response, REQUEST_TYPE.PATCH);
}

async function handleRequestReponse(response, requestTypeString) {
  let responseJson = {};
  if (response.status !== 204) {
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      try {
        responseJson = await response.json();
      } catch (error) {
        return {
          ok: false,
          data: {},
          message: "Received an invalid response from the server",
          backendMessage: "There has been an issue with your request",
        };
      }
    }
  }

  let result = { ok: false, data: responseJson };

  let requestTypeMessage = "";
  if (!response.ok) {
    if (requestTypeString === REQUEST_TYPE.PATCH) {
      requestTypeMessage = "The application information could not be updated";
    } else if (requestTypeString === REQUEST_TYPE.POST) {
      requestTypeMessage = "The application could not be created";
    } else if (requestTypeString === REQUEST_TYPE.DELETE) {
      requestTypeMessage = "The application could not be deleted";
    }
    let httpErrorSource = "";
    let httpErrorMessage = "";
    if (response.status >= 400 && response.status < 500) {
      httpErrorSource = "your request";
      httpErrorMessage = "-" + response.statusText;
    }
    if (response.status >= 500) {
      httpErrorSource = "the server";
    }
    const statusMessage = `There has been an issue with ${httpErrorSource}: ${response.status} ${httpErrorMessage}`;

    result = {
      ...result,
      message: requestTypeMessage,
      backendMessage: statusMessage,
    };
  } else {
    if (requestTypeString === REQUEST_TYPE.PATCH) {
      requestTypeMessage =
        "The application information has been successfully updated";
    } else if (requestTypeString === REQUEST_TYPE.POST) {
      requestTypeMessage = "The application has been successfully created";
    } else if (requestTypeString === REQUEST_TYPE.DELETE) {
      requestTypeMessage = "The application has been successfully deleted";
    }
    result = {
      ...result,
      ok: true,
      message: requestTypeMessage,
      backendMessage: "Request successful.",
    };
  }

  return result;
}
