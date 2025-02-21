document.getElementById("uploadForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const messageBox = document.getElementById("message");
  const fileInput = document.getElementById("fileInput");
  const uploadButton = this.querySelector("button");
  const progressBar = document.getElementById("uploadProgress");
  const progressSection = document.querySelector(".progress-section");
  const downloadButton = document.getElementById("downloadButton");

  // Clear previous messages
  messageBox.textContent = "";
  messageBox.classList.remove("warning");

  // Check if file is selected
  if (!fileInput.files.length) {
    messageBox.textContent = "⚠️ Please select a file before uploading!";
    messageBox.classList.add("warning");
    return;
  }

  // Create FormData
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  // Update button state
  uploadButton.textContent = "Uploading...";
  uploadButton.disabled = true;

  // Show & reset progress bar
  progressSection.classList.remove("hidden");
  progressBar.value = 0;

  // Setup XMLHttpRequest
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/upload");

  // Track progress
  xhr.upload.addEventListener("progress", function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      progressBar.value = percentComplete;
    }
  });

  // Listen for successful load
  xhr.addEventListener("load", function () {
    if (xhr.status >= 200 && xhr.status < 300) {
      const data = JSON.parse(xhr.responseText);
      messageBox.textContent = data.message || "Upload successful!";

      // If there's a download link, show the Download button
      if (data.download_link) {
        downloadButton.dataset.downloadLink = data.download_link;
        downloadButton.classList.remove("hidden");
      }

      // Reset button
      uploadButton.disabled = false;
      uploadButton.textContent = "Build Links";

      // Hide progress bar & reset
      progressSection.classList.add("hidden");
      progressBar.value = 0;

      // Trigger optional animation
      triggerAnimation();
    } else {
      messageBox.textContent = "❌ Upload failed. Please try again.";
      resetUploadUI();
    }
  });

  // Listen for errors (e.g. network issues)
  xhr.addEventListener("error", function () {
    messageBox.textContent = "❌ Upload failed. Please try again.";
    resetUploadUI();
  });

  // Send file
  xhr.send(formData);

  // Helper to reset button & progress bar
  function resetUploadUI() {
    uploadButton.disabled = false;
    uploadButton.textContent = "Build Links";
    progressSection.classList.add("hidden");
    progressBar.value = 0;
  }
});

// Handle the Download button
document.getElementById("downloadButton").addEventListener("click", function () {
  const downloadUrl = this.dataset.downloadLink;
  if (downloadUrl) {
    const tempLink = document.createElement("a");
    tempLink.href = downloadUrl;
    tempLink.download = "";
    document.body.appendChild(tempLink);
    tempLink.click();
    document.body.removeChild(tempLink);
  }
});

// ✨ Optional Fun Animation on Upload
function triggerAnimation() {
  const animationBox = document.getElementById("animation-box");
  animationBox.textContent = "🎇 Processing...";

  setTimeout(() => {
    const successBtn = document.createElement("button");
    successBtn.textContent = "✅ Done!";
    successBtn.classList.add("success-button");

    animationBox.innerHTML = "";
    animationBox.appendChild(successBtn);
  }, 2000);
}
