import http.server
import socketserver
import threading
import json
import time
import os
import Adafruit_BBIO.PWM as PWM

# --- CONFIGURATION ---
PORT = 8888
SERVO_PIN = "P1_36"

# Sonar Pins (Raw GPIO paths)
TRIG_PATH = "/sys/class/gpio/gpio59" # P2_02
ECHO_PATH = "/sys/class/gpio/gpio58" # P2_04

# --- GLOBAL STATE ---
STATE = {
    "angle": 90,
    "distance": 0,
    "mode": "AUTO",
    "scan_speed": 0.03,   # Default Faster Speed
    "manual_target": 90,
    "alarm_threshold": 30,
    "targets": {}
}

# --- HARDWARE HELPERS ---
def write_file(path, value):
    try:
        with open(path, 'w') as f:
            f.write(str(value))
    except:
        pass

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except:
        return "0"

def setup_hardware():
    print("Configuring Hardware...")
    os.system("config-pin P1_36 pwm")
    os.system("config-pin P2_02 gpio")
    os.system("config-pin P2_04 gpio")
    
    PWM.start(SERVO_PIN, 7.5, 50)
    
    write_file("/sys/class/gpio/export", "59")
    write_file("/sys/class/gpio/export", "58")
    
    try:
        with open(f"{TRIG_PATH}/direction", 'w') as f: f.write("out")
        with open(f"{ECHO_PATH}/direction", 'w') as f: f.write("in")
    except: pass

def get_distance():
    try:
        write_file(f"{TRIG_PATH}/value", "1")
        time.sleep(0.00001)
        write_file(f"{TRIG_PATH}/value", "0")
        
        with open(f"{ECHO_PATH}/value", 'r') as f:
            timeout = time.time() + 0.04
            while f.read(1) != "1":
                f.seek(0)
                if time.time() > timeout: return 0
            pulse_start = time.time()
            f.seek(0)
            while f.read(1) == "1":
                f.seek(0)
                if time.time() > timeout: return 0
            pulse_end = time.time()
            
        return int((pulse_end - pulse_start) * 17150)
    except:
        return 0

def move_servo(angle):
    # Clamp to 180 for standard servos
    if angle < 0: angle = 0
    if angle > 180: angle = 180
    
    duty = 2.5 + (angle / 18.0)
    PWM.set_duty_cycle(SERVO_PIN, duty)

# --- MAIN LOOP ---
def radar_engine():
    setup_hardware()
    print("Engine Started.")
    
    step = 3 # Increased step for speed
    direction = 1
    current_angle = 90
    
    while True:
        if STATE["mode"] == "AUTO":
            # Sweep 0 to 180
            current_angle += (step * direction)
            if current_angle >= 180: direction = -1
            if current_angle <= 0: direction = 1
            
            move_servo(current_angle)
            STATE["angle"] = current_angle
            STATE["manual_target"] = current_angle
            
            time.sleep(float(STATE["scan_speed"]))
            
        elif STATE["mode"] == "MANUAL":
            target = int(STATE["manual_target"])
            move_servo(target)
            STATE["angle"] = target
            current_angle = target
            time.sleep(0.1) 

        dist = get_distance()
        STATE["distance"] = dist
        STATE["targets"][int(STATE["angle"])] = dist
        
        # Quick Pause on Target
        if STATE["mode"] == "AUTO" and 0 < dist < int(STATE["alarm_threshold"]):
            time.sleep(0.1) 

# --- WEB SERVER ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>POCKET RADAR</title>
    <style>
        :root { --primary: #0f0; --dim: #004400; --bg: #050505; --alert: #ff0000; }
        body { background-color: var(--bg); color: var(--primary); font-family: 'Courier New', monospace; margin: 0; display: flex; flex-direction: column; align-items: center; height: 100vh; overflow: hidden; }
        
        body::before { content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06)); z-index: 2; background-size: 100% 2px, 3px 100%; pointer-events: none; }
        
        h1 { text-shadow: 0 0 10px var(--primary); margin: 10px 0; letter-spacing: 5px; border-bottom: 2px solid var(--primary); width: 100%; text-align: center; padding-bottom: 10px; }
        
        .main-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; width: 100%; max-width: 1200px; z-index: 1; }
        
        .radar-box { position: relative; width: 500px; height: 500px; border: 2px solid var(--dim); border-radius: 50%; background: radial-gradient(circle, #001100 0%, #000 70%); box-shadow: 0 0 20px var(--dim); }
        canvas { border-radius: 50%; }
        
        .controls { width: 300px; border: 1px solid var(--primary); padding: 20px; background: rgba(0, 20, 0, 0.8); box-shadow: 0 0 15px var(--dim); display: flex; flex-direction: column; gap: 15px; }
        .panel-header { background: var(--primary); color: #000; font-weight: bold; padding: 5px; text-align: center; margin-bottom: 10px; }
        
        .stat-row { display: flex; justify-content: space-between; font-size: 1.2em; border-bottom: 1px dashed var(--dim); padding-bottom: 5px; }
        .value { font-weight: bold; }
        
        input[type=range] { width: 100%; accent-color: var(--primary); cursor: pointer; }
        label { font-size: 0.8em; color: #8f8; text-transform: uppercase; }
        
        .btn-group { display: flex; gap: 10px; }
        button { flex: 1; padding: 10px; background: #002200; border: 1px solid var(--primary); color: var(--primary); font-family: inherit; cursor: pointer; transition: 0.2s; font-weight: bold; }
        button.active { background: var(--primary); color: #000; box-shadow: 0 0 15px var(--primary); }
        button:hover { background: var(--dim); }

        .log-box { width: 300px; height: 200px; border: 1px solid var(--dim); overflow-y: auto; font-size: 0.8em; padding: 5px; color: #8f8; }
        .log-entry { margin-bottom: 4px; border-left: 2px solid var(--dim); padding-left: 5px; }
        .log-alert { color: var(--alert); border-left: 2px solid var(--alert); font-weight: bold; }

        @keyframes flash { 0% { border-color: var(--primary); } 50% { border-color: var(--alert); box-shadow: 0 0 50px var(--alert); } 100% { border-color: var(--primary); } }
        .alert-mode { animation: flash 0.5s infinite; }
    </style>
</head>
<body>
    <h1>POCKET RADAR</h1>
    
    <div class="main-container">
        <div class="radar-box" id="radarFrame">
            <canvas id="radar" width="500" height="500"></canvas>
        </div>

        <div class="controls">
            <div class="panel-header">SYSTEM STATUS</div>
            <div class="stat-row"><span>BEARING:</span><span class="value" id="dispAngle">0°</span></div>
            <div class="stat-row"><span>RANGE:</span><span class="value" id="dispDist">0 cm</span></div>

            <div class="panel-header">CONTROLS</div>
            <div class="btn-group">
                <button id="btnAuto" onclick="setMode('AUTO')" class="active">AUTO SCAN</button>
                <button id="btnManual" onclick="setMode('MANUAL')">MANUAL AIM</button>
            </div>

            <div>
                <label>Manual Aiming</label>
                <input type="range" id="sliderAim" min="0" max="180" value="90" oninput="updateManual(this.value)" disabled>
            </div>

            <div>
                <label>Scan Speed</label>
                <input type="range" id="sliderSpeed" min="1" max="10" value="3" onchange="updateSpeed(this.value)">
            </div>
            
            <div>
                <label>Alarm Threshold</label>
                <input type="range" id="sliderAlarm" min="5" max="50" value="30" onchange="updateThreshold(this.value)">
            </div>

            <div class="panel-header">LOG</div>
            <div class="log-box" id="sysLog"><div class="log-entry">System Initialized...</div></div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('radar');
        const ctx = canvas.getContext('2d');
        const cx = 250, cy = 250;
        
        let config = { angle: 90, distance: 0, targets: {}, mode: 'AUTO' };
        let lastAlertTime = 0;
        let pendingManualVal = null;

        setInterval(() => {
            if (pendingManualVal !== null) {
                fetch('/config', { method: 'POST', body: JSON.stringify({ manual_target: pendingManualVal }) });
                pendingManualVal = null;
            }
        }, 150);

        function updateManual(val) {
            document.getElementById('dispAngle').innerText = val + "°";
            pendingManualVal = parseInt(val);
        }

        function setMode(mode) {
            fetch('/config', { method: 'POST', body: JSON.stringify({ mode: mode }) });
            document.getElementById('btnAuto').className = mode === 'AUTO' ? 'active' : '';
            document.getElementById('btnManual').className = mode === 'MANUAL' ? 'active' : '';
            document.getElementById('sliderAim').disabled = (mode === 'AUTO');
        }

        function updateSpeed(val) {
            let speed = val / 100.0;
            fetch('/config', { method: 'POST', body: JSON.stringify({ scan_speed: speed }) });
        }
        
        function updateThreshold(val) {
            fetch('/config', { method: 'POST', body: JSON.stringify({ alarm_threshold: parseInt(val) }) });
        }

        function logEvent(msg, isAlert=false) {
            const box = document.getElementById('sysLog');
            const div = document.createElement('div');
            div.className = isAlert ? 'log-entry log-alert' : 'log-entry';
            div.innerText = msg;
            box.insertBefore(div, box.firstChild);
            if(box.children.length > 20) box.removeChild(box.lastChild);
        }

        function drawRadar() {
            ctx.fillStyle = 'rgba(0, 15, 0, 0.1)'; ctx.fillRect(0,0,500,500);
            
            // Grid
            ctx.strokeStyle = '#003300'; ctx.lineWidth = 1;
            for(let r=50; r<250; r+=50) { 
                ctx.beginPath(); ctx.arc(cx,cy,r,0,6.3); ctx.stroke(); 
                ctx.fillStyle = '#005500'; ctx.fillText(r/5 + "cm", cx+5, cy-r+10);
            }
            
            // Sweep Line (180 deg logic: 0=Right, 180=Left)
            // Map 0-180 servo to 0-PI radians (Right to Left counter-clockwise)
            let rad = (config.angle * Math.PI) / 180; 
            
            // NOTE: Canvas Y is inverted. To sweep Top-Half, we negate Y sin
            // 0 deg (Right) -> cos=1, sin=0
            // 90 deg (Up) -> cos=0, sin=1 -> We want Y to decrease
            // 180 deg (Left) -> cos=-1, sin=0
            
            let lineX = cx + Math.cos(rad)*250;
            let lineY = cy - Math.sin(rad)*250;

            ctx.strokeStyle = '#0f0'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(cx,cy);
            ctx.lineTo(lineX, lineY);
            ctx.stroke();

            // Targets
            let alertActive = false;
            for(let ang in config.targets) {
                let d = config.targets[ang];
                if(d > 0 && d < 60) { 
                    let r = (ang * Math.PI) / 180;
                    let distPx = (d / 60) * 250;
                    let tx = cx + Math.cos(r) * distPx;
                    let ty = cy - Math.sin(r) * distPx; // Invert Y
                    
                    let isDanger = d < document.getElementById('sliderAlarm').value;
                    ctx.fillStyle = isDanger ? '#ff0000' : '#ffff00';
                    let size = isDanger ? 6 : 4;
                    
                    ctx.beginPath(); ctx.arc(tx, ty, size, 0, 6.3); ctx.fill();
                    
                    if(isDanger && Math.abs(ang - config.angle) < 5) {
                        alertActive = true;
                        if(Date.now() - lastAlertTime > 2000) {
                            logEvent(`TARGET: ${ang}° @ ${d}cm`, true);
                            lastAlertTime = Date.now();
                        }
                    }
                }
            }
            
            const frame = document.getElementById('radarFrame');
            if(alertActive) frame.classList.add('alert-mode');
            else frame.classList.remove('alert-mode');
        }

        setInterval(() => {
            fetch('/data').then(r => r.json()).then(d => {
                config = d;
                document.getElementById('dispAngle').innerText = d.angle + "°";
                document.getElementById('dispDist').innerText = d.distance + " cm";
                if (config.mode === 'AUTO') {
                    document.getElementById('sliderAim').value = d.angle;
                }
                drawRadar();
            });
        }, 100);
    </script>
</body>
</html>
"""

class RadarHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_UI.encode('utf-8'))
        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(STATE).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/config':
            length = int(self.headers.get('Content-Length', 0))
            if length > 0:
                data = json.loads(self.rfile.read(length))
                for key in data:
                    if key in STATE:
                        STATE[key] = data[key]
            self.send_response(200)
            self.end_headers()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    try:
        t = threading.Thread(target=radar_engine)
        t.daemon = True
        t.start()
        print(f"COMMAND CENTER ONLINE @ http://192.168.6.2:{PORT}")
        ReusableTCPServer(("", PORT), RadarHandler).serve_forever()
    except KeyboardInterrupt:
        PWM.stop(SERVO_PIN)
        PWM.cleanup()
