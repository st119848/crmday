function setActive(el) {
    // Remove active class from all items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    // Add active class to clicked item
    el.classList.add('active');
    
    // Update title and path
    document.getElementById('current-page-title').textContent = el.textContent;
    document.getElementById('page-path').textContent = el.getAttribute('href');
}

function setView(mode) {
    const wrapper = document.getElementById('iframe-wrapper');
    const btns = document.querySelectorAll('.control-btn');
    
    // Remove previous mode classes
    wrapper.classList.remove('mobile', 'tablet');
    btns.forEach(b => b.classList.remove('active'));

    if (mode === 'mobile') {
        wrapper.classList.add('mobile');
        document.getElementById('btn-mobile').classList.add('active');
    } else if (mode === 'tablet') {
        wrapper.classList.add('tablet');
        document.getElementById('btn-tablet').classList.add('active');
    } else {
        document.getElementById('btn-desktop').classList.add('active');
    }
}

function openExternal() {
    const iframe = document.querySelector('iframe');
    window.open(iframe.src, '_blank');
}

// Font injection for iframe content
function injectFonts(iframe) {
    try {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        if (!doc) return;

        // 1. Add Google Font link to iframe head
        const link = doc.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600;700&family=Sarabun:wght@300;400;500;600&display=swap';
        doc.head.appendChild(link);

        // 2. Add Style overrides to iframe head
        const style = doc.createElement('style');
        style.textContent = `
            /* Apply Sarabun to body and normal text */
            body, p, span, a, li, input, button, .font-sans { 
                font-family: 'Sarabun', sans-serif !important; 
            }
            /* Apply Prompt to all headings and display text */
            h1, h2, h3, h4, h5, h6, .font-display, [class*="font-bold"], .text-lg, .text-xl, .text-2xl { 
                font-family: 'Prompt', sans-serif !important; 
            }
        `;
        doc.head.appendChild(style);

        // 3. Update Tailwind if available in the iframe context
        if (iframe.contentWindow.tailwind) {
            iframe.contentWindow.tailwind.config.theme.extend.fontFamily = {
                display: ['Prompt', 'sans-serif'],
                sans: ['Sarabun', 'sans-serif']
            };
        }
    } catch (e) {
        console.warn("Cross-origin or initialization error injecting fonts:", e);
    }
}
