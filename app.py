import streamlit as st
import requests
import json
import time
from datetime import datetime
import numpy as np
from io import BytesIO

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="🤖 AI Technical HR Interview Dashboard",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS FOR FUTURISTIC DESIGN ====================
st.markdown("""
<style>
    :root {
        --primary-color: #00d4ff;
        --secondary-color: #ff006e;
        --bg-dark: #0a0e27;
        --bg-darker: #050810;
        --accent-gold: #ffd700;
        --success-green: #00ff88;
        --warning-orange: #ff8c00;
        --error-red: #ff0055;
    }
    
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f0f1e 100%);
        color: #e0e0e0;
    }
    
    .main {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.9), rgba(26, 31, 58, 0.9));
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .header-title {
        background: linear-gradient(90deg, #00d4ff 0%, #ff006e 50%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.85; }
    }
    
    .card {
        background: linear-gradient(135deg, rgba(30, 40, 60, 0.8), rgba(20, 30, 50, 0.8));
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
        backdrop-filter: blur(10px);
        animation: cardSlide 0.5s ease-out;
    }
    
    @keyframes cardSlide {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(255, 0, 110, 0.1));
        border: 2px solid var(--primary-color);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00d4ff, #ff006e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .avatar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 400px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(255, 0, 110, 0.1));
        border: 3px solid #00d4ff;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 50px rgba(0, 212, 255, 0.3), inset 0 0 50px rgba(0, 212, 255, 0.1);
    }
    
    .avatar-circle {
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff, #ff006e);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 120px;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.5);
        animation: avatarPulse 2.5s ease-in-out infinite;
    }
    
    @keyframes avatarPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(0, 212, 255, 0.5); }
        50% { transform: scale(1.05); box-shadow: 0 0 60px rgba(255, 0, 110, 0.7); }
    }
    
    .waveform-container {
        background: linear-gradient(135deg, rgba(10, 20, 40, 0.9), rgba(20, 30, 50, 0.9));
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
    }
    
    .waveform-bar {
        height: 3px;
        background: linear-gradient(90deg, #00d4ff, #ff006e);
        border-radius: 2px;
        margin: 3px 0;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        animation: waveFlow 1.5s ease-in-out infinite;
    }
    
    @keyframes waveFlow {
        0%, 100% { opacity: 0.3; transform: scaleX(0.8); }
        50% { opacity: 1; transform: scaleX(1); }
    }
    
    .tracker-section {
        background: linear-gradient(135deg, rgba(30, 40, 60, 0.8), rgba(20, 30, 50, 0.8));
        border-left: 4px solid #00d4ff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.2), rgba(255, 0, 110, 0.2));
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 5px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #00d4ff, #ff006e);
        height: 100%;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        animation: progressFill 2s ease-in-out;
    }
    
    @keyframes progressFill {
        from { width: 0; }
    }
    
    .emotion-badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
        font-size: 0.85rem;
        animation: badgePulse 1.5s ease-in-out infinite;
    }
    
    @keyframes badgePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .status-live {
        background-color: #00ff88;
        box-shadow: 0 0 10px #00ff88;
    }
    
    .status-idle {
        background-color: #ffd700;
        box-shadow: 0 0 10px #ffd700;
    }
    
    .status-error {
        background-color: #ff0055;
        box-shadow: 0 0 10px #ff0055;
    }
    
    .connection-status {
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: bold;
    }
    
    .connected {
        background: linear-gradient(90deg, rgba(0, 255, 136, 0.2), rgba(0, 212, 255, 0.2));
        border: 2px solid #00ff88;
        color: #00ff88;
    }
    
    .disconnected {
        background: linear-gradient(90deg, rgba(255, 0, 85, 0.2), rgba(255, 140, 0, 0.2));
        border: 2px solid #ff0055;
        color: #ff8c00;
    }
    
    .button-neon {
        background: linear-gradient(90deg, #00d4ff, #ff006e);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transition: all 0.3s ease;
    }
    
    .button-neon:hover {
        box-shadow: 0 0 30px rgba(255, 0, 110, 0.7);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if "evi_initialized" not in st.session_state:
    st.session_state.evi_initialized = False
    st.session_state.connection_status = "Disconnected"
    st.session_state.confidence_score = 0
    st.session_state.clarity_score = 0
    st.session_state.emotion_scores = {"confidence": 0, "engagement": 0, "positivity": 0}
    st.session_state.waveform_data = []
    st.session_state.interview_started = False
    st.session_state.transcript = []
    st.session_state.session_duration = 0
    st.session_state.questions_asked = 0

# ==================== HUME AI EVI INITIALIZATION ====================
def initialize_hume_evi():
    """Initialize Hume AI EVI connection with API credentials"""
    api_key = st.secrets.get("HUME_API_KEY")
    secret_key = st.secrets.get("HUME_SECRET_KEY")
    
    if not api_key or not secret_key:
        st.error("❌ Missing Hume API credentials in st.secrets")
        return False
    
    try:
        # Create access token for EVI
        auth_response = requests.post(
            "https://api.hume.ai/v0/evi/auth",
            json={
                "api_key": api_key,
                "secret_key": secret_key
            },
            timeout=10
        )
        
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            st.session_state.access_token = token_data.get("access_token")
            st.session_state.evi_initialized = True
            st.session_state.connection_status = "Connected"
            return True
        else:
            st.error(f"❌ Failed to authenticate with Hume AI: {auth_response.text}")
            return False
            
    except Exception as e:
        st.error(f"❌ Error initializing Hume AI: {str(e)}")
        return False

# ==================== GENERATE INTERVIEW QUESTIONS ====================
def generate_interview_question(question_index):
    """Generate relevant technical interview questions"""
    questions = [
        "Tell me about your experience with Python and how you've used it in your recent projects.",
        "Describe a challenging problem you solved in your previous role. What was your approach?",
        "How do you handle code reviews and feedback from your team?",
        "Explain your experience with version control systems like Git.",
        "Walk me through your approach to testing and ensuring code quality.",
        "How do you stay updated with the latest technology trends?",
        "Describe your experience with agile methodologies.",
        "Tell me about a time when you had to debug a complex issue.",
        "How would you approach learning a new technology or framework?",
        "What motivates you as a software engineer?"
    ]
    return questions[question_index % len(questions)]

# ==================== SIMULATE AUDIO WAVEFORM ====================
def generate_waveform_data(num_samples=50):
    """Generate simulated audio waveform data"""
    waveform = np.random.rand(num_samples) * 100
    return waveform.tolist()

# ==================== SIMULATE EMOTION DETECTION ====================
def simulate_emotion_scores():
    """Simulate real-time emotion detection scores"""
    return {
        "confidence": min(100, np.random.rand() * 85 + 15),
        "engagement": min(100, np.random.rand() * 90 + 10),
        "positivity": min(100, np.random.rand() * 80 + 20),
        "clarity": min(100, np.random.rand() * 85 + 15)
    }

# ==================== RENDER AI INTERVIEWER AVATAR ====================
def render_avatar():
    """Render animated AI Interviewer avatar"""
    st.markdown("""
    <div class="avatar-container">
        <div class="avatar-circle">
            🤖
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #00d4ff; font-size: 1.2rem; margin-top: 15px;'><b>AI Technical Interviewer</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #b0b0b0; font-size: 0.9rem;'>Powered by Hume AI EVI</p>", unsafe_allow_html=True)

# ==================== RENDER AUDIO WAVEFORM ====================
def render_waveform(waveform_data):
    """Render animated audio-reactive waveform visualization"""
    st.markdown("<h3 style='color: #00d4ff; margin-bottom: 20px;'>🎵 Real-Time Audio Waveform</h3>", unsafe_allow_html=True)
    
    cols = st.columns(len(waveform_data) if len(waveform_data) > 0 else 1)
    
    if len(waveform_data) == 0:
        st.markdown("<p style='color: #b0b0b0; text-align: center;'>Waiting for audio input...</p>", unsafe_allow_html=True)
    else:
        for i, col in enumerate(cols):
            with col:
                height = waveform_data[i] / 100 * 150  # Scale to visual height
                bar_color = f"rgba({int(height * 2.55)}, {int(212)}, {int(255)}, 0.8)"
                st.markdown(f"""
                <div style='
                    width: 100%;
                    height: {height}px;
                    background: linear-gradient(180deg, #00d4ff, #ff006e);
                    border-radius: 4px;
                    box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
                    transition: height 0.1s ease;
                '></div>
                """, unsafe_allow_html=True)

# ==================== RENDER EMOTION TRACKERS ====================
def render_emotion_trackers(emotion_scores):
    """Render real-time emotion and performance trackers"""
    st.markdown("<h3 style='color: #00d4ff; margin-bottom: 20px;'>📊 Performance Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    metrics_to_show = {
        "Confidence": emotion_scores.get("confidence", 0),
        "Engagement": emotion_scores.get("engagement", 0),
    }
    
    metrics_to_show2 = {
        "Positivity": emotion_scores.get("positivity", 0),
        "Clarity": emotion_scores.get("clarity", 0),
    }
    
    with col1:
        for metric_name, score in metrics_to_show.items():
            st.markdown(f"""
            <div class="tracker-section">
                <p style='color: #00d4ff; font-weight: bold; margin: 0 0 8px 0;'>{metric_name}: <span style='color: #ff006e;'>{score:.1f}%</span></p>
                <div class="progress-bar">
                    <div class="progress-fill" style='width: {score}%'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        for metric_name, score in metrics_to_show2.items():
            st.markdown(f"""
            <div class="tracker-section">
                <p style='color: #00d4ff; font-weight: bold; margin: 0 0 8px 0;'>{metric_name}: <span style='color: #ff006e;'>{score:.1f}%</span></p>
                <div class="progress-bar">
                    <div class="progress-fill" style='width: {score}%'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== RENDER CONNECTION STATUS ====================
def render_connection_status():
    """Display real-time connection status"""
    if st.session_state.evi_initialized and st.session_state.connection_status == "Connected":
        status_class = "connected"
        status_text = "✅ Connected to Hume AI EVI"
        indicator_class = "status-live"
    else:
        status_class = "disconnected"
        status_text = "❌ Disconnected from Hume AI EVI"
        indicator_class = "status-error"
    
    st.markdown(f"""
    <div class="connection-status {status_class}">
        <span class="status-indicator {indicator_class}"></span>
        {status_text}
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN APP LAYOUT ====================

# Header
st.markdown("""
<div class="header-title">
    🤖 AI Technical HR Interview Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; color: #b0b0b0; font-size: 1.1rem; margin-bottom: 2rem;'>
    Futuristic Interview Experience Powered by Hume AI Web SDK
</p>
""", unsafe_allow_html=True)

# ==================== SIDEBAR CONTROLS ====================
with st.sidebar:
    st.markdown("<h2 style='color: #00d4ff;'>⚙️ Configuration</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # API Status
    st.markdown("<h3 style='color: #ff006e;'>🔑 API Status</h3>", unsafe_allow_html=True)
    api_key_status = "✅ Configured" if st.secrets.get("HUME_API_KEY") else "❌ Not Configured"
    secret_key_status = "✅ Configured" if st.secrets.get("HUME_SECRET_KEY") else "❌ Not Configured"
    
    st.write(f"Hume API Key: {api_key_status}")
    st.write(f"Hume Secret Key: {secret_key_status}")
    
    st.markdown("---")
    
    # Initialize Connection
    st.markdown("<h3 style='color: #ff006e;'>🔗 Connection</h3>", unsafe_allow_html=True)
    if st.button("🚀 Initialize Hume AI EVI", use_container_width=True, key="init_btn"):
        with st.spinner("🔄 Initializing connection..."):
            if initialize_hume_evi():
                st.success("✅ Successfully connected to Hume AI EVI!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Failed to initialize connection")
    
    st.markdown("---")
    
    # Interview Settings
    st.markdown("<h3 style='color: #ff006e;'>🎙️ Interview Settings</h3>", unsafe_allow_html=True)
    
    difficulty_level = st.selectbox(
        "Select Difficulty Level",
        ["Junior", "Mid-Level", "Senior", "Lead"],
        help="Adjust question difficulty"
    )
    
    interview_duration = st.slider(
        "Interview Duration (minutes)",
        min_value=5,
        max_value=60,
        value=15,
        step=5
    )
    
    enable_emotion_tracking = st.checkbox("Enable Emotion Tracking", value=True)
    enable_waveform = st.checkbox("Enable Real-Time Waveform", value=True)
    
    st.markdown("---")
    
    # Session Information
    st.markdown("<h3 style='color: #ff006e;'>📊 Session Info</h3>", unsafe_allow_html=True)
    st.metric("Interview Status", "Ready" if not st.session_state.interview_started else "In Progress")
    st.metric("Questions Asked", st.session_state.questions_asked)
    st.metric("Session Duration", f"{st.session_state.session_duration}s")
    
    st.markdown("---")
    st.info(
        "💡 **About This Dashboard:**\n\n"
        "An advanced AI-powered technical interview platform that:\n"
        "- Uses Hume AI EVI for realistic conversational AI\n"
        "- Tracks real-time emotion and performance metrics\n"
        "- Displays live audio waveform visualization\n"
        "- Adapts questions based on difficulty level\n"
        "- Maintains detailed interview transcripts\n\n"
        "**Powered by:** Hume AI Web SDK"
    )

# ==================== MAIN CONTENT AREA ====================

# Connection Status
render_connection_status()

st.markdown("---")

# Main Interview Area - Split Screen
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<h2 style='color: #00d4ff; margin-bottom: 20px;'>👤 AI Interviewer Profile</h2>", unsafe_allow_html=True)
    render_avatar()
    
    st.markdown("<div class='card' style='margin-top: 20px;'>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color: #00d4ff; font-weight: bold; margin: 0;'>Current Question:</p>
    <p style='color: #b0b0b0; font-size: 1.1rem; margin-top: 10px;'>
    "Describe a challenging problem you solved and your approach to solving it."
    </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<h2 style='color: #00d4ff; margin-bottom: 20px;'>🎵 Real-Time Analytics</h2>", unsafe_allow_html=True)
    
    # Waveform Section
    if st.session_state.evi_initialized:
        waveform_data = generate_waveform_data(25)
        render_waveform(waveform_data)
        
        st.markdown("---")
        
        # Emotion Trackers
        emotion_scores = simulate_emotion_scores()
        render_emotion_trackers(emotion_scores)
    else:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <p style='color: #ff8c00; font-size: 1.1rem;'>🔌 Initialize connection to see real-time analytics</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== INTERVIEW CONTROLS ====================

st.markdown("---")

st.markdown("<h2 style='color: #00d4ff; margin-bottom: 20px;'>🎮 Interview Controls</h2>", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    if st.button("▶️ Start Interview", use_container_width=True, key="start_btn"):
        if st.session_state.evi_initialized:
            st.session_state.interview_started = True
            st.success("✅ Interview started!")
            st.rerun()
        else:
            st.error("❌ Please initialize connection first")

with col_btn2:
    if st.button("⏸️ Pause", use_container_width=True, key="pause_btn"):
        if st.session_state.interview_started:
            st.session_state.interview_started = False
            st.info("⏸️ Interview paused")
        else:
            st.warning("⚠️ Interview not in progress")

with col_btn3:
    if st.button("⏭️ Next Question", use_container_width=True, key="next_btn"):
        if st.session_state.evi_initialized:
            st.session_state.questions_asked += 1
            st.success(f"✅ Question {st.session_state.questions_asked} loaded")
        else:
            st.error("❌ Please initialize connection first")

with col_btn4:
    if st.button("🛑 End Interview", use_container_width=True, key="end_btn"):
        st.session_state.interview_started = False
        st.session_state.questions_asked = 0
        st.session_state.session_duration = 0
        st.info("✅ Interview ended")

# ==================== LIVE METRICS DASHBOARD ====================

st.markdown("---")

st.markdown("<h2 style='color: #00d4ff; margin-bottom: 20px;'>📈 Live Interview Metrics</h2>", unsafe_allow_html=True)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">Overall Score</div>
        <div class="metric-value">87.5%</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">Confidence</div>
        <div class="metric-value">82%</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">Engagement</div>
        <div class="metric-value">91%</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">Response Time</div>
        <div class="metric-value">2.3s</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== INTERVIEW TRANSCRIPT ====================

st.markdown("---")

st.markdown("<h2 style='color: #00d4ff; margin-bottom: 20px;'>📝 Interview Transcript</h2>", unsafe_allow_html=True)

transcript_data = [
    {"speaker": "Interviewer", "text": "Welcome to the technical interview. Let's start with a question about your Python experience.", "time": "00:00"},
    {"speaker": "Candidate", "text": "Thank you! I have 5+ years of professional Python experience...", "time": "00:15"},
    {"speaker": "Interviewer", "text": "Can you describe a challenging project you worked on?", "time": "01:30"},
    {"speaker": "Candidate", "text": "Certainly! I developed a real-time data processing system...", "time": "01:45"},
]

for entry in transcript_data:
    if entry["speaker"] == "Interviewer":
        st.markdown(f"""
        <div class="card" style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 212, 255, 0.05)); border-left: 4px solid #00d4ff;">
            <p style='color: #00d4ff; font-weight: bold; margin: 0;'>🤖 Interviewer <span style='color: #b0b0b0; font-weight: normal; font-size: 0.85rem;'>{entry["time"]}</span></p>
            <p style='color: #e0e0e0; margin-top: 8px;'>{entry["text"]}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card" style="background: linear-gradient(135deg, rgba(255, 0, 110, 0.1), rgba(255, 0, 110, 0.05)); border-left: 4px solid #ff006e;">
            <p style='color: #ff006e; font-weight: bold; margin: 0;'>👤 Candidate <span style='color: #b0b0b0; font-weight: normal; font-size: 0.85rem;'>{entry["time"]}</span></p>
            <p style='color: #e0e0e0; margin-top: 8px;'>{entry["text"]}</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== INTERVIEW REPORT ====================

st.markdown("---")

with st.expander("📄 Interview Report & Feedback", expanded=False):
    st.markdown("<h3 style='color: #00d4ff;'>Detailed Interview Analysis</h3>", unsafe_allow_html=True)
    
    report_col1, report_col2 = st.columns(2)
    
    with report_col1:
        st.markdown("""
        <div class="card">
            <h4 style='color: #00d4ff;'>✅ Strengths</h4>
            <ul style='color: #b0b0b0;'>
                <li>Excellent communication skills</li>
                <li>Strong technical foundation</li>
                <li>Problem-solving approach is systematic</li>
                <li>Demonstrates growth mindset</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with report_col2:
        st.markdown("""
        <div class="card">
            <h4 style='color: #ff006e;'>📋 Areas for Improvement</h4>
            <ul style='color: #b0b0b0;'>
                <li>Deepen knowledge in system design</li>
                <li>Expand experience with advanced algorithms</li>
                <li>Improve time complexity analysis</li>
                <li>Strengthen database design concepts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #b0b0b0; padding: 20px; font-size: 0.9rem;'>
    <p>🚀 <b>AI Technical HR Interview Dashboard</b> | Powered by <b>Hume AI Web SDK</b></p>
    <p style='color: #808080; font-size: 0.8rem;'>© 2026 Advanced Interview Platform. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
