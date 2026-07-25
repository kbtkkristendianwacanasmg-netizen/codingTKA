// static/script.js

let score = 0;
const scoreDisplay = document.getElementById('score');
const dropZone = document.getElementById('drop-zone');
const faceBase = document.getElementById('face-base');

// Variables to keep track of placed parts
const placedParts = {
    eye: false,
    nose: false,
    mouth: false,
    ear: false,
    hair: false
};

// --- DRAG AND DROP LOGIC (Mouse & Touch) ---

// Get all draggable elements
const draggableParts = document.querySelectorAll('.draggable-part');

// Add event listeners to each draggable part
draggableParts.forEach(part => {
    part.addEventListener('dragstart', dragStart);
    part.addEventListener('touchstart', touchStart, { passive: false });
    part.addEventListener('touchmove', touchMove, { passive: false });
    part.addEventListener('touchend', touchEnd);
});

// Define functions for dragging
function dragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.id);
}

// Enable drop zone to accept items
dropZone.addEventListener('dragover', e => {
    e.preventDefault();
});

// Handle the drop event
dropZone.addEventListener('drop', e => {
    e.preventDefault();
    const partId = e.dataTransfer.getData('text/plain');
    handlePartPlaced(partId, e.clientX, e.clientY);
});


// --- TOUCH HANDLERS (for tablets/phones) ---

let currentTouchElement = null;
let touchOffsetX = 0;
let touchOffsetY = 0;

function touchStart(e) {
    e.preventDefault();
    currentTouchElement = e.target;
    const touch = e.touches[0];
    const rect = currentTouchElement.getBoundingClientRect();
    touchOffsetX = touch.clientX - rect.left;
    touchOffsetY = touch.clientY - rect.top;
    currentTouchElement.style.position = 'absolute'; // Temporarily position for moving
    currentTouchElement.style.zIndex = 1000;
}

function touchMove(e) {
    e.preventDefault();
    if (!currentTouchElement) return;
    const touch = e.touches[0];
    currentTouchElement.style.left = touch.clientX - touchOffsetX + 'px';
    currentTouchElement.style.top = touch.clientY - touchOffsetY + 'px';
}

function touchEnd(e) {
    if (!currentTouchElement) return;
    
    // Check if dropped inside drop zone
    const touch = e.changedTouches[0];
    const dropZoneRect = dropZone.getBoundingClientRect();

    if (
        touch.clientX >= dropZoneRect.left &&
        touch.clientX <= dropZoneRect.right &&
        touch.clientY >= dropZoneRect.top &&
        touch.clientY <= dropZoneRect.bottom
    ) {
        // Position relative to the drop zone
        const x = touch.clientX - dropZoneRect.left;
        const y = touch.clientY - dropZoneRect.top;
        
        handlePartPlaced(currentTouchElement.id, touch.clientX, touch.clientY);
    } else {
        // Reset position if dropped outside
        currentTouchElement.style.position = 'static';
        currentTouchElement.style.zIndex = 'auto';
    }

    currentTouchElement = null;
}


// --- CORE GAME LOGIC ---

function handlePartPlaced(partId, clientX, clientY) {
    const part = document.getElementById(partId);
    
    // Check if part is already placed
    if (placedParts[partId]) {
        alert("Kamu sudah memasang " + partId + "!");
        return;
    }

    const dropZoneRect = dropZone.getBoundingClientRect();

    // Clone the element to place it in the drop zone
    const placedPart = part.cloneNode(true);
    placedPart.classList.remove('draggable-part');
    placedPart.style.position = 'absolute';

    // Calculate position relative to the drop zone
    const offsetX = clientX - dropZoneRect.left;
    const offsetY = clientY - dropZoneRect.top;

    // Center the part at the cursor/touch point
    const placedWidth = part.offsetWidth;
    const placedHeight = part.offsetHeight;
    placedPart.style.left = (offsetX - placedWidth / 2) + 'px';
    placedPart.style.top = (offsetY - placedHeight / 2) + 'px';

    dropZone.appendChild(placedPart);

    // Update state and score
    placedParts[partId] = true;
    updateScore(10); // Gain 10 points per part

    // Optional: Hide original part from the container
    part.style.visibility = 'hidden';

    checkGameComplete();
}

function updateScore(points) {
    score += points;
    scoreDisplay.innerText = score;
}

function checkGameComplete() {
    // Check if all essential parts are placed
    const essentialParts = ['eye', 'nose', 'mouth', 'hair'];
    const complete = essentialParts.every(partId => placedParts[partId]);

    if (complete) {
        updateScore(50); // Bonus for completion
        alert("Hebat! Kamu sudah membuat wajah! Skor total: " + score);
    }
}

function resetGame() {
    // 1. Remove all placed parts from the drop zone
    const placedItems = dropZone.querySelectorAll('img');
    placedItems.forEach(item => item.remove());

    // 2. Reset visibility of parts in the container
    draggableParts.forEach(part => part.style.visibility = 'visible');

    // 3. Reset placedParts object
    for (const partId in placedParts) {
        placedParts[partId] = false;
    }

    // 4. Reset Score
    score = 0;
    scoreDisplay.innerText = score;

    // 5. Change Face Type (handled slightly differently as it's set by Flask initially)
    // We can simulate this by reloading the page to get a new initial_face_type from Flask
    location.reload(); 
    // OR: More complexly, define a Javascript array of face images and cycle through them here.
}
