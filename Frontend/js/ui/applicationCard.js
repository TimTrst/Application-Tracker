export function fillApplicationCardHTML(application) {
  const row_html_string = `
        <div class="kanban-card">
            <div class="application-card" data-app-id="${application.id}">
                <header class="application-card-header">
                    <p class="application-header-text">${application.company_name}</p>
                    <p class="application-header-text">${application.job_title}</p>
                </header>
                <div class="application-card-body">
                    <p class="application-card-date">${application.date_appointment}</p>
                    <p class="application-card-url">${application.url}</p>
                </div>
                <div class="application-card-status-flag">
                    ${application.status.name}
                </div>
                <div class="application-card-footer">
                    <button class="application-card-button-change">Change</button>
                    <button class="application-card-button-delete">Delete</button>
                </div>
            </div>
        </div>
        `;

  return row_html_string;
}
