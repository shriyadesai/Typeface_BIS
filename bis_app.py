import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Typeface BIS Manager", layout="wide")

# --- MOCK DATA GENERATION (INITIAL STATE) ---
def get_initial_data():
    return [
        {"id": "A001", "type": "LinkedIn Post", "content": "Our new feature is a game-changer for the industry! #Tech", "image_url": "https://placehold.co/600x400/EEE/31343C?text=Visual+A", "visual": 98, "compliance": 40, "issues": ["Banned: 'Game-changer'", "Tone: Hype"], "status": "Pending"},
        {"id": "A002", "type": "Email Subject", "content": "Meeting you where you are: Flexible support.", "image_url": None, "visual": 100, "compliance": 95, "issues": [], "status": "Pending"},
        {"id": "A003", "type": "Instagram Ad", "content": "Boost your synergy with our new tool.", "image_url": "https://placehold.co/600x400/FF0000/FFFFFF?text=Logo+Error", "visual": 60, "compliance": 50, "issues": ["Visual: Logo < 10px", "Banned: 'Synergy'"], "status": "Pending"},
        {"id": "A004", "type": "Blog Header", "content": "3 Ways to Streamline Your Workflow", "image_url": "https://placehold.co/800x400/3357FF/FFFFFF?text=On+Brand", "visual": 99, "compliance": 100, "issues": [], "status": "Pending"},
        {"id": "A005", "type": "LinkedIn Post", "content": "Revolutionize your workflow with AI.", "image_url": None, "visual": 100, "compliance": 65, "issues": ["Banned: 'Revolutionize'"], "status": "Pending"},
        {"id": "A006", "type": "Email Body", "content": "Hi Team, just checking in on the project...", "image_url": None, "visual": 100, "compliance": 88, "issues": ["Tone: Too Casual"], "status": "Pending"},
    ]

# --- SESSION STATE MANAGEMENT ---
# This ensures the app "remembers" when you approve/reject something
if 'assets' not in st.session_state:
    st.session_state['assets'] = get_initial_data()

if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- HELPER FUNCTIONS ---
def calculate_bis(visual, compliance):
    return int((visual + compliance) / 2)

def handle_action(asset_id, action):
    # Find the asset
    asset_idx = next((i for i, item in enumerate(st.session_state['assets']) if item["id"] == asset_id), None)
    if asset_idx is not None:
        asset = st.session_state['assets'].pop(asset_idx)
        asset['status'] = "Approved" if action == "approve" else "Rewritten"
        asset['action_timestamp'] = time.time()
        st.session_state['history'].append(asset)
        
        if action == "approve":
            st.toast(f"✅ Asset {asset_id} Approved & Published!")
        else:
            st.toast(f"🤖 Agent is rewriting Asset {asset_id}...")

# --- SIDEBAR FILTERS ---
st.sidebar.title("🎛️ BIS Filters")

# Score Slider
score_filter = st.sidebar.slider("Minimum BIS Score", 0, 100, 0)

# Type Filter
all_types = list(set([a['type'] for a in st.session_state['assets']]))
type_filter = st.sidebar.multiselect("Asset Type", all_types, default=all_types)

# Status Badge
pending_count = len(st.session_state['assets'])
st.sidebar.divider()
st.sidebar.metric("Pending Review", f"{pending_count}", delta=f"-{len(st.session_state['history'])} processed")

# --- MAIN DASHBOARD ---
st.title("🛡️ Brand Integrity Scoring (BIS)")
st.markdown("### Agentic Governance Interface")

tab1, tab2 = st.tabs(["⚡ Action Center", "📊 Live Insights"])

with tab1:
    # Filter Logic
    visible_assets = [
        a for a in st.session_state['assets'] 
        if calculate_bis(a['visual'], a['compliance']) >= score_filter
        and a['type'] in type_filter
    ]
    
    if not visible_assets:
        st.success("🎉 All caught up! No assets match the current filters.")
    
    for asset in visible_assets:
        bis_score = calculate_bis(asset['visual'], asset['compliance'])
        
        # Color coding
        if bis_score >= 90: border_color = "green"
        elif bis_score >= 70: border_color = "orange"
        else: border_color = "red"
        
        with st.expander(f"{asset['type']} | BIS Score: {bis_score}/100", expanded=True):
            c1, c2 = st.columns([1, 2])
            
            with c1:
                if asset['image_url']:
                    st.image(asset['image_url'], use_container_width=True)
                else:
                    st.info("📝 Text-only Asset")
            
            with c2:
                st.markdown(f"**Content:** _{asset['content']}_")
                
                # Metrics Columns
                m1, m2, m3 = st.columns(3)
                m1.metric("Visual Brand", f"{asset['visual']}%")
                m2.metric("Compliance", f"{asset['compliance']}%")
                m3.metric("Composite BIS", f"{bis_score}", delta_color="off")
                
                if asset['issues']:
                    st.error(f"⚠️ Issues: {', '.join(asset['issues'])}")
                else:
                    st.success("✅ No Compliance Issues Detected")
                
                # Action Buttons
                b1, b2 = st.columns([1, 1])
                if b1.button("✅ Approve", key=f"btn_app_{asset['id']}"):
                    handle_action(asset['id'], "approve")
                    st.rerun()
                
                if b2.button("✨ Auto-Rewrite", key=f"btn_rew_{asset['id']}"):
                    handle_action(asset['id'], "rewrite")
                    st.rerun()

with tab2:
    st.subheader("Compliance Analytics")
    
    # Create a DataFrame for analytics (combining active + history for trends)
    all_data = st.session_state['assets'] + st.session_state['history']
    df = pd.DataFrame(all_data)
    df['BIS Score'] = df.apply(lambda x: calculate_bis(x['visual'], x['compliance']), axis=1)
    
    # Chart 1: BIS Score Distribution
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(df, x="BIS Score", nbins=10, title="Distribution of Integrity Scores", color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col2:
            # Breakdown by Type
            fig_pie = px.pie(df, names='type', title="Asset Volume by Channel", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Chart 3: Scatter Plot (Visual vs Compliance)
        st.markdown("#### 📉 Compliance vs. Visual Brand Quality")
        fig_scatter = px.scatter(df, x="visual", y="compliance", color="type", size="BIS Score", hover_data=['content'], title="Outlier Detection Map")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No data available for analytics yet.")
# Footer
st.markdown("© 2024 Typeface Inc. | Prototype for Internal Use Only")
