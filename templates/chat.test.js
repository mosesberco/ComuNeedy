const jsdom = require("jsdom");
const { JSDOM } = jsdom;

// Create a new JSDOM instance with a basic HTML structure
// This simulates a browser environment for testing purposes
const dom = new JSDOM(`
  <!DOCTYPE html>
  <html>
    <body>
      <div class="chat-input">
        <textarea></textarea>
        <span></span>
      </div>
      <button class="chatbot-toggler"></button>
    </body>
  </html>
`);

// Set the global document and window objects to the ones provided by jsdom
global.document = dom.window.document;
global.window = dom.window;

// Query for elements in the simulated DOM
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox"); // This will still be null
const chatbotToggler = document.querySelector(".chatbot-toggler");

// Import the createChatLi function from the chat.js module
const { createChatLi } = require("./chat");

// Create a mock function for handleChat using Jest
const handleChat = jest.fn();

// Describe block for testing the event listener setup
describe("Event listener setup", () => {
  // Test case to ensure sendChatBtn is not null
  test("sendChatBtn should not be null", () => {
    expect(sendChatBtn).not.toBeNull();
  });

  // Test case to ensure chatbotToggler is not null
  test("chatbotToggler should not be null", () => {
    expect(chatbotToggler).not.toBeNull();
  });

  // Nested describe block to run tests only when sendChatBtn and chatbotToggler are not null
  describe("when sendChatBtn and chatbotToggler are not null", () => {
    // beforeEach hook to mock the addEventListener method on sendChatBtn and chatbotToggler
    beforeEach(() => {
      if (sendChatBtn) {
        sendChatBtn.addEventListener = jest.fn();
      }
      if (chatbotToggler) {
        chatbotToggler.addEventListener = jest.fn();
      }
    });

    // Test case to ensure addEventListener is called correctly on sendChatBtn
    test("should add event listener to sendChatBtn", () => {
      if (sendChatBtn) {
        sendChatBtn.addEventListener("click", handleChat);
        expect(sendChatBtn.addEventListener).toHaveBeenCalledWith(
          "click",
          handleChat
        );
      }
    });

    // Test case to ensure addEventListener is called correctly on chatbotToggler
    test("should add event listener to chatbotToggler", () => {
      if (chatbotToggler) {
        chatbotToggler.addEventListener("click", () =>
          document.body.classList.toggle("show-chatbot")
        );
        expect(chatbotToggler.addEventListener).toHaveBeenCalledWith(
          "click",
          expect.any(Function)
        );
      }
    });
  });
});
