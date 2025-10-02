/**
 * Favourite Prompt Functionality
 * Handles saving and removing writing prompts from user favourites
 */

document.addEventListener('DOMContentLoaded', function () {
  // Find all favourite buttons
  const favouriteBtns = document.querySelectorAll('.favouriteBtn');

  if (!favouriteBtns.length) return; // no buttons found

  // Function to update the button appearance
  function updateFavouriteButtonAppearance(button, isFavourite) {
    if (isFavourite) {
      button.classList.remove('text-gray-400');
      button.classList.add('text-yellow-500');
      button.querySelector('svg').setAttribute('fill', 'currentColor');
    } else {
      button.classList.remove('text-yellow-500');
      button.classList.add('text-gray-400');
      button.querySelector('svg').setAttribute('fill', 'none');
    }
  }

  // Toggle favourite status
  function toggleFavourite(event) {
    event.preventDefault();

    const button = this;
    const promptId = button.getAttribute('data-prompt-id');
    if (!promptId) {
      console.error('No prompt ID available');
      return;
    }

    // Pulse animation during request
    button.classList.add('animate-pulse');

    fetch(`/prompts/save/${promptId}/`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin'
    })
      .then(response => response.json())
      .then(data => {
        button.classList.remove('animate-pulse');

        if (data.status === 'success') {
          updateFavouriteButtonAppearance(button, data.is_saved);

          showMessage(
            data.message || (data.is_saved
              ? 'Prompt added to your profile!'
              : 'Prompt removed from your profile.'),
            'success'
          );
        }
      })
      .catch(error => {
        button.classList.remove('animate-pulse');
        console.error('Error toggling favourite:', error);
        showMessage('Error saving favourite. Please try again.', 'error');
      });
  }

  // Attach listener to each star button
  favouriteBtns.forEach((btn) => {
    btn.addEventListener('click', toggleFavourite);
  });

  // Show floating message
  function showMessage(message, type = 'info') {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'fixed top-1/4 left-1/2 transform -translate-x-1/2 z-50';
    messageContainer.id = 'prompt-message-container';

    const messageElement = document.createElement('div');
    messageElement.className = type === 'success'
      ? 'bg-green-100 border-green-600 text-green-700 border px-4 py-3 rounded-lg shadow-lg mb-4'
      : type === 'error'
        ? 'bg-red-100 border-red-800 text-red-900 border px-4 py-3 rounded-lg shadow-lg mb-4'
        : 'bg-blue-100 border-blue-600 text-blue-700 border px-4 py-3 rounded-lg shadow-lg mb-4';

    messageElement.setAttribute('role', 'alert');

    const titleElement = document.createElement('strong');
    titleElement.className = 'font-bold';
    titleElement.textContent = type === 'success' ? 'Success!' : type === 'error' ? 'Error!' : 'Notice';

    const textElement = document.createElement('span');
    textElement.className = 'block sm:inline ml-2';
    textElement.textContent = message;

    messageElement.appendChild(titleElement);
    messageElement.appendChild(textElement);
    messageContainer.appendChild(messageElement);

    // Remove existing messages before showing new one
    document.querySelectorAll('#prompt-message-container').forEach(msg => msg.remove());

    document.body.appendChild(messageContainer);

    // Fade out after 5 seconds
    setTimeout(() => {
      messageElement.style.opacity = '0';
      messageElement.style.transition = 'opacity 0.3s ease-in-out';
      setTimeout(() => {
        messageContainer.remove();
      }, 300);
    }, 5000);
  }
});
