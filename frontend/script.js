const API_BASE = "http://127.0.0.1:8000"; // Backend FastAPI base URL

const uploadArea = document.getElementById("uploadArea");
const imageInput = document.getElementById("imageInput");
const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");
const removeImage = document.getElementById("removeImage");
const classifyBtn = document.getElementById("classifyBtn");
const resultContainer = document.getElementById("resultsContainer");
const resultTitle = document.getElementById("resultTitle");
const tipsList = document.getElementById("tipsList");

// Click upload area to open file dialog
uploadArea.addEventListener("click", () => imageInput.click());

// When file selected
imageInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewContainer.style.display = "block";
        classifyBtn.style.display = "inline-block";
    };
    reader.readAsDataURL(file);
});

// Remove image
removeImage.addEventListener("click", () => {
    imageInput.value = "";
    previewContainer.style.display = "none";
    classifyBtn.style.display = "none";
    resultContainer.style.display = "none";
});

// Classify button click
classifyBtn.addEventListener("click", async () => {
    const file = imageInput.files[0];
    if (!file) return alert("Please select an image first!");

    const btnText = classifyBtn.querySelector(".btn-text");
    const btnLoader = classifyBtn.querySelector(".btn-loader");
    btnText.style.display = "none";
    btnLoader.style.display = "inline";

    try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch(`${API_BASE}/predict/`, {
            method: "POST",
            body: formData,
        });

        const data = await res.json();
        resultContainer.style.display = "block";

        if (data.error) {
            resultTitle.textContent = "❌ " + data.error;
            tipsList.innerHTML = "";
        } else {
            resultTitle.textContent = `🧩 Predicted: ${data.waste_type} (${data.confidence.toFixed(2)}%)`;
            tipsList.innerHTML = `
                <ul>
                    <li>Dispose ${data.waste_type.toLowerCase()} only in certified e-waste centers.</li>
                    <li>Do not mix with regular household waste.</li>
                    <li>Ensure recycling to recover useful materials ♻️</li>
                </ul>
            `;
        }
    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        btnText.style.display = "inline";
        btnLoader.style.display = "none";
    }
});

const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const chatMessages = document.getElementById("chatMessages");

function appendMessage(sender, htmlContent) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender === "user" ? "user-message" : "bot-message");

    const inner = document.createElement("div");
    inner.classList.add("message-content");
    inner.innerHTML = htmlContent;

    msg.appendChild(inner);
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function typeMessage(element, htmlText, delay = 20) {
  element.innerHTML = ""; 
  const parts = htmlText.split(/<br\s*\/?>/i);
  for (let i = 0; i < parts.length; i++) {
    const text = parts[i];
    for (const char of text) {
      element.innerHTML += char;
      chatMessages.scrollTop = chatMessages.scrollHeight;
      await new Promise((r) => setTimeout(r, delay));
    }
    if (i < parts.length - 1) {
      element.innerHTML += "<br>";
    }
  }
}


async function sendChat() {
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    chatInput.value = "";
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("message", "bot-message");
    typingDiv.innerHTML = `<div class="message-content">EcoSort is typing<span class="dots">...</span></div>`;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const res = await fetch(`${API_BASE}/chat/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await res.json();
        chatMessages.removeChild(typingDiv);

        let reply = data.reply || data.error || "⚠️ No response";
        reply = reply
            .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>") 
            .replace(/\n/g, "<br>"); 

        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", "bot-message");

        const contentDiv = document.createElement("div");
        contentDiv.classList.add("message-content");

        msgDiv.appendChild(contentDiv);
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        await typeMessage(contentDiv, reply, 15);
    } catch (err) {
        chatMessages.removeChild(typingDiv);
        appendMessage("bot", `Error: ${err.message}`);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendBtn.addEventListener("click", sendChat);
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendChat();
});
