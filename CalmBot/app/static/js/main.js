let sessionId = Math.random().toString(36).substring(7);
let breathingInterval;

let messageCount = 0;

const specialistsData = {
    'dr-mittal': {
        name: 'Dr. Samir Parikh',
        phone: '+91 98765 43210',
        title: 'Director of Mental Health and Behavioral Sciences',
        location: 'New Delhi',
        specialties: 'Child & Adolescent Psychiatry, Mood Disorders',
        languages: 'English, Hindi',
        experience: '25+ years'
    },
    'dr-shetty': {
        name: 'Dr. Shyam Bhat',
        phone: '+91 98765 43211',
        title: 'Psychiatrist & Integrative Medicine Specialist',
        location: 'Bangalore',
        specialties: 'Depression, Anxiety, Mind-Body Medicine',
        languages: 'English, Kannada, Hindi',
        experience: '20+ years'
    },
    'dr-bhonsle': {
        name: 'Dr. Anjali Chhabria',
        phone: '+91 98765 43212',
        title: 'Clinical Psychiatrist & Relationship Expert',
        location: 'Mumbai',
        specialties: 'Relationship Counseling, Addiction',
        languages: 'English, Hindi, Marathi',
        experience: '30+ years'
    },
    'dr-kumar': {
        name: 'Dr. Alok Sarin',
        phone: '+91 98765 43213',
        title: 'Senior Consultant Psychiatrist',
        location: 'New Delhi',
        specialties: 'Geriatric Psychiatry, Community Mental Health',
        languages: 'English, Hindi, Bengali',
        experience: '35+ years'
    }
};

function addMessage(content, isUser = false) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : ''}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;

    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    if (!isUser) {
        messageCount++;
        if (messageCount === 4) {
            setTimeout(() => {
                showModal('specialistModal');
            }, 1000);
        }
    }
}

function showSpecialistDetails(specialistId) {
    const specialist = specialistsData[specialistId];
    const detailsContent = document.getElementById('specialistDetailsContent');
    
    detailsContent.innerHTML = `
        <div class="specialist-details">
            <img src="https://ui-avatars.com/api/?name=${specialist.name.replace(' ', '+')}&size=80" 
                 alt="${specialist.name}">
            <h2>${specialist.name}</h2>
            <div class="contact-number">
                <i class="fas fa-phone"></i> ${specialist.phone}
            </div>
            
            <div class="info-group">
                <h3>Designation</h3>
                <p>${specialist.title}</p>
            </div>
            
            <div class="info-group">
                <h3>Location</h3>
                <p><i class="fas fa-map-marker-alt"></i> ${specialist.location}</p>
            </div>
            
            <div class="info-group">
                <h3>Experience</h3>
                <p><i class="fas fa-user-clock"></i> ${specialist.experience}</p>
            </div>
            
            <div class="info-group">
                <h3>Specialties</h3>
                <p><i class="fas fa-star"></i> ${specialist.specialties}</p>
            </div>
            
            <div class="info-group">
                <h3>Languages</h3>
                <p><i class="fas fa-globe"></i> ${specialist.languages}</p>
            </div>

            <button class="book-button" onclick="bookAppointment('${specialistId}')">
                Book Appointment
            </button>
        </div>
    `;
    
    closeModal('specialistModal');
    showModal('specialistDetailsModal');
}

function bookAppointment(specialistId) {
    const specialist = specialistsData[specialistId];
    closeModal('specialistDetailsModal');
    addMessage(`Great choice! I'll help you schedule an appointment with ${specialist.name}. You can reach them directly at ${specialist.phone}.`);
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, true);
        input.value = '';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message, session_id: sessionId })
            });
            
            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            addMessage("I apologize, but I'm having trouble responding right now.");
        }
    }
}



function openBreathingExercise() {
    showModal('breathingModal');
    const circle = document.querySelector('.breathing-circle');
    const text = document.querySelector('.breathing-text');
    
    let phase = 'inhale';
    breathingInterval = setInterval(() => {
        if (phase === 'inhale') {
            circle.style.transform = 'scale(1.5)';
            text.textContent = 'Breathe in...';
            phase = 'hold';
            setTimeout(() => {
                if (phase === 'hold') {
                    text.textContent = 'Hold...';
                    phase = 'exhale';
                }
            }, 2000);
        } else {
            circle.style.transform = 'scale(1)';
            text.textContent = 'Breathe out...';
            phase = 'inhale';
        }
    }, 6000);
}

async function openBreathingExercise() {
    showModal('breathingModal');
    const circle = document.querySelector('.breathing-circle');
    const text = document.querySelector('.breathing-text');
    
    let phase = 'inhale';
    breathingInterval = setInterval(() => {
        if (phase === 'inhale') {
            circle.style.transform = 'scale(1.5)';
            text.textContent = 'Breathe in...';
            phase = 'hold';
            setTimeout(() => {
                if (phase === 'hold') {
                    text.textContent = 'Hold...';
                    phase = 'exhale';
                }
            }, 2000);
        } else {
            circle.style.transform = 'scale(1)';
            text.textContent = 'Breathe out...';
            phase = 'inhale';
        }
    }, 6000);

    try {
        await fetch('/api/activities/breathing', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ session_id: sessionId })
        });
    } catch (error) {
        console.error('Error tracking breathing exercise:', error);
    }
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'block';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modalId === 'breathingModal' && breathingInterval) {
        clearInterval(breathingInterval);
    }
    modal.style.display = 'none';
}

function openGratitudeJournal() {
    showModal('gratitudeModal');
}

async function saveGratitudeEntry() {
    const textarea = document.querySelector('.gratitude-textarea');
    const entry = textarea.value.trim();
    
    if (entry) {
        try {
            await fetch('/api/activities/gratitude', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ entry, session_id: sessionId })
            });
            closeModal('gratitudeModal');
            addMessage("Thank you for sharing your gratitude. It's wonderful to focus on the positive things in life!");
            textarea.value = '';
        } catch (error) {
            addMessage("I'm having trouble saving your entry. Please try again.");
        }
    }
}

function openMoodTracker() {
    showModal('moodModal');
}

async function trackMood(mood) {
    try {
        await fetch('/api/activities/mood', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ mood, session_id: sessionId })
        });
        closeModal('moodModal');
        addMessage(`Thank you for sharing that you're feeling ${mood}. How can I support you?`);
    } catch (error) {
        addMessage("I'm having trouble tracking your mood. Please try again.");
    }
}

function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

function clearChat() {
    const messagesDiv = document.getElementById('chatMessages');
    messagesDiv.innerHTML = '';
    addMessage("Hi! I'm CalmBot, your mental health companion. How are you feeling today?");
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    addMessage("Hi! I'm CalmBot, your mental health companion. How are you feeling today?");
    
    document.getElementById('messageInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            closeModal(event.target.id);
        }
    };
});
