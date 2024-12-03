// dashboard.js
let currentDate = new Date();

// Initialize charts when the page loads
document.addEventListener('DOMContentLoaded', () => {
    
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    initMoodChart();
    initTrendChart();
    updateCalendar();
    loadStats();
});

function initMoodChart() {
    const ctx = document.getElementById('moodChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May'],
            datasets: [{
                label: 'Happy',
                data: [12, 19, 15, 17, 14],
                backgroundColor: '#FFD700'
            }, {
                label: 'Sad',
                data: [5, 7, 4, 3, 6],
                backgroundColor: '#4169E1'
            }, {
                label: 'Anxious',
                data: [8, 6, 9, 7, 5],
                backgroundColor: '#FF69B4'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function initTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Anxiety Level',
                data: [65, 59, 55, 47],
                borderColor: '#FF69B4',
                tension: 0.4
            }, {
                label: 'Depression Level',
                data: [45, 40, 35, 30],
                borderColor: '#4169E1',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

async function updateCalendar() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    
    const month = currentDate.getMonth() + 1;
    const year = currentDate.getFullYear();
    
    try {
        const response = await fetch(`/api/moods/${month}/${year}`);
        const data = await response.json();
        console.log('Mood data received:', data);  // Debug log
        
        document.getElementById('currentMonth').textContent = 
            `${monthNames[currentDate.getMonth()]} ${year}`;
        
        const grid = document.getElementById('calendarGrid');
        grid.innerHTML = '';
        
        // Add day labels
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        days.forEach(day => {
            const dayLabel = document.createElement('div');
            dayLabel.className = 'calendar-day day-label';
            dayLabel.textContent = day;
            grid.appendChild(dayLabel);
        });
        
        // Get first day of month
        const firstDay = new Date(year, currentDate.getMonth(), 1);
        
        // Add empty cells for days before the first day
        for (let i = 0; i < firstDay.getDay(); i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'calendar-day empty';
            grid.appendChild(emptyCell);
        }
        
        // Add days of the month
        const lastDay = new Date(year, currentDate.getMonth() + 1, 0).getDate();
        for (let day = 1; day <= lastDay; day++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'calendar-day';
            
            const dateString = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const dayMood = data.moods.find(m => m.date === dateString);
            
            if (dayMood) {
                const moodClass = dayMood.mood.toLowerCase().replace(' ', '-').replace('😊', 'happy')
                    .replace('😔', 'sad').replace('😠', 'angry')
                    .replace('😰', 'anxious').replace('😐', 'neutral');
                dayCell.classList.add(`mood-${moodClass}`);
                dayCell.innerHTML = `${day}<span class="mood-emoji">${dayMood.mood.split(' ')[0]}</span>`;
            } else {
                dayCell.textContent = day;
            }
            
            grid.appendChild(dayCell);
        }
    } catch (error) {
        console.error('Error updating calendar:', error);
    }
}

function previousMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
}

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        document.getElementById('breathingCount').textContent = data.breathing_exercises || 0;
        document.getElementById('journalCount').textContent = data.journal_entries || 0;
        document.getElementById('moodCheckCount').textContent = data.mood_checks || 0;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}
