async function generatePatientCase() {
    window.location.href = '/chat';
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
  
    const result = `
        <strong>Situation:</strong> ${data.Situation}<br>
        <strong>Background:</strong> ${data.Background}<br>
        <strong>Assessment:</strong> ${data.Assessment}<br>
        <strong>Recommendation:</strong> ${data.Recommendation}
    `;
    console.log("case generated")
  
  // Store the generated case in local storage
    localStorage.setItem('generatedCase', result.case);
}

document.getElementById('generate-btn').addEventListener('click', generatePatientCase);
