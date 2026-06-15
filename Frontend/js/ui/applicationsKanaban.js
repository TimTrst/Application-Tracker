import { fillApplicationCardHTML } from "./applicationCard.js";

function createHTMLPhaseColumn(phase) {
  let phase_column_html = `<div class="kanban-column-flex-container">`;

  let phase_header = `<div class="kanban-column-header"></div>`;

  let phase_name = `<p>${phase["name"]}</p>`;

  phase_column_html += phase_header + phase_name;

  let phase_column_inner = (phase["applications"] ?? [])
    .map((application) => fillApplicationCardHTML(application))
    .join("");

  phase_column_html = phase_column_html + phase_column_inner + `</div>`;

  return phase_column_html;
}

export function renderApplicationKanban(applications, phases) {
  const container = document.getElementById("applications-list");

  phases.forEach((phase) => {
    applications.forEach((application) => {
      if (phase["name"] === application["status"]["phase"]["name"]) {
        if (!Object.hasOwn(phase, "applications")) {
          phase["applications"] = [];
        }

        phase["applications"].push(application);
      }
    });
  });

  container.innerHTML = `
        ${phases
          .map((phase) => {
            return createHTMLPhaseColumn(phase);
          })
          .join("")}
    `;
}
