import { formatDateString, buildApplicationObject } from "../helper.js";

export function createApplicationForm(
  container_to_insert_html,
  statuses_for_phase,
  element_to_restore,
  submitCallback,
  application_object = {},
) {
  // div to render the form into
  const create_application_form = document.createElement("div");

  create_application_form.innerHTML = renderApplicationForm(
    statuses_for_phase,
    application_object,
  );

  container_to_insert_html.appendChild(create_application_form);

  // listen to any close event on application forms
  // remove the form
  // turn form create button visible again
  create_application_form
    .querySelectorAll(".application-form-close")
    .forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const formContainer = e.currentTarget.closest(".kanban-card");

        create_application_form.remove();
        element_to_restore.classList.remove("hidden");
      }),
    );

  // listen to the form submit
  create_application_form
    .querySelector("form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      // currentTarget refers to the element that the listener was attached to (the form in this case)
      const container = e.currentTarget.closest("form");

      const company_name = container.querySelector(".cname").value;
      const job_title = container.querySelector(".jname").value;
      const url = container.querySelector(".jurl").value;
      const status_id = container.querySelector(".astatus").value;
      const date_appointment = container.querySelector(".jappointment").value;

      const newApplication = buildApplicationObject({
        company_name,
        job_title,
        url,
        status_id,
        date_appointment,
      });

      await submitCallback(newApplication, application_object.id);
    });
}

// render the form
function renderApplicationForm(statuses_for_phase, application) {
  let date = "";

  if (Object.keys(application).length !== 0) {
    date = formatDateString(application.application_appointment);
  }

  return `
    <form class="create-application-form">
        <div>
          <label>
            Company Name:
            <input required minlength="3" maxlength="40" class="cname" name="cname" type="text" value="${application.company_name || ""}">
          </label>
        </div>
        <div class="application-create-form-field">
          <label>
            Job Title:
            <input required minlength="3" maxlength="40" class="jname" name="jname" type="text" value="${application.job_title || ""}">
          </label>
        </div>
        <div class="application-create-form-field">
          <label>
            URL:
            <input class="jurl" name="jurl" type="url" value="${application.url || ""}">
          </label>
        </div>
        <div class="application-create-form-field">
          <label>
          Status:
            <select class="astatus" name="status">
                ${statuses_for_phase
                  .map((status) => {
                    return `<option value="${status["id"]}" ${status.id === application?.status?.id ? "selected" : ""}>${status["name"]}</option>`;
                  })
                  .join("")}
            </select>
          </label>
        </div>
        <div class="application-create-form-field">
          <label>Next Appointment:
            <input class="jappointment" name="jappointment" type="date" value="${date}">
          </label>
        </div>
        <input class="application-form-submit" type="submit" value="Submit">
        <button class="application-form-close" type="button">Close</button>
    </form>
    `;
}
