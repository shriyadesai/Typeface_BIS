import streamlit as st
import pandas as pd
import random
import time

# --- MOCK DATA: THE BRAND HUB ---
# In a real app, this would come from the Vector Database
BRAND_GUIDELINES = {
    "colors": ["#FF5733", "#33FF57", "#3357FF"],
    "tone": "Empathetic, Direct, Professional",
    "banned_words": ["Synergy", "Revolutionary", "Cutting-edge", "Game-changer"],
    "min_logo_padding": 20
}

# --- MOCK DATA: GENERATED ASSETS ---
# Simulating AI-generated content that needs review
MOCK_ASSETS = [
    {
        "id": "A001",
        "type": "LinkedIn Post",
        "content": "Our new feature is a game-changer for the industry! #Tech #Growth",
        "image_url": "https://placehold.co/600x400/EEE/31343C?text=Visual+Asset+A",
        "visual_score": 98,
        "compliance_score": 40,  # Low because of "game-changer"
        "detected_issues": ["Banned Word: 'Game-changer'", "Tone: Too Hype-driven"]
    },
    {
        "id": "A002",
        "type": "Email Subject Line",
        "content": "Meeting you where you are: A guide to flexible enterprise support.",
        "image_url": None,
        "visual_score": 100,
        "compliance_score": 95,
        "detected_issues": []
    },
    {
        "id": "A003",
        "type": "Instagram Ad",
        "content": "Boost your synergy with our new tool.",
        "image_url": "https://placehold.co/600x400/FF0000/FFFFFF?text=Logo+Too+Close",
        "visual_score": 60, # Low because of visual noise
        "compliance_score": 50,
        "detected_issues": ["Visual: Logo padding < 10px", "Banned Word: 'Synergy'"]
    },
    {
        "id": "A004",
        "type": "Blog Header",
        "content": "3 Ways to Streamline Your Workflow Today",
        "image_url": "https://placehold.co/800x400/3357FF/FFFFFF?text=On+Brand+Visual",
        "visual_score": 99,
        "compliance_score": 100,
        "detected_issues": []
    }
]

# --- HELPER FUNCTIONS ---
def calculate_aggregate_score(visual, compliance):
    return int((visual + compliance) / 2)

def get_status_color(score):
    if score >= 90:
        return "green"
    elif score >= 70:
        return "orange"
    else:
        return "red"

# --- MAIN APP UI ---
st.set_page_config(page_title="Typeface BIS Prototype", layout="wide")

# Sidebar: Brand Context
st.sidebar.title("🛡️ BIS Control Center")
st.sidebar.markdown("**Active Brand Profile:** Typeface Enterprise")
st.sidebar.divider()
st.sidebar.subheader("Guardrails Active")
st.sidebar.checkbox("Tone Check", value=True)
st.sidebar.checkbox("Visual Compliance", value=True)
st.sidebar.checkbox("Legal/Safety", value=True)
st.sidebar.divider()
st.sidebar.info("This prototype simulates the automated review loop for 500+ daily assets.")

# Main Dashboard
st.title("Brand Integrity Scoring (BIS) Dashboard")
st.markdown("### ⚡ Governance by Exception")
st.markdown("Reviewing AI-generated assets against **Typeface Brand Hub** rules.")

# Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Assets Pending", "4")
col2.metric("Auto-Approved", "1,240")
col3.metric("Avg Integrity Score", "88/100")

st.divider()

# Asset Feed
st.subheader("⚠️ Requires Human Attention (Low BIS Score)")

for asset in MOCK_ASSETS:
    bis_score = calculate_aggregate_score(asset['visual_score'], asset['compliance_score'])
    color = get_status_color(bis_score)
    
    with st.container():
        # Create a "Card" layout
        c1, c2, c3 = st.columns([1, 2, 1])
        
        with c1:
            # Display Image if available, else text placeholder
            if asset['image_url']:
                st.image(asset['image_url'], use_container_width=True)
            else:
                st.markdown(f"**{asset['type']}** (Text Only)")
        
        with c2:
            st.markdown(f"#### {asset['type']}")
            st.markdown(f"_{asset['content']}_")
            
            if asset['detected_issues']:
                st.error(f"**Issues Detected:** {', '.join(asset['detected_issues'])}")
            else:
                st.success("✅ Brand Compliant")
                
        with c3:
            st.markdown(f"### BIS: :{color}[{bis_score}]")
            st.progress(bis_score / 100)
            
            # Action Buttons
            b1, b2 = st.columns(2)
            if b1.button("Approve", key=f"app_{asset['id']}"):
                st.toast(f"Asset {asset['id']} Published!")
            if b2.button("Rewrite", key=f"rew_{asset['id']}"):
                st.toast(f"Agent regenerating {asset['id']}...")
        
        st.divider()

# Footer
st.markdown("© 2024 Typeface Inc. | Prototype for Internal Use Only")
