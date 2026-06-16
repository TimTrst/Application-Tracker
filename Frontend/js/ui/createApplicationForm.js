export function createApplicationForm(
  container_to_insert_html,
  statuses_list,
  createFormCallback,
) {
  // const container = document.getElementById("application-create-form");

  const create_application_form = document.createElement("div");

  create_application_form.innerHTML = renderApplicationInputs(statuses_list);

  container_to_insert_html.appendChild(create_application_form);

  create_application_form
    .querySelectorAll(".application-form-close")
    .forEach((btn) =>
      btn.addEventListener("click", (e) => {
        create_application_form.remove();
      }),
    );

  const application_submit_button = create_application_form.querySelectorAll(
    ".application-form-submit",
  );

  application_submit_button.forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const container = e.target.closest("form");
      const company_name = container.querySelector(".cname").value;
      const job_title = container.querySelector(".jname").value;
      const job_url = container.querySelector(".jurl").value;
      const status_id = container.querySelector(".astatus_id").value;
      const application_appointment =
        container.querySelector(".jappointment").value;

      let new_application = {
        company_name: "",
        job_title: "",
        url: "",
        status_id: 1,
        date_appointment: "",
      };

      new_application.company_name = company_name;
      new_application.job_title = job_title;
      new_application.url = job_url;
      new_application.status_id = status_id;
      new_application.date_appointment = application_appointment;

      console.log(new_application);

      createFormCallback(new_application);
    }),
  );
}

function renderApplicationInputs(statuses_list) {
  return `
    <form>
        <label for="cname">Company Name:</label><br>
        <input class="cname" type="text"></input><br>
        <label for="jname">Job Title:</label><br>
        <input class="jname" type="text"></input><br>
        <label for="jurl">URL:</label><br>
        <input class="jurl" type="text"></input><br>
        <label for="status-select">Status:</label><br>
        <select class="astatus_id" name="status">
            ${statuses_list
              .map((status) => {
                return `<option value="${status["id"]}">${status["name"]}</option>`;
              })
              .join("")}
        </select><br>
        <label for="jappointment">Next Appointment:</label><br>
        <input class="jappointment" type="date"></input><br>
        <input class="application-form-submit" type="submit" value="Create Application"></input>
        <button class="application-form-close" type="button">Close</button>
    </form>
    `;
}
