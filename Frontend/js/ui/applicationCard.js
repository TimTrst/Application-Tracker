import { formatDateString, loadIconString, loadIcon } from "../helper.js";

export function fillApplicationCardHTML(application) {
  let date = "";
  date = formatDateString(application?.date_appointment);

  const rowToHtmlString = `
        <div class="kanban-card">
            <div class="application-card" draggable="true" data-app-id="${application.id}">
                <div class="application-card-header">
                    <p class="heading-text font-head">
                        ${application.company_name}
                    </p>
                    ${application.url ? `<a class="application-card-button-link" href="${application.url}">${loadIconString("icon-link", "icon-small")}</a>` : `<div></div>`}
                </div>
                <p class="application-card-job-title">${application.job_title}</p>
                <div class="application-card-body">
                    <span class="application-card-date">
                        ${date}
                    </span>
                    <span class="application-card-dot">&middot;</span>
                    <div class="application-card-status-flag">
                        ${application.status.name}
                    </div>
                    <span class="application-card-dot">&middot;</span>
                    <button class="application-card-button-change">${loadIconString("icon-edit", "icon-small")}</button>
                    <button class="application-card-button-delete">${loadIconString("icon-trash", "icon-small")}</button>                    
                </div>
            </div>
        </div>
        `;

  return rowToHtmlString;
}
