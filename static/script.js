var ChatApi = {
  sendMessage: (username, message) => {
    ChatApi.socket.emit("send question", { username, message });
  },
  subscribe: callback => {
    ChatApi.socket.on("bot answer", function({ username, message }) {
      callback(null, { username, message });
    });

    ChatApi.socket.on("error", function({ username, message }) {
      callback({ username, message });
    });
  },
  init: callback => {
    ChatApi.socket = io.connect(
      "http://" + document.domain + ":" + location.port
    );

    ChatApi.socket.on("connect", () => callback && callback());
  }
};

var UI = {
  getUsernameField: () => $("#username"),
  getMessageField: () => $("#message"),
  getChatBox: () => $(".chat-messages"),
  getSubmitButton: () => $("#submit"),
  disableSubmit: (text = "Send message") => {
    let submitButton = UI.getSubmitButton();
    submitButton.attr("disabled", true);
    submitButton.val(text);
  },
  enableSubmit: () => {
    let submitButton = UI.getSubmitButton();
    submitButton.attr("disabled", false);
    submitButton.val("Send message");
  },
  getForm: () => $("form"),
  validate: () => {
    const username = UI.getUsernameField().val();
    const message = UI.getMessageField().val();

    return $.trim(username) && $.trim(message);
  },
  addMessage: (username, message, type) => {
    const className = type === "error" ? "error-message" : "message";
    const usernameMarkup = `<strong>${username}: </strong>`;
    const messageMarkup = `<span>${message}</span>`;

    UI.getChatBox().append(`<p class="${className}">
      ${usernameMarkup}
      ${messageMarkup}
    </p>`);
    UI.scrollToBottomOfChat();
  },
  scrollToBottomOfChat: () => {
    const chatBox = UI.getChatBox();
    chatBox.scrollTop(chatBox.prop("scrollHeight"));
  },
  init: () => {
    const validate = () => {
      if (UI.validate()) {
        UI.enableSubmit();
      } else {
        UI.disableSubmit();
      }
    };

    UI.getUsernameField().on("change keyup paste", validate);
    UI.getMessageField().on("change keyup paste", validate);
    UI.getForm().on("submit", event => {
      event.preventDefault();

      const username = $.trim(UI.getUsernameField().val());
      const message = $.trim(UI.getMessageField().val());

      UI.disableSubmit("Sending...");
      UI.addMessage("You", message);
      ChatApi.sendMessage(username, message);
      UI.getMessageField()
        .val("")
        .focus();
    });
  }
};

$(document).ready(() => {
  UI.init();
  ChatApi.init();
  ChatApi.subscribe((error, data) => {
    if (error) {
      UI.addMessage(error.username, error.message, "error");
    } else {
      UI.addMessage(data.username, data.message);
    }
  });
});
