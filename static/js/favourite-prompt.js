document.addEventListener("DOMContentLoaded", function () {
  const favouriteButtons = document.querySelectorAll(".favouriteBtn");

  favouriteButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const promptId = this.dataset.promptId;
      const card = this.closest(".saved-prompt-card");

      fetch(`/prompts/save/${promptId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "saved") {
            this.classList.add("text-yellow-500");
            this.classList.remove("text-gray-400");
          } else if (data.status === "removed") {
            this.classList.remove("text-yellow-500");
            this.classList.add("text-gray-400");

            // remove from dashboard immediately
            if (card) {
              card.remove();
            }

            // remove detail wrapper if on detail page
            const detailWrapper = document.querySelector(".detail-wrapper");
            if (detailWrapper) {
              detailWrapper.remove();
            }
          }
        })
        .catch((error) => console.error("Error toggling favourite:", error));
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
