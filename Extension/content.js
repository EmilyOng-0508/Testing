if (!document.getElementById('sa-widget')) {
  const widget = document.createElement('div');
  widget.id = 'sa-widget';
  widget.style.cssText = 'position:fixed;top:100px;right:30px;width:160px;background:#1E1E1E;border:2px solid #6A1B9A;border-radius:10px;z-index:999999;box-shadow:0 8px 24px rgba(0,0,0,0.6);font-family:Arial;text-align:center;overflow:hidden;';

  widget.innerHTML = `
    <div id="sa-header" style="background:#6A1B9A;color:white;padding:8px;cursor:grab;font-weight:bold;user-select:none;display:flex;justify-content:space-between;">
      <span>🧠 Capture</span><span id="sa-close" style="cursor:pointer;font-size:18px;">&times;</span>
    </div>
    <div style="padding:15px;">
      <button id="sa-q" style="width:100%;padding:10px;margin-bottom:10px;background:#6A1B9A;color:white;border:none;border-radius:6px;cursor:pointer;">📝 Question</button>
      <button id="sa-s" style="width:100%;padding:10px;background:#2196F3;color:white;border:none;border-radius:6px;cursor:pointer;">💡 Solution</button>
    </div>
  `;
  document.body.appendChild(widget);

  const header = document.getElementById('sa-header');
  let isDragging = false, offsetX, offsetY;

  header.onmousedown = (e) => {
    isDragging = true;
    offsetX = e.clientX - widget.getBoundingClientRect().left;
    offsetY = e.clientY - widget.getBoundingClientRect().top;
    header.style.cursor = 'grabbing';
  };
  document.onmousemove = (e) => {
    if (!isDragging) return;
    widget.style.right = 'auto';
    widget.style.left = (e.clientX - offsetX) + 'px';
    widget.style.top = (e.clientY - offsetY) + 'px';
  };
  document.onmouseup = () => { isDragging = false; header.style.cursor = 'grab'; };

  document.getElementById('sa-close').onclick = () => widget.remove();

  const capture = (type) => {
    widget.style.display = 'none';
    chrome.runtime.sendMessage({ action: "capture", type: type }, (res) => {
      widget.style.display = 'block';
      if(chrome.runtime.lastError) { alert('❌ Error. Refresh page!'); return; }
      alert(res && res.success ? '✅ Sent! Check dashboard.' : '❌ API not running?');
    });
  };

  document.getElementById('sa-q').onclick = () => capture('question');
  document.getElementById('sa-s').onclick = () => capture('solution');
}