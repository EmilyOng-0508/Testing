// 1. 监听浏览器右上角的 Extension 图标点击事件
chrome.action.onClicked.addListener((tab) => {
  // 当你点击图标时，把悬浮窗的 UI 代码 (content.js) 强行打入当前网页
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content.js']
  });
});

// 2. 接收来自网页悬浮窗的“截图”指令
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "capture") {
    
    // 稍微延迟 150 毫秒，这是为了等悬浮窗先隐藏起来，免得把自己也截进去了！
    setTimeout(() => {
      chrome.tabs.captureVisibleTab(null, { format: 'png' }, function(dataUrl) {
        
        // 在 background.js 中
        const EMILY_API_URL = 'https://testing2-d9g4.onrender.com/diagnose'; // 确保加上路由后缀
        // 截图完成，直接发送给你的 Python API 服务员
        fetch(EMILY_API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: dataUrl, type: request.type })
        })
        .then(response => response.json())
        .then(data => {
          // 发送成功后，回复悬浮窗
          sendResponse({ success: true, diagnosis: data });
        })
        .catch(error => {
          console.error('API Error:', error);
          sendResponse({ success: false });
        });
        
      });
    }, 150);
    
    return true; // 告诉 Chrome 这个任务是异步的，请等我处理完再关闭通道
  }
});