document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const resultBox = document.getElementById('resultBox');
    const predictionName = document.getElementById('predictionName');
    const predictionClass = document.getElementById('predictionClass');
    const tbody = document.querySelector('#historyTable tbody');
    const btn = document.getElementById('predictBtn');

    // Chart.js Setup
    const ctx = document.getElementById('predictionChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['setosa', 'versicolor', 'virginica'],
            datasets: [{
                label: 'Prediction Count',
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.5)',
                    'rgba(139, 92, 246, 0.5)',
                    'rgba(34, 197, 94, 0.5)'
                ],
                borderColor: [
                    '#3b82f6',
                    '#8b5cf6',
                    '#22c55e'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#94a3b8',
                        stepSize: 1
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#f8fafc' }
                }
            }
        }
    });

    let counter = 1;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Loading state
        btn.textContent = "Loading...";
        btn.disabled = true;

        const features = [
            parseFloat(document.getElementById('sepalLength').value),
            parseFloat(document.getElementById('sepalWidth').value),
            parseFloat(document.getElementById('petalLength').value),
            parseFloat(document.getElementById('petalWidth').value)
        ];
        
        const apiKey = document.getElementById('apiKey').value;

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': apiKey
                },
                body: JSON.stringify({ features })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Prediction failed');
            }

            const data = await response.json();
            
            // Show result
            predictionName.textContent = data.prediction_name;
            predictionClass.textContent = data.prediction;
            resultBox.classList.remove('hidden');

            // Update Chart dynamically
            chart.data.datasets[0].data[data.prediction]++;
            chart.update();

            // Add to table
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${counter++}</td>
                <td>[${features.join(', ')}]</td>
                <td>${data.prediction_name}</td>
                <td>${new Date().toLocaleTimeString()}</td>
            `;
            tbody.prepend(tr);

        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            btn.textContent = "Make Prediction";
            btn.disabled = false;
        }
    });
});
