let currentUser = null;

const menuOptions = {
    'admin': [
        {title: 'Dashboard', action: 'dashboard', desc: 'Overview & stats'},
        {title: 'Insert Record', action: 'insert', desc: 'Add new data'},
        {title: 'Waste Distribution', action: 'distribution', desc: 'Type analysis'},
        {title: 'Carbon Reports', action: 'carbon', desc: 'Emissions tracking'},
        {title: 'Location Analysis', action: 'location', desc: 'Geographic data'},
        {title: 'Trend Forecast', action: 'forecast', desc: 'Future predictions'},
        {title: 'Export Data', action: 'export', desc: 'Download reports'}
    ],
    'waste collector': [
        {title: 'Dashboard', action: 'dashboard', desc: 'Overview & stats'},
        {title: 'Insert Record', action: 'insert', desc: 'Add new data'},
        {title: 'Waste Distribution', action: 'distribution', desc: 'Type analysis'},
        {title: 'Location Analysis', action: 'location', desc: 'Geographic data'}
    ],
    'municipal officer': [
        {title: 'Dashboard', action: 'dashboard', desc: 'Overview & stats'},
        {title: 'Waste Distribution', action: 'distribution', desc: 'Type analysis'},
        {title: 'Carbon Reports', action: 'carbon', desc: 'Emissions tracking'},
        {title: 'Location Analysis', action: 'location', desc: 'Geographic data'},
        {title: 'Trend Forecast', action: 'forecast', desc: 'Future predictions'},
        {title: 'Export Data', action: 'export', desc: 'Download reports'}
    ],
    'household/institution': [
        {title: 'Dashboard', action: 'dashboard', desc: 'Overview & stats'},
        {title: 'Waste Distribution', action: 'distribution', desc: 'Type analysis'},
        {title: 'Carbon Reports', action: 'carbon', desc: 'Emissions tracking'},
        {title: 'Location Analysis', action: 'location', desc: 'Geographic data'}
    ]
};

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const credentials = {
        'admin': 'admin123',
        'waste collector': 'collector123',
        'municipal officer': 'officer123',
        'household/institution': 'user123'
    };

    if (credentials[username] === password) {
        currentUser = username;
        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('main-content').classList.remove('hidden');
        document.getElementById('user-role').textContent = `Logged in as: ${username}`;
        loadMenu();
        executeAction('dashboard');
    } else {
        alert('Invalid credentials! Please check username and password.');
    }
}

function logout() {
    currentUser = null;
    document.getElementById('login-section').classList.remove('hidden');
    document.getElementById('main-content').classList.add('hidden');
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}

function loadMenu() {
    const menuSection = document.getElementById('menu-section');
    const options = menuOptions[currentUser] || [];
    
    let html = '<div class="menu-grid">';
    options.forEach(option => {
        html += `
            <div class="menu-item" onclick="executeAction('${option.action}')">
                <h3>${option.title}</h3>
                <p>${option.desc}</p>
            </div>
        `;
    });
    html += '</div>';
    
    menuSection.innerHTML = html;
}

function executeAction(action) {
    switch(action) {
        case 'dashboard':
            window.show_dashboard();
            break;
        case 'distribution':
            window.show_waste_distribution();
            break;
        case 'carbon':
            window.show_carbon_reports();
            break;
        case 'location':
            window.show_location_analysis();
            break;
        case 'forecast':
            window.show_trend_forecast();
            break;
        case 'insert':
            showInsertForm();
            break;
        case 'export':
            showExportOptions();
            break;
    }
}

function showInsertForm() {
    const content = document.getElementById('content-section');
    content.innerHTML = `
        <h2>Insert New Waste Record</h2>
        <div class="alert alert-info">
            Fill in all fields to record a new waste entry
        </div>
        <div class="form-group">
            <label>Year</label>
            <input type="number" id="year" value="2025" min="2020" max="2030">
        </div>
        <div class="form-group">
            <label>Month</label>
            <input type="number" id="month" placeholder="1-12" min="1" max="12" value="1">
        </div>
        <div class="form-group">
            <label>Date</label>
            <input type="number" id="date" placeholder="1-31" min="1" max="31" value="1">
        </div>
        <div class="form-group">
            <label>Location (City)</label>
            <select id="location">
                <option>Mumbai</option>
                <option>Delhi</option>
                <option>Pune</option>
                <option>Bengaluru</option>
                <option>Chennai</option>
                <option>Hyderabad</option>
                <option>Kolkata</option>
                <option>Ahmedabad</option>
            </select>
        </div>
        <div class="form-group">
            <label>Waste Type</label>
            <select id="waste-type">
                <option>Plastic</option>
                <option>Organic</option>
                <option>Glass</option>
                <option>E-Waste</option>
                <option>Hazardous</option>
                <option>Paper</option>
            </select>
        </div>
        <div class="form-group">
            <label>Waste Source</label>
            <select id="waste-source">
                <option>household</option>
                <option>commercial</option>
                <option>industrial</option>
                <option>institution</option>
                <option>municipal</option>
            </select>
        </div>
        <div class="form-group">
            <label>Quantity (kg)</label>
            <input type="number" id="quantity" placeholder="Enter quantity" step="0.1" min="0">
        </div>
        <button class="btn btn-success" onclick="submitRecord()">Submit Record</button>
    `;
}

function submitRecord() {
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const date = document.getElementById('date').value;
    const location = document.getElementById('location').value;
    const wasteType = document.getElementById('waste-type').value;
    const wasteSource = document.getElementById('waste-source').value;
    const quantity = document.getElementById('quantity').value;

    if (!quantity || parseFloat(quantity) <= 0) {
        alert('Please enter a valid quantity');
        return;
    }

    const emissionFactors = {
        'Plastic': 6.0,
        'Organic': 0.2,
        'Glass': 0.5,
        'E-Waste': 2.5,
        'Hazardous': 4.0,
        'Paper': 1.5
    };

    const carbon = parseFloat(quantity) * emissionFactors[wasteType];

    const content = document.getElementById('content-section');
    content.innerHTML = `
        <div class="alert alert-success">
            <h3>Record Successfully Added!</h3>
            <p><strong>Date:</strong> ${year}-${month}-${date}</p>
            <p><strong>Location:</strong> ${location}</p>
            <p><strong>Waste Type:</strong> ${wasteType}</p>
            <p><strong>Source:</strong> ${wasteSource}</p>
            <p><strong>Quantity:</strong> ${quantity} kg</p>
            <p><strong>Carbon Footprint:</strong> ${carbon.toFixed(2)} kg CO2</p>
        </div>
        <button class="btn" onclick="showInsertForm()">Add Another Record</button>
        <button class="btn btn-secondary" onclick="executeAction('dashboard')">Back to Dashboard</button>
    `;
}

function showExportOptions() {
    const content = document.getElementById('content-section');
    content.innerHTML = `
        <h2>Export Data & Reports</h2>
        <div class="alert alert-info">
            Download your waste management data in various formats
        </div>
        
        <div style="margin-top: 30px;">
            <h3>Available Export Options:</h3>
            <div class="export-buttons">
                <button class="btn btn-success" onclick="window.export_csv()">
                    Export Full Dataset (CSV)
                </button>
                <button class="btn" onclick="window.export_summary()">
                    Export Summary Report
                </button>
            </div>
        </div>

        <div style="margin-top: 30px; padding: 20px; background: #f0f4f8; border-radius: 12px;">
            <h4>Export Information:</h4>
            <ul style="margin-top: 10px; line-height: 1.8;">
                <li><strong>CSV Export:</strong> Complete dataset with all records</li>
                <li><strong>Summary Report:</strong> Statistical overview and key insights</li>
                <li>Check your browser console for exported data</li>
                <li>In a full implementation, files would download automatically</li>
            </ul>
        </div>
    `;
}