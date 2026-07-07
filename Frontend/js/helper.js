export function formatDateString(date) {
  if (date) {
    let dateFormatted = new Date(date);
    return dateFormatted.toISOString().slice(0, 10);
  } else {
    return "";
  }
}

export function buildApplicationObject({
  company_name = "",
  job_title = "",
  url = null,
  status_id = 1,
  date_appointment = null,
} = {}) {
  if (url === "") {
    url = null;
  }
  if (date_appointment === "") {
    date_appointment = null;
  }

  status_id = parseInt(status_id);

  return { company_name, job_title, url, status_id, date_appointment };
}
