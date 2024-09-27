async function generatePatientCase() {

    const response = await fetch('http://localhost:5500/generate-case', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    document.getElementById('case-output').textContent = data.case;
}

document.getElementById('generate-btn').addEventListener('click', generatePatientCase);
