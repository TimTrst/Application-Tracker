export function fillApplicationCardHTML(application) {
  const row_html_string = `
        <div class="kanban-card">
            <header class="application-header">
                <p class="application-header-text">${application.company_name}</p>
                <p class="application-header-text">${application.job_title}</p>
            </header>
            <div class="application-body">
                <p class="application-date">${application.date_appointment}</p>
                <p class="application-url">${application.url}</p>
            </div>
            <div class="application-status-flag">
                ${application.status.name}
            </div>
            <div class="application-footer">
                <button class="application-button-change">Change</button>
                <button class="application-button-delete" data-app-id="${application.id}">Delete</button>
            </div>
        </div>
        `;

  return row_html_string;
}
