async function generatePatientCase() {
    const response = await fetch('http://127.0.0.1:5500/generate-case', {  
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const errorMessage = await response.text();
        console.error('Error:', errorMessage);
        return;
    }

    const data = await response.json();
    document.getElementById('case-output').textContent = data.case;
}

document.getElementById('generate-btn').addEventListener('click', generatePatientCase);
