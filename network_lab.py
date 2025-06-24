from flask import Flask, render_template_string, request, jsonify, session
import secrets
import webbrowser
import threading
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

class NetworkLabSim:
    def __init__(self):
        # Correct answers for SW1 and SW2
        self.sw1_sw2_answers = [
            "enable",
            "config t",
            "int e0/1",
            "switchport trunk allowed vlan 56, 77, 99",
            "int e0/2",
            "switchport trunk allowed vlan 56, 77, 99",
            "exit",
            "int e0/1",
            "switchport trunk native vlan 99",
            "end",
            "wr"
        ]
        
        # Correct answers for SW3 and SW4
        self.sw3_sw4_answers = [
            "enable",
            "config t",
            "int range e0-1",
            "channel-group 34 mode active",
            "exit",
            "int po 34",
            "switchport trunk allowed vlan 56, 77, 99",
            "int e0/2",
            "switchport trunk allowed vlan 56, 77, 99",
            "end",
            "wr"
        ]
    
    def check_configuration(self, switch_number, commands):
        if switch_number in [1, 2]:
            correct_answers = self.sw1_sw2_answers
        else:
            correct_answers = self.sw3_sw4_answers
        
        correct_commands = []
        for cmd in commands:
            if cmd in correct_answers:
                correct_commands.append(cmd)
        
        is_correct = set(correct_commands) == set(correct_answers)
        missing_commands = set(correct_answers) - set(correct_commands)
        
        return {
            'is_correct': is_correct,
            'correct_commands': correct_commands,
            'missing_commands': list(missing_commands),
            'total_required': len(correct_answers),
            'total_correct': len(correct_commands)
        }

# Initialize the simulation
lab_sim = NetworkLabSim()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Lab Simulation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e);
            color: #00ff41;
            min-height: 100vh;
            padding: 20px;
            animation: backgroundShift 10s ease-in-out infinite;
        }

        @keyframes backgroundShift {
            0%, 100% { background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e); }
            50% { background: linear-gradient(135deg, #16213e, #0f0f23, #1a1a2e); }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff41;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 50px rgba(0, 255, 65, 0.3);
            backdrop-filter: blur(10px);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #00ff41;
            text-shadow: 0 0 20px #00ff41;
            font-size: 2.8em;
            margin-bottom: 10px;
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 20px #00ff41; }
            to { text-shadow: 0 0 30px #00ff41, 0 0 40px #00ff41; }
        }

        .lab-info {
            background: rgba(0, 17, 0, 0.6);
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .lab-info h3 {
            color: #00ff41;
            margin-bottom: 15px;
            text-decoration: underline;
        }

        .lab-info ol {
            padding-left: 20px;
            line-height: 1.6;
        }

        .lab-info li {
            margin-bottom: 5px;
        }

        .progress-section {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .progress-bar {
            background: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            height: 30px;
            position: relative;
            overflow: hidden;
        }

        .progress-fill {
            background: linear-gradient(90deg, #00ff41, #00cc33);
            height: 100%;
            border-radius: 10px;
            transition: width 0.8s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000;
            font-weight: bold;
            position: relative;
        }

        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .switch-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .switch-card {
            background: rgba(0, 17, 0, 0.6);
            border: 2px solid #00ff41;
            border-radius: 10px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .switch-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 255, 65, 0.4);
            border-color: #00cc33;
        }

        .switch-card.completed {
            border-color: #00ff41;
            background: rgba(0, 255, 65, 0.1);
        }

        .switch-card.completed::after {
            content: '✓';
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 24px;
            color: #00ff41;
            font-weight: bold;
        }

        .switch-card h3 {
            color: #00ff41;
            margin-bottom: 10px;
            font-size: 1.5em;
        }

        .switch-card p {
            color: #88ffaa;
            line-height: 1.4;
        }

        .terminal {
            background: rgba(0, 17, 0, 0.9);
            border: 1px solid #00ff41;
            border-radius: 10px;
            height: 400px;
            overflow-y: auto;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 14px;
            line-height: 1.6;
            display: none;
        }

        .terminal.active {
            display: block;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .terminal::-webkit-scrollbar {
            width: 8px;
        }

        .terminal::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }

        .terminal::-webkit-scrollbar-thumb {
            background: #00ff41;
            border-radius: 4px;
        }

        .input-section {
            display: flex;
            gap: 10px;
            align-items: center;
            background: rgba(0, 17, 0, 0.5);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #00ff41;
        }

        .prompt-label {
            color: #00ff41;
            font-weight: bold;
            white-space: nowrap;
            min-width: 60px;
        }

        #command-input {
            flex: 1;
            background: transparent;
            border: none;
            color: #00ff41;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            outline: none;
        }

        #command-input::placeholder {
            color: rgba(0, 255, 65, 0.5);
        }

        .btn-group {
            display: flex;
            gap: 10px;
        }

        .btn {
            background: linear-gradient(45deg, #00ff41, #00cc33);
            color: #000;
            border: none;
            padding: 12px 20px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            border-radius: 8px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }

        .btn:hover {
            background: linear-gradient(45deg, #00cc33, #009929);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 65, 0.4);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .output-line {
            margin-bottom: 5px;
            animation: typewriter 0.1s ease;
        }

        @keyframes typewriter {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .success { color: #00ff41; font-weight: bold; }
        .error { color: #ff4444; font-weight: bold; }
        .warning { color: #ffaa00; }
        .info { color: #4488ff; }
        .command { color: #88ffaa; }

        .hidden { display: none; }

        .completion-message {
            background: linear-gradient(45deg, #00ff41, #00cc33);
            color: #000;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
            margin: 20px 0;
            animation: celebration 1s ease-in-out;
        }

        @keyframes celebration {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .back-btn {
            background: linear-gradient(45deg, #ff6b35, #f7931e);
            margin-right: 10px;
        }

        .back-btn:hover {
            background: linear-gradient(45deg, #f7931e, #ff6b35);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Network Lab Simulation 🌐</h1>
        </div>

        <div class="topology-section">
            <h3>Network Topology</h3>
            <div class="topology-diagram">
                <img src="images/labsim1.jpg">
            </div>
        </div>  

        <div class="lab-info">
            <h3>📋 Lab Tasks</h3>
            <p><strong>All physical cabling is in place and verified.</strong></p>
            <p><strong>Connectivity between all four switches must be established and operational.</strong></p>
            <p><strong>All ports are pre-configured as 802.1q trunks.</strong></p>
            <br>
            <ol>
                <li>Configure both SW-1 and SW-2 ports e0/1 and e0/2 to permit only the allowed VLANs</li>
                <li>Configure both SW-1 and SW-2 e0/1 ports to send and receive untagged traffic over VLAN99</li>
                <li>Configure both SW-3 and SW-4 ports e0/2 to permit only the allowed VLANs</li>
                <li>Configure both SW-3 and SW-4 ports e0/0 and e0/1 for link aggregation using the industry standard protocol</li>
                <li>Permit only the allowed VLANs on the new link</li>
            </ol>
        </div>

        <div class="progress-section">
            <h3>📊 Progress</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width: 0%">0/4 Switches Completed</div>
            </div>
        </div>

        <div id="switch-selection" class="switch-grid">
            <div class="switch-card" onclick="selectSwitch(1)">
                <h3>🔌 SW-1</h3>
                <p>Configure trunk ports e0/1 and e0/2 with allowed VLANs and set native VLAN for e0/1</p>
            </div>
            <div class="switch-card" onclick="selectSwitch(2)">
                <h3>🔌 SW-2</h3>
                <p>Configure trunk ports e0/1 and e0/2 with allowed VLANs and set native VLAN for e0/1</p>
            </div>
            <div class="switch-card" onclick="selectSwitch(3)">
                <h3>🔌 SW-3</h3>
                <p>Configure link aggregation on e0/0-e0/1 and trunk port e0/2 with allowed VLANs</p>
            </div>
            <div class="switch-card" onclick="selectSwitch(4)">
                <h3>🔌 SW-4</h3>
                <p>Configure link aggregation on e0/0-e0/1 and trunk port e0/2 with allowed VLANs</p>
            </div>
        </div>

        <div id="terminal-section" class="hidden">
            <div class="terminal" id="terminal"></div>
            <div class="input-section">
                <div class="prompt-label" id="prompt">SW#></div>
                <input type="text" id="command-input" placeholder="Enter Cisco IOS command..." autocomplete="off">
                <div class="btn-group">
                    <button class="btn back-btn" onclick="backToSwitchSelection()">Back</button>
                    <button class="btn" onclick="submitCommand()">Submit</button>
                    <button class="btn" onclick="finishConfiguration()">Done</button>
                </div>
            </div>
        </div>

        <div id="completion-message" class="completion-message hidden">
            🎉 CONGRATULATIONS! 🎉<br>
            All switch configurations completed! Lab finished successfully!
        </div>
    </div>

    <script>
        let currentSwitch = null;
        let switchCommands = {1: [], 2: [], 3: [], 4: []};
        let completedSwitches = new Set();

        function selectSwitch(switchNumber) {
            currentSwitch = switchNumber;
            document.getElementById('switch-selection').style.display = 'none';
            document.getElementById('terminal-section').classList.remove('hidden');
            document.getElementById('terminal-section').querySelector('.terminal').classList.add('active');
            
            const prompt = document.getElementById('prompt');
            prompt.textContent = `SW${switchNumber}#`;
            
            const terminal = document.getElementById('terminal');
            terminal.innerHTML = `<div class="output-line info">🔧 Configuring SW${switchNumber}</div>
                                <div class="output-line">Enter Cisco IOS commands one by one.</div>
                                <div class="output-line">Type commands and click Submit or press Enter.</div>
                                <div class="output-line">Click Done when you finish configuring this switch.</div>
                                <div class="output-line">─────────────────────────────────────────</div>`;
            
            document.getElementById('command-input').focus();
        }

        function backToSwitchSelection() {
            document.getElementById('terminal-section').classList.add('hidden');
            document.getElementById('switch-selection').style.display = 'grid';
            currentSwitch = null;
        }

        function submitCommand() {
            const input = document.getElementById('command-input');
            const command = input.value.trim();
            
            if (command && currentSwitch) {
                switchCommands[currentSwitch].push(command);
                
                const terminal = document.getElementById('terminal');
                terminal.innerHTML += `<div class="output-line command">SW${currentSwitch}# ${command}</div>`;
                terminal.scrollTop = terminal.scrollHeight;
                
                input.value = '';
                input.focus();
            }
        }

        function finishConfiguration() {
            if (currentSwitch && switchCommands[currentSwitch].length > 0) {
                fetch('/check_configuration', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        switch_number: currentSwitch,
                        commands: switchCommands[currentSwitch]
                    })
                })
                .then(response => response.json())
                .then(data => {
                    const terminal = document.getElementById('terminal');
                    
                    if (data.is_correct) {
                        terminal.innerHTML += `<div class="output-line success">✅ SW${currentSwitch} configuration CORRECT!</div>`;
                        terminal.innerHTML += `<div class="output-line success">All required commands executed successfully.</div>`;
                        completedSwitches.add(currentSwitch);
                        
                        // Mark switch as completed
                        const switchCards = document.querySelectorAll('.switch-card');
                        switchCards[currentSwitch - 1].classList.add('completed');
                        
                        updateProgress();
                        
                        if (completedSwitches.size === 4) {
                            setTimeout(() => {
                                document.getElementById('completion-message').classList.remove('hidden');
                                document.getElementById('terminal-section').classList.add('hidden');
                                document.getElementById('switch-selection').style.display = 'none';
                            }, 2000);
                        } else {
                            setTimeout(() => {
                                backToSwitchSelection();
                            }, 3000);
                        }
                    } else {
                        terminal.innerHTML += `<div class="output-line error">❌ SW${currentSwitch} configuration INCORRECT!</div>`;
                        terminal.innerHTML += `<div class="output-line error">Correct commands: ${data.total_correct}/${data.total_required}</div>`;
                        if (data.missing_commands.length > 0) {
                            terminal.innerHTML += `<div class="output-line warning">Missing commands:</div>`;
                            data.missing_commands.forEach(cmd => {
                                terminal.innerHTML += `<div class="output-line warning">  - ${cmd}</div>`;
                            });
                        }
                        terminal.innerHTML += `<div class="output-line info">Please try again with the correct commands.</div>`;
                        
                        // Reset commands for this switch
                        switchCommands[currentSwitch] = [];
                    }
                    
                    terminal.scrollTop = terminal.scrollHeight;
                });
            }
        }

        function updateProgress() {
            const progress = (completedSwitches.size / 4) * 100;
            const progressFill = document.getElementById('progress-fill');
            progressFill.style.width = progress + '%';
            progressFill.textContent = `${completedSwitches.size}/4 Switches Completed`;
        }

        // Enter key support
        document.getElementById('command-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                submitCommand();
            }
        });

        // Focus input when terminal is clicked
        document.getElementById('terminal').addEventListener('click', function() {
            document.getElementById('command-input').focus();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    # Initialize session
    if 'completed_switches' not in session:
        session['completed_switches'] = []
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/check_configuration', methods=['POST'])
def check_configuration():
    data = request.get_json()
    switch_number = data.get('switch_number')
    commands = data.get('commands', [])
    
    result = lab_sim.check_configuration(switch_number, commands)
    
    if result['is_correct']:
        if 'completed_switches' not in session:
            session['completed_switches'] = []
        
        if switch_number not in session['completed_switches']:
            session['completed_switches'].append(switch_number)
            session.permanent = True
    
    return jsonify(result)

def open_browser():
    """Open the web browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("🌐 Starting Network Lab Simulation...")
    print("📡 Server starting on http://127.0.0.1:5000")
    print("🚀 Opening web browser...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the Flask app
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for using Network Lab Simulation!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure Flask is installed: pip install flask")