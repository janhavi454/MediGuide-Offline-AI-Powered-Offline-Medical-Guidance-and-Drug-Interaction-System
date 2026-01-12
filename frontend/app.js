// API base URL
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const appElement = document.getElementById('app');

// Utility Functions
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Render Functions
function renderHomePage() {
    appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
        <div class="content">
            <h2>Welcome to MediGuide - Your Medical Assistant</h2>
            <p>Use this application to search for medicines, check drug interactions, and get answers to your medical questions.</p>

            <div class="guide-section">
                <h3>🚀 Quick Access</h3>
                <div class="quick-access-grid">
                    <div class="quick-access-card" onclick="renderMedicinesPage()">
                        <h4>💊 Search Medicines</h4>
                        <p>Find detailed information about medications</p>
                    </div>
                    <div class="quick-access-card" onclick="renderInteractionChecker()">
                        <h4>⚡ Check Interactions</h4>
                        <p>Verify drug compatibility and safety</p>
                    </div>
                    <div class="quick-access-card" onclick="renderAskMediGuide()">
                        <h4>💬 Ask MediGuide</h4>
                        <p>Get answers to medical questions instantly</p>
                    </div>
                    <div class="quick-access-card" onclick="renderMedicineScheduler()">
                        <h4>⏰ Medicine Scheduler</h4>
                        <p>Set reminders for your medications</p>
                    </div>
                    <div class="quick-access-card" onclick="renderEmergencyContacts()">
                        <h4>📞 Emergency Contacts</h4>
                        <p>Access important contact information quickly</p>
                    </div>
                </div>
            </div>
            
            <div class="guide-section">
                <h3>🌟 Solution-Focused Medical Assistant</h3>
                <div class="info-card">
                    <h4>Get Specific Medical Solutions</h4>
                    <p>MediGuide now provides:</p>
                    <ul>
                        <li><strong>Specific tablet recommendations</strong> for your symptoms</li>
                        <li><strong>Home care instructions</strong> and self-care guidance</li>
                        <li><strong>Emergency situation protocols</strong> and immediate actions</li>
                        <li><strong>When to seek medical attention</strong> guidance</li>
                    </ul>
                    <p>Try the "Ask MediGuide" tab for actionable medical solutions!</p>
                </div>
            </div>
            
            <div class="guide-section">
                <h3>⚠️ Important Notice</h3>
                <div class="safety-card">
                    <p><strong>This tool is for informational purposes only.</strong> Always consult with qualified healthcare professionals for medical advice and before making any changes to your medication regimen.</p>
                </div>
            </div>
        </div>
    `;
}

function renderMedicinesPage() {
    appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
        <div class="content">
            <h2>Medicines</h2>
            <div>
                <input type="text" id="searchInput" placeholder="Search medicines...">
                <button onclick="searchMedicines()">Search</button>
            </div>
            <div id="medicinesList"></div>
        </div>
    `;
}

function renderInteractionChecker() {
    appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
        <div class="content">
            <h2>Check Drug Interactions</h2>
            <div>
                <input type="text" id="medicineInput" placeholder="Enter medicine name">
                <button onclick="addMedicine()">Add Medicine</button>
            </div>
            <div id="selectedMedicines"></div>
            <button onclick="checkInteractions()">Check Interactions</button>
            <div id="interactionResults"></div>
        </div>
    `;
}

function renderMediGuide() {
    appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
        <div class="content">
            <h2>MediGuide - Your Medication Assistant</h2>
            
            <div class="guide-section">
                <h3>💊 How to Use This Application</h3>
                <div class="guide-card">
                    <h4>Search Medicines</h4>
                    <p>Use the Medicines tab to search for medications by name or generic name. You can view detailed information about each medicine.</p>
                </div>
                
                <div class="guide-card">
                    <h4>Check Interactions</h4>
                    <p>Use the Check Interactions tab to add multiple medications and check for potential drug interactions between them.</p>
                </div>
                
                <div class="guide-card">
                    <h4>Get Recommendations</h4>
                    <p>The system provides severity ratings and recommendations for any detected interactions to help you make informed decisions.</p>
                </div>
                
                <div class="guide-card">
                    <h4>Ask MediGuide</h4>
                    <p>Use the Ask MediGuide tab to get answers to your medical questions about medications, side effects, and general health concerns.</p>
                </div>
                
                <div class="guide-card">
                    <h4>Medicine Scheduler</h4>
                    <p>Use the Medicine Scheduler tab to set reminders for your medications and stay on track with your treatment.</p>
                </div>
            </div>
            
            <div class="guide-section">
                <h3>⚠️ Important Safety Information</h3>
                <div class="safety-card">
                    <h4>Always Consult Healthcare Professionals</h4>
                    <p>This tool is for informational purposes only. Always consult with qualified healthcare professionals before making any changes to your medication regimen.</p>
                </div>
                
                <div class="safety-card">
                    <h4>Emergency Situations</h4>
                    <p>If you experience severe side effects or adverse reactions, seek immediate medical attention.</p>
                </div>
                
                <div class="safety-card">
                    <h4>Medication Safety Tips</h4>
                    <ul>
                        <li>Always follow prescribed dosages</li>
                        <li>Keep an updated list of all medications you're taking</li>
                        <li>Inform all healthcare providers about all medications you use</li>
                        <li>Be aware of potential side effects</li>
                    </ul>
                </div>
            </div>
            
            <div class="guide-section">
                <h3>🔍 Understanding Drug Interactions</h3>
                <div class="info-card">
                    <h4>Types of Interactions</h4>
                    <p>Drug interactions can affect how your medications work and increase the risk of serious side effects.</p>
                </div>
                
                <div class="info-card">
                    <h4>Severity Levels</h4>
                    <ul>
                        <li><strong>High:</strong> Potentially dangerous interactions requiring immediate attention</li>
                        <li><strong>Moderate:</strong> Interactions that may require monitoring or dosage adjustments</li>
                        <li><strong>Low:</strong> Minor interactions with minimal clinical significance</li>
                    </ul>
                </div>
            </div>
            
            <div class="guide-section">
                <h3>📞 Need More Help?</h3>
                <div class="help-card">
                    <p>For personalized medical advice, please consult with:</p>
                    <ul>
                        <li>Your primary care physician</li>
                        <li>Pharmacist</li>
                        <li>Specialist doctors</li>
                    </ul>
                </div>
            </div>
        </div>
    `;
}

// API Functions
async function searchMedicines() {
    const query = document.getElementById('searchInput').value;
    if (!query) {
        alert('Please enter a search query');
        return;
    }

    try {
        const response = await fetchAPI('/medicines/search', {
            method: 'POST',
            body: JSON.stringify({ query, limit: 10 })
        });
        
        const medicinesList = document.getElementById('medicinesList');
        medicinesList.innerHTML = response.medicines.map(med => `
            <div class="medicine-card">
                <h3>${med.name}</h3>
                <p><strong>Generic Name:</strong> ${med.generic_name || 'N/A'}</p>
                <p><strong>Manufacturer:</strong> ${med.manufacturer || 'N/A'}</p>
                <button onclick="viewMedicineDetails('${med.name}')">View Details</button>
            </div>
        `).join('');
    } catch (error) {
        alert('Error searching medicines');
    }
}

async function viewMedicineDetails(medicineName) {
    try {
        const medicine = await fetchAPI(`/medicines/${encodeURIComponent(medicineName)}`);

        appElement.innerHTML = `
            <nav>
                <button onclick="renderHomePage()">Home</button>
                <button onclick="renderMedicinesPage()">Medicines</button>
                <button onclick="renderInteractionChecker()">Check Interactions</button>
                <button onclick="renderAskMediGuide()">Ask MediGuide</button>
                <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
                <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
                <button onclick="checkHealth()">Health Check</button>
            </nav>
            <div class="content">
                <h2>${medicine.name}</h2>
                <p><strong>Generic Name:</strong> ${medicine.generic_name || 'N/A'}</p>
                <p><strong>Manufacturer:</strong> ${medicine.manufacturer || 'N/A'}</p>
                <p><strong>Uses:</strong> ${medicine.uses || 'N/A'}</p>
                <p><strong>Side Effects:</strong> ${medicine.side_effects || 'N/A'}</p>
            </div>
        `;
    } catch (error) {
        alert('Error fetching medicine details');
    }
}

async function checkHealth() {
    try {
        const health = await fetchAPI('/health');

        appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
            <div class="content">
                <h2>API Health Status</h2>
                <p><strong>Status:</strong> ${health.status}</p>
                <p><strong>Medicines Loaded:</strong> ${health.medicines_loaded}</p>
                <p><strong>Interactions Loaded:</strong> ${health.interactions_loaded}</p>
                <p><strong>Model Loaded:</strong> ${health.model_loaded}</p>
            </div>
        `;
    } catch (error) {
        alert('Error checking health status');
    }
}

// Interaction Checker Functions
let selectedMedicines = [];

function addMedicine() {
    const medicineInput = document.getElementById('medicineInput');
    const medicineName = medicineInput.value.trim();
    
    if (!medicineName) {
        alert('Please enter a medicine name');
        return;
    }
    
    if (selectedMedicines.includes(medicineName)) {
        alert('Medicine already added');
        return;
    }
    
    selectedMedicines.push(medicineName);
    medicineInput.value = '';
    updateSelectedMedicines();
}

function updateSelectedMedicines() {
    const selectedMedicinesElement = document.getElementById('selectedMedicines');
    selectedMedicinesElement.innerHTML = `
        <h3>Selected Medicines (${selectedMedicines.length})</h3>
        ${selectedMedicines.map(med => `
            <div class="medicine-card">
                <span>${med}</span>
                <button onclick="removeMedicine('${med}')">Remove</button>
            </div>
        `).join('')}
    `;
}

function removeMedicine(medicineName) {
    selectedMedicines = selectedMedicines.filter(med => med !== medicineName);
    updateSelectedMedicines();
}

async function checkInteractions() {
    if (selectedMedicines.length < 2) {
        alert('Please add at least 2 medicines to check interactions');
        return;
    }
    
    try {
        const response = await fetchAPI('/interactions/check', {
            method: 'POST',
            body: JSON.stringify({ medicines: selectedMedicines })
        });
        
        const resultsElement = document.getElementById('interactionResults');
        resultsElement.innerHTML = `
            <h3>Interaction Results</h3>
            <p><strong>Severity Summary:</strong></p>
            <ul>
                ${Object.entries(response.severity_summary).map(([severity, count]) => 
                    `<li>${severity}: ${count}</li>`
                ).join('')}
            </ul>
            
            ${response.interactions.length > 0 ? `
                <h4>Interactions Found:</h4>
                ${response.interactions.map(interaction => `
                    <div class="medicine-card">
                        <p><strong>${interaction.drug_a} + ${interaction.drug_b}</strong></p>
                        <p><strong>Severity:</strong> ${interaction.severity}</p>
                        <p><strong>Description:</strong> ${interaction.description}</p>
                        ${interaction.recommendations ? `
                            <p><strong>Recommendations:</strong> ${interaction.recommendations}</p>
                        ` : ''}
                    </div>
                `).join('')}
            ` : '<p>No interactions found between the selected medicines.</p>'}
            
            ${response.recommendations.length > 0 ? `
                <h4>General Recommendations:</h4>
                <ul>
                    ${response.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            ` : ''}
        `;
    } catch (error) {
        alert('Error checking interactions');
    }
}

// Ask MediGuide Functions
function renderAskMediGuide() {
    appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
        <div class="content">
            <h2>Ask MediGuide - Solution-Focused Medical Assistant</h2>
            <p>Get specific tablet recommendations, home care instructions, and emergency guidance for your health concerns.</p>

            <div class="guide-section">
                <h3>💬 Ask Your Question</h3>
                <div class="guide-card">
                    <input type="text" id="questionInput" placeholder="e.g., I have a headache, what should I do?" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <button onclick="askMediGuideQuestion()" style="width: 100%;">Get Solutions</button>
                </div>
            </div>

            <div id="mediguideResponse" class="response-area"></div>

            <div class="guide-section">
                <h3>💡 What You Can Ask About</h3>
                <div class="info-card">
                    <h4>Common Symptoms & Solutions</h4>
                    <ul>
                        <li>"I have a fever, which tablets should I take?"</li>
                        <li>"What should I do for a headache?"</li>
                        <li>"I have stomach pain, what medicine can help?"</li>
                        <li>"How to manage cold symptoms?"</li>
                        <li>"What tablets for allergies?"</li>
                    </ul>
                </div>

                <div class="info-card">
                    <h4>Emergency Situations</h4>
                    <ul>
                        <li>"What to do in case of chest pain?"</li>
                        <li>"I think I'm having a heart attack, what should I do?"</li>
                        <li>"Someone is unconscious, what are the immediate actions?"</li>
                        <li>"What to do for severe allergic reaction?"</li>
                        <li>"Emergency first aid for stroke symptoms"</li>
                    </ul>
                </div>

                <div class="info-card">
                    <h4>Home Care & Prevention</h4>
                    <ul>
                        <li>"How to care for fever at home?"</li>
                        <li>"What are the home remedies for cold?"</li>
                        <li>"How to manage headache without medicine?"</li>
                        <li>"When should I see a doctor for these symptoms?"</li>
                    </ul>
                </div>
            </div>

            <div class="guide-section">
                <h3>⚠️ Important Notice</h3>
                <div class="safety-card">
                    <p><strong>MediGuide provides general guidance only.</strong> For personalized medical advice, always consult with healthcare professionals. In case of medical emergencies, call emergency services immediately.</p>
                </div>
            </div>
        </div>
    `;
}

async function askMediGuideQuestion() {
    const question = document.getElementById('questionInput').value.trim();
    if (!question) {
        alert('Please enter a question');
        return;
    }

    try {
        const response = await fetchAPI('/ask-mediguide', {
            method: 'POST',
            body: JSON.stringify({ question })
        });

        displayAnimatedResponse(response.question, response.response);
    } catch (error) {
        alert('Error getting response from MediGuide');
    }
}

// Function to display response with animation and enhanced formatting
function displayAnimatedResponse(question, text) {
    const responseArea = document.getElementById('mediguideResponse');
    responseArea.innerHTML = `
        <div class="doctor-response">
            <h4>Your Question:</h4>
            <p>"${question}"</p>
            <h4>MediGuide Response:</h4>
            <div class="response-bubble">
                <div id="responseContent"></div>
            </div>
        </div>
    `;

    const contentDiv = document.getElementById('responseContent');

    // Enhanced parsing for actionable content
    const formattedText = formatResponseText(text);
    const points = formattedText.split(/(?=<[^>]*>)/).filter(p => p.trim());

    let pointIndex = 0;
    let charIndex = 0;
    let currentElement = null;

    function animateNextChar() {
        if (pointIndex >= points.length) return;

        if (charIndex === 0) {
            // Start new element
            currentElement = document.createElement('div');
            currentElement.innerHTML = points[pointIndex];
            contentDiv.appendChild(currentElement);
        }

        const textContent = points[pointIndex].replace(/<[^>]*>/g, ''); // Remove HTML for counting
        if (charIndex < textContent.length) {
            // For animation, we'll show the full content immediately but could add char-by-char if needed
            charIndex = textContent.length;
            setTimeout(animateNextChar, 50);
        } else {
            // Element complete, move to next
            pointIndex++;
            charIndex = 0;
            setTimeout(animateNextChar, 300); // Delay between elements
        }
    }

    animateNextChar();
}

// Function to format response text for better actionability
function formatResponseText(text) {
    let formatted = text;

    // Format tablet recommendations
    formatted = formatted.replace(/(take|use|try)\s+([^.!?]+(?:tablet|medicine|drug|medication)[^.!?]*)/gi,
        '<div class="action-item tablet-rec"><strong>💊 Tablet Recommendation:</strong> $2</div>');

    // Format emergency actions
    formatted = formatted.replace(/(call|seek|go to|contact)\s+([^.!?]+(?:emergency|doctor|hospital|ambulance)[^.!?]*)/gi,
        '<div class="action-item emergency"><strong>🚨 Emergency Action:</strong> $2</div>');

    // Format home care instructions
    formatted = formatted.replace(/(rest|drink|apply|use)\s+([^.!?]+(?:water|fluids|ice|compress|bed rest)[^.!?]*)/gi,
        '<div class="action-item home-care"><strong>🏠 Home Care:</strong> $2</div>');

    // Format when to see doctor
    formatted = formatted.replace(/(see|consult|visit)\s+(?:a\s+)?(?:doctor|physician|healthcare|medical)[^.!?]*(?:if|when)[^.!?]*/gi,
        '<div class="action-item doctor-visit"><strong>👨‍⚕️ When to See Doctor:</strong> $&</div>');

    // Format general recommendations
    formatted = formatted.replace(/^(recommend|important|suggestion)[^.!?]*/gim,
        '<div class="action-item recommendation"><strong>💡 Recommendation:</strong> $&</div>');

    // Split into paragraphs and format
    const sentences = formatted.split(/[.!?]+/).filter(s => s.trim());
    return sentences.map(sentence => {
        const trimmed = sentence.trim();
        if (trimmed.includes('<div class="action-item')) {
            return trimmed;
        } else {
            return `<p>${trimmed}.</p>`;
        }
    }).join('');
}

// Medicine Scheduler Functions
function renderMedicineScheduler() {
    appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
        <div class="content">
            <h2>Medicine Scheduler & Reminders</h2>
            <p>Set reminders for your medications to stay on track with your treatment.</p>

            <div class="guide-section">
                <h3>➕ Add New Reminder</h3>
                <div class="guide-card">
                    <input type="text" id="medicineName" placeholder="Medicine Name" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <input type="time" id="reminderTime" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <select id="reminderFrequency" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                        <option value="once">Once</option>
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                    <input type="text" id="reminderDescription" placeholder="Description (optional)" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <button onclick="addReminder()" style="width: 100%;">Add Reminder</button>
                </div>
            </div>

            <div id="remindersList" class="guide-section">
                <h3>📅 Your Reminders</h3>
                <div id="remindersContainer"></div>
            </div>
        </div>
    `;
    loadReminders();
}

function addReminder() {
    const medicineName = document.getElementById('medicineName').value.trim();
    const reminderTime = document.getElementById('reminderTime').value;
    const reminderFrequency = document.getElementById('reminderFrequency').value;
    const description = document.getElementById('reminderDescription').value.trim();

    if (!medicineName || !reminderTime) {
        alert('Please enter medicine name and time');
        return;
    }

    const reminders = getReminders();
    const newReminder = {
        id: Date.now(),
        medicine: medicineName,
        time: reminderTime,
        frequency: reminderFrequency,
        description: description,
        created: new Date().toISOString()
    };

    reminders.push(newReminder);
    saveReminders(reminders);

    // Clear form
    document.getElementById('medicineName').value = '';
    document.getElementById('reminderTime').value = '';
    document.getElementById('reminderFrequency').value = 'once';
    document.getElementById('reminderDescription').value = '';

    loadReminders();
}

function loadReminders() {
    const reminders = getReminders();
    const container = document.getElementById('remindersContainer');

    if (reminders.length === 0) {
        container.innerHTML = '<p>No reminders set yet. Add your first reminder above!</p>';
        return;
    }

    container.innerHTML = reminders.map(reminder => `
        <div class="medicine-card">
            <h4>${reminder.medicine}</h4>
            <p><strong>Time:</strong> ${reminder.time}</p>
            <p><strong>Frequency:</strong> ${reminder.frequency.charAt(0).toUpperCase() + reminder.frequency.slice(1)}</p>
            ${reminder.description ? `<p><strong>Description:</strong> ${reminder.description}</p>` : ''}
            <p><strong>Added:</strong> ${new Date(reminder.created).toLocaleDateString()}</p>
            <button onclick="removeReminder(${reminder.id})">Remove</button>
        </div>
    `).join('');
}

function removeReminder(id) {
    const reminders = getReminders().filter(r => r.id !== id);
    saveReminders(reminders);
    loadReminders();
}

function getReminders() {
    const stored = localStorage.getItem('medicineReminders');
    return stored ? JSON.parse(stored) : [];
}

function saveReminders(reminders) {
    localStorage.setItem('medicineReminders', JSON.stringify(reminders));
}

// Emergency Contacts Functions
function renderEmergencyContacts() {
    appElement.innerHTML = `
        <nav>
            <button onclick="renderHomePage()">Home</button>
            <button onclick="renderMedicinesPage()">Medicines</button>
            <button onclick="renderInteractionChecker()">Check Interactions</button>
            <button onclick="renderAskMediGuide()">Ask MediGuide</button>
            <button onclick="renderMedicineScheduler()">Medicine Scheduler</button>
            <button onclick="renderEmergencyContacts()">Emergency Contacts</button>
            <button onclick="checkHealth()">Health Check</button>
        </nav>
        <div class="content">
            <h2>Emergency Contacts</h2>
            <p>Store important emergency contact information for quick access during medical emergencies.</p>

            <div class="guide-section">
                <h3>➕ Add New Contact</h3>
                <div class="guide-card">
                    <input type="text" id="contactName" placeholder="Contact Name" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <input type="text" id="contactPhone" placeholder="Phone Number" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <input type="text" id="contactRelationship" placeholder="Relationship (e.g., Doctor, Family)" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <input type="text" id="contactNotes" placeholder="Notes (optional)" style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <button onclick="addEmergencyContact()" style="width: 100%;">Add Contact</button>
                </div>
            </div>

            <div id="contactsList" class="guide-section">
                <h3>📞 Your Emergency Contacts</h3>
                <div id="contactsContainer"></div>
            </div>
        </div>
    `;
    loadEmergencyContacts();
}

function addEmergencyContact() {
    const name = document.getElementById('contactName').value.trim();
    const phone = document.getElementById('contactPhone').value.trim();
    const relationship = document.getElementById('contactRelationship').value.trim();
    const notes = document.getElementById('contactNotes').value.trim();

    if (!name || !phone) {
        alert('Please enter contact name and phone number');
        return;
    }

    const contacts = getEmergencyContacts();
    const newContact = {
        id: Date.now(),
        name: name,
        phone: phone,
        relationship: relationship,
        notes: notes,
        created: new Date().toISOString()
    };

    contacts.push(newContact);
    saveEmergencyContacts(contacts);

    // Clear form
    document.getElementById('contactName').value = '';
    document.getElementById('contactPhone').value = '';
    document.getElementById('contactRelationship').value = '';
    document.getElementById('contactNotes').value = '';

    loadEmergencyContacts();
}

function loadEmergencyContacts() {
    const contacts = getEmergencyContacts();
    const container = document.getElementById('contactsContainer');

    if (contacts.length === 0) {
        container.innerHTML = '<p>No emergency contacts added yet. Add your first contact above!</p>';
        return;
    }

    container.innerHTML = contacts.map(contact => `
        <div class="medicine-card">
            <h4>${contact.name}</h4>
            <p><strong>Phone:</strong> <a href="tel:${contact.phone}">${contact.phone}</a></p>
            ${contact.relationship ? `<p><strong>Relationship:</strong> ${contact.relationship}</p>` : ''}
            ${contact.notes ? `<p><strong>Notes:</strong> ${contact.notes}</p>` : ''}
            <p><strong>Added:</strong> ${new Date(contact.created).toLocaleDateString()}</p>
            <button onclick="removeEmergencyContact(${contact.id})">Remove</button>
        </div>
    `).join('');
}

function removeEmergencyContact(id) {
    const contacts = getEmergencyContacts().filter(c => c.id !== id);
    saveEmergencyContacts(contacts);
    loadEmergencyContacts();
}

function getEmergencyContacts() {
    const stored = localStorage.getItem('emergencyContacts');
    return stored ? JSON.parse(stored) : [];
}

function saveEmergencyContacts(contacts) {
    localStorage.setItem('emergencyContacts', JSON.stringify(contacts));
}

// Initialize the application
renderHomePage();
