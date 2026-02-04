import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="DeltaMath | Data Dashboard", layout="wide", page_icon="📐")

# 2. DeltaMath UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; color: #334155 !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    header[data-testid="stHeader"] { background-color: #2c3e50 !important; }
    .dm-header { background-color: #2c3e50; padding: 15px 30px; color: white; margin: -60px -50px 25px -50px; border-bottom: 4px solid #0056b3; }
    .mastery-container { display: flex; justify-content: center; margin-bottom: 20px; }
    .mastery-box { background-color: #ffffff; border: 1px solid #d1d5db; border-top: 4px solid #0056b3; padding: 10px 40px; text-align: center; }
    .hero-label { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #64748b; }
    .hero-value { font-size: 3rem; font-weight: 900; color: #2c3e50; line-height: 1; }
    .summary-box { padding: 15px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; text-align: center; min-height: 150px; }
    .summary-val { font-size: 1.8rem; font-weight: 800; color: #2c3e50; }
    .summary-label { font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase; }
    .goal-text { font-size: 1.1rem; font-weight: 800; color: #1e293b; margin-top: 8px; border-top: 1px dashed #cbd5e1; padding-top: 5px; }
    .integrity-callout { color: #b45309; font-weight: 800; font-size: 0.85rem; margin-top: 10px; line-height: 1.2; background: #fffbeb; padding: 4px; border-radius: 4px; }
    .strategy-container { background-color: #eff6ff; border-left: 5px solid #3b82f6; padding: 20px; border-radius: 4px; margin: 15px 0 25px 0; }
    .strategy-text { color: #1e3a8a; font-size: 1.1rem; line-height: 1.4; }
    .unified-card { background-color: #ffffff; border: 1px solid #e2e8f0; margin-bottom: 25px; border-radius: 4px; }
    .card-header { font-size: 1rem; font-weight: 700; padding: 10px; border-bottom: 1px solid #e2e8f0; background-color: #f8fafc; text-align: center; color: #1e293b; }
    .student-row { padding: 8px 15px; border-bottom: 1px solid #f1f5f9; font-size: 1rem; font-weight: 500; display: flex; justify-content: space-between; align-items: center; }
    .color-integrity { color: #b45309; font-weight: 800; } 
    .color-tier2 { color: #b91c1c; font-weight: 700; } 
    .color-mastery { color: #15803d; font-weight: 700; } 
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="dm-header"><h3>Δ DeltaMath | Data Dashboard</h3></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ Teacher Tools")
    uploaded_file = st.file_uploader("Upload Assignment CSV", type="csv")
    st.markdown("---")
    mastery_threshold = st.slider("Mastery Threshold (%)", 50, 100, 70, 5)
    st.markdown("---")
    show_colors = st.toggle("Enable Metric Color-Coding", value=True)
    goal_mastery_pct = st.slider("Goal Mastery Rate (%)", 0, 100, 80, 5)
    st.markdown("---")
    st.caption("AI Integration Specialist Prototype v6.0")

# --- DATA LOADING LOGIC (FIXED) ---
df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("sample_data.csv")
        st.info("💡 Pro Tip: I've loaded sample data so you can see how this works. To use your own, just upload a DeltaMath CSV in the sidebar!")
    except FileNotFoundError:
        st.warning("Please upload a DeltaMath CSV file to begin.")
        st.stop()

if df is not None:
    try:
        score_col = [c for c in df.columns if any(w in c for w in ['Grade', 'Score', 'Percent'])][0]
        ppm_col = "Problems Per Minute"
        df[ppm_col] = (df['Problems_Solved'] / df['Time_Spent_Minutes'].replace(0, 1)).astype(float).round(2)
        
        total_students = len(df)
        speed_gamers = df[df[ppm_col] > 3.5]
        struggling = df[(df[score_col] < mastery_threshold) & (df[ppm_col] <= 3.5)]
        mastery_group = df[(df[score_col] >= mastery_threshold) & (df[ppm_col] <= 3.5)]
        
        actual_mastery_rate = (len(mastery_group)/total_students)*100
        intervention_rate = (len(struggling)/total_students)*100
        integrity_flag_rate = (len(speed_gamers)/total_students)*100
        trend_pass = actual_mastery_rate >= goal_mastery_pct

        st.markdown(f'<div class="mastery-container"><div class="mastery-box"><div class="hero-label">AVG MASTERY</div><div class="hero-value">{df[score_col].mean():.1f}%</div></div></div>', unsafe_allow_html=True)

        s1, s2, s3 = st.columns(3)
        with s1: 
            callout = f'<div class="integrity-callout">↩️ Conference with flagged students.</div>' if integrity_flag_rate > 0 else ""
            st.markdown(f'<div class="summary-box"><div class="summary-label">Integrity Flag Rate</div><div class="summary-val" style="color:#b45309">{integrity_flag_rate:.1f}%</div>{callout}</div>', unsafe_allow_html=True)
        with s2: st.markdown(f'<div class="summary-box"><div class="summary-label">Intervention Rate</div><div class="summary-val" style="color:#b91c1c">{intervention_rate:.1f}%</div></div>', unsafe_allow_html=True)
        with s3: st.markdown(f'''<div class="summary-box"><div class="summary-label">Mastery Rate {"✅" if trend_pass else "❌"}</div><div class="summary-val" style="color:#15803d">{actual_mastery_rate:.1f}%</div><div class="goal-text">Goal: {goal_mastery_pct}%</div></div>''', unsafe_allow_html=True)

        strategy_text = "🔍 **Targeted Small Groups.** Pull Tier 2 students for quick feedback while others maintain momentum."
        if trend_pass: strategy_text = "🎉 **Goal Achieved.** Students are ready for extensions. Consider assigning the next skill or challenge problems."
        elif intervention_rate > 30: strategy_text = "⚠️ **High Intervention Required.** Pause independent work for a targeted whole-class re-teach."
        st.markdown(f'<div class="strategy-container"><div class="strategy-text">{strategy_text}</div></div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="unified-card"><div class="card-header">🚩 Integrity Check</div>', unsafe_allow_html=True)
            for _, r in speed_gamers.iterrows():
                st.markdown(f'<div class="student-row"><span class="color-integrity">{r["First"]} {r["Last"]}</span><span class="color-integrity">{r[score_col]}%</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="unified-card"><div class="card-header">🛠️ Tier 2 (Below {mastery_threshold}%)</div>', unsafe_allow_html=True)
            for _, r in struggling.iterrows():
                st.markdown(f'<div class="student-row"><span>{r["First"]} {r["Last"]}</span><span class="color-tier2">{r[score_col]}%</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="unified-card"><div class="card-header">✅ Mastery ({mastery_threshold}%+)</div>', unsafe_allow_html=True)
            for _, r in mastery_group.iterrows():
                st.markdown(f'<div class="student-row"><span>{r["First"]} {r["Last"]}</span><span class="color-mastery">{r[score_col]}%</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Full Roster Performance Explorer")
        st.dataframe(df, use_container_width=True, hide_index=True, column_config={ppm_col: st.column_config.NumberColumn(format="%.2f")})

    except Exception as e:
        st.error(f"Analysis Error: {e}. Please ensure your CSV has the correct headers.")
