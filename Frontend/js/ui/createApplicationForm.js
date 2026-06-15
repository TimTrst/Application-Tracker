export function renderCreateApplicationForm(statuses_list, createFormCallback) {
  const container = document.getElementById("application-create-form");

  container.innerHTML = renderApplicationInputs(statuses_list);

  const application_submit_button = document.getElementById(
    "application-form-submit",
  );

  application_submit_button.addEventListener("click", async (e) => {
    e.preventDefault();
    const company_name = document.getElementById("cname").value;
    const job_title = document.getElementById("jname").value;
    const job_url = document.getElementById("jurl").value;
    const status_id = document.getElementById("astatus_id").value;
    const application_appointment =
      document.getElementById("jappointment").value;

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

    createFormCallback(new_application);
  });
}

function renderApplicationInputs(statuses_list) {
  return `
    <form>
        <label for="cname">Company Name:</label><br>
        <input id="cname" type="text"></input><br>
        <label for="jname">Job Title:</label><br>
        <input id="jname" type="text"></input><br>
        <label for="jurl">URL:</label><br>
        <input id="jurl" type="text"></input><br>
        <label for="status-select">Status:</label><br>
        <select id="astatus_id" name="status">
            ${statuses_list
              .map((status) => {
                return `<option value="${status["id"]}">${status["name"]}</option>`;
              })
              .join("")}
        </select><br>
        <label for="jappointment">Next Appointment:</label><br>
        <input id="jappointment" type="date"></input><br>
        <input id="application-form-submit" type="submit" value="Create Application"></input>
    </form>
    `;
}
