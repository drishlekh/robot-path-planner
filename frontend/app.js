// frontend/app.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Configuration ---
    const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
    const ANIMATION_SPEED_FACTOR = 0.5; // Lower is faster, higher is slower

    // --- DOM Elements ---
    const calculateBtn = document.getElementById("calculateBtn");
    const statusText = document.getElementById("status-text");
    const statusCoords = document.getElementById("status-coords");
    const canvas = document.getElementById("pathCanvas");
    const ctx = canvas.getContext("2d");

    let animationFrameId;

    // --- Event Listener ---
    calculateBtn.addEventListener("click", handleDeployRobot);

    async function handleDeployRobot() {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }

        const { requestBody, toolWidth } = getInputs();
        if (!requestBody) return;

        setUIState("calculating");

        try {
            const url = `${API_BASE_URL}/trajectories/?tool_width=${toolWidth}`;
            
            const createResponse = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            });

            if (!createResponse.ok) {
                const errorData = await createResponse.json();
                throw new Error(`API Error: ${errorData.detail || createResponse.statusText}`);
            }

            const trajectoryData = await createResponse.json();
            setUIState("painting");
            drawInitialState(trajectoryData); // Draw the red obstacle
            animateRobot(trajectoryData, toolWidth); // Start the painting animation

        } catch (error) {
            console.error("Failed to process trajectory:", error);
            setUIState("error", error.message);
        }
    }

    function getInputs() { /* ... same as before ... */ }
    function setUIState(state, message = "") { /* ... same as before ... */ }
    function drawInitialState(trajectory) { /* ... same as before ... */ }
    
    // --- NEW, SIMPLIFIED, AND CORRECT ANIMATION LOGIC ---
    function animateRobot(trajectory, toolWidth) {
        const scale = canvas.width / trajectory.wall_dimensions.width;
        const path = trajectory.path;
        const toolWidthPx = Math.max(2, toolWidth * scale); // Ensure line is at least 2px thick

        let i = 1; // Start from the second point to draw the first line segment

        function drawNextSegment() {
            if (i >= path.length) {
                setUIState("complete");
                // Final coordinate update
                const finalPoint = path[path.length - 1];
                statusCoords.textContent = `X: ${finalPoint.x.toFixed(2)}m, Y: ${finalPoint.y.toFixed(2)}m`;
                return;
            }

            const p1 = path[i-1];
            const p2 = path[i];

            // Convert world coordinates to canvas coordinates
            const x1 = p1.x * scale;
            const y1 = canvas.height - (p1.y * scale);
            const x2 = p2.x * scale;
            const y2 = canvas.height - (p2.y * scale);
            
            // Draw the paint stroke
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = "rgba(0, 170, 255, 0.9)";
            ctx.lineWidth = toolWidthPx;
            ctx.lineCap = "round"; // Makes the paint strokes look smoother
            ctx.stroke();

            // Update status text with the robot's current position
            statusCoords.textContent = `X: ${p2.x.toFixed(2)}m, Y: ${p2.y.toFixed(2)}m`;
            
            i++;

            // Use a small timeout to control animation speed
            setTimeout(() => {
                animationFrameId = requestAnimationFrame(drawNextSegment);
            }, ANIMATION_SPEED_FACTOR);
        }

        animationFrameId = requestAnimationFrame(drawNextSegment);
    }
    
    // --- Helper functions ---
    function getInputs() {
        return {
            requestBody: {
                wall_dimensions: { width: parseFloat(document.getElementById("wallWidth").value), height: parseFloat(document.getElementById("wallHeight").value) },
                obstacles: [{
                    bottom_left: { x: parseFloat(document.getElementById("obsX").value), y: parseFloat(document.getElementById("obsY").value) },
                    dimensions: { width: parseFloat(document.getElementById("obsWidth").value), height: parseFloat(document.getElementById("obsHeight").value) }
                }]
            },
            toolWidth: parseFloat(document.getElementById("robotWidth").value)
        };
    }
    
    function setUIState(state, message = "") {
        calculateBtn.disabled = (state === "calculating" || state === "painting");
        switch (state) {
            case "idle": statusText.textContent = "Status: Idle"; statusText.style.color = "var(--text-color)"; statusCoords.textContent = ""; break;
            case "calculating": statusText.textContent = "Status: Calculating Path..."; statusText.style.color = "var(--primary-color)"; break;
            case "painting": statusText.textContent = "Status: Painting..."; statusText.style.color = "var(--success-color)"; break;
            case "complete": statusText.textContent = "Status: Complete!"; statusText.style.color = "var(--success-color)"; calculateBtn.disabled = false; break;
            case "error": statusText.textContent = `Error: ${message}`; statusText.style.color = "var(--error-color)"; calculateBtn.disabled = false; break;
        }
    }

    function drawInitialState(trajectory) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const scale = canvas.width / trajectory.wall_dimensions.width;
        ctx.fillStyle = "rgba(220, 53, 69, 0.9)";
        ctx.strokeStyle = "#ff6b81";
        ctx.lineWidth = 2;
        trajectory.obstacles.forEach(obs => {
            ctx.beginPath();
            const x = obs.bottom_left.x * scale;
            const y = canvas.height - (obs.bottom_left.y * scale) - (obs.dimensions.height * scale);
            const w = obs.dimensions.width * scale;
            const h = obs.dimensions.height * scale;
            ctx.rect(x, y, w, h);
            ctx.fill();
            ctx.stroke();
        });
    }
});