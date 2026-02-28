// ================= LOGIN PAGE TOGGLE =================
function toggleMode() {
    const title = document.getElementById("form-title");
    const actionInput = document.getElementById("actionInput");
    const toggleText = document.getElementById("toggleText");

    if (actionInput.value === "login") {
        actionInput.value = "register";
        title.innerText = "Register";
        toggleText.innerHTML = 'Already have an account? <span onclick="toggleMode()">Login</span>';
    } else {
        actionInput.value = "login";
        title.innerText = "Login";
        toggleText.innerHTML = 'Don’t have an account? <span onclick="toggleMode()">Register</span>';
    }
}

// ================= SHOW / HIDE PASSWORD =================
function togglePassword() {
    const passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

// ================= FILE NAME DISPLAY =================
function showFileName(input) {
    const fileName = document.getElementById("fileName");
    if (input.files.length > 0) {
        fileName.innerText = "Selected File: " + input.files[0].name;
    }
}

// ================= LOADING EFFECT =================
function showLoading() {
    const button = document.getElementById("analyzeBtn");
    button.innerText = "Analyzing...";
    button.disabled = true;
}