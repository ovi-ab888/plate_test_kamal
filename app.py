# ================================================================
# app.py — V27 ENGINE ONLY (FIXED)
# Pure V27 Engine Application
# Design by Ovi
# ================================================================

import os
import copy
import random
import math
import string
from collections import defaultdict
from math import ceil, floor
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Tuple, Optional

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import streamlit as st
import pandas as pd

# ================================================================
# LIBRARY IMPORTS & CHECKS
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
    page_title="Mr Kamal - Plate Ratio System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================================================================
# CSS STYLING
# ================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #1a1a3e, #24243e, #1a1a3e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 30px;
        margin: 1rem 1rem 2rem 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
    }
    .main-header .subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 1.1rem;
        margin-top: 0.3rem;
    }
    .main-header .designer {
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
    .result-card {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        border-radius: 20px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        border: none;
        box-shadow: 0 10px 30px rgba(0,176,155,0.3);
        margin-bottom: 2rem;
    }
    .result-card .big-number {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .result-card .label {
        font-size: 0.9rem;
        opacity: 0.9;
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
    .stNumberInput input, .stTextInput input {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 5px !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
    }
    .stDataFrame { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 0.5rem; }
    .metric-item {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .metric-item .value {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-item .label {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.6);
        margin-top: 0.2rem;
    }
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================================================================
# HEADER
# ================================================================
st.markdown("""
<div class="main-header">
    <h1>🚀 V27 Engine</h1>
    <div class="subtitle">Smart Production Planning & Ratio Optimization</div>
    <div class="designer">✨ Design by Ovi ✨</div>
</div>
""", unsafe_allow_html=True)

# ================================================================
# HELPER FUNCTIONS
# ================================================================

def plate_name(n: int) -> str:
    """Convert number to Excel-style column name"""
    n -= 1
    chars = string.ascii_uppercase
    out = ""
    while True:
        out = chars[n % 26] + out
        n = n // 26 - 1
        if n < 0:
            break
    return out

def ensure_demand_met(plates: list, demand: dict) -> list:
    """Ensure all demand is met"""
    if not plates:
        return plates
    
    for tag in demand.keys():
        total_produced = 0
        for plate in plates:
            total_produced += plate["layout"].get(tag, 0) * plate["sheets"]
        
        if total_produced < demand.get(tag, 0):
            shortfall = demand.get(tag, 0) - total_produced
            if plates:
                last_plate = plates[-1]
                ups = last_plate["layout"].get(tag, 1)
                additional_sheets = ceil(shortfall / max(1, ups))
                last_plate["sheets"] += additional_sheets
    
    for idx, plate in enumerate(plates):
        if "name" not in plate:
            plate["name"] = plate_name(idx + 1)
    
    return plates

def calculate_waste_percent(plates: list, demand: dict) -> float:
    """Calculate waste percentage"""
    total_produced = 0
    total_demand = sum(demand.values())
    
    if total_demand == 0:
        return 0.0

    for plate in plates:
        for tag, ups in plate["layout"].items():
            total_produced += ups * plate.get("sheets", 0)

    if total_produced == 0:
        return 100.0

    waste = total_produced - total_demand
    waste_percent = (waste / total_produced) * 100
    
    if waste_percent < 0:
        waste_percent = 0.0
    
    return round(waste_percent, 2)

def build_full_summary(plates: list, demand: dict, original_qty: dict) -> pd.DataFrame:
    """Build complete summary DataFrame"""
    rows = []
    sl = 1

    for tag in demand.keys():
        row = {
            "SL": sl,
            "Tag": tag,
            "Original QTY": original_qty.get(tag, 0),
            "Produced (+Add-on)": demand[tag]
        }

        for idx, p in enumerate(plates):
            if p and "layout" in p and "name" in p:
                ups = p["layout"].get(tag, 0)
                row[f"Plate {p['name']}"] = ups
            else:
                row[f"Plate {idx+1}"] = 0

        total_produced = 0
        for p in plates:
            if p and "layout" in p:
                ups = p["layout"].get(tag, 0)
                sheets = p.get("sheets", 0)
                total_produced += ups * sheets

        excess = total_produced - demand[tag]
        excess_percent = round((excess / demand[tag]) * 100, 2) if demand[tag] else 0

        row["Total Produced QTY"] = total_produced
        row["Excess"] = max(0, excess)
        row["Excess %"] = f"{max(0, excess_percent)}%"
        rows.append(row)
        sl += 1

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    total_row = {
        "SL": "📊",
        "Tag": "TOTAL",
        "Original QTY": df["Original QTY"].sum(),
        "Produced (+Add-on)": df["Produced (+Add-on)"].sum(),
    }

    for idx, p in enumerate(plates):
        col_name = f"Plate {p['name']}" if "name" in p else f"Plate {idx+1}"
        if col_name in df.columns:
            total_row[col_name] = df[col_name].sum()
        else:
            total_row[col_name] = 0

    total_row["Total Produced QTY"] = df["Total Produced QTY"].sum()
    total_excess = df["Excess"].sum()
    total_row["Excess"] = total_excess
    
    total_produced_qty = total_row["Total Produced QTY"]
    total_excess_percent = round((total_excess / total_produced_qty) * 100, 2) if total_produced_qty > 0 else 0
    total_row["Excess %"] = f"{total_excess_percent}%"

    df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
    return df

def generate_pdf_report(plates: list, demand: dict, original_qty: dict,
                        algo_name: str, waste_percent: float,
                        styles_dict: dict = None, colors_dict: dict = None, 
                        sizes_dict: dict = None, job_number: str = "") -> BytesIO | None:
    """Generate professional PDF report"""
    if not REPORTLAB_AVAILABLE:
        return None

    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=landscape(A4),
            rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
        )
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Heading1'],
            fontSize=14, alignment=TA_CENTER, 
            textColor=colors.HexColor('#667eea'),
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            'CustomSubtitle', parent=styles['Normal'],
            fontSize=9, alignment=TA_CENTER, 
            textColor=colors.grey,
            spaceAfter=12
        )
        footer_style = ParagraphStyle(
            'Footer', parent=styles['Normal'],
            fontSize=8, alignment=TA_CENTER, 
            textColor=colors.grey,
            spaceTop=12
        )

        story = []
        
        story.append(Paragraph("🚀 V27 Engine - Ratio Report", title_style))
        if job_number:
            story.append(Paragraph(f"🔢 Job Number: {job_number}", 
                          ParagraphStyle('JobStyle', parent=styles['Heading2'],
                                       fontSize=12, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#764ba2'),
                                       spaceAfter=8)))
        story.append(Paragraph(
            f"Algorithm: {algo_name} | Waste: {waste_percent}% | "
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            subtitle_style
        ))
        story.append(Spacer(1, 10))

        # Build header
        header_row = ["SL", "Style", "Color", "Size", "Original", "With Add-on"]
        for p in plates:
            header_row.append(f"Plate {p['name']}")
        header_row.extend(["Total Prod.", "Excess", "Excess %"])
        
        summary_data = [header_row]
        
        sl = 1
        for tag in demand.keys():
            style = styles_dict.get(tag, "N/A") if styles_dict else "N/A"
            color = colors_dict.get(tag, "N/A") if colors_dict else "N/A"
            size = sizes_dict.get(tag, "N/A") if sizes_dict else "N/A"
            
            row = [str(sl), style, color, size, 
                   str(original_qty.get(tag, 0)), str(demand[tag])]
            
            total_produced = 0
            for p in plates:
                ups = p["layout"].get(tag, 0)
                row.append(str(ups))
                total_produced += ups * p["sheets"]
            
            excess = total_produced - demand[tag]
            excess_percent = f"{round((excess / demand[tag]) * 100, 2) if demand[tag] else 0}%"
            row.extend([str(total_produced), str(excess), excess_percent])
            summary_data.append(row)
            sl += 1
        
        # Total row
        total_row = ["📊", "TOTAL", "", "", 
                     str(sum(original_qty.values())), str(sum(demand.values()))]
        
        total_produced_sum = 0
        for p in plates:
            plate_total = 0
            for tag in demand:
                plate_total += p["layout"].get(tag, 0) * p["sheets"]
            total_row.append(str(plate_total))
            total_produced_sum += plate_total
        
        total_excess_sum = total_produced_sum - sum(demand.values())
        total_excess_percent = (
            f"{round((total_excess_sum / total_produced_sum) * 100, 2) if total_produced_sum > 0 else 0}%"
        )
        total_row.extend([str(total_produced_sum), str(total_excess_sum), total_excess_percent])
        summary_data.append(total_row)
        
        main_table = Table(summary_data, repeatRows=1)
        
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 6),
            ('ALIGN', (0, 1), (-1, -2), 'CENTER'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        for i in range(1, len(summary_data) - 1):
            if i % 2 == 0:
                table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa')))
        
        main_table.setStyle(TableStyle(table_style))
        story.append(main_table)
        story.append(Spacer(1, 15))
        
        # Plate Details
        story.append(Paragraph("🧾 Plate Configuration Details", 
                              ParagraphStyle('SubHeader', parent=styles['Heading2'],
                                           fontSize=11, alignment=TA_CENTER,
                                           textColor=colors.HexColor('#667eea'))))
        story.append(Spacer(1, 8))
        
        plate_data = [["SL", "Plate ID", "Sheets", "Total UPS"]]
        for idx, p in enumerate(plates, 1):
            plate_data.append([
                str(idx), 
                p["name"], 
                str(p["sheets"]), 
                str(sum(p["layout"].values()))
            ])
        
        plate_table = Table(plate_data)
        plate_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(plate_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(
            f"This Report Generated by Ovi's V27 Engine | Job: {job_number if job_number else 'N/A'} | All Rights Reserved",
            footer_style
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        return None


# ================================================================
# V27 ENGINE - COMPLETE IMPLEMENTATION
# ================================================================

class V27Engine:
    """
    V27 Engine - Smart Production Planning System
    """
    
    def __init__(self, capacity: int, max_plates: int, max_sheets: int = 100):
        self.capacity = capacity
        self.max_plates = max_plates
        self.max_sheets = max_sheets
        self.learning_memory = {}
    
    # ================================================================
    # 1. INPUT VALIDATOR
    # ================================================================
    class InputValidator:
        @staticmethod
        def validate(demand: dict, capacity: int, max_plates: int) -> Tuple[bool, str]:
            if not demand:
                return False, "Demand data is empty"
            if not all(isinstance(v, (int, float)) and v >= 0 for v in demand.values()):
                return False, "All quantities must be positive numbers"
            if capacity <= 0:
                return False, "Plate capacity must be greater than 0"
            if max_plates <= 0:
                return False, "Max plates must be greater than 0"
            total_demand = sum(demand.values())
            if total_demand == 0:
                return False, "Total demand is zero"
            return True, "Validation successful"
    
    # ================================================================
    # 2. CANDIDATE SHEET GENERATOR
    # ================================================================
    class CandidateSheetGenerator:
        def __init__(self, capacity: int, max_plates: int, max_sheets: int = 100):
            self.capacity = capacity
            self.max_plates = max_plates
            self.max_sheets = max_sheets
        
        def generate_candidates(self, remaining_total: int) -> List[int]:
            capacity_per_round = self.max_plates * self.capacity
            if capacity_per_round == 0:
                return [1]
            
            base_sheets = math.ceil(remaining_total / capacity_per_round)
            candidates = []
            
            # First: base sheets
            candidates.append(base_sheets)
            
            # Second: reduced sheets (like your 12)
            if base_sheets > 3:
                candidates.append(max(1, base_sheets // 5))
            
            # Third: minimal sheets (like your 2)
            if base_sheets > 5:
                candidates.append(max(1, base_sheets // 30))
            
            # Add variations
            for i in range(max(1, base_sheets - 2), base_sheets + 3):
                if i not in candidates and i <= self.max_sheets:
                    candidates.append(i)
            
            return sorted(set(candidates))
    
    # ================================================================
    # 3. PLATE BUILDER
    # ================================================================
    class PlateBuilder:
        def __init__(self, capacity: int):
            self.capacity = capacity
        
        def build_layout(self, remaining: dict) -> dict:
            active = {k: v for k, v in remaining.items() if v > 0}
            if not active:
                return {}
            
            total_remaining = sum(active.values())
            layout = {}
            used_capacity = 0
            
            sorted_items = sorted(active.items(), key=lambda x: x[1], reverse=True)
            
            for tag, qty in sorted_items:
                if used_capacity >= self.capacity:
                    break
                
                ratio = qty / total_remaining if total_remaining > 0 else 0
                ups = max(1, int(ratio * self.capacity))
                ups = min(ups, self.capacity - used_capacity)
                
                if ups > 0:
                    layout[tag] = ups
                    used_capacity += ups
            
            while used_capacity < self.capacity and active:
                best_tag = max(active, key=lambda t: remaining[t] / (layout.get(t, 1) + 1))
                layout[best_tag] = layout.get(best_tag, 0) + 1
                used_capacity += 1
            
            return layout
    
    # ================================================================
    # 4. SINGLE ROUND SIMULATOR
    # ================================================================
    class SingleRoundSimulator:
        def __init__(self, max_plates: int, capacity: int):
            self.max_plates = max_plates
            self.capacity = capacity
            self.plate_builder = V27Engine.PlateBuilder(capacity)
        
        def simulate_round(self, remaining: dict, sheet_counts: List[int]) -> Tuple[List[dict], dict]:
            all_plates = []
            current_remaining = remaining.copy()
            
            for sheet_count in sheet_counts:
                for plate_num in range(self.max_plates):
                    if not any(v > 0 for v in current_remaining.values()):
                        break
                    
                    layout = self.plate_builder.build_layout(current_remaining)
                    if not layout:
                        break
                    
                    for tag, ups in layout.items():
                        current_remaining[tag] = max(0, current_remaining.get(tag, 0) - (ups * sheet_count))
                    
                    all_plates.append({
                        "name": plate_name(len(all_plates) + 1),
                        "layout": layout,
                        "sheets": sheet_count
                    })
            
            return all_plates, current_remaining
    
    # ================================================================
    # 5. WASTE CALCULATOR
    # ================================================================
    @staticmethod
    def calculate_waste(plates: list, demand: dict) -> float:
        total_produced = 0
        total_demand = sum(demand.values())
        
        if total_demand == 0:
            return 0.0
        
        for plate in plates:
            for tag, ups in plate["layout"].items():
                total_produced += ups * plate.get("sheets", 0)
        
        if total_produced == 0:
            return 100.0
        
        waste = total_produced - total_demand
        waste_percent = (waste / total_produced) * 100
        return max(0, round(waste_percent, 2))
    
    # ================================================================
    # 6. SOLUTION SCORER
    # ================================================================
    class SolutionScorer:
        def __init__(self, waste_weight: float = 0.5, plates_weight: float = 0.25, sheets_weight: float = 0.25):
            self.waste_weight = waste_weight
            self.plates_weight = plates_weight
            self.sheets_weight = sheets_weight
        
        def score(self, plates: list, demand: dict) -> float:
            waste = V27Engine.calculate_waste(plates, demand)
            num_plates = len(plates)
            total_sheets = sum(p.get("sheets", 0) for p in plates)
            
            waste_score = waste / 100
            plates_score = num_plates / 100
            sheets_score = total_sheets / 100
            
            return (self.waste_weight * waste_score +
                    self.plates_weight * plates_score +
                    self.sheets_weight * sheets_score)
    
    # ================================================================
    # 7. SEARCH ENGINE
    # ================================================================
    class SearchEngine:
        def __init__(self, max_plates: int, capacity: int, iterations: int = 50):
            self.max_plates = max_plates
            self.capacity = capacity
            self.iterations = iterations
        
        def search(self, demand: dict) -> Tuple[list, dict]:
            best_solution = None
            best_score = float('inf')
            best_details = {}
            
            strategies = [
                self._greedy_strategy,
                self._balanced_strategy,
                self._proportional_strategy,
                self._random_strategy,
            ]
            
            for strategy in strategies:
                for _ in range(max(1, self.iterations // len(strategies))):
                    solution, details = strategy(demand)
                    if solution:
                        scorer = V27Engine.SolutionScorer()
                        score = scorer.score(solution, demand)
                        
                        if score < best_score:
                            best_score = score
                            best_solution = solution
                            best_details = details
            
            return best_solution, best_details
        
        def _greedy_strategy(self, demand: dict) -> Tuple[list, dict]:
            return self._simulate_with_strategy(demand, "greedy")
        
        def _balanced_strategy(self, demand: dict) -> Tuple[list, dict]:
            return self._simulate_with_strategy(demand, "balanced")
        
        def _proportional_strategy(self, demand: dict) -> Tuple[list, dict]:
            return self._simulate_with_strategy(demand, "proportional")
        
        def _random_strategy(self, demand: dict) -> Tuple[list, dict]:
            return self._simulate_with_strategy(demand, "random")
        
        def _simulate_with_strategy(self, demand: dict, strategy: str) -> Tuple[list, dict]:
            remaining = demand.copy()
            total_demand = sum(demand.values())
            capacity_per_round = self.max_plates * self.capacity
            
            if capacity_per_round == 0:
                return [], {}
            
            generator = V27Engine.CandidateSheetGenerator(self.capacity, self.max_plates)
            sheet_counts = generator.generate_candidates(total_demand)
            
            simulator = V27Engine.SingleRoundSimulator(self.max_plates, self.capacity)
            plates, final_remaining = simulator.simulate_round(remaining, sheet_counts)
            
            plates = ensure_demand_met(plates, demand)
            return plates, {
                "strategy": strategy, 
                "sheet_counts": sheet_counts,
                "final_balance": sum(final_remaining.values())
            }
    
    # ================================================================
    # 8. OUTPUT GENERATOR
    # ================================================================
    class OutputGenerator:
        @staticmethod
        def generate_summary(plates: list, demand: dict) -> dict:
            waste = V27Engine.calculate_waste(plates, demand)
            
            return {
                "plates": plates,
                "waste_percent": waste,
                "total_plates": len(plates),
                "total_sheets": sum(p.get("sheets", 0) for p in plates),
                "total_production": sum(
                    ups * p.get("sheets", 0) 
                    for p in plates 
                    for ups in p["layout"].values()
                ),
                "total_demand": sum(demand.values()),
            }


# ================================================================
# V27 ENGINE - YOUR IDEA IMPLEMENTATION
# ================================================================

def v27_optimizer(demand: dict, capacity: int, max_plates: int) -> list:
    """
    V27 Engine - Based on Your Idea
    
    Rules:
    1. UPS (capacity) কখনো পরিবর্তন হবে না
    2. Plate সংখ্যা User-এর Max Plates-এর বেশি হবে না
    3. অনেক Candidate Sheet Test করবে
    4. Manual Trial-এর বদলে Computer Search করবে
    """
    
    total_qty = sum(demand.values())
    capacity_per_round = max_plates * capacity
    
    # ================================================================
    # STEP 1: Estimated Sheet বের করুন
    # ================================================================
    estimated_sheets = math.ceil(total_qty / capacity_per_round)
    
    # ================================================================
    # STEP 2: অনেক Candidate Sheet তৈরি করুন
    # ================================================================
    candidate_sheets = []
    
    # Estimated Sheet এর আশেপাশে 20-30 টা Candidate তৈরি করুন
    for i in range(-15, 16):  # -15 to +15
        candidate = estimated_sheets + i
        if candidate >= 1:  # Sheet 0 বা negative হতে পারে না
            candidate_sheets.append(candidate)
    
    # Unique এবং Sorted করুন
    candidate_sheets = sorted(set(candidate_sheets))
    
    # ================================================================
    # STEP 3: প্রতিটি Candidate দিয়ে Simulation করুন
    # ================================================================
    best_solution = None
    best_waste = float('inf')
    best_details = {}
    
    for sheets in candidate_sheets:
        # 3.1: এই Candidate দিয়ে Production Calculate করুন
        remaining = demand.copy()
        plates = []
        plate_count = 0
        
        # 3.2: Max Plates পর্যন্ত প্লেট তৈরি করুন
        while plate_count < max_plates and any(v > 0 for v in remaining.values()):
            # Layout তৈরি করুন (UPS Fixed = capacity)
            layout = create_layout(remaining, capacity)
            
            if not layout:
                break
            
            # এই প্লেট Apply করুন
            for tag, ups in layout.items():
                remaining[tag] = max(0, remaining[tag] - (ups * sheets))
            
            plates.append({
                "name": plate_name(plate_count + 1),
                "layout": layout,
                "sheets": sheets
            })
            
            plate_count += 1
        
        # 3.3: Final Waste Calculate করুন
        final_waste = calculate_waste_percent(plates, demand)
        
        # 3.4: Best Solution Update করুন
        if final_waste < best_waste:
            best_waste = final_waste
            best_solution = plates
            best_details = {
                "sheets_used": sheets,
                "candidate_index": candidate_sheets.index(sheets),
                "total_candidates": len(candidate_sheets),
                "total_plates": len(plates)
            }
    
    # ================================================================
    # STEP 4: Best Solution Return করুন
    # ================================================================
    return ensure_demand_met(best_solution, demand)


def create_layout(remaining: dict, capacity: int) -> dict:
    """
    Plate Layout তৈরি করুন - UPS কখনো capacity এর বেশি হবে না
    """
    active = {k: v for k, v in remaining.items() if v > 0}
    if not active:
        return {}
    
    total_remaining = sum(active.values())
    layout = {}
    used_capacity = 0
    
    # ডিমান্ড অনুযায়ী সাজান (বড় থেকে ছোট)
    sorted_items = sorted(active.items(), key=lambda x: x[1], reverse=True)
    
    for tag, qty in sorted_items:
        if used_capacity >= capacity:
            break
        
        # UPS ক্যালকুলেট করুন (capacity এর বেশি হবে না)
        ratio = qty / total_remaining if total_remaining > 0 else 0
        ups = max(1, int(ratio * capacity))
        ups = min(ups, capacity - used_capacity)
        
        if ups > 0:
            layout[tag] = ups
            used_capacity += ups
    
    # বাকি ক্যাপাসিটি পূরণ করুন
    while used_capacity < capacity and active:
        best_tag = max(active, key=lambda t: remaining[t] / (layout.get(t, 1) + 1))
        layout[best_tag] = layout.get(best_tag, 0) + 1
        used_capacity += 1
    
    return layout


# ================================================================
# MAIN UI
# ================================================================

# ================================================================
# CONFIGURATION
# ================================================================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">⚙️ Production Configuration</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    n = st.number_input("🏷️ Number of Items", 1, 500, 1)
with col2:
    cap = st.number_input("📀 Plate Capacity (UPS)", 1, 200, 10)
with col3:
    maxp = st.number_input("🎨 Max Plates per Round", 1, 100, 60)
with col4:
    addon = st.number_input("📈 Add-on (%)", 0.0, 50.0, 0.0, step=0.5)
with col5:
    iterations = st.number_input("🔄 Search Iterations", 10, 200, 50, step=10)

st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# INPUT METHOD
# ================================================================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Input Method</div>', unsafe_allow_html=True)

input_mode = st.radio(
    "Select Input Mode:",
    options=["✏️ Manual Input", "📂 Upload Excel File"],
    horizontal=True,
    index=0
)

st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# MANUAL INPUT
# ================================================================
if input_mode == "✏️ Manual Input":
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Item Quantity Details (Manual)</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
    with col1:
        st.markdown("**SL**")
    with col2:
        st.markdown("**Style**")
    with col3:
        st.markdown("**Color**")
    with col4:
        st.markdown("**Size**")
    with col5:
        st.markdown("**Quantity**")
    
    st.markdown("---")
    
    tags = []
    styles = []
    colors = []
    sizes = []
    qty = []
    
    for i in range(n):
        col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
        
        with col1:
            st.markdown(f"**{i+1}**")
        with col2:
            style_val = st.text_input("Style", value="N/A", key=f"style_{i}", label_visibility="collapsed", placeholder="N/A")
        with col3:
            color_val = st.text_input("Color", value="N/A", key=f"color_{i}", label_visibility="collapsed", placeholder="N/A")
        with col4:
            size_val = st.text_input("Size", value="N/A", key=f"size_{i}", label_visibility="collapsed", placeholder="N/A")
        with col5:
            qty_val = st.number_input("Quantity", min_value=0, value=0, step=100, key=f"qty_manual_{i}", label_visibility="collapsed")
        
        styles.append(style_val.strip() if style_val.strip() else "N/A")
        colors.append(color_val.strip() if color_val.strip() else "N/A")
        sizes.append(size_val.strip() if size_val.strip() else "N/A")
        tags.append(f"Item {i+1}")
        qty.append(qty_val)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if any(q > 0 for q in qty):
        preview_df = pd.DataFrame({
            "SL": range(1, n + 1),
            "Style": styles,
            "Color": colors,
            "Size": sizes,
            "Quantity": qty
        })
        st.info("📋 Data Preview")
        st.dataframe(preview_df, use_container_width=True, height=200)
    
    original_qty = {f"Item {i+1}": int(q) for i, q in enumerate(qty) if q > 0}
    demand = {f"Item {i+1}": ceil(int(q) * (1 + addon / 100)) for i, q in enumerate(qty) if q > 0}
    
    st.session_state['item_styles'] = {f"Item {i+1}": styles[i] for i in range(n)}
    st.session_state['item_colors'] = {f"Item {i+1}": colors[i] for i in range(n)}
    st.session_state['item_sizes'] = {f"Item {i+1}": sizes[i] for i in range(n)}

# ================================================================
# EXCEL UPLOAD
# ================================================================
else:
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📂 Upload Excel File</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Excel file with Item Details",
        type=["xlsx", "xls"],
        help="File must have columns: SL, Style, Color, Size, Quantity"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            df = df.dropna(how='all')
            
            style_col = None
            color_col = None
            size_col = None
            qty_col = None
            
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if col_lower in ['style', 'styles']:
                    style_col = col
                elif col_lower in ['color', 'colors', 'colour']:
                    color_col = col
                elif col_lower in ['size', 'sizes']:
                    size_col = col
                elif col_lower in ['quantity', 'qty', 'qty.', 'quantities', 'total']:
                    qty_col = col
            
            if qty_col is None and len(df.columns) >= 2:
                for col in df.columns:
                    if df[col].dtype in ['int64', 'float64']:
                        qty_col = col
                        break
            
            if qty_col is None and len(df.columns) >= 2:
                qty_col = df.columns[-1]
            
            if style_col is None:
                style_col = df.columns[1] if len(df.columns) >= 2 else None
            if color_col is None:
                color_col = df.columns[2] if len(df.columns) >= 3 else None
            if size_col is None:
                size_col = df.columns[3] if len(df.columns) >= 4 else None
            
            if qty_col is None:
                st.error("❌ Could not find 'Quantity' column.")
                st.stop()
            
            style_data = df[style_col].astype(str).tolist() if style_col else ["N/A"] * len(df)
            color_data = df[color_col].astype(str).tolist() if color_col else ["N/A"] * len(df)
            size_data = df[size_col].astype(str).tolist() if size_col else ["N/A"] * len(df)
            qty_data = df[qty_col].tolist()
            
            cleaned_data = []
            for idx, (style, color, size, qty) in enumerate(zip(style_data, color_data, size_data, qty_data)):
                if pd.isna(qty):
                    continue
                try:
                    qty_int = int(float(qty))
                    if qty_int > 0:
                        style_val = str(style).strip() if not pd.isna(style) and str(style).strip() != '' else "N/A"
                        color_val = str(color).strip() if not pd.isna(color) and str(color).strip() != '' else "N/A"
                        size_val = str(size).strip() if not pd.isna(size) and str(size).strip() != '' else "N/A"
                        cleaned_data.append((style_val, color_val, size_val, qty_int))
                except (ValueError, TypeError):
                    continue
            
            if not cleaned_data:
                st.error("❌ No valid data found.")
                st.stop()
            
            style_list = [item[0] for item in cleaned_data]
            color_list = [item[1] for item in cleaned_data]
            size_list = [item[2] for item in cleaned_data]
            qty_list = [item[3] for item in cleaned_data]
            
            preview_df = pd.DataFrame({
                "Style": style_list,
                "Color": color_list,
                "Size": size_list,
                "Quantity": qty_list
            })
            
            st.success(f"✅ {len(cleaned_data)} items loaded successfully!")
            st.dataframe(preview_df, use_container_width=True)
            
            n = len(cleaned_data)
            tags = [f"Item {i+1}" for i in range(n)]
            qty = qty_list
            
            st.session_state['item_styles'] = {f"Item {i+1}": style_list[i] for i in range(n)}
            st.session_state['item_colors'] = {f"Item {i+1}": color_list[i] for i in range(n)}
            st.session_state['item_sizes'] = {f"Item {i+1}": size_list[i] for i in range(n)}
            
            original_qty = {t: int(q) for t, q in zip(tags, qty) if q > 0}
            demand = {t: ceil(int(q) * (1 + addon / 100)) for t, q in zip(tags, qty) if q > 0}
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.stop()
    else:
        st.info("📤 Please upload an Excel file to continue.")
        st.stop()

st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# GENERATE BUTTON
# ================================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("🚀 Generate with V27 Engine", use_container_width=True, type="primary")

# ================================================================
# RESULTS
# ================================================================
if generate_clicked:
    if not demand:
        st.error("⚠️ Please enter at least one item with quantity greater than 0")
        st.stop()
    
    with st.spinner("🔍 V27 Engine searching for optimal solution..."):
        
        # ✅ এখন v27_optimizer ডিফাইন করা আছে
        plates = v27_optimizer(demand, cap, maxp, iterations)
        
        if not plates:
            st.error("❌ V27 Engine could not find a solution. Please check your inputs.")
            st.stop()
        
        # Calculate metrics
        waste_percent = calculate_waste_percent(plates, demand)
        total_plates = len(plates)
        total_sheets = sum(p.get("sheets", 0) for p in plates)
        total_production = sum(
            ups * p.get("sheets", 0) 
            for p in plates 
            for ups in p["layout"].values()
        )
        total_demand = sum(demand.values())
        
        # ====================== RESULTS UI ======================
        st.markdown(f"""
        <div class="result-card">
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">✅ Solution Found!</div>
            <div class="big-number">Waste: {waste_percent}%</div>
            <div style="margin-top: 0.5rem;">
                <span class="label">📊 {total_plates} Plates</span>
                <span style="margin: 0 1rem;">|</span>
                <span class="label">📄 {total_sheets} Sheets</span>
                <span style="margin: 0 1rem;">|</span>
                <span class="label">📦 {total_production} Produced</span>
                <span style="margin: 0 1rem;">|</span>
                <span class="label">🎯 {total_demand} Demand</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============= SUMMARY TABLE =============
        st.markdown("### 📊 Production Summary")
        full_df = build_full_summary(plates, demand, original_qty)
        if not full_df.empty:
            st.dataframe(full_df, use_container_width=True, height=400)
        
        # ============= PLATE DETAILS =============
        st.markdown("### 🧾 Plate Configuration Details")
        plate_rows = []
        for idx, p in enumerate(plates, 1):
            plate_rows.append({
                "SL": idx,
                "Plate ID": p.get("name", f"Plate {idx}"),
                "Sheets Required": p.get("sheets", 0),
                "Total UPS": sum(p["layout"].values()),
                "Layout": str(p["layout"])
            })
        
        plate_df = pd.DataFrame(plate_rows)
        st.dataframe(plate_df, use_container_width=True)
        
        # ============= METRICS =============
        st.markdown("### 📈 Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-item">
                <div class="value">{waste_percent}%</div>
                <div class="label">Waste</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-item">
                <div class="value">{total_plates}</div>
                <div class="label">Total Plates</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-item">
                <div class="value">{total_sheets}</div>
                <div class="label">Total Sheets</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            efficiency = 100 - waste_percent
            st.markdown(f"""
            <div class="metric-item">
                <div class="value">{efficiency:.1f}%</div>
                <div class="label">Efficiency</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ============= DOWNLOAD BUTTONS =============
        st.markdown("### 📥 Download Report")
        col1, col2 = st.columns(2)
        
        with col1:
            bio_excel = BytesIO()
            with pd.ExcelWriter(bio_excel, engine="openpyxl") as writer:
                full_df.to_excel(writer, sheet_name="Summary", index=False)
                plate_df.to_excel(writer, sheet_name="Plate Details", index=False)
            bio_excel.seek(0)
            
            st.download_button(
                "📊 Download Excel",
                bio_excel,
                f"V27_Engine_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                use_container_width=True
            )
        
        with col2:
            if REPORTLAB_AVAILABLE:
                try:
                    styles_dict = st.session_state.get('item_styles', {})
                    colors_dict = st.session_state.get('item_colors', {})
                    sizes_dict = st.session_state.get('item_sizes', {})
                    
                    pdf_buffer = generate_pdf_report(
                        plates,
                        demand,
                        original_qty,
                        "V27 Engine",
                        waste_percent,
                        styles_dict,
                        colors_dict,
                        sizes_dict,
                        f"V27_{datetime.now().strftime('%Y%m%d')}"
                    )
                    
                    if pdf_buffer:
                        st.download_button(
                            "📄 Download PDF",
                            pdf_buffer,
                            f"V27_Engine_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.warning(f"PDF not available: {str(e)}")
            else:
                st.info("ℹ️ PDF requires reportlab. Install: pip install reportlab")

# ================================================================
# FOOTER
# ================================================================
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid rgba(102,126,234,0.3); background: rgba(255,255,255,0.02); border-radius: 20px;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">
        © 2025 V27 Engine | Smart Production Planning System
    </p>
    <p style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.85rem; font-weight: 600; margin: 10px 0 0 0;">
        ✨ Developed by Ovi | All Rights Reserved ✨
    </p>
</div>
""", unsafe_allow_html=True)
