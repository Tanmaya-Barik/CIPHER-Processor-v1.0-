    async function processText(action) {
        const text = document.getElementById('textInput').value;
        const key = document.getElementById('keyInput').value;
        const outputEl = document.getElementById('outputText');

        if (!text || !key) {
            outputEl.innerHTML = '<span class="error">ERR: Missing data/key.</span>';
            return;
        }

        outputEl.style.color = '#fff'; 
        outputEl.innerHTML = '>> PROCESSING_STATUS: ACTIVE...';

        try {
            const response = await fetch('/api/cipher', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action, text: text, key: key })
            });

            const data = await response.json();

            if (response.ok) {
                outputEl.style.color = '#fff';
                setTimeout(() => outputEl.style.color = '#ccf', 150);
                outputEl.innerHTML = `>> PROCESS_COMPLETE: <br/><br/>${data.result}`;
            } else {
                outputEl.innerHTML = `<span class="error">ERR: ${data.error}</span>`;
            }
        } catch (error) {
            outputEl.innerHTML = '<span class="error">ERR: SYS//CRITICAL - No server connection.</span>';
        }
    }