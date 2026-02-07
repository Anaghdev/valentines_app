import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import base64
import os
import json
import requests
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="A Rose for Ammu 🌹", layout="centered", page_icon="🌹")

# ---------------- ASSETS & FUNCTIONS ----------------
def get_audio_html(file_path):
    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"""
        <audio id="love-audio" loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.getElementById("love-audio");
            audio.volume = 0.4;
            function playAudio() {{
                audio.play().catch(function(e){{ console.log(e); }});
            }}
            playAudio();
            window.parent.document.addEventListener('click', playAudio, {{ once: true }});
        </script>
        """
    except Exception as e:
        return ""

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottiefile(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "rose_accepted" not in st.session_state:
    st.session_state.rose_accepted = False

# ---------------- GLOBAL CSS (VELVET & ROSE GOLD) ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;700&family=Lato:wght@300;400&display=swap');

/* 1. VELVET NIGHT BACKGROUND */
body, .stApp {
    background: radial-gradient(circle at 50% 50%, #4a0404 0%, #2b0c16 40%, #000000 100%);
    background-size: cover;
    background-attachment: fixed;
    color: #ffd700; /* Gold text mostly */
    font-family: 'Lato', sans-serif;
}

/* 2. ELEGANT GLASS CARD */
.glass-card {
    background: rgba(40, 0, 0, 0.4); /* Dark Red Tint */
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(183, 110, 121, 0.3); /* Rose Gold Border */
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border-radius: 15px;
    padding: 40px;
    margin: 30px 0;
    position: relative;
    overflow: hidden;
}

/* Rose Gold Glow on Hover */
.glass-card:hover {
    border: 1px solid rgba(183, 110, 121, 0.6);
    box-shadow: 0 10px 40px rgba(210, 4, 45, 0.2);
}

/* 3. ROMANTIC TYPOGRAPHY */
.romantic-title {
    font-family: 'Great Vibes', cursive;
    font-size: 80px;
    color: #E0BFB8; /* Rose Gold/Pale Pink */
    text-align: center;
    margin-top: 20px;
    text-shadow: 0 0 15px rgba(224, 191, 184, 0.3);
    animation: float-text 3s ease-in-out infinite;
}

@keyframes float-text {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.sub-title {
    font-family: 'Cinzel', serif;
    text-align: center;
    color: rgba(255,255,255,0.7);
    font-size: 16px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 50px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    display: inline-block;
    padding-bottom: 10px;
}

/* 4. GOLDEN BUTTONS */
.stButton button {
    background: linear-gradient(135deg, #4a0404 0%, #2b0c16 100%) !important;
    border: 1px solid #B76E79 !important; /* Rose Gold */
    color: #E0BFB8 !important;
    font-family: 'Cinzel', serif !important;
    border-radius: 5px !important;
    padding: 10px 30px !important;
    transition: all 0.4s ease !important;
}
.stButton button:hover {
    background: #B76E79 !important;
    color: #2b0c16 !important;
    box-shadow: 0 0 20px rgba(183, 110, 121, 0.4) !important;
}

/* 5. INPUT FIELDS */
.stTextInput input {
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid #4a0404 !important;
    color: #E0BFB8 !important;
    text-align: center;
    font-family: 'Cinzel', serif;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FALLING PETALS JS ----------------
components.html("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.7.2/vanilla-tilt.min.js"></script>

<div id="petal-container" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:-1; overflow:hidden;"></div>

<script>
// SVG PETAL SHAPES
const petalPaths = [
    "M10,0 C10,0 20,5 20,15 C20,25 10,25 0,15 C-10,5 10,0 10,0 Z", // Simple petal
    "M10,0 C10,0 25,5 25,20 C25,40 5,40 5,20 C5,5 10,0 10,0 Z"  // Elongated petal
];

const colors = ["#8B0000", "#DC143C", "#B22222", "#FFC0CB", "#C71585"];

function createPetal() {
    const container = document.getElementById("petal-container");
    const petal = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    
    petal.setAttribute("viewBox", "0 0 30 50");
    petal.style.width = (Math.random() * 20 + 10) + "px";
    petal.style.height = (Math.random() * 20 + 20) + "px";
    petal.style.position = "absolute";
    petal.style.left = Math.random() * 100 + "vw";
    petal.style.top = "-50px";
    petal.style.opacity = Math.random() * 0.5 + 0.3;
    petal.style.zIndex = "-1";
    
    path.setAttribute("d", petalPaths[Math.floor(Math.random() * petalPaths.length)]);
    path.setAttribute("fill", colors[Math.floor(Math.random() * colors.length)]);
    
    petal.appendChild(path);
    container.appendChild(petal);
    
    // Fall Animation with Sway
    gsap.to(petal, {
        y: window.innerHeight + 100,
        x: "+=" + (Math.random() * 100 - 50),
        rotation: Math.random() * 360,
        rotationX: Math.random() * 360,
        rotationY: Math.random() * 360,
        duration: Math.random() * 5 + 5,
        ease: "none",
        onComplete: () => petal.remove()
    });
}

// Create petals frequently
setInterval(createPetal, 300);

// Tilt Init
setInterval(() => {
    VanillaTilt.init(window.parent.document.querySelectorAll('.glass-card'), {
        max: 5, speed: 400, "glare": true, "max-glare": 0.2
    });
}, 1000);
</script>
""", height=0)


# ---------------- CONTENT ----------------

# LOCK SCREEN
if not st.session_state.authenticated:
    st.markdown("<div style='height: 30vh'></div>", unsafe_allow_html=True)
    st.markdown("<div class='romantic-title'>Only For You</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-family:Cinzel; color:#B76E79; margin-bottom:20px;'>ENTER YOUR BIRTHDAY</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        pwd = st.text_input("Key", type="password", label_visibility="collapsed")
        if st.button("Unlock Heart"):
             if pwd == "11072007":
                 st.session_state.authenticated = True
                 st.rerun()
             else:
                 st.error("Incorrect.")
    st.stop()

# MAIN CONTENT
components.html(get_audio_html("love.mp3"), height=0)

# HEADER
st.markdown("<div class='romantic-title'>Happy Rose Day, Ammu</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'><span class='sub-title'>ETERNAL LOVE & DEVOTION</span></div>", unsafe_allow_html=True)

# GLASS LETTER
st.markdown("""
<div class='glass-card' data-tilt>
    <div style='text-align:center; margin-bottom:20px;'>
        <span style='font-size:40px;'>🌹</span>
    </div>
    <h3 style='color:#E0BFB8; text-align:center; font-family:"Great Vibes"; font-size:42px; margin-bottom:20px;'>My Dearest Ammu,</h3>
    <p style='font-size:20px; line-height:1.8; text-align:center; color: #fff; font-family:"Cinzel", serif; font-weight:400;'>
    "I would rather spend one lifetime with you, than face all the ages of this world alone."
    <br><br>
    This rose is a symbol of my undying passion. In the quiet of this velvet night, know that you are my heart's only desire.
    </p>
</div>
""", unsafe_allow_html=True)

# VIDEO
if os.path.exists("Boy_Gives_Roses_To_Girl_Video.mp4"):
    st.markdown("<div class='glass-card' style='padding:10px;'>", unsafe_allow_html=True)
    st.video("Boy_Gives_Roses_To_Girl_Video.mp4")
    st.markdown("</div>", unsafe_allow_html=True)

# INTERACTION
if not st.session_state.rose_accepted:
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Accept My Love"):
            st.session_state.rose_accepted = True
            st.rerun()
    with c2:
         # Minimalist "No" button that runs away
         components.html("""
        <button id="noBtn" style="padding:10px 25px; background:transparent; color:#777; border: 1px solid #555; border-radius: 5px; cursor: pointer; font-family:serif;">Decline</button>
        <script>
            const btn = document.getElementById("noBtn");
            btn.addEventListener('mouseover', () => {
                const x = Math.random() * (window.innerWidth - 100);
                const y = Math.random() * (window.innerHeight - 50);
                btn.style.position = 'fixed'; btn.style.left = x + 'px'; btn.style.top = y + 'px';
            });
        </script>
        """, height=60)

if st.session_state.rose_accepted:
    # Confetti - Red & Gold only
    components.html("""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
      var end = Date.now() + (5 * 1000);
      var colors = ['#bb0000', '#ffffff', '#ffd700'];
      (function frame() {
        confetti({ particleCount: 5, angle: 60, spread: 55, origin: { x: 0 }, colors: colors });
        confetti({ particleCount: 5, angle: 120, spread: 55, origin: { x: 1 }, colors: colors });
        if (Date.now() < end) { requestAnimationFrame(frame); }
      }());
    </script>
    """, height=0)

    # Lottie
    lottie_rose = None
    if os.path.exists("rose.json"):
        lottie_rose = load_lottiefile("rose.json")
    else:
        lottie_rose = load_lottieurl("https://lottie.host/93222be8-9646-4a4b-8451-93c833c9406e/HJM5Wd9dG6.json") 
    
    if lottie_rose:
        try:
             from streamlit_lottie import st_lottie
             with st.container():
                c1,c2,c3 = st.columns([1,2,1])
                with c2:
                    st_lottie(lottie_rose, height=250, key="romance_rose")
        except: pass
    
    st.markdown("<div class='romantic-title' style='font-size:50px; margin-bottom:30px;'>Forever Yours</div>", unsafe_allow_html=True)
    
    if os.path.exists("celebration.mp4"):
         st.video("celebration.mp4", autoplay=True)

    # Gallery
    st.markdown("<div style='margin-top:50px; text-align:center; font-family:Cinzel; color:#B76E79; letter-spacing:3px;'>OUR MEMORIES</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    images = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
    for i, img_path in enumerate(images):
        with cols[i]:
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    img_data = base64.b64encode(f.read()).decode()
                st.markdown(f"<div class='glass-card' style='padding:5px;'><img src='data:image/jpeg;base64,{img_data}' style='width:100%; border-radius:10px; opacity:0.9;'></div>", unsafe_allow_html=True)

    # Countdown
    anniversary = datetime(2026, 10, 22)
    days_left = (anniversary - datetime.now()).days
    st.markdown(f"""
    <div style='text-align:center; margin-top:50px; border-top:1px solid #4a0404; padding-top:20px;'>
        <div style='font-family:Cinzel; color:#E0BFB8; letter-spacing:2px;'>COUNTDOWN TO FOREVER</div>
        <div style='font-family:Great Vibes; color:#DC143C; font-size:60px;'>{days_left} Days</div>
        <div style='font-family:Cinzel; color:#777; font-size:12px;'>UNTIL october 22</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 100px; text-align:center; color:#555; padding-top:50px; font-family:Cinzel;'>With all my love</div>", unsafe_allow_html=True)


