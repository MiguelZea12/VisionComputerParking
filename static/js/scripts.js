const ctx = document.getElementById('occupancyChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: Array.from({ length: 10 }, (_, i) => `Min ${i + 1}`),
        datasets: [{
            label: 'Espacios Ocupados',
            data: Array(10).fill(0),
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 12
            }
        }
    }
});

const pieCtx = document.getElementById('occupancyPieChart').getContext('2d');
const pieChart = new Chart(pieCtx, {
    type: 'doughnut',
    data: {
        labels: ['Ocupados', 'Libres'],
        datasets: [{
            data: [0, 12],
            backgroundColor: ['rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)'],
            borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

async function fetchSpaceStatus() {
    try {
        const response = await fetch('/spaces_status');
        if (!response.ok) throw new Error('Error en la respuesta del servidor');
        const data = await response.json();
        document.getElementById('occupied').textContent = data.occupied;
        document.getElementById('free').textContent = data.free;

        pieChart.data.datasets[0].data = [data.occupied, data.free];
        pieChart.update();
    } catch (error) {
        console.error('Error fetching space status:', error);
        document.getElementById('occupied').textContent = 'Error';
        document.getElementById('free').textContent = 'Error';
    }
}

async function updateChart() {
    try {
        const response = await fetch('/historical_data');
        if (!response.ok) throw new Error('Error en la respuesta del servidor');
        const data = await response.json();
        chart.data.datasets[0].data = data.historical;
        chart.update();
    } catch (error) {
        console.error('Error updating chart:', error);
    }
}


async function controlVideo(action) {
    try {
        await fetch('/control_video', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
        });
    } catch (error) {
        console.error('Error controlling video:', error);
    }
}

setInterval(fetchSpaceStatus, 1000);
setInterval(updateChart, 1000);
