import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import {
  sankey,
  sankeyLinkHorizontal,
} from "https://cdn.jsdelivr.net/npm/d3-sankey@0.12/+esm";

export function renderSankeyDiagram(history_log_transitions, phases, statuses) {
  const container = document.getElementById("sankey-diagram");

  // TODO 1: build phase/status lookup Maps (same pattern you already use
  // for the Kanban board — id -> name)
  const statusMap = new Map(statuses.map((s) => [s.id, s]));
  const phaseMap = new Map(phases.map((p) => [p.id, p]));

  // TODO 2: build a deduplicated `nodes` array from the phase/status
  // combinations appearing in `transitions`, plus a lookup from your ids
  // to each node's index in that array (d3-sankey wants indices, not ids)
  const transitionsStatusValues = history_log_transitions.flatMap((entry) => [
    entry.from_status_id,
    entry.to_status_id,
  ]);

  const statusesDeduplicated = [
    ...new Set(transitionsStatusValues.filter((value) => value != null)),
  ];

  let nodesArray = statusesDeduplicated.map((statusId) => ({
    id: statusId,
    title: statusMap.get(statusId).name,
  }));

  nodesArray.push({ id: "start", title: "Start" });

  // TODO 3: build the `links` array from `transitions`, referencing node
  // indices, with a `value` for link width

  const linksMap = history_log_transitions.reduce((accumulator, logEntry) => {
    let from_status_id = logEntry.from_status_id;
    const to_status_id = logEntry.to_status_id;
    if (from_status_id === null) {
      from_status_id = "start";
    }

    const transitionStatusKey = `${from_status_id}-${to_status_id}`;

    if (accumulator.has(transitionStatusKey)) {
      accumulator.get(transitionStatusKey).value++;
    } else {
      accumulator.set(transitionStatusKey, {
        source: from_status_id,
        target: to_status_id,
        value: 1,
      });
    }
    return accumulator;
  }, new Map());

  const linksArray = [...linksMap.values()];

  // TODO 4: run the layout generator, then render nodes as <rect>,
  // links as <path> via sankeyLinkHorizontal(), labels as <text>
  // --- D3 layout + rendering ---
  const width = container.clientWidth || 800;
  const height = 500;

  const svg = d3
    .select(container)
    .append("svg")
    .attr("viewBox", [0, 0, width, height])
    .attr("width", width)
    .attr("height", height);

  const sankeyGenerator = sankey()
    .nodeId((d) => d.id)
    .nodeWidth(15)
    .nodePadding(12)
    .extent([
      [1, 5],
      [width - 1, height - 5],
    ]);

  const { nodes, links } = sankeyGenerator({
    nodes: nodesArray,
    links: linksArray,
  });

  const color = d3.scaleOrdinal(d3.schemeTableau10);

  svg
    .append("g")
    .attr("fill", "none")
    .attr("stroke-opacity", 0.4)
    .selectAll("path")
    .data(links)
    .join("path")
    .attr("d", sankeyLinkHorizontal())
    .attr("stroke", (d) => color(d.source.title))
    .attr("stroke-width", (d) => Math.max(1, d.width));

  const node = svg.append("g").selectAll("g").data(nodes).join("g");

  node
    .append("rect")
    .attr("x", (d) => d.x0)
    .attr("y", (d) => d.y0)
    .attr("width", (d) => d.x1 - d.x0)
    .attr("height", (d) => d.y1 - d.y0)
    .attr("fill", (d) => color(d.title));

  node
    .append("text")
    .attr("x", (d) => (d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6))
    .attr("y", (d) => (d.y0 + d.y1) / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", (d) => (d.x0 < width / 2 ? "start" : "end"))
    .text((d) => `${d.title} (${d.value})`);
}
