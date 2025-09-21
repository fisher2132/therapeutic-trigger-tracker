import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import os
from supabase import create_client, Client
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from collections import Counter
import re
from typing import List, Dict, Any

# -------------------------
# Supabase initialization
# -------------------------
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception as e:
    st.error("Supabase credentials missing from Streamlit secrets. Add SUPABASE_URL and SUPABASE_KEY.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# Page config & paths
# -------------------------
st.set_page_config(
    page_title="Therapeutic Trigger Tracker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Local CSV paths are kept only for fallback / local dev (not used when Supabase available)
DATA_FILE = "data/triggers.csv"
GOALS_FILE = "data/goals.csv"
COPING_FILE = "data/coping_strategies.csv"
os.makedirs("data", exist_ok=True)

# -------------------------
# Therapeutic data constants
# -------------------------
TRIGGER_CATEGORIES = {
    "Interpersonal": ["Conflict", "Rejection", "Criticism", "Abandonment", "Boundary violations"],
    "Environmental": ["Noise", "Crowds", "Specific locations", "Weather", "Lighting"],
    "Cognitive": ["Negative thoughts", "Rumination", "Self-criticism", "Catastrophizing", "Perfectionism"],
    "Physical": ["Pain", "Fatigue", "Hunger", "Illness", "Sleep deprivation"],
    "Situational": ["Work stress", "Financial pressure", "Time pressure", "Change", "Uncertainty"],
    "Emotional": ["Feeling overwhelmed", "Loneliness", "Guilt", "Fear", "Sadness"],
    "Trauma-related": ["Flashbacks", "Memories", "Anniversaries", "Similar situations", "Reminders"]
}

COPING_STRATEGIES = {
    "Grounding Techniques": ["5-4-3-2-1 sensory", "Deep breathing", "Progressive muscle relaxation", "Cold water", "Physical movement"],
    "Cognitive Strategies": ["Thought challenging", "Reframing", "Mindfulness", "Self-compassion", "Positive affirmations"],
    "Behavioral": ["Remove from situation", "Call support person", "Journaling", "Exercise", "Creative expression"],
    "Self-Soothing": ["Warm bath", "Comfort items", "Music", "Nature", "Aromatherapy"],
    "Social Support": ["Talk to friend", "Professional help", "Support group", "Family", "Peer support"]
}

THERAPEUTIC_THEMES = {
    "CBT": ["Thought patterns", "Behavioral responses", "Mood tracking"],
    "DBT": ["Distress tolerance", "Emotion regulation", "Interpersonal effectiveness"],
    "ACT": ["Values alignment", "Psychological flexibility", "Mindful awareness"],
    "Trauma-Informed": ["Safety", "Trustworthiness", "Choice", "Collaboration"]
}

# -------------------------
# CSS (Fixed to remove empty space at top)
# -------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
    
   /* Hide Streamlit branding - FIXED to properly remove empty space */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {display: none !important;}

/* Remove default padding that causes empty space */
.stApp > header {
    display: none !important;
}

.stApp {
    margin-top: -80px; /* Adjust this value if needed to remove empty space */
    padding-top: 0 !important;
}
    
    /* Therapeutic color palette - calming and healing */
    :root {
        --primary-sage: #87a96b;
        --primary-ocean: #4a90a4;
        --primary-lavender: #9d84b7;
        --accent-warm: #d4a574;
        --accent-coral: #e07a5f;
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-bg-medium: rgba(255, 255, 255, 0.06);
        --glass-bg-strong: rgba(255, 255, 255, 0.09);
        --glass-border: rgba(255, 255, 255, 0.15);
        --glass-border-strong: rgba(255, 255, 255, 0.25);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.9);
        --text-muted: rgba(255, 255, 255, 0.7);
        --healing-green: #6faa7a;
        --calming-blue: #7ea4c4;
        --gentle-purple: #a084ca;
        --warning-amber: #f4a261;
        --backdrop-blur: blur(60px);
        --shadow-therapeutic: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Calming gradient background */
    .stApp {
        background: 
            radial-gradient(ellipse at top left, rgba(135, 169, 107, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at top right, rgba(74, 144, 164, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at bottom left, rgba(157, 132, 183, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at bottom right, rgba(212, 165, 116, 0.05) 0%, transparent 50%),
            linear-gradient(135deg, #0a1628 0%, #1a1a2e 25%, #16213e 50%, #1f2937 75%, #111827 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
        padding-top: 0 !important;
    }
    
    /* Enhanced glass morphism */
    .glass-card {
        background: var(--glass-bg-strong);
        backdrop-filter: var(--backdrop-blur);
        border-radius: 24px;
        border: 1px solid var(--glass-border);
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-therapeutic);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .glass-card:hover {
        background: var(--glass-bg-medium);
        border-color: var(--glass-border-strong);
        transform: translateY(-2px);
    }
    
    /* Therapeutic headers */
    .therapeutic-header {
        font-family: 'Crimson Text', serif;
        background: linear-gradient(135deg, var(--text-primary) 0%, var(--primary-sage) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
        letter-spacing: -0.02em;
    }
    
    .section-header {
        font-family: 'Crimson Text', serif;
        color: var(--text-primary);
        font-size: 1.6rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-sage);
        text-align: center;
    }
    
    /* Enhanced form elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: var(--glass-bg-medium) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
        color: var(--text-primary) !important;
        backdrop-filter: var(--backdrop-blur);
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid var(--primary-sage) !important;
        box-shadow: 0 0 0 3px rgba(135, 169, 107, 0.2) !important;
        background: var(--glass-bg-strong) !important;
    }
    
    /* Therapeutic buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-sage) 0%, var(--primary-ocean) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(135, 169, 107, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(135, 169, 107, 0.4) !important;
    }
    
    /* Progress indicators */
    .progress-ring {
        display: inline-block;
        position: relative;
        width: 120px;
        height: 120px;
        margin: 1rem;
    }
    
    .progress-ring circle {
        fill: transparent;
        stroke-width: 8;
        stroke-linecap: round;
        transform: rotate(-90deg);
        transform-origin: 50% 50%;
    }
    
    /* Therapeutic metrics */
    [data-testid="metric-container"] {
        background: var(--glass-bg-strong);
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-therapeutic);
    }
    
    [data-testid="metric-container"]:hover {
        background: var(--glass-bg-medium);
        transform: translateY(-3px);
        border-color: var(--primary-sage);
    }
    
    /* Calm sidebar */
    .css-1d391kg {
        background: rgba(135, 169, 107, 0.05) !important;
        backdrop-filter: var(--backdrop-blur);
        border-right: 1px solid var(--glass-border-strong);
    }
    
    /* Enhanced data visualization */
    .js-plotly-plot {
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        backdrop-filter: var(--backdrop-blur);
        background: var(--glass-bg-medium) !important;
    }
    
    /* Mindfulness quotes */
    .mindfulness-quote {
        background: linear-gradient(135deg, rgba(135, 169, 107, 0.1), rgba(74, 144, 164, 0.1));
        border-left: 4px solid var(--primary-sage);
        padding: 1.5rem;
        margin: 2rem 0;
        border-radius: 0 16px 16px 0;
        font-style: italic;
        color: var(--text-secondary);
        backdrop-filter: var(--backdrop-blur);
    }
    
    /* Therapeutic badges */
    .therapy-badge {
        background: linear-gradient(135deg, var(--primary-sage), var(--primary-ocean));
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
        display: inline-block;
    }
    
    /* Wellness indicators */
    .wellness-indicator {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: inline-block;
        margin: 0.2rem;
        position: relative;
    }
    
    .wellness-indicator.low { background: var(--healing-green); }
    .wellness-indicator.medium { background: var(--warning-amber); }
    .wellness-indicator.high { background: var(--accent-coral); }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .glass-card { padding: 1.5rem; margin: 1rem 0; }
        .therapeutic-header { font-size: 2.2rem; }
        .section-header { font-size: 1.4rem; }
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Helper functions (enhanced)
# -------------------------
def get_wellness_color(value, max_val=10):
    ratio = value / max_val
    if ratio <= 0.3:
        return "#6faa7a"
    elif ratio <= 0.6:
        return "#f4a261"
    else:
        return "#e07a5f"

def calculate_wellness_score(row):
    # ensure keys exist
    anxiety = int(row.get('anxiety', 0) or 0)
    sadness = int(row.get('sadness', 0) or 0)
    anger = int(row.get('anger', 0) or 0)
    shame = int(row.get('shame', 0) or 0)
    relief = int(row.get('relief', 0) or 0)
    gratitude = int(row.get('gratitude', 0) or 0)
    hope = int(row.get('hope', 0) or 0)
    coping_effectiveness = int(row.get('coping_effectiveness', 5) or 5)

    negative_emotions = anxiety + sadness + anger + shame
    positive_emotions = relief + gratitude + hope

    score = max(0, 10 - (negative_emotions * 0.6) + (positive_emotions * 0.4) + (coping_effectiveness * 0.3))
    return min(10, score)

def calculate_consistency_streak(df: pd.DataFrame) -> int:
    """
    Calculate current consecutive-day streak of entries (based on timestamp).
    """
    if df is None or len(df) == 0:
        return 0
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    days = sorted(set(d.date() for d in df['timestamp']))
    days = sorted(days, reverse=True)
    streak = 0
    today = date.today()
    # Allow streak to count up to yesterday if no entry today
    expected_day = today
    for d in days:
        if d == expected_day:
            streak += 1
            expected_day = expected_day - timedelta(days=1)
        elif d < expected_day:
            # gap -> stop
            break
    return streak

def get_therapeutic_insights(df: pd.DataFrame) -> List[str]:
    insights = []
    if df is None or len(df) < 3:
        return ["Continue logging entries to discover meaningful patterns and insights."]
    # compute metrics
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    avg_intensity = df['intensity'].astype(float).mean()
    recent_intensity = df.tail(7)['intensity'].astype(float).mean() if len(df) >= 7 else avg_intensity
    emotion_cols = ['anxiety', 'sadness', 'anger', 'shame']
    dominant_emotion = None
    dominant_value = 0
    if set(emotion_cols).issubset(set(df.columns)):
        means = df[emotion_cols].astype(float).mean()
        dominant_emotion = means.idxmax()
        dominant_value = means.max()
    df['hour'] = df['timestamp'].dt.hour
    peak_trigger_hours = df.groupby('hour')['intensity'].mean().idxmax()
    all_triggers = ' '.join(df['trigger'].fillna('').str.lower())
    trigger_words = Counter(re.findall(r'\b\w+\b', all_triggers))
    common_triggers = [w for w,c in trigger_words.most_common(5) if len(w)>3]

    if recent_intensity > avg_intensity * 1.2:
        insights.append("💡 Your recent trigger intensity has increased. Consider reaching out for additional support.")
    elif recent_intensity < avg_intensity * 0.8:
        insights.append("🌱 Great progress! Your recent trigger intensity has decreased compared to your average.")
    if dominant_value > 6 and dominant_emotion:
        emotion_advice = {
            'anxiety': "Consider grounding techniques like the 5-4-3-2-1 method when anxiety peaks.",
            'sadness': "Gentle self-compassion and connection with others may help during sad moments.",
            'anger': "Physical movement or progressive muscle relaxation can help manage anger responses.",
            'shame': "Remember: you are not your thoughts. Practice self-compassion when shame arises."
        }
        insights.append(f"🎯 {dominant_emotion.title()} appears frequently in your entries. {emotion_advice.get(dominant_emotion, '')}")
    if 6 <= peak_trigger_hours <= 12:
        insights.append("⏰ Morning hours show higher trigger intensity. Consider morning mindfulness practices.")
    elif 18 <= peak_trigger_hours <= 23:
        insights.append("🌅 Evening triggers are common. An evening wind-down routine might be beneficial.")
    if common_triggers:
        insights.append(f"📋 Common trigger themes: {', '.join(common_triggers[:3])}. Consider developing specific coping strategies for these.")
    return insights

# -------------------------
# Auth helpers (Supabase) - UPDATED WITH SIGNUP
# -------------------------
def supabase_sign_in(email: str, password: str) -> Dict[str, Any]:
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"success": True, "data": res}
    except Exception as e:
        return {"success": False, "error": str(e)}

def supabase_sign_up(email: str, password: str) -> Dict[str, Any]:
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return {"success": True, "data": res}
    except Exception as e:
        return {"success": False, "error": str(e)}

def supabase_sign_out():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

# -------------------------
# Sidebar: branding + auth + navigation - UPDATED WITH SIGNUP
# -------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🧠</div>
        <h1 class='therapeutic-header' style='font-size: 2rem; margin: 0;'>
            Therapeutic Tracker
        </h1>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-top: 0.5rem; font-style: italic;'>
            Evidence-based self-awareness
        </p>
    </div>
    """, unsafe_allow_html=True)

# Add this function near your other helper functions (around line 200-250)
def supabase_sign_up(email: str, password: str) -> Dict[str, Any]:
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return {"success": True, "data": res}
    except Exception as e:
        return {"success": False, "error": str(e)}

# -------------------------
# Authentication Block 
# -------------------------
with st.sidebar:
    # Authentication block
    if "user" not in st.session_state or st.session_state.get("user") is None:
        # Create tabs for login and signup
        auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with auth_tab1:
            st.subheader("Login")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Login")
                
                if login_button:
                    if email and password:
                        auth_res = supabase_sign_in(email, password)
                        if auth_res["success"]:
                            user_obj = auth_res["data"].user if hasattr(auth_res["data"], "user") else auth_res["data"]
                            st.session_state["user"] = {
                                "id": user_obj.get("id") if isinstance(user_obj, dict) else user_obj.id,
                                "email": user_obj.get("email") if isinstance(user_obj, dict) else getattr(user_obj, "email", None)
                            }
                            st.success("Login successful! Refreshing...")
                            st.rerun()
                        else:
                            st.error("Login failed. Check credentials.")
                    else:
                        st.error("Please enter both email and password.")
        
        with auth_tab2:
            st.subheader("Create Account")
            with st.form("signup_form"):
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                signup_button = st.form_submit_button("Create Account")
                
                if signup_button:
                    if not new_email or not new_password:
                        st.error("Please enter both email and password.")
                    elif new_password != confirm_password:
                        st.error("Passwords don't match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        auth_res = supabase_sign_up(new_email, new_password)
                        if auth_res["success"]:
                            st.success("Account created successfully! Please check your email for verification, then return to login.")
                        else:
                            error_msg = auth_res["error"]
                            if "already registered" in error_msg.lower():
                                st.error("Email already registered. Please use the Login tab.")
                            else:
                                st.error(f"Error creating account: {error_msg}")
        
        st.write("---")
        st.info("Create an account above or contact your administrator for access.")
    
    else:
        st.success(f"Welcome, {st.session_state['user'].get('email')}")
        if st.button("Logout"):
            st.session_state.pop("user", None)
            supabase_sign_out()
            st.rerun()

    # Navigation 
    page = st.radio(
        "",
        ["✨ New Entry", "📊 Dashboard", "🎯 Insights", "🛠️ Coping Tools", "📈 Progress", "📚 All Entries", "🎯 Goals"],
        label_visibility="collapsed"
    )

# ==============================
# PAGE: New Entry (Enhanced)
# ==============================
if page == "✨ New Entry":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='therapeutic-header'>✨ Mindful Entry</h1>", unsafe_allow_html=True)
    
    # Mindfulness prompt
    st.markdown("""
    <div class='mindfulness-quote'>
        💫 "The present moment is the only time over which we have dominion." - Thích Nhất Hạnh
        <br><br>
        Take three deep breaths before beginning. This is a safe space for honest self-reflection.
    </div>
    """, unsafe_allow_html=True)

    with st.form("enhanced_trigger_form", clear_on_submit=True):
        # Basic trigger information
        st.markdown("<div class='section-header'>🎯 Trigger Information</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            # Categorized trigger selection
            trigger_category = st.selectbox(
                "Trigger Category", 
                list(TRIGGER_CATEGORIES.keys()),
                help="What type of trigger was this?"
            )
            
            specific_triggers = st.multiselect(
                "Specific Triggers",
                TRIGGER_CATEGORIES[trigger_category],
                help="Select all that apply"
            )
            
            custom_trigger = st.text_input(
                "Additional Description", 
                placeholder="Describe what happened in your own words..."
            )
            
        with col2:
            intensity = st.slider("🌡️ Overall Intensity", 1, 10, 5, 
                                help="How overwhelming was this experience overall?")
            
            duration = st.selectbox(
                "⏱️ Duration of Impact",
                ["A few minutes", "30 minutes", "1-2 hours", "Several hours", "All day", "Multiple days"],
                help="How long did the effects last?"
            )
            
            location = st.selectbox(
                "📍 Where did this occur?",
                ["Home", "Work", "School", "Social setting", "Public place", "Online", "Other"],
                help="Environmental context matters"
            )

        # Context and narrative
        st.markdown("<div class='section-header'>📖 The Story</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            before = st.text_area(
                "⏪ What was happening before?", 
                placeholder="Set the scene. What was your emotional state? What events led up to this moment?",
                height=120
            )
            
            thoughts = st.text_area(
                "🧠 What thoughts went through your mind?",
                placeholder="What did you tell yourself? What beliefs or fears came up?",
                height=100
            )
            
        with col2:
            after = st.text_area(
                "⏩ What happened after?", 
                placeholder="How did you respond? What were the immediate consequences?",
                height=120
            )
            
            physical = st.text_area(
                "💪 Physical sensations",
                placeholder="What did you notice in your body? Tension, changes in breathing, etc.",
                height=100
            )

        # Enhanced emotional tracking
        st.markdown("<div class='section-header'>🎭 Emotional Landscape</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("**Primary Emotions**")
            anxiety = st.slider("😰 Anxiety/Fear", 0, 10, 0, help="Worry, panic, nervousness")
            sadness = st.slider("😢 Sadness/Grief", 0, 10, 0, help="Sorrow, loss, melancholy")
            anger = st.slider("😡 Anger/Irritation", 0, 10, 0, help="Frustration, rage, annoyance")
            
        with col2:
            st.markdown("**Complex Emotions**")
            shame = st.slider("😳 Shame/Guilt", 0, 10, 0, help="Self-blame, embarrassment")
            loneliness = st.slider("😔 Loneliness", 0, 10, 0, help="Isolation, disconnection")
            overwhelm = st.slider("🌪️ Overwhelm", 0, 10, 0, help="Too much to handle")
            
        with col3:
            st.markdown("**Positive States**")
            relief = st.slider("😌 Relief/Calm", 0, 10, 0, help="Peace, release, comfort")
            hope = st.slider("🌈 Hope", 0, 10, 0, help="Optimism about the future")
            gratitude = st.slider("🙏 Gratitude", 0, 10, 0, help="Appreciation, thankfulness")

        # Coping and response
        st.markdown("<div class='section-header'>🛠️ Coping & Response</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            coping_used = st.multiselect(
                "Coping strategies you tried",
                [strategy for category in COPING_STRATEGIES.values() for strategy in category],
                help="What did you do to manage this situation?"
            )
            
            coping_effectiveness = st.slider(
                "🎯 How effective were your coping strategies?",
                1, 10, 5,
                help="1 = Not helpful at all, 10 = Very effective"
            )
            
        with col2:
            support_used = st.multiselect(
                "Support you accessed",
                ["Talked to friend/family", "Called therapist", "Used support group", 
                 "Online resources", "Journaling", "Self-soothing", "None"],
                help="What support did you use or could you have used?"
            )
            
            recovery_time = st.selectbox(
                "⏳ Recovery time",
                ["Still ongoing", "A few minutes", "30 minutes", "1-2 hours", 
                 "Several hours", "Next day", "Several days"],
                help="How long until you felt more stable?"
            )

        # Learning and growth
        st.markdown("<div class='section-header'>🌱 Learning & Growth</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            learned = st.text_area(
                "💡 What did you learn about yourself?",
                placeholder="Any insights, patterns, or realizations?",
                height=100
            )
            
            next_time = st.text_area(
                "🎯 What would you do differently next time?",
                placeholder="How might you prepare or respond differently in the future?",
                height=100
            )
            
        with col2:
            strengths = st.text_area(
                "💪 What strengths did you show?",
                placeholder="How did you demonstrate resilience, courage, or wisdom?",
                height=100
            )
            
            additional_notes = st.text_area(
                "📝 Additional reflections",
                placeholder="Anything else you want to remember about this experience?",
                height=100
            )

        # Therapeutic check-ins
        st.markdown("<div class='section-header'>🔍 Therapeutic Check-ins</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            self_compassion = st.slider(
                "💝 Self-compassion level",
                1, 10, 5,
                help="How kind are you being to yourself right now?"
            )
            
        with col2:
            safety_feeling = st.slider(
                "🛡️ Feeling of safety",
                1, 10, 5,
                help="How safe do you feel right now?"
            )
            
        with col3:
            energy_level = st.slider(
                "⚡ Energy level",
                1, 10, 5,
                help="What's your energy level after processing this?"
            )

        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("💾 Save This Sacred Entry", use_container_width=True)

        if submitted:
            if not st.session_state.get("user"):
                st.warning("⚠️ Please log in to save entries.")
            elif not (custom_trigger or specific_triggers):
                st.warning("⚠️ Please provide a description or select specific triggers.")
            else:
                trigger_desc = custom_trigger
                if specific_triggers:
                    trigger_desc += f" [{', '.join(specific_triggers)}]" if custom_trigger else ', '.join(specific_triggers)
                entry = {
                    "user_id": st.session_state["user"]["id"],
                    "timestamp": datetime.now().isoformat(),
                    "trigger": trigger_desc,
                    "category": trigger_category,
                    "before": before,
                    "after": after,
                    "thoughts": thoughts,
                    "physical": physical,
                    "intensity": intensity,
                    "duration": duration,
                    "location": location,
                    "anxiety": anxiety,
                    "sadness": sadness,
                    "anger": anger,
                    "shame": shame,
                    "loneliness": loneliness,
                    "overwhelm": overwhelm,
                    "relief": relief,
                    "hope": hope,
                    "gratitude": gratitude,
                    "coping_used": ', '.join(coping_used) if coping_used else '',
                    "coping_effectiveness": coping_effectiveness,
                    "support_used": ', '.join(support_used) if support_used else '',
                    "recovery_time": recovery_time,
                    "learned": learned,
                    "next_time": next_time,
                    "strengths": strengths,
                    "notes": additional_notes,
                    "self_compassion": self_compassion,
                    "safety_feeling": safety_feeling,
                    "energy_level": energy_level
                }
                try:
                    supabase.table("triggers").insert(entry).execute()
                    st.success("✨ Your entry has been saved with deep respect for your courage in self-reflection. This is meaningful work.")
                    
                    # Show brief affirmation
                    st.markdown("""
                    <div class='mindfulness-quote'>
                        🌟 "You are brave for looking at your patterns with such honesty. 
                        Each entry is a step toward greater self-understanding and healing."
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error saving entry: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PAGE: Enhanced Dashboard
# ==============================
elif page == "📊 Dashboard":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='therapeutic-header'>📊 Wellness Dashboard</h1>", unsafe_allow_html=True)

    if not st.session_state.get("user"):
        st.warning("⚠️ Please log in to view your dashboard.")
    else:
        try:
            resp = supabase.table("triggers").select("*").eq("user_id", st.session_state["user"]["id"]).execute()
            df = pd.DataFrame(resp.data)
            
            if df.empty:
                st.markdown("""
                <div style='text-align: center; padding: 3rem;'>
                    <h3 style='color: rgba(255, 255, 255, 0.8);'>🌱 Your Wellness Journey Begins Here</h3>
                    <p style='color: rgba(255, 255, 255, 0.6); font-size: 1.1rem; line-height: 1.6;'>
                        Your dashboard will bloom with insights as you document your experiences. 
                        Each entry is a seed of self-awareness that will grow into profound understanding.
                    </p>
                    <div style='margin: 2rem 0;'>
                        <div style='font-size: 4rem; opacity: 0.3;'>📊</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Calculate wellness scores if not present
                if 'wellness_score' not in df.columns:
                    df['wellness_score'] = df.apply(calculate_wellness_score, axis=1)

                st.markdown("""
                <div class='mindfulness-quote'>
                    📈 "Progress, not perfection. Every data point represents your commitment to growth and self-awareness."
                </div>
                """, unsafe_allow_html=True)

                # Enhanced summary metrics
                col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
                
                with col1:
                    st.metric("📊 Total Entries", len(df))
                with col2:
                    avg_intensity = df["intensity"].mean()
                    color = get_wellness_color(10 - avg_intensity)
                    st.metric("🌡️ Avg Intensity", f"{avg_intensity:.1f}/10")
                with col3:
                    recent_entries = len(df[df['timestamp'] > (datetime.now() - pd.Timedelta(days=7))])
                    st.metric("📅 This Week", recent_entries)
                with col4:
                    avg_wellness = df['wellness_score'].mean() if 'wellness_score' in df.columns else 5
                    st.metric("🌟 Wellness Score", f"{avg_wellness:.1f}/10")
                with col5:
                    streak = calculate_consistency_streak(df)
                    st.metric("🔥 Entry Streak", f"{streak} days")

                st.markdown("---")

                # Wellness trends
                col1, col2 = st.columns(2, gap="large")
                
                with col1:
                    st.markdown("<h3>🌈 Emotional Trends (Last 30 Days)</h3>", unsafe_allow_html=True)
                    
                    recent_30 = df[df['timestamp'] > (datetime.now() - pd.Timedelta(days=30))].copy()
                    if len(recent_30) > 0:
                        emotions = ['anxiety', 'sadness', 'anger', 'shame', 'relief', 'hope']
                        emotion_data = []
                        
                        for emotion in emotions:
                            if emotion in recent_30.columns:
                                emotion_data.append({
                                    'emotion': emotion.title(),
                                    'average': recent_30[emotion].mean(),
                                    'trend': 'improving' if recent_30[emotion].tail(7).mean() < recent_30[emotion].head(7).mean() else 'stable'
                                })
                        
                        if emotion_data:
                            emotion_df = pd.DataFrame(emotion_data)
                            fig = px.bar(emotion_df, x='emotion', y='average',
                                        title="", 
                                        color='average',
                                        color_continuous_scale=['#6faa7a', '#f4a261', '#e07a5f'])
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='white',
                                showlegend=False,
                                xaxis_title="",
                                yaxis_title="Average Level"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.markdown("<h3>📈 Intensity & Wellness Over Time</h3>", unsafe_allow_html=True)
                    
                    if len(df) > 1:
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        
                        # Intensity line
                        fig.add_trace(
                            go.Scatter(x=df['timestamp'], y=df['intensity'], 
                                      name="Intensity", line=dict(color='#e07a5f', width=3)),
                            secondary_y=False
                        )
                        
                        # Wellness score line
                        if 'wellness_score' in df.columns:
                            fig.add_trace(
                                go.Scatter(x=df['timestamp'], y=df['wellness_score'],
                                          name="Wellness", line=dict(color='#6faa7a', width=3)),
                                secondary_y=True
                            )
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white',
                            legend=dict(bgcolor='rgba(0,0,0,0.3)')
                        )
                        
                        fig.update_yaxes(title_text="Intensity Level", secondary_y=False, color='white')
                        fig.update_yaxes(title_text="Wellness Score", secondary_y=True, color='white')
                        
                        st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")

                # Trigger patterns analysis
                st.markdown("<h3>🎯 Trigger Pattern Analysis</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3, gap="large")
                
                with col1:
                    st.markdown("**📊 Trigger Categories**")
                    if 'category' in df.columns:
                        category_counts = df['category'].value_counts()
                        fig = px.pie(values=category_counts.values, names=category_counts.index,
                                    title="", color_discrete_sequence=px.colors.qualitative.Set3)
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**⏰ Time Patterns**")
                    df['hour'] = df['timestamp'].dt.hour
                    hourly_intensity = df.groupby('hour')['intensity'].mean()
                    
                    fig = px.bar(x=hourly_intensity.index, y=hourly_intensity.values,
                                title="", color=hourly_intensity.values,
                                color_continuous_scale=['#6faa7a', '#f4a261', '#e07a5f'])
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        xaxis_title="Hour of Day",
                        yaxis_title="Average Intensity",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col3:
                    st.markdown("**📍 Location Impact**")
                    if 'location' in df.columns:
                        location_intensity = df.groupby('location')['intensity'].mean().sort_values(ascending=False)
                        
                        fig = px.bar(x=location_intensity.values, y=location_intensity.index,
                                    title="", orientation='h',
                                    color=location_intensity.values,
                                    color_continuous_scale=['#6faa7a', '#f4a261', '#e07a5f'])
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white',
                            xaxis_title="Average Intensity",
                            yaxis_title="Location",
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")

                # Recent activity summary
                st.markdown("<h3>📋 Recent Activity Summary</h3>", unsafe_allow_html=True)
                
                recent_df = df.tail(5)[['timestamp', 'trigger', 'intensity', 'category']].copy()
                recent_df['timestamp'] = recent_df['timestamp'].dt.strftime('%m/%d %H:%M')
                recent_df.columns = ['Date & Time', 'Trigger', 'Intensity', 'Category']
                
                # Add color coding for intensity
                def color_intensity(val):
                    if isinstance(val, (int, float)):
                        if val <= 3:
                            return 'background-color: rgba(111, 170, 122, 0.3)'
                        elif val <= 7:
                            return 'background-color: rgba(244, 162, 97, 0.3)'
                        else:
                            return 'background-color: rgba(224, 122, 95, 0.3)'
                    return ''
                
                styled_df = recent_df.style.applymap(color_intensity, subset=['Intensity'])
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Error loading data: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PAGE: Therapeutic Insights
# ==============================
elif page == "🎯 Insights":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='therapeutic-header'>🎯 Therapeutic Insights</h1>", unsafe_allow_html=True)
    
    if not st.session_state.get("user"):
        st.warning("⚠️ Please log in to view insights.")
    else:
        try:
            resp = supabase.table("triggers").select("*").eq("user_id", st.session_state["user"]["id"]).execute()
            df = pd.DataFrame(resp.data)
            
            if df.empty:
                st.markdown("""
                <div style='text-align: center; padding: 3rem;'>
                    <h3 style='color: rgba(255, 255, 255, 0.8);'>🔍 Insights Await Your Journey</h3>
                    <p style='color: rgba(255, 255, 255, 0.6); font-size: 1.1rem; line-height: 1.6;'>
                        As you document your experiences, patterns will emerge and insights will unfold. 
                        This space will become a treasure trove of self-understanding and therapeutic guidance.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                insights = get_therapeutic_insights(df)
                
                st.markdown("""
                <div class='mindfulness-quote'>
                    🔍 "The curious paradox is that when I accept myself just as I am, then I can change." - Carl Rogers
                    <br><br>
                    These insights are invitations to deeper self-understanding, not judgments.
                </div>
                """, unsafe_allow_html=True)
                
                # Display insights
                st.markdown("<div class='section-header'>💡 Current Insights</div>", unsafe_allow_html=True)
                
                for i, insight in enumerate(insights):
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, rgba(135, 169, 107, 0.1), rgba(74, 144, 164, 0.1));
                        border-left: 4px solid var(--primary-sage);
                        padding: 1.5rem;
                        margin: 1rem 0;
                        border-radius: 0 16px 16px 0;
                        backdrop-filter: var(--backdrop-blur);
                    '>
                        {insight}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Pattern analysis
                col1, col2 = st.columns(2, gap="large")
                
                with col1:
                    st.markdown("<h3>🔄 Pattern Recognition</h3>", unsafe_allow_html=True)
                    
                    # Trigger frequency analysis
                    if 'category' in df.columns:
                        st.markdown("**Most Common Trigger Categories:**")
                        category_counts = df['category'].value_counts()
                        for category, count in category_counts.head(3).items():
                            percentage = (count / len(df)) * 100
                            st.write(f"• {category}: {count} times ({percentage:.1f}%)")
                    
                    # Emotional patterns
                    emotions = ['anxiety', 'sadness', 'anger', 'shame', 'relief', 'hope']
                    emotion_averages = {}
                    for emotion in emotions:
                        if emotion in df.columns:
                            emotion_averages[emotion] = df[emotion].mean()
                    
                    if emotion_averages:
                        st.markdown("**Dominant Emotional Patterns:**")
                        sorted_emotions = sorted(emotion_averages.items(), key=lambda x: x[1], reverse=True)
                        for emotion, avg in sorted_emotions[:3]:
                            if avg > 0:
                                st.write(f"• {emotion.title()}: {avg:.1f}/10 average")
                
                with col2:
                    st.markdown("<h3>📈 Progress Indicators</h3>", unsafe_allow_html=True)
                    
                    # Calculate trends
                    if len(df) >= 14:
                        recent_two_weeks = df.tail(14)
                        previous_two_weeks = df.iloc[-28:-14] if len(df) >= 28 else df.head(14)
                        
                        recent_avg_intensity = recent_two_weeks['intensity'].mean()
                        previous_avg_intensity = previous_two_weeks['intensity'].mean()
                        
                        intensity_change = recent_avg_intensity - previous_avg_intensity
                        
                        if intensity_change < -0.5:
                            st.success("📉 Trigger intensity is decreasing - great progress!")
                        elif intensity_change > 0.5:
                            st.warning("📈 Trigger intensity has increased - consider additional support")
                        else:
                            st.info("➡️ Trigger intensity is stable")
                        
                        # Coping effectiveness trend
                        if 'coping_effectiveness' in df.columns:
                            recent_coping = recent_two_weeks['coping_effectiveness'].mean()
                            previous_coping = previous_two_weeks['coping_effectiveness'].mean()
                            
                            coping_change = recent_coping - previous_coping
                            
                            if coping_change > 0.5:
                                st.success("🛠️ Coping strategies are becoming more effective!")
                            elif coping_change < -0.5:
                                st.warning("🛠️ Consider exploring new coping strategies")
                            else:
                                st.info("🛠️ Coping effectiveness is stable")
                
                st.markdown("---")
                
                # Therapeutic recommendations
                st.markdown("<h3>🌟 Personalized Recommendations</h3>", unsafe_allow_html=True)
                
                # Generate recommendations based on data
                recommendations = []
                
                if len(df) > 0:
                    avg_intensity = df['intensity'].mean()
                    dominant_emotions = df[['anxiety', 'sadness', 'anger', 'shame']].mean().sort_values(ascending=False)
                    
                    if avg_intensity > 7:
                        recommendations.append({
                            'type': 'Crisis Support',
                            'icon': '🚨',
                            'title': 'High Intensity Patterns Detected',
                            'description': 'Your average trigger intensity is quite high. Consider reaching out to a mental health professional for additional support.',
                            'action': 'Schedule a therapy appointment or call a crisis helpline if needed.'
                        })
                    
                    if dominant_emotions.iloc[0] > 6:
                        emotion = dominant_emotions.index[0]
                        emotion_recommendations = {
                            'anxiety': {
                                'title': 'Anxiety-Focused Interventions',
                                'description': 'Anxiety appears frequently in your entries. Grounding techniques and breathing exercises may be particularly helpful.',
                                'action': 'Try the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.'
                            },
                            'sadness': {
                                'title': 'Depression-Informed Support',
                                'description': 'Persistent sadness patterns suggest you might benefit from gentle activity scheduling and connection with others.',
                                'action': 'Consider one small pleasurable activity each day and reach out to a trusted friend or family member.'
                            },
                            'anger': {
                                'title': 'Anger Management Strategies',
                                'description': 'High anger levels suggest a need for physical outlets and cognitive restructuring techniques.',
                                'action': 'Try progressive muscle relaxation or physical exercise when you notice anger building.'
                            },
                            'shame': {
                                'title': 'Self-Compassion Focus',
                                'description': 'Shame patterns can be particularly challenging. Self-compassion practices may be transformative.',
                                'action': 'Practice speaking to yourself as you would to a dear friend going through the same experience.'
                            }
                        }
                        
                        if emotion in emotion_recommendations:
                            rec = emotion_recommendations[emotion]
                            recommendations.append({
                                'type': 'Emotional Support',
                                'icon': '💚',
                                'title': rec['title'],
                                'description': rec['description'],
                                'action': rec['action']
                            })
                    
                    # Add general recommendations
                    recommendations.extend([
                        {
                            'type': 'Mindfulness',
                            'icon': '🧘',
                            'title': 'Daily Mindfulness Practice',
                            'description': 'Regular mindfulness can increase awareness of triggers before they escalate.',
                            'action': 'Start with 5 minutes of daily meditation or mindful breathing.'
                        },
                        {
                            'type': 'Professional Support',
                            'icon': '👩‍⚕️',
                            'title': 'Consider Professional Guidance',
                            'description': 'A therapist can help you develop personalized strategies based on your specific patterns.',
                            'action': 'Research therapists who specialize in your primary concerns (anxiety, trauma, depression, etc.).'
                        }
                    ])
                
                # Display recommendations
                for rec in recommendations:
                    st.markdown(f"""
                    <div style='
                        background: var(--glass-bg-medium);
                        border-radius: 16px;
                        border: 1px solid var(--glass-border);
                        padding: 1.5rem;
                        margin: 1rem 0;
                        backdrop-filter: var(--backdrop-blur);
                    '>
                        <h4 style='color: var(--primary-sage); margin-bottom: 1rem;'>
                            {rec['icon']} {rec['title']}
                        </h4>
                        <p style='color: var(--text-secondary); margin-bottom: 1rem;'>
                            {rec['description']}
                        </p>
                        <div style='
                            background: rgba(135, 169, 107, 0.1);
                            border-radius: 8px;
                            padding: 1rem;
                            border-left: 3px solid var(--primary-sage);
                        '>
                            <strong>Action Step:</strong> {rec['action']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PAGE: Coping Tools
# ==============================
elif page == "🛠️ Coping Tools":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='therapeutic-header'>🛠️ Therapeutic Coping Tools</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='mindfulness-quote'>
        🌟 "You have been assigned this mountain to show others it can be moved." - Mel Robbins
        <br><br>
        These are evidence-based tools used by therapists worldwide. Practice them regularly for best results.
    </div>
    """, unsafe_allow_html=True)
    
    # Coping strategy categories
    for category, strategies in COPING_STRATEGIES.items():
        with st.expander(f"{category} ({len(strategies)} techniques)"):
            for i, strategy in enumerate(strategies, 1):
                
                # Detailed descriptions for key strategies
                descriptions = {
                    "5-4-3-2-1 sensory": {
                        "description": "A grounding technique to anchor you in the present moment",
                        "instructions": "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
                        "when_to_use": "When feeling anxious, dissociated, or overwhelmed"
                    },
                    "Deep breathing": {
                        "description": "Activates the parasympathetic nervous system to promote calm",
                        "instructions": "Breathe in for 4 counts, hold for 4, out for 6. Repeat 5-10 times",
                        "when_to_use": "Anytime you notice stress, anxiety, or need to center yourself"
                    },
                    "Progressive muscle relaxation": {
                        "description": "Systematically tense and release muscle groups to reduce physical tension",
                        "instructions": "Start with toes, tense for 5 seconds, release. Work up through your entire body",
                        "when_to_use": "When experiencing physical tension, anger, or having trouble sleeping"
                    },
                    "Thought challenging": {
                        "description": "Examine and reframe negative or distorted thoughts",
                        "instructions": "Ask: Is this thought realistic? What evidence supports/contradicts it? What would I tell a friend?",
                        "when_to_use": "When caught in negative thinking patterns or catastrophizing"
                    },
                    "Self-compassion": {
                        "description": "Treat yourself with the same kindness you'd show a good friend",
                        "instructions": "Place hand on heart, acknowledge your pain, remind yourself that suffering is human, offer yourself kindness",
                        "when_to_use": "During self-criticism, shame, or when feeling like you're not good enough"
                    }
                }
                
                if strategy in descriptions:
                    info = descriptions[strategy]
                    st.markdown(f"""
                    <div style='
                        background: var(--glass-bg-medium);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin: 1rem 0;
                        border-left: 4px solid var(--primary-sage);
                    '>
                        <h4 style='color: var(--primary-sage); margin-bottom: 0.5rem;'>
                            {i}. {strategy}
                        </h4>
                        <p style='color: var(--text-secondary); margin-bottom: 1rem;'>
                            {info['description']}
                        </p>
                        <div style='background: rgba(135, 169, 107, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                            <strong>How to do it:</strong> {info['instructions']}
                        </div>
                        <div style='background: rgba(74, 144, 164, 0.1); padding: 1rem; border-radius: 8px;'>
                            <strong>When to use:</strong> {info['when_to use']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write(f"{i}. **{strategy}**")
    
    st.markdown("---")
    
    # Quick access tools
    st.markdown("<h3>⚡ Quick Access Tools</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        if st.button("🫁 Breathing Exercise", use_container_width=True):
            st.markdown("""
            <div style='text-align: center; padding: 2rem; background: var(--glass-bg-medium); border-radius: 16px;'>
                <h4>Box Breathing</h4>
                <p>Follow along:</p>
                <div style='font-size: 1.2rem; color: var(--primary-sage);'>
                    Breathe in... 1... 2... 3... 4...<br>
                    Hold... 1... 2... 3... 4...<br>
                    Breathe out... 1... 2... 3... 4...<br>
                    Hold... 1... 2... 3... 4...
                </div>
                <p style='margin-top: 1rem;'><em>Repeat this cycle 4-8 times</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🌊 Grounding Exercise", use_container_width=True):
            st.markdown("""
            <div style='text-align: center; padding: 2rem; background: var(--glass-bg-medium); border-radius: 16px;'>
                <h4>5-4-3-2-1 Technique</h4>
                <div style='text-align: left; max-width: 300px; margin: 0 auto;'>
                    <p><strong>5</strong> things you can <strong>see</strong></p>
                    <p><strong>4</strong> things you can <strong>touch</strong></p>
                    <p><strong>3</strong> things you can <strong>hear</strong></p>
                    <p><strong>2</strong> things you can <strong>smell</strong></p>
                    <p><strong>1</strong> thing you can <strong>taste</strong></p>
                </div>
                <p style='margin-top: 1rem;'><em>Take your time with each step</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if st.button("💝 Self-Compassion", use_container_width=True):
            st.markdown("""
            <div style='text-align: center; padding: 2rem; background: var(--glass-bg-medium); border-radius: 16px;'>
                <h4>Self-Compassion Break</h4>
                <div style='text-align: left; max-width: 300px; margin: 0 auto;'>
                    <p>1. <strong>Acknowledge:</strong> "This is a moment of suffering"</p>
                    <p>2. <strong>Normalize:</strong> "Suffering is part of life"</p>
                    <p>3. <strong>Be kind:</strong> "May I be kind to myself"</p>
                </div>
                <p style='margin-top: 1rem;'><em>Place your hand on your heart as you say these</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Personalized coping plan
    st.markdown("<h3>📝 Build Your Personal Coping Plan</h3>", unsafe_allow_html=True)
    
    if not st.session_state.get("user"):
        st.warning("⚠️ Please log in to save your coping plan.")
    else:
        with st.form("coping_plan"):
            st.markdown("Create a personalized plan for different intensity levels:")
            
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                low_intensity = st.multiselect(
                    "📗 Low Intensity (1-3): Preventive strategies",
                    [strategy for strategies in COPING_STRATEGIES.values() for strategy in strategies],
                    help="What helps when you first notice stress building?"
                )
                
                medium_intensity = st.multiselect(
                    "📙 Medium Intensity (4-6): Active coping",
                    [strategy for strategies in COPING_STRATEGIES.values() for strategy in strategies],
                    help="What works when you're moderately triggered?"
                )
            
            with col2:
                high_intensity = st.multiselect(
                    "📕 High Intensity (7-10): Crisis management",
                    [strategy for strategies in COPING_STRATEGIES.values() for strategy in strategies],
                    help="What helps during intense episodes?"
                )
                
                emergency_contacts = st.text_area(
                    "🆘 Emergency contacts/resources",
                    placeholder="Therapist, crisis line, trusted friend, etc.",
                    help="Who can you reach out to in crisis?"
                )
            
            if st.form_submit_button("💾 Save My Coping Plan"):
                plan = {
                    "user_id": st.session_state["user"]["id"],
                    "timestamp": datetime.now().isoformat(),
                    "low_intensity": ', '.join(low_intensity),
                    "medium_intensity": ', '.join(medium_intensity),
                    "high_intensity": ', '.join(high_intensity),
                    "emergency_contacts": emergency_contacts
                }
                
                try:
                    supabase.table("coping_strategies").insert(plan).execute()
                    st.success("✨ Your personalized coping plan has been saved!")
                except Exception as e:
                    st.error(f"Error saving coping plan: {e}")
        
        # Display existing plan if available
        try:
            resp = supabase.table("coping_strategies").select("*").eq("user_id", st.session_state["user"]["id"]).execute()
            coping_df = pd.DataFrame(resp.data)
            if not coping_df.empty:
                latest_plan = coping_df.tail(1).iloc[0]
                
                st.markdown("---")
                st.markdown("<h3>📋 Your Current Coping Plan</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3, gap="medium")
                
                with col1:
                    st.markdown("**📗 Low Intensity**")
                    if latest_plan['low_intensity']:
                        for strategy in latest_plan['low_intensity'].split(', '):
                            st.write(f"• {strategy}")
                
                with col2:
                    st.markdown("**📙 Medium Intensity**")
                    if latest_plan['medium_intensity']:
                        for strategy in latest_plan['medium_intensity'].split(', '):
                            st.write(f"• {strategy}")
                
                with col3:
                    st.markdown("**📕 High Intensity**")
                    if latest_plan['high_intensity']:
                        for strategy in latest_plan['high_intensity'].split(', '):
                            st.write(f"• {strategy}")
                
                if latest_plan['emergency_contacts']:
                    st.markdown("**🆘 Emergency Resources:**")
                    st.write(latest_plan['emergency_contacts'])
        except Exception as e:
            st.error(f"Error loading coping plan: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PAGE: Progress Tracking
# ==============================
elif page == "📈 Progress":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='therapeutic-header'>📈 Progress & Growth</h1>", unsafe_allow_html=True)
    
    if not st.session_state.get("user"):
        st.warning("⚠️ Please log in to view progress.")
    else:
        try:
            resp = supabase.table("triggers").select("*").eq("user_id", st.session_state["user"]["id"]).execute()
            df = pd.DataFrame(resp.data)
            
            if df.empty:
                st.info("📝 Add entries to track progress.")
            else:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                st.markdown("""
                <div class='mindfulness-quote'>
                    📊 "Progress is impossible without change, and those who cannot change their minds cannot change anything." - George Bernard Shaw
                    <br><br>
                    Celebrate every step forward, no matter how small. Growth is not always linear.
                </div>
                """, unsafe_allow_html=True)
                
                # Progress metrics
                col1, col2, col3, col4 = st.columns(4, gap="medium")
                
                with col1:
                    total_days = (df['timestamp'].max() - df['timestamp'].min()).days + 1 if len(df) > 1 else 1
                    st.metric("📅 Journey Length", f"{total_days} days")
                
                with col2:
                    consistency = calculate_consistency_streak(df)
                    st.metric("🔥 Current Streak", f"{consistency} days")
                
                with col3:
                    if 'coping_effectiveness' in df.columns:
                        avg_coping = df['coping_effectiveness'].mean()
                        st.metric("🛠️ Coping Effectiveness", f"{avg_coping:.1f}/10")
                    else:
                        st.metric("🛠️ Coping Data", "Not available")
                
                with col4:
                    if len(df) >= 7:
                        recent_week = df.tail(7)['intensity'].mean()
                        previous_week = df.iloc[-14:-7]['intensity'].mean() if len(df) >= 14 else recent_week
                        improvement = previous_week - recent_week
                        st.metric("📉 Weekly Improvement", f"{improvement:+.1f}")
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PAGE: Goals
# ==============================
elif page == "🎯 Goals":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='therapeutic-header'>🎯 Your Goals</h1>", unsafe_allow_html=True)

    if not st.session_state.get("user"):
        st.warning("⚠️ Please log in to manage goals.")
    else:
        with st.form("goal_form"):
            goal_text = st.text_input("New Goal")
            target_date = st.date_input("Target Date", value=date.today())
            if st.form_submit_button("💾 Add Goal"):
                try:
                    supabase.table("goals").insert({
                        "user_id": st.session_state["user"]["id"],
                        "goal": goal_text,
                        "target_date": target_date.isoformat(),
                        "completed": False,
                        "progress": 0
                    }).execute()
                    st.success("🎯 Goal added!")
                except Exception as e:
                    st.error(f"Error adding goal: {e}")

        try:
            resp = supabase.table("goals").select("*").eq("user_id", st.session_state["user"]["id"]).execute()
            goals_df = pd.DataFrame(resp.data)
            if not goals_df.empty:
                st.dataframe(goals_df[["goal", "target_date", "progress", "completed"]])
        except Exception as e:
            st.error(f"Error loading goals: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# PAGE: All Entries
# ==============================
elif page == "📚 All Entries":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h1 class='therapeutic-header'>📚 All Entries</h1>", unsafe_allow_html=True)

    if not st.session_state.get("user"):
        st.warning("⚠️ Please log in to see your entries.")
    else:
        try:
            resp = supabase.table("triggers").select("*").eq("user_id", st.session_state["user"]["id"]).execute()
            df = pd.DataFrame(resp.data)
            if df.empty:
                st.info("📝 No entries yet.")
            else:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                st.dataframe(df.sort_values('timestamp', ascending=False))
        except Exception as e:
            st.error(f"Error loading data: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
