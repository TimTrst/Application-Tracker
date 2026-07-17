import { formatDateString, buildApplicationObject } from "../helper.js";

export function createApplicationForm(
  containerToInsertHtml,
  statusesForPhase,
  elementToRestore,
  submitCallback,
  applicationObject = {},
) {
  // div to render the form into
  const applicationFormElement = document.createElement("div");

  applicationFormElement.innerHTML = renderApplicationForm(
    statusesForPhase,
    applicationObject,
  );

  containerToInsertHtml.appendChild(applicationFormElement);

  // listen to any close event on application forms
  // remove the form
  // turn form create button visible again
  applicationFormElement
    .querySelectorAll(".application-form-close")
    .forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const formContainer = e.currentTarget.closest(".kanban-card");

        applicationFormElement.remove();
        elementToRestore.classList.remove("hidden");
      }),
    );

  // listen to the form submit
  applicationFormElement
    .querySelector("form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      // currentTarget refers to the element that the listener was attached to (the form in this case)
      const container = e.currentTarget.closest("form");

      const companyName = container.querySelector(".cname").value;
      const jobTitle = container.querySelector(".jname").value;
      const url = container.querySelector(".jurl").value;
      const statusId = container.querySelector(".astatus").value;
      const dateAppointment = container.querySelector(".jappointment").value;

      const newApplication = buildApplicationObject({
        company_name: companyName,
        job_title: jobTitle,
        url,
        status_id: statusId,
        date_appointment: dateAppointment,
      });

      await submitCallback(newApplication, applicationObject.id);
    });
}

// render the form
function renderApplicationForm(statusesForPhase, application) {
  let date = "";
  let isNewApplication = true;

  if (Object.keys(application).length !== 0) {
    isNewApplication = false;
    date = formatDateString(application.application_appointment);
  }

  return `
    <form class="create-application-form">
        <div class="create-application-form-header">
          <span class="heading-text font-head">${isNewApplication ? "New application" : "Update application"}</span>
        </div>
        <div class="application-create-form-field">
          <label>
            COMPANY:
            <input required minlength="3" maxlength="40" class="cname" name="cname" type="text" value="${application.company_name || ""}">
          </label>
        </div>
        <div class="application-create-form-field">
          <label>
            JOB TITLE:
            <input required minlength="3" maxlength="40" class="jname" name="jname" type="text" value="${application.job_title || ""}">
          </label>
        </div>
        <div class="application-create-form-field">
          <label>
            URL:
            <input class="jurl" name="jurl" type="url" value="${application.url || ""}">
          </label>
        </div>
        <div class="application-create-status-and-appointment">
          <div class="application-create-form-field">
            <label>
            STATUS:
              <select class="astatus" name="status">
                  ${statusesForPhase
                    .map((status) => {
                      return `<option value="${status["id"]}" ${status.id === application?.status?.id ? "selected" : ""}>${status["name"]}</option>`;
                    })
                    .join("")}
              </select>
            </label>
          </div>
          <div class="application-create-form-field">
            <label>APOINTMENT:
              <input class="jappointment" name="jappointment" type="date" value="${date}">
            </label>
          </div>
        </div>
        <div class="application-form-buttons">
          <input class="application-form-submit" type="submit" value="SAVE &#8594;">
          <button class="application-form-close" type="button">CANCEL</button>
        </div>
    </form>
    `;
}
