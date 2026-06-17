// =========================================================================
// GeoAlert System Client JS Workspace
// =========================================================================

// Memory Registry Buckets 
let globalLeafletMapInstance = null;
let globalLeafletMarkerNode = null;

// Preset Mapping Configurations for realistic Simulation coordinate matching
const PRESET_COORDINATE_MAP = {
    "GATEWAY OF INDIA": { lat: 18.9220, lng: 72.8347 },
    "MARINE DRIVE": { lat: 18.9431, lng: 72.8230 },
    "PHOENIX MALL": { lat: 18.9942, lng: 72.8256 },
    "JIO WORLD DRIVE": { lat: 19.0617, lng: 72.8614 },
    "R CITY MALL": { lat: 19.0997, lng: 72.9163 },
    "LULU MALL": { lat: 10.0261, lng: 76.3113 },
    "PUNE AIRPORT": { lat: 18.5822, lng: 73.9197 },
    "PANVEL STATION": { lat: 18.9894, lng: 73.1175 },
    "DEFAULT": { lat: 18.9900, lng: 73.1200 }
};

// -------------------------------------------------------------------------
// Global Lifecycle Initializations 
// -------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
    updateSystemTimeNode();
    setInterval(updateSystemTimeNode, 30000);

    // Form Event Wireups
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", handleSystemLoginFlow);
    }

    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", handleSystemRegistrationFlow);
    }

    // Contextual routing state discovery
    if (document.getElementById("leafletMap")) {
        initializeLeafletWorkspaceEngine();
    }
    if (document.getElementById("historicalNotificationCardsContainer")) {
        renderHistoricalNotificationMatrix();
    }
    if (document.getElementById("dashLastLocation")) {
        hydrateDashboardTelemetryMetrics();
    }
    if (document.getElementById("profileName")) {
        hydrateUserProfileFields();
    }
    renderSearchBadgesHistory();
});

function updateSystemTimeNode() {
    const timeNode = document.getElementById("panelCurrentTime");
    if (timeNode) {
        const timeNow = new Date();
        timeNode.innerText = timeNow.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
}

// -------------------------------------------------------------------------
// CORE IDENTITY BINDINGS & AUTH PIPELINES
// -------------------------------------------------------------------------
async function handleSystemLoginFlow(event) {
    event.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        
        if (data.status) {
            localStorage.setItem("user", JSON.stringify(data.user));
            window.location.href = "/dashboard";
        } else {
            alert(data.message || "Invalid credentials provided.");
        }
    } catch (err) {
        console.error("Auth server connection fault:", err);
    }
}

async function handleSystemRegistrationFlow(event) {
    event.preventDefault();
    const full_name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ full_name, email, phone, password })
        });
        const data = await response.json();
        
        if (data.status) {
            alert("Registration successful! Proceeding to login screen.");
            window.location.href = "/";
        } else {
            alert(data.message || "Registration encountered an issue.");
        }
    } catch (err) {
        console.error("Registration endpoint server failure:", err);
    }
}

function hydrateUserProfileFields() {
    try {
        const cachedUser = localStorage.getItem("user");
        if (!cachedUser) {
            window.location.href = "/";
            return;
        }
        const userObj = JSON.parse(cachedUser);
        
        if (document.getElementById("profileName")) document.getElementById("profileName").value = userObj.full_name || "N/A";
        if (document.getElementById("profileEmail")) document.getElementById("profileEmail").value = userObj.email || "N/A";
        if (document.getElementById("profilePhone")) document.getElementById("profilePhone").value = userObj.phone || "N/A";
        
        // Load preference setting fallback state if saved locally
        const prefNode = document.getElementById("profilePreference");
        if (prefNode) {
            const savedPref = localStorage.getItem("geoalert_pref_" + userObj.user_id) || "All";
            prefNode.value = savedPref;
            prefNode.addEventListener("change", function() {
                localStorage.setItem("geoalert_pref_" + userObj.user_id, prefNode.value);
            });
        }
    } catch (e) {
        console.error("Error hydrating profile inputs fields:", e);
    }
}

function logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("geoalert_latest_telemetry");
    window.location.href = "/";
}

// -------------------------------------------------------------------------
// LEAFLET WORKSPACE MAP FRAMEWORK ENGINE IMPLEMENTATION
// -------------------------------------------------------------------------
function initializeLeafletWorkspaceEngine() {
    let lastKnownCoords = { lat: 18.9894, lng: 73.1175 }; 
    const sessionMemory = localStorage.getItem("geoalert_last_context");
    if (sessionMemory) {
        const parsed = JSON.parse(sessionMemory);
        if (parsed.lat && parsed.lng) lastKnownCoords = parsed;
    }

    globalLeafletMapInstance = L.map('leafletMap', {
        zoomControl: true,
        fadeAnimation: true,
        markerZoomAnimation: true
    }).setView([lastKnownCoords.lat, lastKnownCoords.lng], 14);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(globalLeafletMapInstance);

    globalLeafletMarkerNode = L.marker([lastKnownCoords.lat, lastKnownCoords.lng], {
        draggable: true,
        bounceOnAdd: true
    }).addTo(globalLeafletMapInstance);

    globalLeafletMarkerNode.on('dragend', function (e) {
        const droppedPosition = globalLeafletMarkerNode.getLatLng();
        globalLeafletMapInstance.flyTo(droppedPosition, globalLeafletMapInstance.getZoom(), { animate: true, duration: 0.8 });
        
        const simulatedName = deduceSimulatedLocationLabel(droppedPosition.lat, droppedPosition.lng);
        executeGeofenceVerificationWorkflow(simulatedName, droppedPosition.lat, droppedPosition.lng);
    });

    const pendingSearch = localStorage.getItem("geoalert_pending_search");
    if (pendingSearch) {
        localStorage.removeItem("geoalert_pending_search");
        executeGeofenceVerificationWorkflow(pendingSearch);
    } else {
        const activeLocName = localStorage.getItem("geoalert_last_location_name") || "Panvel Framework Hub";
        executeGeofenceVerificationWorkflow(activeLocName, lastKnownCoords.lat, lastKnownCoords.lng);
    }
}

function deduceSimulatedLocationLabel(lat, lng) {
    let bestMatch = "Dynamic GPS Vector Block";
    let minDistance = Infinity;
    for (const [key, val] of Object.entries(PRESET_COORDINATE_MAP)) {
        let dist = Math.sqrt(Math.pow(val.lat - lat, 2) + Math.pow(val.lng - lng, 2));
        if (dist < minDistance) {
            minDistance = dist;
            bestMatch = key;
        }
    }
    return toTitleCase(bestMatch);
}

// -------------------------------------------------------------------------
// SEARCH INTEGRATION & TRANSIT ROUTING ENGINE WIDGETS
// -------------------------------------------------------------------------
function searchLocation() {
    const queryInput = document.getElementById("locationInput");
    if (!queryInput || !queryInput.value.trim()) return;
    
    const targetQuery = queryInput.value.trim();
    saveSearchQueryToHistory(targetQuery);

    if (!document.getElementById("leafletMap")) {
        localStorage.setItem("geoalert_pending_search", targetQuery);
        window.location.href = "/map";
        return;
    }

    executeGeofenceVerificationWorkflow(targetQuery);
}

function triggerPresetSearch(presetLabel) {
    if (document.getElementById("locationInput")) {
        document.getElementById("locationInput").value = presetLabel;
        searchLocation();
    }
}

function executeDashboardSearch() {
    const dashInput = document.getElementById("dashboardSearchInput");
    if (!dashInput || !dashInput.value.trim()) return;
    localStorage.setItem("geoalert_pending_search", dashInput.value.trim());
    saveSearchQueryToHistory(dashInput.value.trim());
    window.location.href = "/map";
}

// -------------------------------------------------------------------------
// REVISED ASYNC GEOFENCE & TELEMETRY GENERATION WORKFLOW
// -------------------------------------------------------------------------
async function executeGeofenceVerificationWorkflow(locName, forcedLat = null, forcedLng = null) {
    toggleMapSkeletonState(true);

    let lookupKey = locName.toUpperCase();
    let coords = { lat: 18.9894, lng: 73.1175 };
    
    if (forcedLat && forcedLng) {
        coords = { lat: forcedLat, lng: forcedLng };
    } else {
        let matchFound = false;
        for (const [k, v] of Object.entries(PRESET_COORDINATE_MAP)) {
            if (lookupKey.includes(k)) {
                coords = v;
                matchFound = true;
                break;
            }
        }
        if (!matchFound) {
            coords = {
                lat: 18.9 + (Math.random() * 0.15),
                lng: 72.8 + (Math.random() * 0.25)
            };
        }
    }

    localStorage.setItem("geoalert_last_context", JSON.stringify(coords));
    localStorage.setItem("geoalert_last_location_name", locName);

    if (globalLeafletMapInstance && globalLeafletMarkerNode) {
        globalLeafletMarkerNode.setLatLng([coords.lat, coords.lng]);
        globalLeafletMapInstance.flyTo([coords.lat, coords.lng], 15, {
            animate: true,
            duration: 1.2
        });
    }

    await new Promise(resolve => setTimeout(resolve, 1000));

    try {
        const response = await fetch("/update-location", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: getSessionUserIdToken(),
                location: locName
            })
        });
        
        const data = await response.json();
        toggleMapSkeletonState(false);

        if (data.status || data[0]?.status) {
            const normalizedPayload = data.notifications ? data : data[0];
            hydrateMapPanelsInterface(normalizedPayload, locName);
        }
    } catch (err) {
        console.error("Critical Telemetry payload retrieval faults detected:", err);
        toggleMapSkeletonState(false);
    }
}

// -------------------------------------------------------------------------
// DYNAMIC DOM UI MANIPULATIONS AND CODES
// -------------------------------------------------------------------------
function toggleMapSkeletonState(showSkeleton) {
    const listNode = document.getElementById("leftPanelNotifications");
    const skelNode = document.getElementById("skeletonLoader");
    if (!listNode || !skelNode) return;

    if (showSkeleton) {
        listNode.classList.add("d-none");
        skelNode.classList.remove("d-none");
    } else {
        listNode.classList.remove("d-none");
        skelNode.classList.add("d-none");
    }
}

function hydrateMapPanelsInterface(payload, resolvedLabel) {
    const locField = document.getElementById("panelCurrentLocation");
    if (locField) locField.innerText = resolvedLabel;

    const notifications = payload.notifications || [];
    const contextCards = payload.context_cards || {};

    localStorage.setItem("geoalert_latest_telemetry", JSON.stringify({
        location: resolvedLabel,
        context_cards: contextCards,
        latest_notification: notifications[0] || null
    }));

    const feedContainer = document.getElementById("leftPanelNotifications");
    if (feedContainer) {
        feedContainer.innerHTML = "";
        if (notifications.length === 0) {
            feedContainer.innerHTML = `<div class='text-muted small text-center py-3'>No alerts active here.</div>`;
        } else {
            notifications.forEach(item => {
                feedContainer.innerHTML += `
                    <div class="card p-3 shadow-sm border-0 mb-2 notification-node rounded-3 bg-white">
                        <div class="d-flex align-items-start gap-2">
                            <span class="fs-4">${item.icon || '🔔'}</span>
                            <div class="flex-grow-1">
                                <div class="d-flex justify-content-between align-items-center">
                                    <h6 class="fw-bold mb-0 text-dark" style="font-size:0.95rem;">${item.title}</h6>
                                    <span class="badge bg-light text-secondary border rounded-pill px-2" style="font-size:0.7rem;">${item.category}</span>
                                </div>
                                <p class="text-secondary small mb-1 mt-1" style="line-height:1.3;">${item.description || item.message}</p>
                                <div class="d-flex justify-content-between text-muted" style="font-size:0.75rem;">
                                    <span>📍 ${item.location}</span>
                                    <span>${item.time}</span>
                                </div>
                            </div>
                        </div>
                    </div>`;
            });
        }
    }

    const overlayContainer = document.getElementById("contextOverlayDeck");
    if (overlayContainer) {
        overlayContainer.innerHTML = "";
        
        const cardConfigs = [
            { label: "Traffic Flow", val: contextCards.traffic_status, color: "text-warning", icon: "🚦" },
            { label: "Nearby Promos", val: contextCards.nearby_offer, color: "text-success", icon: "🛍️" },
            { label: "Safety Level", val: contextCards.safety_level, color: "text-info", icon: "🛡️" },
            { label: "Parking Allocation", val: contextCards.parking_status, color: "text-secondary", icon: "🅿️" },
            { label: "Crowd Footfall", val: contextCards.crowd_status, color: "text-dark", icon: "👥" },
            { label: "Simulated Weather", val: contextCards.weather, color: "text-primary", icon: "🌤️" },
            { label: "Radius Space", val: contextCards.distance, color: "text-dark", icon: "📏" },
            { label: "ETA Window", val: contextCards.arrival_time, color: "text-danger", icon: "⏳" }
        ];

        cardConfigs.forEach(c => {
            overlayContainer.innerHTML += `
                <div class="context-card-node">
                    <div class="d-flex align-items-center gap-2 mb-1">
                        <span>${c.icon}</span>
                        <small class="text-muted text-uppercase fw-bold" style="font-size:0.7rem; tracking-wider:1px;">${c.label}</small>
                    </div>
                    <span class="fw-bold d-block text-dark fs-6 text-truncate">${c.val || 'N/A'}</span>
                </div>`;
        });
    }
}

// -------------------------------------------------------------------------
// NOTIFICATION HISTORICAL CHRONOLOGY ENGINE CODES
// -------------------------------------------------------------------------
async function renderHistoricalNotificationMatrix() {
    const gridContainer = document.getElementById("historicalNotificationCardsContainer");
    if (!gridContainer) return;

    try {
        const response = await fetch("/notifications/" + getSessionUserIdToken());
        const rawData = await response.json();
        const list = rawData.data || rawData;
        gridContainer.innerHTML = "";

        if (!list || list.length === 0) {
            gridContainer.innerHTML = `
                <div class="col-12 text-center py-5">
                    <p class="text-muted">No historic geospatial lookup tracking frames saved to MongoDB logs data blocks.</p>
                </div>`;
            return;
        }

        list.forEach(item => {
            gridContainer.innerHTML += `
                <div class="col-md-6 col-lg-4">
                    <div class="card history-card p-3 mb-2 cat-${item.category || 'General'}">
                        <div class="d-flex align-items-center gap-2 mb-2">
                            <span class="fs-3">${item.icon || '🔔'}</span>
                            <div>
                                <h6 class="fw-bold text-dark mb-0">${item.title}</h6>
                                <span class="badge bg-secondary-subtle text-secondary rounded-pill small" style="font-size:0.75rem;">${item.category || 'General'}</span>
                            </div>
                        </div>
                        <p class="text-secondary small mb-2" style="min-height:40px;">${item.message || item.description}</p>
                        <div class="bg-light p-2 rounded-2 small text-muted" style="font-size:0.8rem;">
                            <div class="text-truncate"><strong>📍 Location:</strong> ${item.location || 'Monitored Spot'}</div>
                            <div class="d-flex justify-content-between mt-1">
                                <span><strong>⏱️ Time:</strong> ${item.time || '00:00'}</span>
                                <span class="text-success fw-bold">● ${item.status || 'Active'}</span>
                            </div>
                        </div>
                    </div>
                </div>`;
        });
    } catch(err) {
        gridContainer.innerHTML = `<div class="col-12 text-danger text-center">Failed matching database connections sequence maps arrays channels.</div>`;
    }
}

// -------------------------------------------------------------------------
// HYDRATE AND HARNESS DASHBOARD METRIC ELEMENTS
// -------------------------------------------------------------------------
function hydrateDashboardTelemetryMetrics() {
    const cachedTelemetry = localStorage.getItem("geoalert_latest_telemetry");
    if (!cachedTelemetry) return; 

    const parsed = JSON.parse(cachedTelemetry);
    const cards = parsed.context_cards || {};
    const latest = parsed.latest_notification || {};

    if (document.getElementById("dashLastLocation")) 
        document.getElementById("dashLastLocation").innerText = parsed.location || "None Mapped";
    if (document.getElementById("dashTrafficStatus")) 
        document.getElementById("dashTrafficStatus").innerText = cards.traffic_status || "No Active Delays Mapped";
    if (document.getElementById("dashNearbyOffer")) 
        document.getElementById("dashNearbyOffer").innerText = cards.nearby_offer || "No Active Local Coupons";
    
    if (latest && latest.title) {
        if (document.getElementById("dashLatestTitle")) 
            document.getElementById("dashLatestTitle").innerText = latest.title;
        if (document.getElementById("dashLatestTime")) 
            document.getElementById("dashLatestTime").innerText = latest.time || "--:--";
        if (document.getElementById("dashLatestDesc")) 
            document.getElementById("dashLatestDesc").innerText = latest.description || latest.message || "";
    }
}

// -------------------------------------------------------------------------
// INTERNAL HELPER STRUCTS & STORAGE PERSISTENCE MECHANISMS
// -------------------------------------------------------------------------
function getSessionUserIdToken() {
    try {
        const userObj = JSON.parse(localStorage.getItem("user"));
        if (userObj && userObj.user_id) return parseInt(userObj.user_id);
    } catch(e) {}
    return 1; 
}

function saveSearchQueryToHistory(q) {
    let history = JSON.parse(localStorage.getItem("geoalert_search_history") || "[]");
    if (!history.includes(q)) {
        history.unshift(q);
        if (history.length > 6) history.pop();
        localStorage.setItem("geoalert_search_history", JSON.stringify(history));
    }
    renderSearchBadgesHistory();
}

function renderSearchBadgesHistory() {
    const historyDeck = document.getElementById("recentSearchesList");
    const dashHistoryDeck = document.getElementById("dashSearchHistoryList");
    let history = JSON.parse(localStorage.getItem("geoalert_search_history") || "[\"Gateway of India\", \"Phoenix Mall\", \"Pune Airport\"]");

    if (historyDeck) {
        historyDeck.innerHTML = "";
        history.forEach(item => {
            historyDeck.innerHTML += `<span class="badge bg-primary-subtle text-primary px-2 py-2 cursor-pointer rounded-pill shadow-sm" style="cursor:pointer;" onclick="triggerPresetSearch('${item}')">${item}</span>`;
        });
    }

    if (dashHistoryDeck) {
        dashHistoryDeck.innerHTML = "";
        history.forEach(item => {
            dashHistoryDeck.innerHTML += `
                <div class="p-2 border-bottom d-flex justify-content-between align-items-center bg-light mb-1 rounded-2">
                    <span class="text-dark fw-semibold small">📍 ${item}</span>
                    <a href="/map" class="btn btn-sm btn-link p-0 text-decoration-none" style="font-size:0.75rem;" onclick="localStorage.setItem('geoalert_pending_search', '${item}')">Trace Node</a>
                </div>`;
        });
    }
}

async function clearNotificationLogsMemory() {
    if(!confirm("Purge all recorded MongoDB tracking log historical sequences?")) return;
    try {
        await fetch(`/notifications/${getSessionUserIdToken()}`, { method: "DELETE" });
        location.reload();
    } catch(e) {}
}

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}