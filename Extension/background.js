// 1. Listen for the Extension icon click event in the browser toolbar
chrome.action.onClicked.addListener((tab) => {
  // When the icon is clicked, inject the floating widget UI code (content.js) into the current page
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content.js']
  });
});

// 2. Receive the "capture" command from the floating widget in the webpage
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "capture") {
    
    // Delay for 150ms to ensure the floating widget is hidden before taking the screenshot
    setTimeout(() => {
      chrome.tabs.captureVisibleTab(null, { format: 'png' }, function(dataUrl) {
        
        // Define the backend API endpoint
        const EMILY_API_URL = 'https://snap-tutor.onrender.com/diagnose';
        
        // Send the captured image data to your Python API service
        fetch(EMILY_API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: dataUrl, type: request.type })
        })
        .then(response => response.json())
        .then(data => {
          // Send the diagnosis result back to the floating widget upon success
          sendResponse({ success: true, diagnosis: data });
        })
        .catch(error => {
          console.error('API Error:', error);
          sendResponse({ success: false });
        });
        
      });
    }, 150);
    
    // Return true to indicate that the response will be sent asynchronously
    return true; 
  }
});