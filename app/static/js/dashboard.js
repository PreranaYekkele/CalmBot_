// dashboard.js
let currentDate = new Date();
let calendarData = [];

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
            labels: ['October','November'],
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
        options: chartOptions
    });
}

function renderCalendarDay(dayData) {
    const dayCell = document.createElement('div');
    dayCell.className = 'calendar-day';
    
    if (dayData.mood) {
        dayCell.innerHTML += `<span class="mood-indicator">${dayData.mood}</span>`;
    }
    if (dayData.gratitude) {
        dayCell.innerHTML += '<i class="fas fa-journal-whills gratitude-icon"></i>';
    }
    if (dayData.breathingExercise) {
        dayCell.innerHTML += '<i class="fas fa-lungs breathing-icon"></i>';
    }
    
    dayCell.addEventListener('click', () => showDayDetails(dayData));
    return dayCell;
}


function getActivityIcon(activity) {
    const icons = {
        'breathing': 'fa-lungs',
        'gratitude': 'fa-journal-whills',
        'mood': 'fa-chart-line'
    };
    return icons[activity] || 'fa-check';
}

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                boxWidth: 10,
                padding: 5,
                font: { size: 10 }
            }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                font: { size: 9 }
            }
        },
        x: {
            ticks: {
                font: { size: 9 }
            }
        }
    }
};

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
        options: chartOptions
    });
}

async function updateCalendar() {
    const month = currentDate.getMonth() + 1;
    const year = currentDate.getFullYear();
    
    try {
        const response = await fetch(`/api/calendar/${month}/${year}`);
        const data = await response.json();
        calendarData = data.entries.reduce((acc, entry) => {
            acc[entry.date] = entry;
            return acc;
        }, {});
        
        renderCalendar();
    } catch (error) {
        console.error('Error fetching calendar data:', error);
    }
}

function renderCalendar() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    
    document.getElementById('currentMonth').textContent = 
        `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
    
    const grid = document.getElementById('calendarGrid');
    grid.innerHTML = '';
    
    // Add day headers
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    days.forEach(day => {
        const dayLabel = document.createElement('div');
        dayLabel.className = 'calendar-day day-label';
        dayLabel.textContent = day;
        grid.appendChild(dayLabel);
    });
    
    // Add empty cells for days before start of month
    const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    for (let i = 0; i < firstDay.getDay(); i++) {
        grid.appendChild(createEmptyCell());
    }
    
    // Add month days
    const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    for (let day = 1; day <= lastDay.getDate(); day++) {
        grid.appendChild(createDayCell(day));
    }
}

function createEmptyCell() {
    const cell = document.createElement('div');
    cell.className = 'calendar-day empty';
    return cell;
}

function createDayCell(day) {
    const cell = document.createElement('div');
    cell.className = 'calendar-day';
    
    const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const dayData = calendarData[dateStr];
    
    cell.textContent = day;
    
    if (dayData) {
        cell.classList.add('has-entry');
        cell.onclick = () => showDayDetails(dateStr, dayData);
    }
    
    return cell;
}

function previousMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
}

function showDayDetails(date, data) {
    document.getElementById('detailsDate').textContent = new Date(date).toLocaleDateString();
    
    const moodDiv = document.getElementById('dayMood');
    const gratitudeDiv = document.getElementById('dayGratitude');
    const activitiesDiv = document.getElementById('dayActivities');
    
    moodDiv.textContent = data.mood || 'No record';
    gratitudeDiv.textContent = data.gratitude || 'No gratitude entry';
    
    // activitiesDiv.innerHTML = data.activities.length ? 
    //     data.activities.map(activity => 
    //         `<p><i class="fas ${getActivityIcon(activity)}"></i>${activity}</p>`
    //     ).join('') : 
        // '<p>No activities recorded</p>';
    
    showModal('dayDetailsModal');
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'block';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

function logout() {
    window.location.href = '/logout';
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

document.addEventListener('DOMContentLoaded', () => {
            updateCalendar();
});

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        closeModal(event.target.id);
    }
};