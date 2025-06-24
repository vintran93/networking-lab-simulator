
from flask import Flask, render_template, request, jsonify, session
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

class NetworkLabSimulation:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'listA1': [], 'listA3': [], 'listA4': [], 'listA5': [],
            'listA6': [], 'listA8': [], 'listA9': [], 'listA10': [],
            'listS': [], 'current_mode': 'menu', 'current_switch': None
        }
        return session_id
    
    def get_session(self, session_id):
        return self.sessions.get(session_id, {})
    
    def get_correct_answers_sw12(self):
        return [
            "enable", "config t", "int e0/1",
            "switchport trunk allowed vlan 56, 77, 99",
            "int e0/2", "switchport trunk allowed vlan 56, 77, 99",
            "exit", "int e0/1", "switchport trunk native vlan 99",
            "end", "wr"
        ]
    
    def get_correct_answers_sw34(self):
        return [
            "enable", "config t", "int range e0-1",
            "channel-group 34 mode active", "exit", "int po 34",
            "switchport trunk allowed vlan 56, 77, 99",
            "int e0/2", "switchport trunk allowed vlan 56, 77, 99",
            "end", "wr"
        ]
    
    def process_command(self, session_id, command):
        session_data = self.get_session(session_id)
        if not session_data:
            return {"error": "Session not found"}
        
        response = {"output": "", "mode": session_data['current_mode']}
        
        if session_data['current_mode'] == 'menu':
            response = self.handle_menu(session_data, command)
        elif session_data['current_mode'] == 'switch_selection':
            response = self.handle_switch_selection(session_data, command)
        elif session_data['current_mode'].startswith('configuring_'):
            response = self.handle_configuration(session_data, command)
        
        return response
    
    def handle_menu(self, session_data, command):
        if command.lower() == 's':
            session_data['current_mode'] = 'switch_selection'
            return {
                "output": "Processing...\nStart -->\n\nSW1 = 1, SW2 = 2, SW3 = 3, SW4 = 4\nChoose a switch to begin. Or press q to quit:",
                "mode": "switch_selection"
            }
        elif command.lower() == 'h':
            return {
                "output": "** HELP **\nChoose a switch to begin. You will configure 4 switches from the network topology.\n\nh = help\nx = exit\ns = start\nEnter an option:",
                "mode": "menu"
            }
        elif command.lower() == 'x':
            return {"output": "See you later!", "mode": "exit"}
        else:
            return {
                "output": "Option not available!\n\nh = help\nx = exit\ns = start\nEnter an option:",
                "mode": "menu"
            }
    
    def handle_switch_selection(self, session_data, command):
        if command.lower() == 'q':
            session_data['current_mode'] = 'menu'
            return {
                "output": "h = help\nx = exit\ns = start\nEnter an option:",
                "mode": "menu"
            }
        
        try:
            switch_num = int(command)
            if switch_num in [1, 2, 3, 4]:
                session_data['current_switch'] = switch_num
                session_data['current_mode'] = f'configuring_SW{switch_num}'
                return {
                    "output": f"Configuring SW{switch_num}\nEnter configuration commands (type 'done' when finished):",
                    "mode": f"configuring_SW{switch_num}"
                }
            else:
                return {
                    "output": "Not a valid option. Please try again.\n\nSW1 = 1, SW2 = 2, SW3 = 3, SW4 = 4\nChoose a switch to begin. Or press q to quit:",
                    "mode": "switch_selection"
                }
        except ValueError:
            return {
                "output": "You must enter a valid switch number\n\nSW1 = 1, SW2 = 2, SW3 = 3, SW4 = 4\nChoose a switch to begin. Or press q to quit:",
                "mode": "switch_selection"
            }
    
    def handle_configuration(self, session_data, command):
        if command.lower() == 'done':
            return self.check_configuration(session_data)
        else:
            switch_num = session_data['current_switch']
            list_key = f'listA{1 if switch_num == 1 else 4 if switch_num == 2 else 6 if switch_num == 3 else 9}'
            session_data[list_key].append(command)
            return {
                "output": f"SW{switch_num}> {command}",
                "mode": session_data['current_mode']
            }
    
    def check_configuration(self, session_data):
        switch_num = session_data['current_switch']
        
        if switch_num in [1, 2]:
            correct_answers = self.get_correct_answers_sw12()
            if switch_num == 1:
                user_answers = session_data['listA1']
                correct_list = 'listA3'
                switch_letter = 'a'
            else:
                user_answers = session_data['listA4']
                correct_list = 'listA5'
                switch_letter = 'b'
        else:
            correct_answers = self.get_correct_answers_sw34()
            if switch_num == 3:
                user_answers = session_data['listA6']
                correct_list = 'listA8'
                switch_letter = 'c'
            else:
                user_answers = session_data['listA9']
                correct_list = 'listA10'
                switch_letter = 'd'
        
        # Check answers
        for cmd in user_answers:
            if cmd in correct_answers:
                session_data[correct_list].append(cmd)
        
        if set(session_data[correct_list]) == set(correct_answers):
            session_data['listS'].append(switch_letter)
            result = f"SW{switch_num} configuration is CORRECT!"
        else:
            result = f"SW{switch_num} configuration is INCORRECT!"
            # Clear incorrect attempts
            if switch_num == 1:
                session_data['listA1'].clear()
                session_data['listA3'].clear()
            elif switch_num == 2:
                session_data['listA4'].clear()
                session_data['listA5'].clear()
            elif switch_num == 3:
                session_data['listA6'].clear()
                session_data['listA8'].clear()
            else:
                session_data['listA9'].clear()
                session_data['listA10'].clear()
        
        # Check if all switches are configured
        if len(session_data['listS']) == 4:
            result += "\n\n🎉 CONGRATULATIONS! 🎉\nYou have completed all switch configurations!\nThe lab is completed!"
            session_data['current_mode'] = 'completed'
        else:
            result += f"\n\nProgress: {len(session_data['listS'])}/4 switches configured"
            result += "\n\nSW1 = 1, SW2 = 2, SW3 = 3, SW4 = 4\nChoose a switch to begin. Or press q to quit:"
            session_data['current_mode'] = 'switch_selection'
        
        return {"output": result, "mode": session_data['current_mode']}

# Initialize the simulation
lab_sim = NetworkLabSimulation()

@app.route('/')
def index():
    # Create a new session
    session_id = lab_sim.create_session()
    session['lab_session_id'] = session_id
    
    return render_template('lab_simulation.html')

@app.route('/command', methods=['POST'])
def process_command():
    data = request.get_json()
    command = data.get('command', '')
    
    session_id = session.get('lab_session_id')
    if not session_id:
        return jsonify({"error": "No session found"})
    
    response = lab_sim.process_command(session_id, command)
    return jsonify(response)

# Create templates/lab_simulation.html
@app.route('/create_template')
def create_template():
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Networking Lab Simulation</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background-color: #1e1e1e;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .terminal {
            background-color: #2d2d2d;
            border-radius: 8px;
            padding: 20px;
            height: 600px;
            overflow-y: auto;
            border: 2px solid #444;
        }
        .network-diagram {
            background-color: #2d2d2d;
            border-radius: 8px;
            padding: 20px;
            border: 2px solid #444;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .switch {
            width: 120px;
            height: 60px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            margin: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .topology {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 20px;
            width: 300px;
            height: 200px;
        }
        #output {
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.4;
            margin-bottom: 20px;
        }
        .input-area {
            background-color: #333;
            padding: 10px;
            border-radius: 4px;
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            background-color: #444;
            color: white;
            border: 1px solid #666;
            padding: 8px;
            border-radius: 4px;
            flex-grow: 1;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="terminal">
            <h2>Networking Lab Simulation</h2>
            <div id="output">Welcome to the Networking Lab Simulation!

Tasks - All physical cabling is in place and verified.
Connectivity between all four switches must be established and operational.
All ports are pre-configured as 802.1q trunks.

1. Configure both SW-1 and SW2 ports e0/1 and e0/2 to permit only the allowed VLANs
2. Configure both SW-1 and SW-2 e0/1 ports to send and receive untagged traffic over VLAN99
3. Configure both SW-3 and SW-4 ports e0/2 to permit only the allowed VLANs
4. Configure both SW-3 and SW-4 ports e0/0 and e0/1 for link aggregation using the industry standard protocol
5. Permit only the allowed VLANs on the new link

h = help
x = exit
s = start

Enter an option:</div>
            <div class="input-area">
                <input type="text" id="command-input" placeholder="Enter command...">
                <button onclick="sendCommand()">Send</button>
            </div>
        </div>
        
        <div class="network-diagram">
            <div class="topology">
                <div class="switch">SW-1</div>
                <div class="switch">SW-2</div>
                <div class="switch">SW-3</div>
                <div class="switch">SW-4</div>
            </div>
        </div>
    </div>

    <script>
        function sendCommand() {
            const input = document.getElementById('command-input');
            const command = input.value.trim();
            if (!command) return;
            
            // Clear input
            input.value = '';
            
            // Send command to server
            fetch('/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({command: command})
            })
            .then(response => response.json())
            .then(data => {
                const output = document.getElementById('output');
                output.textContent += '\\n> ' + command + '\\n' + data.output + '\\n';
                output.scrollTop = output.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        
        // Handle Enter key
        document.getElementById('command-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendCommand();
            }
        });
    </script>
</body>
</html>'''
    
    # You need to create templates directory and save this as lab_simulation.html
    return f"<pre>{template_content}</pre>"

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)