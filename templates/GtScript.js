// Selecting the DOM elements
const captchaTextBox = document.querySelector(".captch_box input");
const refreshButton = document.querySelector(".refresh_button");
const captchaInputBox = document.querySelector(".captch_input input");
const message = document.querySelector(".message");
const submitButton = document.querySelector(".button");

// Variable to store generated captcha
let captchaText = null;

// Function to generate captcha
const generateCaptcha = () => {
  const randomString = Math.random().toString(36).substring(2, 7);
  const randomStringArray = randomString.split("");
  const changeString = randomStringArray.map((char) =>
    Math.random() > 0.5 ? char.toUpperCase() : char
  );
  captchaText = changeString.join("  ");
  captchaTextBox.value = captchaText;
  console.log(captchaText);
};

const refreshBtnClick = () => {
  generateCaptcha();
  captchaInputBox.value = "";
  captchaKeyUpValidate();
};

const captchaKeyUpValidate = () => {
  submitButton.classList.toggle("disabled", !captchaInputBox.value);

  if (captchaInputBox.value === "") message.classList.remove("active");
};

const submitBtnClick = () => {
  const enteredCaptcha = captchaInputBox.value.replace(/\s/g, ""); // Remove spaces from entered captcha

  message.classList.add("active");

  // Check if the Entered Text is correct
  if (enteredCaptcha === captchaText.replace(/\s/g, "")) {
    // Remove spaces from generated captcha for comparison
    message.innerText = "Entered captcha is correct";
    message.style.color = "#826afb";
    window.location.href = "index.html"
  } else {
    message.innerText = "Entered captcha is not correct";
    message.style.color = "#FF2525";
  }
};

//Add event listeners for the refresh button, captchaInputBox, submitButton
refreshButton.addEventListener("click", refreshBtnClick);
captchaInputBox.addEventListener("keyup", captchaKeyUpValidate);
submitButton.addEventListener("click", submitBtnClick);
// Generate a captcha when loading the page
generateCaptcha();
