export function responseNotification(responseObject) {
  let notificationContainer = document.querySelector(
    ".response-notifications-container",
  );
  if (!notificationContainer) {
    notificationContainer = document.createElement("div");
    notificationContainer.className = "response-notifications-container";
    document.body.appendChild(notificationContainer);
  }

  const notificationCard = notificationCardHtml(responseObject);
  notificationContainer.appendChild(notificationCard);

  setTimeout(() => {
    notificationCard.remove();
  }, 4000);
}

function notificationCardHtml(response) {
  const card = document.createElement("div");

  card.className = "response-notification-card";

  if (response.ok) {
    card.style.backgroundColor = "rgba(14, 206, 39, 0.6)";
  } else {
    card.style.backgroundColor = "rgba(255, 0, 0, 0.6)";
  }

  card.innerHTML = `
        <p>${response.message ?? "Message missing"}</p>   
        <p>${response.backendMessage ?? "Message missing"}</p>
    `;

  return card;
}
