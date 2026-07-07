# app.py — COMPLETE PLATE RATIO SYSTEM (V27 SHEET-DRIVEN SPECIAL EDITION)
# Design by Ovi • Max Plates Enforced & Candidate Sheets Driven Optimization

import os
import copy
import random
import math
import string
from collections import Counter
from math import ceil, floor
from datetime import datetime
from io import BytesIO

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import streamlit as st
import pandas as pd

# ================================================================
# LIBRARY IMPORTS & CHECKS FOR PDF GENERATION
# ================================================================
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ================================================================
# STREAMLIT PAGE CONFIGURATION
# ================================================================
st.set_page_config(
    page_title="Plate Ratio System - V27 Sheet Edition",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ================================================================
# MODERN UI STYLING & CUSTOM CSS
# ================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { 
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p { color: rgba(255,255,255,0.7); margin-top: 0.5rem; }
    .designer-name {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    .card:hover { border-color: rgba(102,126,234,0.5); box-shadow: 0 8px 32px rgba(0,0,0,0.2); }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 2px solid #667eea;
        display: inline-block;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
        color: white;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label { font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem; }
    .best-algo {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        border-radius: 20px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        border: none;
        box-shadow: 0 10px 30px rgba(0,176,155,0.3);
        margin-bottom: 2rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 12px;
        width: 100%;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102,126,234,0.4); }
    .stDataFrame { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 0.5rem; }
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ================================================================
# HEADER DISPLAY
# ================================================================
st.markdown("""
<div class="main-header">
    <h1>📊 Plate Ratio Intelligence System</h1>
    <p>Algorithm V27 • Expert Candidate Sheet-Driven Optimization</p>
    <div class="designer-name">✨ Design by Ovi ✨</div>
</div>
""", unsafe_allow_html=True)


# ================================================================
# HELPER FUNCTIONS
# ================================================================
def plate_name(n: int) -> str:
    """Convert number to Alphabetical ID (A, B, C... Z, AA...)"""
    n -= 1
    chars = string.ascii_uppercase
    out = ""
    while True:
        out = chars[n % 26] + out
        n = n // 26 - 1
        if n < 0:
            break
    return out


def calculate_waste_percent(plates: list, demand: dict) -> float:
    """Calculate material waste percentage"""
    total_produced = 0
    total_demand = sum(demand.values())
    if total_demand == 0: 
        return 0.0

    for tag in demand:
        produced_qty = 0
        for p in plates:
            if p and "layout" in p:
                produced_qty += p["layout"].get(tag, 0) * p.get("sheets", 0)
        total_produced += produced_qty

    if total_produced == 0: 
        return 100.0
    waste = total_produced - total_demand
    return round(max(0, (waste / total_produced) * 100), 2)


def ensure_demand_met(plates: list, demand: dict) -> list:
    """Adjust sheets to ensure absolutely no shortfall across any size"""
    if not plates: 
        return plates
    for tag in demand.keys():
        total_produced = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
        if total_produced < demand[tag]:
            shortfall = demand[tag] - total_produced
            last_plate = plates[-1]
            ups = max(1, last_plate["layout"].get(tag, 1))
            last_plate["sheets"] += ceil(shortfall / ups)
            
    for p in plates:
        p["production"] = {tag: ups * p["sheets"] for tag, ups in p["layout"].items()}
    return plates


def build_full_summary(plates: list, demand: dict, original_qty: dict) -> pd.DataFrame:
    """Generate final presentation data matrix"""
    rows = []
    sl = 1
    for tag in demand.keys():
        row = {
            "SL": sl, 
            "Tag": tag, 
            "Original QTY": original_qty.get(tag, 0), 
            "Produced (+Add-on)": demand[tag]
        }
        for p in plates:
            row[f"Plate {p['name']}"] = p["layout"].get(tag, 0)
            
        total_produced = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
        excess = total_produced - demand[tag]
        row["Total Produced QTY"] = total_produced
        row["Excess"] = max(0, excess)
        row["Excess %"] = f"{round((excess / demand[tag]) * 100, 2) if demand[tag] else 0}%"
        rows.append(row)
        sl += 1

    df = pd.DataFrame(rows)
    total_row = {
        "SL": "📊", 
        "Tag": "TOTAL", 
        "Original QTY": df["Original QTY"].sum(), 
        "Produced (+Add-on)": df["Produced (+Add-on)"].sum()
    }
    for p in plates:
        total_row[f"Plate {p['name']}"] = df[f"Plate {p['name']}"].sum()
        
    total_row["Total Produced QTY"] = df["Total Produced QTY"].sum()
    total_row["Excess"] = df["Excess"].sum()
    
    total_prod_sum = total_row["Total Produced QTY"]
    total_row["Excess %"] = f"{round((df['Excess'].sum() / total_prod_sum) * 100, 2) if total_prod_sum else 0}%"
    
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)


def generate_pdf_report(plates: list, demand: dict, original_qty: dict,
                        algo_name: str, waste_percent: float,
                        styles_dict: dict, colors_dict: dict, sizes_dict: dict, job_number: str) -> BytesIO or None:
    """Generate official ReportLab PDF documentation"""
    if not REPORTLAB_AVAILABLE: 
        return None
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('T1', parent=styles['Heading1'], fontSize=14, alignment=TA_CENTER, textColor=colors.HexColor('#667eea'))
        job_style = ParagraphStyle('T2', parent=styles['Heading2'], fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#764ba2'))
        sub_style = ParagraphStyle('T3', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)

        story = [
            Paragraph("📊 Plate Ratio System - Layout Report", title_style),
            Paragraph(f"🔢 Job Number: {job_number}", job_style),
            Paragraph(f"Engine: {algo_name} | Total Waste: {waste_percent}% | Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", sub_style),
            Spacer(1, 15)
        ]

        # Table Header Configuration
        header = ["SL", "Style", "Color", "Size", "Original", "Target"]
        for p in plates: 
            header.append(f"Plate {p['name']}")
        header.extend(["Total Prod", "Excess", "Excess %"])
        
        table_data = [header]
        sl = 1
        for tag in demand.keys():
            row = [
                str(sl), styles_dict.get(tag, "N/A"), colors_dict.get(tag, "N/A"), sizes_dict.get(tag, "N/A"),
                str(original_qty.get(tag, 0)), str(demand[tag])
            ]
            for p in plates:
                row.append(str(p["layout"].get(tag, 0)))
                
            total_prod = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
            excess = total_prod - demand[tag]
            row.extend([str(total_prod), str(excess), f"{round((excess/demand[tag])*100,1) if demand[tag] else 0}%"])
            table_data.append(row)
            sl += 1
            
        # Compile ReportLab PDF
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception:
        return None


# ================================================================
# ADVANCED V27 ENGINE: EXPERT CANDIDATE SHEET SIMULATION
# ================================================================
def algo_v27_candidate_sheet_optimization(demand_dict, plate_capacity=60, max_plates=3):
    """
    Simulates all matching candidate round sheets based on actual demand metrics.
    Completely eliminates rigid scaling multipliers.
    """
    TOTAL_UPS = plate_capacity
    total_initial_demand = sum(demand_dict.values())
    if total_initial_demand == 0: 
        return None
    
    # ১. এস্টিমেটেড বেস শিট
    estimated_base_sheets = total_initial_demand / TOTAL_UPS
    
    # ২. প্রোডাকশন ফ্রেন্ডলি ক্যান্ডিডেট শিটের তালিকা জেনারেট (২৫ বা ৫০ ব্যবধানে)
    start_sheet = max(25, int(estimated_base_sheets * 0.4))
    end_sheet = int(estimated_base_sheets * 1.7)
    step = 50 if estimated_base_sheets > 500 else 25
    
    candidate_sheets = list(range(start_sheet, end_sheet, step))
    if int(estimated_base_sheets) not in candidate_sheets:
        candidate_sheets.append(int(estimated_base_sheets))
    candidate_sheets = sorted([c for c in candidate_sheets if c > 0])

    best_result = None
    min_total_waste = float('inf')
    
    # ৩. ক্যান্ডিডেট শিট ধরে কমপ্লিট ডাইনামিক প্লেট সিমুলেশন লুপ
    for candidate in candidate_sheets:
        current_demand = copy.deepcopy(demand_dict)
        plates_list = []
        run_count = 1
        is_first_run = True
        
        while sum(current_demand.values()) > 0 and run_count <= max_plates:
            active_sizes = {k: v for k, v in current_demand.items() if v > 0}
            if not active_sizes: 
                break
            
            allocated_ups = {}
            total_active_demand = sum(active_sizes.values())
            
            # শেষ প্লেটের জন্য অবশিষ্ট সব ডিমান্ড কাভার করার স্ট্র্যাটেজি
            if run_count == max_plates:
                if len(active_sizes) <= TOTAL_UPS:
                    for size in active_sizes: 
                        allocated_ups[size] = 1
                    remaining_ups = TOTAL_UPS - sum(allocated_ups.values())
                    if remaining_ups > 0:
                        for size, _ in sorted(active_sizes.items(), key=lambda x: x[1], reverse=True):
                            if remaining_ups == 0: break
                            allocated_ups[size] += 1
                            remaining_ups -= 1
                else:
                    allocated_ups = {sz: int(floor((qty / total_active_demand) * TOTAL_UPS)) for sz, qty in active_sizes.items()}
                    remaining_ups = TOTAL_UPS - sum(allocated_ups.values())
                    for size, _ in sorted(active_sizes.items(), key=lambda x: (x[1]/total_active_demand * TOTAL_UPS) - floor((x[1]/total_active_demand) * TOTAL_UPS), reverse=True):
                        if remaining_ups == 0: break
                        allocated_ups[size] += 1
                        remaining_ups -= 1
            else:
                # রেগুলার প্লেটের জন্য ডাইনামিক রেশিও ডিস্ট্রিবিউশন
                raw_ups = {sz: (qty / total_active_demand) * TOTAL_UPS for sz, qty in active_sizes.items()}
                allocated_ups = {sz: max(1, int(floor(val))) for sz, val in raw_ups.items()}
                remaining_ups = TOTAL_UPS - sum(allocated_ups.values())
                if remaining_ups > 0:
                    for size, _ in sorted(raw_ups.items(), key=lambda x: x[1] - allocated_ups[x[0]], reverse=True):
                        if remaining_ups == 0: break
                        allocated_ups[size] += 1
                        remaining_ups -= 1
                while sum(allocated_ups.values()) > TOTAL_UPS:
                    max_tag = max(allocated_ups, key=allocated_ups.get)
                    allocated_ups[max_tag] -= 1

            # প্রথম কম্বিনেশনে ক্যান্ডিডেট শিট অ্যাসাইন হবে
            if is_first_run:
                run_sheets = candidate
                is_first_run = False
                if run_count == max_plates:
                    needed = [ceil(current_demand[sz] / max(1, allocated_ups.get(sz, 1))) for sz in active_sizes]
                    if needed: 
                        run_sheets = max(run_sheets, max(needed))
            else:
                if run_count == max_plates:
                    needed = [ceil(current_demand[sz] / max(1, allocated_ups.get(sz, 1))) for sz in active_sizes]
                    run_sheets = max(needed) if needed else 1
                else:
                    run_sheets = max(1, min(ceil(qty / allocated_ups.get(sz, 1)) for sz, qty in active_sizes.items()))
            
            plate_production = {sz: ups * run_sheets for sz, ups in allocated_ups.items()}
            for sz, qty in plate_production.items():
                current_demand[sz] = max(0, current_demand[sz] - qty)
            
            plates_list.append({
                "plate_index": run_count, 
                "name": plate_name(run_count),
                "layout": allocated_ups, 
                "sheets": run_sheets, 
                "production": plate_production
            })
            run_count += 1
            
        # অপ্টিমাইজেশন ম্যাট্রিক্স স্কোরিং (মিনিমাম ওয়েস্টেজ ট্র্যাকিং)
        total_produced = {sz: 0 for sz in demand_dict.keys()}
        for p in plates_list:
            for sz, qty in p["production"].items(): 
                total_produced[sz] += qty
        
        scenario_waste = sum(max(0, total_produced[sz] - target) for sz, target in demand_dict.items())
        
        if scenario_waste < min_total_waste:
            min_total_waste = scenario_waste
            best_result = {
                "plates": plates_list, 
                "waste": scenario_waste, 
                "candidate_sheet": candidate
            }
            
    return best_result


# ================================================================
# CONTROL PANEL INTERFACE
# ================================================================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">⚙️ Production Configuration Panel</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1: n = st.number_input("🏷️ Number of Items", 1, 500, 3)
with col2: cap = st.number_input("📀 Plate Capacity (UPS)", 1, 200, 60)
with col3: maxp = st.number_input("🎨 Max Plates Allowed", 1, 50, 3)
with col4: addon = st.number_input("📈 Add-on / Waste Margin (%)", 0.0, 50.0, 0.0, step=0.5)
with col5: job_number = st.text_input("🔢 Production Job ID", value="JOB-001")
st.markdown('</div>', unsafe_allow_html=True)


# ================================================================
# INPUT METHOD ROUTING
# ================================================================
input_mode = st.radio("Choose Preferred Input Pipeline:", options=["✏️ Manual Input Matrix", "📂 Automated Excel Pipeline (.xlsx)"], horizontal=True)

styles_dict, colors_dict, sizes_dict, original_qty, demand_dict = {}, {}, {}, {}, {}
tags = []

if "✏️ Manual Input Matrix" in input_mode:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for i in range(n):
        c1, c2, c3, c4, c5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
        c1.markdown(f"<p style='margin-top:2rem; font-weight:bold;'>#{i+1}</p>", unsafe_allow_html=True)
        style_val = c2.text_input("Style Identification", value=f"Style_{i+1}", key=f"s_{i}")
        color_val = c3.text_input("Color Specification", value="Black", key=f"c_{i}")
        size_val = c4.text_input("Size Standard", value=chr(83 + i % 4), key=f"z_{i}")
        qty_val = c5.number_input("Target Order Volume", min_value=0, value=1000 * (i+1), step=100, key=f"q_{i}")
        
        tag = f"Item_{i+1}_{style_val}_{size_val}"
        tags.append(tag)
        styles_dict[tag], colors_dict[tag], sizes_dict[tag], original_qty[tag] = style_val, color_val, size_val, qty_val
        demand_dict[tag] = int(qty_val * (1 + addon / 100))
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="card"><div class="card-title">📂 Upload Industrial Production Matrix</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload .xlsx Spreadsheet Matrix", type=["xlsx"])
    if uploaded_file:
        try:
            # Skiprows fixed to skip exactly 29 lines of metadata and headers
            df_xl = pd.read_excel(uploaded_file, skiprows=29)
            st.success("Production Matrix Extracted Successfully!")
            st.dataframe(df_xl.head(10), use_container_width=True)
            
            columns_list = list(df_xl.columns)
            c_1, c_2, c_3, c_4 = st.columns(4)
            style_col = c_1.selectbox("Map Style Target Column", columns_list, index=0 if "Style" not in columns_list else columns_list.index("Style"))
            color_col = c_2.selectbox("Map Color Target Column", columns_list, index=min(1, len(columns_list)-1) if "Color" not in columns_list else columns_list.index("Color"))
            size_col = c_3.selectbox("Map Size Target Column", columns_list, index=min(2, len(columns_list)-1) if "Size" not in columns_list else columns_list.index("Size"))
            qty_col = c_4.selectbox("Map Volume Target Column", columns_list, index=min(3, len(columns_list)-1) if "Quantity" not in columns_list else columns_list.index("Quantity"))
            
            for index, row in df_xl.iterrows():
                st_val = str(row.get(style_col, 'N/A')).strip()
                cl_val = str(row.get(color_col, 'N/A')).strip()
                sz_val = str(row.get(size_col, 'N/A')).strip()
                q_val = int(row[qty_col]) if pd.notnull(row.get(qty_col)) else 0
                
                if q_val > 0:
                    tag = f"Item_{index+1}_{st_val}_{sz_val}"
                    tags.append(tag)
                    styles_dict[tag], colors_dict[tag], sizes_dict[tag], original_qty[tag] = st_val, cl_val, sz_val, q_val
                    demand_dict[tag] = int(q_val * (1 + addon / 100))
        except Exception as e:
            st.error(f"Spreadsheet Parsing Blocked: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)


# ================================================================
# SYSTEM CORE PROCESSOR EXECUTION
# ================================================================
if tags and sum(original_qty.values()) > 0:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🚀 Run V27 Candidate Sheet Simulation Solver", type="primary"):
        with st.spinner("Processing Matrix Multi-Pass Scenarios..."):
            res = algo_v27_candidate_sheet_optimization(demand_dict, cap, int(maxp))
            if res:
                final_plates = ensure_demand_met(res["plates"], demand_dict)
                w_percent = calculate_waste_percent(final_plates, demand_dict)
                
                # Global Session caching
                st.session_state['v27_plates'] = final_plates
                st.session_state['v27_waste'] = w_percent
                st.session_state['v27_cand'] = res["candidate_sheet"]
                st.session_state['run_success'] = True
    st.markdown('</div>', unsafe_allow_html=True)


# ================================================================
# ANALYTICS GRAPHICS AND DISPLAYS
# ================================================================
if st.session_state.get('run_success', False):
    plates = st.session_state['v27_plates']
    w_percent = st.session_state['v27_waste']
    cand_sheet = st.session_state['v27_cand']
    
    st.markdown(f'<div class="best-algo">🎖️ Best Candidate Print Sheet Selected: {cand_sheet} Sheets </div>', unsafe_allow_html=True)
    
    cm1, cm2, cm3 = st.columns(3)
    cm1.markdown(f'<div class="metric-card"><div class="metric-value">{len(plates)}</div><div class="metric-label">Active Plates Formed</div></div>', unsafe_allow_html=True)
    cm2.markdown(f'<div class="metric-card"><div class="metric-value">{w_percent}%</div><div class="metric-label">Calculated Material Over-production (Waste)</div></div>', unsafe_allow_html=True)
    cm3.markdown(f'<div class="metric-card"><div class="metric-value">{sum(p["sheets"] for p in plates)}</div><div class="metric-label">Combined Print Sheet Count</div></div>', unsafe_allow_html=True)
    
    st.write("##")
    
    # Summary Sheet Output
    st.markdown('<div class="card"><div class="card-title">📊 Final Optimized Production Matrix</div>', unsafe_allow_html=True)
    df_summary = build_full_summary(plates, demand_dict, original_qty)
    if not df_summary.empty:
        df_summary['Tag'] = df_summary['Tag'].apply(lambda x: styles_dict.get(x, x) if x != "TOTAL" else "TOTAL")
    st.dataframe(df_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed Expander Matrices
    st.markdown('<div class="card"><div class="card-title">🛠️ Micro Layout Formats per Plate</div>', unsafe_allow_html=True)
    for p in plates:
        with st.expander(f"⚙️ Plate {p['name']} Layout Structure — ({p['sheets']} Sheets)", expanded=True):
            p_cols = st.columns(2)
            with p_cols[0]:
                st.write("**Plate Ratio Allocation (UPS):**")
                st.json({sizes_dict.get(k, k): v for k, v in p["layout"].items() if v > 0})
            with p_cols[1]:
                st.write("**Net Physical Production Outputs:**")
                st.json({sizes_dict.get(k, k): v for k, v in p["production"].items() if v > 0})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Documentation Export Pipeline
    if REPORTLAB_AVAILABLE:
        st.markdown('<div class="card"><div class="card-title">📄 Industrial Documentation Pipeline</div>', unsafe_allow_html=True)
        pdf_buffer = generate_pdf_report(plates, demand_dict, original_qty, "V27 Candidate Sheet Driver", w_percent, styles_dict, colors_dict, sizes_dict, job_number)
        if pdf_buffer:
            st.download_button("📥 Download Ratio Breakdown PDF Report", pdf_buffer, f"{job_number}_V27_Analysis.pdf", mime="application/pdf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ================================================================
# SYSTEM FOOTER
# ================================================================
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid rgba(102,126,234,0.3); background: rgba(255,255,255,0.02); border-radius: 20px;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">© 2026 Plate Ratio System | Version 27 (Candidate Sheet Edition)</p>
    <p style="color: rgba(255,255,255,0.4); font-size: 0.8rem; margin: 5px 0;">Optimized Framework Engine • Injected with Sheet Driver Automations • Production Ready</p>
</div>
""", unsafe_allow_html=True)
