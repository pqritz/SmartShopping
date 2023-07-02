// Variables
const imageContainer = document.getElementById('image-container');
const image = document.getElementById('image');
let initialScale = 1;
let scale = initialScale;
let posX = 0;
let posY = 0;
let isDragging = false;
let initialX = 0;
let initialY = 0;

// Event Listeners
image.addEventListener('wheel', handleZoom);
image.addEventListener('mousedown', startDrag);
image.addEventListener('mouseup', stopDrag);
image.addEventListener('mousemove', handleMove);
image.addEventListener('touchstart', handleTouchStart);
image.addEventListener('touchmove', handleTouchMove);
image.addEventListener('touchend', handleTouchEnd);
image.addEventListener('touchcancel', handleTouchEnd);

// Functions
function handleZoom(event) {
    event.preventDefault();
    const delta = Math.sign(event.deltaY);

    if (delta > 0) {
        // Zoom out
        scale -= 0.1;
        scale = Math.max(scale, 1);
    } else {
        // Zoom in
        scale += 0.1;
        scale = Math.min(scale, 3);
    }

    const rect = image.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
    const imageCenterX = rect.width / 2;
    const imageCenterY = rect.height / 2;
    const deltaScale = scale / initialScale;
    const deltaPosX = (mouseX - imageCenterX) * (1 - deltaScale);
    const deltaPosY = (mouseY - imageCenterY) * (1 - deltaScale);
    posX -= deltaPosX;
    posY -= deltaPosY;

    applyTransform();
}

function startDrag(event) {
    event.preventDefault();
    isDragging = true;
    initialX = event.clientX;
    initialY = event.clientY;
    image.style.cursor = 'grabbing';
}

function stopDrag() {
    isDragging = false;
    image.style.cursor = 'grab';
}

function handleMove(event) {
    event.preventDefault();
    if (!isDragging) return;

    const deltaX = event.clientX - initialX;
    const deltaY = event.clientY - initialY;

    posX += deltaX;
    posY += deltaY;

    initialX = event.clientX;
    initialY = event.clientY;

    applyTransform();
}

function handleTouchStart(event) {
    if (event.touches.length === 2) {
        const touch1 = event.touches[0];
        const touch2 = event.touches[1];

        initialScale = scale;
        initialX = Math.abs(touch1.clientX + touch2.clientX) / 2;
        initialY = Math.abs(touch1.clientY + touch2.clientY) / 2;
    }
}

function handleTouchMove(event) {
    event.preventDefault();
    if (event.touches.length === 2) {
        const touch1 = event.touches[0];
        const touch2 = event.touches[1];

        const touchDistance = Math.hypot(
            touch1.clientX - touch2.clientX,
            touch1.clientY - touch2.clientY
        );

        scale = initialScale * (touchDistance / initialDistance);

        const touchCenterX = Math.abs(touch1.clientX + touch2.clientX) / 2;
        const touchCenterY = Math.abs(touch1.clientY + touch2.clientY) / 2;

        posX += touchCenterX - initialX;
        posY += touchCenterY - initialY;

        initialX = touchCenterX;
        initialY = touchCenterY;

        applyTransform();
    }
}

function handleTouchEnd() {
    initialScale = scale;
    initialDistance = 0;
}

function applyTransform() {
    image.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
}


function addMarkerToImage(path, points, color, size, fontSize) {
    const image = new Image();
    image.onload = function () {
        const canvas = document.createElement('canvas');
        canvas.width = image.width;
        canvas.height = image.height;
        const context = canvas.getContext('2d');

        context.drawImage(image, 0, 0);

        for (const p of points) {
            addMarker(context, p, color, size, '', [0, 0], fontSize);
        }

        const imageDataURL = canvas.toDataURL('image/png');

        const imgElement = document.createElement('img');
        imgElement.src = imageDataURL;

        document.body.appendChild(imgElement);
    };

    image.src = path;
}

function addMarker(context, position, color, size, text, textPos, fontSize) {
    const [markerX, markerY] = position;
    const [textX, textY] = textPos;

    context.font = `${fontSize}px Arial`;
    context.fillStyle = 'white';
    context.fillText(text, textX, textY);

    const { width, height } = context.canvas;
    const markerRadius = size * Math.min(width, height);
    const markerCenterX = markerX * width;
    const markerCenterY = markerY * height;
    const markerStartAngle = Math.PI;
    const markerEndAngle = 0;

    context.beginPath();
    context.arc(markerCenterX, markerCenterY, markerRadius, markerStartAngle, markerEndAngle);
    context.fillStyle = color;
    context.fill();

    const triangleSize = size * Math.min(width, height);

    context.beginPath();
    context.moveTo(markerCenterX, markerCenterY + triangleSize * 2);
    context.lineTo(markerCenterX - triangleSize, markerCenterY);
    context.lineTo(markerCenterX + triangleSize, markerCenterY);
    context.closePath();
    context.fillStyle = color;
    context.fill();
}

function renderImage() {
    // Example usage
    const imagePath = '../json/stores/Lidl, Nuernberger Str., Altdorf bei Nuernberg.png';
    const markerPoints = [[0.5, 0.5], [0.3, 0.7], [1, 1], [0.8, 0.2]];
    const markerColor = '#FF0000';
    const markerSize = 0.02;
    const markerFontSize = 18;

    addMarkerToImage(imagePath, markerPoints, markerColor, markerSize, markerFontSize);
}

renderImage()