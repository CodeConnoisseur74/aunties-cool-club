document.addEventListener("DOMContentLoaded", function () {
  const roomName = "{{ chat_room.id|escapejs }}";  // Ensure room ID is interpolated correctly
  const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
  );

  // Handle incoming messages
  chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const messages = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
    messages.appendChild(messageElement);
  };

  // Handle socket close
  chatSocket.onclose = function (event) {
    console.error('Chat socket closed unexpectedly');
  };

  // Send message via WebSocket
  const chatForm = document.querySelector('#chat-form');
  if (chatForm) {
    chatForm.onsubmit = function (event) {
      event.preventDefault();
      const messageInput = document.querySelector('#message-input');
      const message = messageInput.value;

      if (message.trim()) {
        chatSocket.send(
          JSON.stringify({
            message: message,
          })
        );
        messageInput.value = ''; // Clear input
      }
    };
  } else {
    console.error("Chat form not found!");
  }
});
