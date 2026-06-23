export function formatDateString(date) {
  if (date) {
    let date_formatted = new Date(date);
    return date_formatted.toISOString().slice(0, 10);
  } else {
    return "";
  }
}
