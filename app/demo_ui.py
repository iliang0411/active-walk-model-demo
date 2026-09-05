from pathlib import Path
import base64
import time

import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Active Walk Model",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# HTML HELPER
# =========================================================

def render_html(content):
    cleaned = " ".join(
        line.strip()
        for line in content.splitlines()
    )

    st.markdown(
        cleaned,
        unsafe_allow_html=True,
    )

# ========================================================
 # walking loader!
# ========================================================
def render_walking_loader(
        placeholder,
        percent,
        stage,
        stage_number,
    ):
        """
        Custom warehouse-operator loading animation.
        """

        percent = max(
            2,
            min(
                percent,
                98,
            ),
        )

        stage_labels = [
            "Facility",
            "Transactions",
            "Match",
            "Walking",
            "Standard",
            "Impact",
        ]

        labels_html = ""

        for index, label in enumerate(
            stage_labels,
            start=1,
        ):

            active_class = (
                "active"
                if index <= stage_number
                else ""
            )

            labels_html += (
                f'<div class="{active_class}">'
                f'{label}'
                f'</div>'
            )

        html = f"""
        <div class="walk-loader">

            <div class="walk-loader-stage">
                {stage}
            </div>

            <div class="walk-track-container">

                <div class="walk-track">

                    <div
                        class="walk-fill"
                        style="width:{percent}%;">
                    </div>

                    <div
                        class="walk-operator"
                        style="left:{percent}%;">
                        <span class="operator-emoji">🚶‍♂️</span>
                    </div>

                </div>

            </div>

            <div class="walk-loader-footer">

                <div class="walk-loader-status">
                    Processing synthetic warehouse model
                </div>

                <div class="walk-loader-percent">
                    {percent}%
                </div>

            </div>

            <div class="walk-loader-steps">
                {labels_html}
            </div>

        </div>
        """

        cleaned = " ".join(
            line.strip()
            for line in html.splitlines()
        )

        placeholder.markdown(
            cleaned,
            unsafe_allow_html=True,
        )
# =========================================================
# GLOBAL STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

    .stApp {
        background: #FFFFFF;
        color: #161E2D;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #161E2D;
        letter-spacing: -0.02em;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    .hero-eyebrow {
        color: #FF9900;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .hero-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        margin-bottom: 18px;
    }

    .hero-title {
        color: #161E2D;
        font-size: 44px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -1.5px;
    }

    .hero-subtitle {
        color: #667085;
        font-size: 16px;
        margin-top: 10px;
        line-height: 1.5;
        max-width: 780px;
    }

    .demo-badge {
        flex-shrink: 0;
        background: #ECFDF3;
        border: 1px solid #ABEFC6;
        color: #067647;
        font-size: 13px;
        font-weight: 700;
        padding: 8px 13px;
        border-radius: 999px;
    }


    /* =====================================================
       WAREHOUSE HERO IMAGE
    ===================================================== */

    .warehouse-hero {
        position: relative;
        width: 100%;
        height: 340px;
        border-radius: 14px;
        overflow: hidden;
        margin-top: 10px;

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;

        box-shadow:
            0 4px 14px rgba(16,24,40,0.09),
            0 2px 6px rgba(16,24,40,0.05);
    }

    .warehouse-dark-overlay {
        position: absolute;
        inset: 0;

        background:
            linear-gradient(
                90deg,
                rgba(19,26,34,0.72) 0%,
                rgba(19,26,34,0.42) 38%,
                rgba(19,26,34,0.12) 76%,
                rgba(19,26,34,0.03) 100%
            );

        z-index: 1;
    }

    .warehouse-bottom-fade {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 150px;

        background:
            linear-gradient(
                to bottom,
                rgba(255,255,255,0) 0%,
                rgba(255,255,255,0.08) 22%,
                rgba(255,255,255,0.76) 74%,
                rgba(255,255,255,1) 100%
            );

        z-index: 2;
    }

    .warehouse-hero-content {
        position: absolute;
        left: 36px;
        top: 36px;
        z-index: 3;
        max-width: 540px;
    }

    .warehouse-kicker {
        color: #FFB84D;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .warehouse-title {
        color: #FFFFFF;
        font-size: 36px;
        line-height: 1.08;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 11px;
    }

    .warehouse-subtitle {
        color: rgba(255,255,255,0.94);
        font-size: 15px;
        line-height: 1.55;
        max-width: 500px;
    }


    /* =====================================================
       PORTFOLIO NOTICE
    ===================================================== */

    .portfolio-banner {
        margin-top: 0;
        margin-bottom: 32px;
        padding: 13px 16px;
        background: #F8FAFC;
        border: 1px solid #E4E7EC;
        border-left: 4px solid #FF9900;
        border-radius: 7px;
        color: #475467;
        font-size: 14px;
    }


    /* =====================================================
       SECTION HEADINGS
    ===================================================== */

    .section-eyebrow {
        color: #FF9900;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .section-title {
        color: #161E2D;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .section-description {
        color: #667085;
        font-size: 15px;
        line-height: 1.6;
        margin-top: 7px;
        margin-bottom: 22px;
        max-width: 880px;
    }


    /* =====================================================
       PROJECT IMPACT
    ===================================================== */

    .impact-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0,1fr));
        gap: 14px;
        margin-top: 18px;
        margin-bottom: 46px;
    }

    .impact-card {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 11px;
        padding: 21px;
        min-height: 155px;
        box-shadow: 0 1px 2px rgba(16,24,40,0.04);
        transition: 0.18s ease;
    }

    .impact-card:hover {
        border-color: #FFB65C;
        box-shadow: 0 5px 16px rgba(16,24,40,0.08);
        transform: translateY(-2px);
    }

    .impact-label {
        color: #667085;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.9px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .impact-value {
        color: #161E2D;
        font-size: 27px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .impact-value.orange {
        color: #EC7211;
    }

    .impact-text {
        color: #667085;
        font-size: 13px;
        line-height: 1.5;
    }


    /* =====================================================
       WORKFLOW
    ===================================================== */

    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(6, minmax(0,1fr));
        gap: 12px;
        margin-top: 20px;
        margin-bottom: 45px;
        position: relative;
        overflow: visible;
    }

    .workflow-card {
        position: relative;
        background: #F8FAFC;
        border: 1px solid #DDE3EA;
        border-radius: 9px;
        padding: 16px 10px;
        min-height: 98px;
        text-align: center;
        cursor: default;
        outline: none;
        z-index: 2;

        transition:
            border-color 0.15s ease,
            box-shadow 0.15s ease,
            transform 0.15s ease,
            background 0.15s ease;
    }

    .workflow-card:hover,
    .workflow-card:focus {
        background: #FFF9F3;
        border-color: #FF9900;
        box-shadow: 0 6px 18px rgba(16,24,40,0.10);
        transform: translateY(-3px);
        z-index: 100;
    }

    .workflow-number {
        color: #FF7A00;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .workflow-icon {
        color: #344054;
        font-size: 22px;
        margin-bottom: 7px;
    }

    .workflow-name {
        color: #344054;
        font-size: 13px;
        font-weight: 750;
        line-height: 1.3;
    }


    /* =====================================================
       WORKFLOW TOOLTIPS
    ===================================================== */

    .workflow-tooltip {
        position: absolute;
        top: calc(100% + 14px);
        left: 50%;

        transform:
            translateX(-50%)
            translateY(-3px);

        width: 390px;
        padding: 14px;

        background: #FFFFFF;
        border: 1px solid #D0D5DD;
        border-radius: 10px;

        box-shadow:
            0 12px 28px rgba(16,24,40,0.16),
            0 2px 5px rgba(16,24,40,0.06);

        text-align: left;

        opacity: 0;
        visibility: hidden;
        pointer-events: none;

        transition:
            opacity 0.15s ease,
            transform 0.15s ease;

        z-index: 500;
    }

    .workflow-card:hover .workflow-tooltip,
    .workflow-card:focus .workflow-tooltip {
        opacity: 1;
        visibility: visible;

        transform:
            translateX(-50%)
            translateY(0);
    }

    .workflow-tooltip.tooltip-left {
        left: 0;
        transform: translateY(-3px);
    }

    .workflow-card:hover .workflow-tooltip.tooltip-left,
    .workflow-card:focus .workflow-tooltip.tooltip-left {
        transform: translateY(0);
    }

    .workflow-tooltip.tooltip-right {
        left: auto;
        right: 0;
        transform: translateY(-3px);
    }

    .workflow-card:hover .workflow-tooltip.tooltip-right,
    .workflow-card:focus .workflow-tooltip.tooltip-right {
        transform: translateY(0);
    }

    .tooltip-title {
        color: #161E2D;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .tooltip-subtitle {
        color: #667085;
        font-size: 11px;
        margin-bottom: 9px;
    }

    .preview-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }

    .preview-table th {
        background: #F2F4F7;
        color: #475467;
        font-weight: 700;
        padding: 7px;
        border: 1px solid #EAECF0;
        text-align: left;
    }

    .preview-table td {
        color: #475467;
        padding: 7px;
        border: 1px solid #EAECF0;
        white-space: nowrap;
    }

    .tooltip-footer {
        color: #98A2B3;
        font-size: 10px;
        margin-top: 9px;
    }


    /* =====================================================
       WHY IT MATTERS
    ===================================================== */

    .why-card {
        background:
            linear-gradient(
                135deg,
                #131A22 0%,
                #232F3E 100%
            );

        color: #FFFFFF;
        border-radius: 12px;
        padding: 27px 30px;
        margin-top: 10px;
        margin-bottom: 45px;
    }

    .why-eyebrow {
        color: #FFB84D;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .why-title {
        color: #FFFFFF;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 9px;
    }

    .why-text {
        color: #D5DBDB;
        font-size: 15px;
        line-height: 1.65;
        max-width: 900px;
    }


    /* =====================================================
       BEFORE / AFTER
    ===================================================== */

    .modernization-grid {
        display: grid;
        grid-template-columns: 1fr 48px 1fr;
        gap: 14px;
        align-items: stretch;
        margin-top: 19px;
        margin-bottom: 45px;
    }

    .modernization-card {
        border: 1px solid #E4E7EC;
        border-radius: 11px;
        padding: 23px;
        background: #FFFFFF;
        box-shadow: 0 1px 2px rgba(16,24,40,0.04);
    }

    .modernization-card.before {
        border-top: 4px solid #98A2B3;
    }

    .modernization-card.after {
        border-top: 4px solid #FF9900;
    }

    .modernization-label {
        color: #667085;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .modernization-title {
        color: #161E2D;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 16px;
    }

    .modernization-row {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 9px 0;
        border-bottom: 1px solid #F2F4F7;
        color: #475467;
        font-size: 14px;
    }

    .modernization-row:last-child {
        border-bottom: none;
    }

    .modernization-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FF9900;
        font-size: 24px;
        font-weight: 800;
    }


    /* =====================================================
       WHAT I BUILT
    ===================================================== */

    .build-card {
        border: 1px solid #E4E7EC;
        border-radius: 11px;
        padding: 22px;
        background: #FFFFFF;
        margin-bottom: 44px;
    }

    .build-intro {
        color: #475467;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 16px;
    }

    .tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .tech-tag {
        background: #F2F4F7;
        border: 1px solid #E4E7EC;
        border-radius: 999px;
        padding: 7px 11px;
        color: #344054;
        font-size: 12px;
        font-weight: 650;
    }

    .tech-tag.orange {
        background: #FFF7ED;
        border-color: #FED7AA;
        color: #C2410C;
    }


    /* =====================================================
       RESULT COMPARISON
    ===================================================== */

    .comparison-container {
        display: grid;
        gap: 16px;
        margin-top: 18px;
        margin-bottom: 30px;
    }

    .comparison-card {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 12px;
        padding: 23px 24px;
        box-shadow:
            0 1px 2px rgba(16,24,40,0.04);
    }

    .comparison-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 21px;
    }

    .comparison-name {
        color: #161E2D;
        font-size: 18px;
        font-weight: 800;
    }

    .impact-pill {
        background: #FFF7ED;
        color: #C2410C;
        border: 1px solid #FED7AA;
        border-radius: 999px;
        padding: 6px 11px;
        font-size: 12px;
        font-weight: 800;
    }

    .comparison-row {
        display: grid;
        grid-template-columns: 100px 1fr 75px;
        align-items: center;
        gap: 14px;
        margin-bottom: 14px;
    }

    .comparison-row:last-child {
        margin-bottom: 0;
    }

    .comparison-label {
        color: #667085;
        font-size: 12px;
        font-weight: 700;
    }

    .comparison-value {
        color: #344054;
        font-size: 13px;
        font-weight: 750;
        text-align: right;
    }

    .comparison-track {
        width: 100%;
        height: 13px;
        background: #F2F4F7;
        border-radius: 999px;
        overflow: hidden;
    }

    .comparison-fill-current {
        height: 100%;
        background: #344054;
        border-radius: 999px;
    }

    .comparison-fill-proposed {
        height: 100%;
        background:
            linear-gradient(
                90deg,
                #FFB84D,
                #FF9900
            );
        border-radius: 999px;
    }


    /* =====================================================
       RESULT EXPLANATION
    ===================================================== */

    .result-explanation {
        padding: 18px 20px;
        margin-top: 8px;
        margin-bottom: 24px;

        background: #F8FAFC;

        border: 1px solid #E4E7EC;
        border-left: 4px solid #FF9900;
        border-radius: 8px;
    }

    .result-explanation-title {
        color: #161E2D;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .result-explanation-text {
        color: #667085;
        font-size: 13px;
        line-height: 1.55;
    }


    /* =====================================================
       RESULT HIGHLIGHT CARDS
    ===================================================== */

    .results-summary-grid {
        display: grid;
        grid-template-columns: repeat(3,minmax(0,1fr));
        gap: 14px;
        margin-top: 18px;
        margin-bottom: 28px;
    }

    .results-summary-card {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 10px;
        padding: 19px 20px;
    }

    .results-summary-label {
        color: #667085;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }

    .results-summary-value {
        color: #161E2D;
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .results-summary-note {
        color: #98A2B3;
        font-size: 11px;
        line-height: 1.4;
    }


    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {
        background: #131A22;
        border-right: 1px solid #232F3E;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.3rem;
    }

    .sidebar-brand {
        color: #FF9900;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .sidebar-title {
        color: #FFFFFF;
        font-size: 23px;
        font-weight: 750;
        margin-bottom: 4px;
    }

    .sidebar-description {
        color: #AAB7C4;
        font-size: 13px;
        line-height: 1.45;
        margin-bottom: 24px;
    }

    section[data-testid="stSidebar"] label {
        color: #E7E9EA !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #3A4553;
    }


    /* =====================================================
       SELECT BOXES
    ===================================================== */

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background: #FFFFFF;
        border: 1px solid #D5D9D9;
        border-radius: 7px;
        min-height: 44px;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] p,
    section[data-testid="stSidebar"]
    div[data-baseweb="select"] span {
        color: #161E2D !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] svg {
        fill: #161E2D !important;
    }


    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton > button {
        background: #FF9900;
        color: #111111;
        border: 1px solid #FF9900;
        border-radius: 7px;
        min-height: 44px;
        font-weight: 750;
        box-shadow: 0 1px 2px rgba(16,24,40,0.08);
        transition: 0.15s ease;
    }

    .stButton > button:hover {
        background: #EC8B00;
        color: #111111;
        border-color: #EC8B00;
        transform: translateY(-1px);
    }


    /* =====================================================
       STREAMLIT METRICS
    ===================================================== */

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 10px;
        padding: 19px 21px;
        min-height: 118px;

        box-shadow:
            0 1px 2px rgba(16,24,40,0.04),
            0 1px 3px rgba(16,24,40,0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #667085;
        font-size: 13px;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #161E2D;
        font-size: 30px;
        font-weight: 750;
    }


    /* =====================================================
       TABS
    ===================================================== */

    div[data-baseweb="tab-list"] {
        gap: 26px;
        border-bottom: 1px solid #E4E7EC;
    }

    button[data-baseweb="tab"] {
        font-weight: 650;
        color: #667085;
        padding-left: 2px;
        padding-right: 2px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #161E2D;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: #FF9900;
    }


    /* =====================================================
       DATAFRAME
    ===================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #E4E7EC;
        border-radius: 9px;
        overflow: hidden;
    }


    /* =====================================================
       PROGRESS
    ===================================================== */

    div[data-testid="stProgress"] > div > div > div {
        background-color: #FF9900;
    }

    /* =====================================================
    WALKING OPERATOR
    ===================================================== */

    .operator-emoji {
        display: inline-block;
        font-size: 30px;
        transform: scaleX(-1);
    }

    /* =====================================================
       FOOTER
    ===================================================== */

    .custom-footer {
        color: #98A2B3;
        font-size: 12px;
        text-align: center;
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #EAECF0;
    }


    /* =====================================================
       RESPONSIVE
    ===================================================== */

    @media (max-width: 950px) {

        .impact-grid {
            grid-template-columns: repeat(2,minmax(0,1fr));
        }

        .workflow-grid {
            grid-template-columns: repeat(2,minmax(0,1fr));
        }

        .modernization-grid {
            grid-template-columns: 1fr;
        }

        .modernization-arrow {
            transform: rotate(90deg);
        }

        .results-summary-grid {
            grid-template-columns: 1fr;
        }

        .comparison-row {
            grid-template-columns: 75px 1fr 65px;
        }

        .demo-badge {
            display: none;
        }

        .hero-title {
            font-size: 36px;
        }

        .warehouse-hero {
            height: 310px;
        }
    }

    /* =====================================================
    WALKING OPERATOR LOADER
    ===================================================== */

    .walk-loader {
        width: 100%;
        margin: 22px 0 28px 0;
    }

    .walk-loader-stage {
        color: #475467;
        font-size: 13px;
        font-weight: 650;
        margin-bottom: 18px;
    }

    .walk-track-container {
        position: relative;
        width: 100%;
        padding-top: 23px;
    }

    .walk-track {
        position: relative;
        width: 100%;
        height: 10px;
        background: #EAECF0;
        border-radius: 999px;
        overflow: visible;
    }

    .walk-fill {
        position: absolute;
        left: 0;
        top: 0;
        height: 10px;

        background:
            linear-gradient(
                90deg,
                #FFB84D,
                #FF9900
            );

        border-radius: 999px;

        transition: width 0.35s ease;
    }

    .walk-operator {
        position: absolute;
        top: -34px;

        font-size: 27px;
        line-height: 1;

        transform: translateX(-50%);
        transition: left 0.35s ease;

        animation: operator-step 0.45s infinite alternate ease-in-out;

        z-index: 10;
    }

    @keyframes operator-step {
        from {
            transform:
                translateX(-50%)
                translateY(0px)
                rotate(-2deg);
        }

        to {
            transform:
                translateX(-50%)
                translateY(-3px)
                rotate(2deg);
        }
    }

    .walk-loader-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;

        margin-top: 9px;
    }

    .walk-loader-status {
        color: #667085;
        font-size: 11px;
    }

    .walk-loader-percent {
        color: #161E2D;
        font-size: 12px;
        font-weight: 800;
    }

    .walk-loader-steps {
        display: grid;
        grid-template-columns: repeat(6, 1fr);

        margin-top: 13px;

        color: #98A2B3;
        font-size: 9px;
        font-weight: 650;

        text-align: center;
    }

    .walk-loader-steps .active {
        color: #EC7211;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FILE PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEMO_DATA = PROJECT_ROOT / "demo_data"
ASSETS_DIR = PROJECT_ROOT / "assets"

LOCATIONS_FILE = DEMO_DATA / "locations.csv"
TRANSACTIONS_FILE = DEMO_DATA / "transactions.csv"
STANDARDS_FILE = DEMO_DATA / "current_standards.csv"

HERO_IMAGE_FILE = (
    ASSETS_DIR / "warehouse_picking.jpg"
)


# =========================================================
# DEMO ASSUMPTIONS
# =========================================================

WALK_SPEED_FT_PER_SEC = 4.0


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_demo_data():

    locations = pd.read_csv(
        LOCATIONS_FILE
    )

    transactions = pd.read_csv(
        TRANSACTIONS_FILE
    )

    standards = pd.read_csv(
        STANDARDS_FILE
    )

    return (
        locations,
        transactions,
        standards,
    )


# =========================================================
# IMAGE LOADER
# =========================================================

@st.cache_data
def load_image_as_base64(
    image_path_string,
):

    image_path = Path(
        image_path_string
    )

    with open(
        image_path,
        "rb",
    ) as image_file:

        encoded = (
            base64
            .b64encode(
                image_file.read()
            )
            .decode("utf-8")
        )

    suffix = image_path.suffix.lower()

    if suffix == ".png":
        mime = "image/png"

    elif suffix == ".webp":
        mime = "image/webp"

    else:
        mime = "image/jpeg"

    return (
        encoded,
        mime,
    )


# =========================================================
# WALK MODEL
# =========================================================

def calculate_walk_model(
    locations,
    transactions,
):

    walk = transactions.merge(
        locations[
            [
                "location_id",
                "aisle",
                "x_coord",
                "y_coord",
            ]
        ],
        on="location_id",
        how="left",
    )

    walk = (
        walk
        .sort_values(
            [
                "transaction_id",
                "sequence",
            ]
        )
        .reset_index(drop=True)
    )

    walk["previous_x"] = (
        walk
        .groupby("transaction_id")["x_coord"]
        .shift(1)
    )

    walk["previous_y"] = (
        walk
        .groupby("transaction_id")["y_coord"]
        .shift(1)
    )

    walk["previous_x"] = (
        walk["previous_x"]
        .fillna(walk["x_coord"])
    )

    walk["previous_y"] = (
        walk["previous_y"]
        .fillna(walk["y_coord"])
    )

    walk["walk_distance_ft"] = (
        (
            walk["x_coord"]
            -
            walk["previous_x"]
        ).abs()
        +
        (
            walk["y_coord"]
            -
            walk["previous_y"]
        ).abs()
    )

    walk["walk_time_sec"] = (
        walk["walk_distance_ft"]
        /
        WALK_SPEED_FT_PER_SEC
    )

    return walk


# =========================================================
# TRANSACTION SUMMARY
# =========================================================

def summarize_transactions(
    walk,
):

    return (
        walk
        .groupby(
            [
                "transaction_id",
                "pallet_count",
            ],
            as_index=False,
        )
        .agg(
            pick_count=(
                "location_id",
                "count",
            ),
            total_distance_ft=(
                "walk_distance_ft",
                "sum",
            ),
            modeled_walk_time_sec=(
                "walk_time_sec",
                "sum",
            ),
        )
    )


# =========================================================
# STANDARD COMPARISON
# =========================================================

def build_standard_comparison(
    transaction_summary,
    standards,
):

    modeled_walk = (
        transaction_summary
        .groupby(
            "pallet_count",
            as_index=False,
        )
        .agg(
            average_walk_time_sec=(
                "modeled_walk_time_sec",
                "mean",
            )
        )
    )

    results = standards.merge(
        modeled_walk,
        on="pallet_count",
        how="left",
    )

    results[
        "average_walk_time_sec"
    ] = (
        results[
            "average_walk_time_sec"
        ]
        .fillna(0)
    )

    # Simplified public-demo model.
    results[
        "proposed_standard"
    ] = (
        results[
            "current_standard"
        ]
        +
        results[
            "average_walk_time_sec"
        ]
    )

    results[
        "impact_pct"
    ] = (
        (
            results[
                "proposed_standard"
            ]
            /
            results[
                "current_standard"
            ]
        )
        - 1
    ) * 100

    return results


# =========================================================
# OVERALL IMPACT
# =========================================================

def calculate_overall_impact(
    results,
):

    current_total = (
        results[
            "current_standard"
        ]
        .sum()
    )

    proposed_total = (
        results[
            "proposed_standard"
        ]
        .sum()
    )

    if current_total == 0:
        return 0.0

    return (
        (
            proposed_total
            /
            current_total
        )
        - 1
    ) * 100


# =========================================================
# RESULT VISUALIZATION
# =========================================================

def render_standard_comparison(
    display_results,
):

    if display_results.empty:
        return

    max_value = max(
        display_results[
            "Current Standard"
        ].max(),
        display_results[
            "Proposed Standard"
        ].max(),
    )

    cards = []

    for _, row in display_results.iterrows():

        current = float(
            row["Current Standard"]
        )

        proposed = float(
            row["Proposed Standard"]
        )

        impact = float(
            row["Impact %"]
        )

        current_width = (
            current
            /
            max_value
            *
            100
        )

        proposed_width = (
            proposed
            /
            max_value
            *
            100
        )

        cards.append(
            f"""
            <div class="comparison-card">

                <div class="comparison-header">

                    <div class="comparison-name">
                        {row["Pallet Configuration"]}
                    </div>

                    <div class="impact-pill">
                        +{impact:.2f}% impact
                    </div>

                </div>


                <div class="comparison-row">

                    <div class="comparison-label">
                        Current
                    </div>

                    <div class="comparison-track">

                        <div
                            class="comparison-fill-current"
                            style="
                                width:{current_width:.1f}%;
                            "
                        >
                        </div>

                    </div>

                    <div class="comparison-value">
                        {current:.2f}
                    </div>

                </div>


                <div class="comparison-row">

                    <div class="comparison-label">
                        Proposed
                    </div>

                    <div class="comparison-track">

                        <div
                            class="comparison-fill-proposed"
                            style="
                                width:{proposed_width:.1f}%;
                            "
                        >
                        </div>

                    </div>

                    <div class="comparison-value">
                        {proposed:.2f}
                    </div>

                </div>

            </div>
            """
        )

    render_html(
        """
        <div class="comparison-container">
        """
        +
        "".join(cards)
        +
        """
        </div>
        """
    )


# =========================================================
# SESSION STATE
# =========================================================

if "model_has_run" not in st.session_state:
    st.session_state.model_has_run = False

if "show_run_animation" not in st.session_state:
    st.session_state.show_run_animation = False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">
            Active Walk Model
        </div>

        <div class="sidebar-title">
            Run Configuration
        </div>

        <div class="sidebar-description">
            Configure the demonstration analysis environment.
        </div>
        """
    )

    dc = st.selectbox(
        "Distribution Centre",
        [
            "Demo Distribution Centre",
        ],
    )

    work_area = st.selectbox(
        "Work Area",
        [
            "Case Picking",
        ],
    )

    analysis_window = st.selectbox(
        "Analysis Window",
        [
            "Synthetic Demo Dataset",
        ],
    )

    st.divider()

    if st.button(
        "Run Walk Model",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.model_has_run = True
        st.session_state.show_run_animation = True

    if st.session_state.model_has_run:

        if st.button(
            "Reset Demo",
            use_container_width=True,
        ):

            st.session_state.model_has_run = False
            st.session_state.show_run_animation = False

            st.rerun()

    st.caption(
        "Synthetic portfolio environment"
    )


# =========================================================
# HEADER
# =========================================================

render_html(
    """
    <div class="hero-eyebrow">
        Warehouse Analytics Platform
    </div>

    <div class="hero-row">

        <div>

            <div class="hero-title">
                Active Walk Model
            </div>

            <div class="hero-subtitle">

                A warehouse analytics application that estimates
                walking time for order-picking operations using
                facility layout and ordered picking sequences.

            </div>

        </div>

        <div class="demo-badge">
            ● Demo Environment
        </div>

    </div>
    """
)


# =========================================================
# WAREHOUSE HERO IMAGE
# =========================================================

if HERO_IMAGE_FILE.exists():

    (
        hero_base64,
        hero_mime,
    ) = load_image_as_base64(
        str(HERO_IMAGE_FILE)
    )

    render_html(
        f"""
        <div
            class="warehouse-hero"
            style="
                background-image:
                url(data:{hero_mime};base64,{hero_base64});
            "
        >

            <div
                class="warehouse-dark-overlay">
            </div>

            <div
                class="warehouse-hero-content"
            >

                <div
                    class="warehouse-kicker"
                >
                    Warehouse Operations
                </div>

                <div
                    class="warehouse-title"
                >
                    From pick sequence
                    to walking standard
                </div>

                <div
                    class="warehouse-subtitle"
                >
                    Facility layout and ordered picking activity
                    are transformed into measurable travel
                    components for engineering analysis.
                </div>

            </div>

            <div
                class="warehouse-bottom-fade">
            </div>

        </div>
        """
    )

else:

    st.warning(
        "Warehouse image not found. "
        "Add `assets/warehouse_picking.jpg`."
    )


# =========================================================
# PORTFOLIO NOTICE
# =========================================================

render_html(
    """
    <div class="portfolio-banner">

        <strong>
            Portfolio environment
        </strong>

        &nbsp;·&nbsp;

        This application runs exclusively on synthetic
        demonstration data. No proprietary operational data,
        credentials, or production database connections are included.

    </div>
    """
)


# =========================================================
# LANDING PAGE
# =========================================================

if not st.session_state.model_has_run:

    # =====================================================
    # PROJECT IMPACT
    # =====================================================

    render_html(
        """
        <div class="section-eyebrow">
            Project Impact
        </div>

        <div class="section-title">
            Modernizing a legacy engineering workflow
        </div>

        <div class="section-description">

            The project re-engineered a multi-hour analytical
            workflow into a modular Python application designed
            for faster warehouse engineering analysis.

        </div>
        """
    )

    render_html(
        """
        <div class="impact-grid">

            <div class="impact-card">

                <div class="impact-label">
                    Processing Time
                </div>

                <div class="impact-value orange">
                    &gt;98% faster
                </div>

                <div class="impact-text">
                    Reduced model execution from roughly
                    five hours to a few minutes.
                </div>

            </div>


            <div class="impact-card">

                <div class="impact-label">
                    Modernization
                </div>

                <div class="impact-value">
                    Python + Web UI
                </div>

                <div class="impact-text">
                    Rebuilt a legacy desktop workflow as a
                    modular analytical application.
                </div>

            </div>


            <div class="impact-card">

                <div class="impact-label">
                    Data Pipeline
                </div>

                <div class="impact-value">
                    10+ sources
                </div>

                <div class="impact-text">
                    Integrated relational facility,
                    transaction and engineering data.
                </div>

            </div>


            <div class="impact-card">

                <div class="impact-label">
                    Cloud Direction
                </div>

                <div class="impact-value">
                    AWS target
                </div>

                <div class="impact-text">
                    Planned deployment using Docker,
                    ECR, ECS/Fargate and CloudWatch.
                </div>

            </div>

        </div>
        """
    )


    # =====================================================
    # HOW MODEL WORKS
    # =====================================================

    render_html(
        """
        <div class="section-eyebrow">
            Model Workflow
        </div>

        <div class="section-title">
            How the model works
        </div>

        <div class="section-description">

            The model reconstructs a picker's route through
            the warehouse and estimates the walking component
            of their work.

            <strong>
                Hover over any step to preview the data.
            </strong>

        </div>
        """
    )

    render_html(
        """
        <div class="workflow-grid">


            <div class="workflow-card" tabindex="0">

                <div class="workflow-number">
                    01
                </div>

                <div class="workflow-icon">
                    ▦
                </div>

                <div class="workflow-name">
                    Warehouse Layout
                </div>

                <div
                    class="
                        workflow-tooltip
                        tooltip-left
                    "
                >

                    <div class="tooltip-title">
                        Facility Layout Preview
                    </div>

                    <div class="tooltip-subtitle">
                        Synthetic warehouse location master
                    </div>

                    <table class="preview-table">

                        <tr>
                            <th>location_id</th>
                            <th>aisle</th>
                            <th>x_coord</th>
                            <th>y_coord</th>
                        </tr>

                        <tr>
                            <td>LOC001</td>
                            <td>A01</td>
                            <td>0</td>
                            <td>0</td>
                        </tr>

                        <tr>
                            <td>LOC004</td>
                            <td>A01</td>
                            <td>0</td>
                            <td>36</td>
                        </tr>

                        <tr>
                            <td>LOC008</td>
                            <td>A02</td>
                            <td>20</td>
                            <td>24</td>
                        </tr>

                    </table>

                    <div class="tooltip-footer">
                        Example synthetic facility data
                    </div>

                </div>

            </div>


            <div class="workflow-card" tabindex="0">

                <div class="workflow-number">
                    02
                </div>

                <div class="workflow-icon">
                    ≡
                </div>

                <div class="workflow-name">
                    Pick Activity
                </div>

                <div
                    class="
                        workflow-tooltip
                        tooltip-left
                    "
                >

                    <div class="tooltip-title">
                        Pick Activity Preview
                    </div>

                    <div class="tooltip-subtitle">
                        Ordered transaction sequence
                    </div>

                    <table class="preview-table">

                        <tr>
                            <th>transaction</th>
                            <th>seq</th>
                            <th>location</th>
                            <th>pallets</th>
                        </tr>

                        <tr>
                            <td>TXN001</td>
                            <td>1</td>
                            <td>LOC001</td>
                            <td>1</td>
                        </tr>

                        <tr>
                            <td>TXN001</td>
                            <td>2</td>
                            <td>LOC003</td>
                            <td>1</td>
                        </tr>

                        <tr>
                            <td>TXN001</td>
                            <td>3</td>
                            <td>LOC005</td>
                            <td>1</td>
                        </tr>

                    </table>

                    <div class="tooltip-footer">
                        Example synthetic transaction data
                    </div>

                </div>

            </div>


            <div class="workflow-card" tabindex="0">

                <div class="workflow-number">
                    03
                </div>

                <div class="workflow-icon">
                    ⌖
                </div>

                <div class="workflow-name">
                    Match Locations
                </div>

                <div class="workflow-tooltip">

                    <div class="tooltip-title">
                        Location Match Preview
                    </div>

                    <div class="tooltip-subtitle">
                        Transactions joined to facility coordinates
                    </div>

                    <table class="preview-table">

                        <tr>
                            <th>transaction</th>
                            <th>location</th>
                            <th>aisle</th>
                            <th>x</th>
                            <th>y</th>
                        </tr>

                        <tr>
                            <td>TXN001</td>
                            <td>LOC001</td>
                            <td>A01</td>
                            <td>0</td>
                            <td>0</td>
                        </tr>

                        <tr>
                            <td>TXN001</td>
                            <td>LOC003</td>
                            <td>A01</td>
                            <td>0</td>
                            <td>24</td>
                        </tr>

                        <tr>
                            <td>TXN002</td>
                            <td>LOC008</td>
                            <td>A02</td>
                            <td>20</td>
                            <td>24</td>
                        </tr>

                    </table>

                    <div class="tooltip-footer">
                        Example joined analytical dataset
                    </div>

                </div>

            </div>


            <div class="workflow-card" tabindex="0">

                <div class="workflow-number">
                    04
                </div>

                <div class="workflow-icon">
                    ↝
                </div>

                <div class="workflow-name">
                    Estimate Walking
                </div>

                <div class="workflow-tooltip">

                    <div class="tooltip-title">
                        Walking Calculation Preview
                    </div>

                    <div class="tooltip-subtitle">
                        Sequential travel between picks
                    </div>

                    <table class="preview-table">

                        <tr>
                            <th>transaction</th>
                            <th>from</th>
                            <th>to</th>
                            <th>distance</th>
                            <th>time</th>
                        </tr>

                        <tr>
                            <td>TXN001</td>
                            <td>LOC001</td>
                            <td>LOC003</td>
                            <td>24 ft</td>
                            <td>6.0 sec</td>
                        </tr>

                        <tr>
                            <td>TXN001</td>
                            <td>LOC003</td>
                            <td>LOC005</td>
                            <td>24 ft</td>
                            <td>6.0 sec</td>
                        </tr>

                    </table>

                    <div class="tooltip-footer">
                        Simplified public-demo calculation
                    </div>

                </div>

            </div>


            <div class="workflow-card" tabindex="0">

                <div class="workflow-number">
                    05
                </div>

                <div class="workflow-icon">
                    ✓
                </div>

                <div class="workflow-name">
                    Proposed Standard
                </div>

                <div
                    class="
                        workflow-tooltip
                        tooltip-right
                    "
                >

                    <div class="tooltip-title">
                        Proposed Standard Preview
                    </div>

                    <div class="tooltip-subtitle">
                        Current standard plus modeled walking component
                    </div>

                    <table class="preview-table">

                        <tr>
                            <th>pallets</th>
                            <th>current</th>
                            <th>walk</th>
                            <th>proposed</th>
                        </tr>

                        <tr>
                            <td>1</td>
                            <td>63.50</td>
                            <td>7.83</td>
                            <td>71.33</td>
                        </tr>

                        <tr>
                            <td>2</td>
                            <td>96.20</td>
                            <td>14.50</td>
                            <td>110.70</td>
                        </tr>

                    </table>

                    <div class="tooltip-footer">
                        Illustrative synthetic output
                    </div>

                </div>

            </div>


            <div class="workflow-card" tabindex="0">

                <div class="workflow-number">
                    06
                </div>

                <div class="workflow-icon">
                    %
                </div>

                <div class="workflow-name">
                    Compare Impact
                </div>

                <div
                    class="
                        workflow-tooltip
                        tooltip-right
                    "
                >

                    <div class="tooltip-title">
                        Impact Preview
                    </div>

                    <div class="tooltip-subtitle">
                        Current versus proposed comparison
                    </div>

                    <table class="preview-table">

                        <tr>
                            <th>pallets</th>
                            <th>current</th>
                            <th>proposed</th>
                            <th>impact</th>
                        </tr>

                        <tr>
                            <td>1</td>
                            <td>63.50</td>
                            <td>71.33</td>
                            <td>+12.3%</td>
                        </tr>

                        <tr>
                            <td>2</td>
                            <td>96.20</td>
                            <td>110.70</td>
                            <td>+15.1%</td>
                        </tr>

                    </table>

                    <div class="tooltip-footer">
                        Illustrative synthetic impact
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # =====================================================
    # WHY IT MATTERS
    # =====================================================

    render_html(
        """
        <div class="why-card">

            <div class="why-eyebrow">
                Why It Matters
            </div>

            <div class="why-title">
                Faster analysis supports faster engineering decisions.
            </div>

            <div class="why-text">

                Warehouse standards influence labour planning and
                operational decision-making. Reducing a multi-hour
                model run to minutes allows engineering teams to
                evaluate scenarios, investigate changes and validate
                assumptions much more quickly.

            </div>

        </div>
        """
    )


    # =====================================================
    # BEFORE / AFTER
    # =====================================================

    render_html(
        """
        <div class="section-eyebrow">
            Modernization
        </div>

        <div class="section-title">
            From legacy desktop tool to modern analytical application
        </div>

        <div class="section-description">

            The modernization separates the user interface,
            analytical logic and data-processing layers into
            a maintainable Python application.

        </div>
        """
    )

    render_html(
        """
        <div class="modernization-grid">

            <div
                class="
                    modernization-card
                    before
                "
            >

                <div class="modernization-label">
                    Before
                </div>

                <div class="modernization-title">
                    Legacy Workflow
                </div>

                <div class="modernization-row">
                    Access / VBA desktop application
                </div>

                <div class="modernization-row">
                    Tightly coupled processing logic
                </div>

                <div class="modernization-row">
                    Multi-hour model execution
                </div>

                <div class="modernization-row">
                    Local desktop environment
                </div>

            </div>


            <div class="modernization-arrow">
                →
            </div>


            <div
                class="
                    modernization-card
                    after
                "
            >

                <div class="modernization-label">
                    After
                </div>

                <div class="modernization-title">
                    Python Application
                </div>

                <div class="modernization-row">
                    Python + Streamlit web interface
                </div>

                <div class="modernization-row">
                    Modular analytical pipeline
                </div>

                <div class="modernization-row">
                    Model execution in minutes
                </div>

                <div class="modernization-row">
                    Cloud-deployable architecture
                </div>

            </div>

        </div>
        """
    )


    # =====================================================
    # WHAT I BUILT
    # =====================================================

    render_html(
        """
        <div class="section-eyebrow">
            My Contribution
        </div>

        <div class="section-title">
            What I built
        </div>

        <div class="section-description">

            The project combines data engineering,
            analytical modelling, validation and
            application development.

        </div>
        """
    )

    render_html(
        """
        <div class="build-card">

            <div class="build-intro">

                Designed and implemented the Python modernization,
                processing pipeline, model validation workflow and
                interactive application interface.

            </div>

            <div class="tag-row">

                <span class="tech-tag">
                    Python
                </span>

                <span class="tech-tag">
                    Pandas
                </span>

                <span class="tech-tag">
                    Oracle SQL
                </span>

                <span class="tech-tag">
                    Streamlit
                </span>

                <span class="tech-tag">
                    Regression
                </span>

                <span class="tech-tag">
                    Data Validation
                </span>

                <span class="tech-tag orange">
                    Docker — planned
                </span>

                <span class="tech-tag orange">
                    Amazon ECR
                </span>

                <span class="tech-tag orange">
                    ECS / Fargate
                </span>

                <span class="tech-tag orange">
                    CloudWatch
                </span>

            </div>

        </div>
        """
    )


    # =====================================================
    # DEMO CTA
    # =====================================================

    render_html(
        """
        <div class="section-eyebrow">
            Interactive Demo
        </div>

        <div class="section-title">
            Try the model
        </div>

        <div class="section-description">

            Use the configuration panel on the left and
            select <strong>Run Walk Model</strong> to process
            the synthetic warehouse dataset and explore the results.

        </div>
        """
    )


# =========================================================
# MODEL RESULTS
# =========================================================

else:

    try:

        (
            locations,
            transactions,
            standards,
        ) = load_demo_data()


        # =================================================
        # RUN ANIMATION
        # =================================================

        if st.session_state.show_run_animation:

            loader = st.empty()

            stages = [
                "Loading synthetic facility layout",
                "Reading ordered pick transactions",
                "Matching picks to warehouse locations",
                "Reconstructing operator walking",
                "Building proposed walking standards",
                "Comparing current and proposed impact",
            ]

            for i, stage in enumerate(
                stages,
                start=1,
            ):

                percent = int(
                    i
                    /
                    len(stages)
                    *
                    100
                )

                render_walking_loader(
                    placeholder=loader,
                    percent=percent,
                    stage=stage,
                    stage_number=i,
                )

                time.sleep(0.45)

            # Show operator reaching destination
            render_walking_loader(
                placeholder=loader,
                percent=98,
                stage="Walk Model complete",
                stage_number=6,
            )

            time.sleep(0.35)

            loader.empty()

            st.success(
                "Walk Model completed successfully"
            )

            st.session_state.show_run_animation = False
        # =================================================
        # CALCULATIONS
        # =================================================

        walk = calculate_walk_model(
            locations,
            transactions,
        )

        transaction_summary = (
            summarize_transactions(
                walk
            )
        )

        results = (
            build_standard_comparison(
                transaction_summary,
                standards,
            )
        )

        overall_impact = (
            calculate_overall_impact(
                results
            )
        )


        # =================================================
        # FORMAT RESULTS
        # =================================================

        display_results = (
            results.copy()
        )

        display_results[
            "Pallet Configuration"
        ] = (
            display_results[
                "pallet_count"
            ]
            .astype(str)
            +
            " Pallet"
        )

        display_results = (
            display_results[
                [
                    "Pallet Configuration",
                    "current_standard",
                    "average_walk_time_sec",
                    "proposed_standard",
                    "impact_pct",
                ]
            ]
        )

        display_results.columns = [
            "Pallet Configuration",
            "Current Standard",
            "Modeled Walk Component",
            "Proposed Standard",
            "Impact %",
        ]

        for column in [
            "Current Standard",
            "Modeled Walk Component",
            "Proposed Standard",
            "Impact %",
        ]:

            display_results[
                column
            ] = (
                display_results[
                    column
                ]
                .round(2)
            )


        transaction_display = (
            transaction_summary.copy()
        )

        transaction_display.columns = [
            "Transaction",
            "Pallet Count",
            "Pick Count",
            "Travel Distance (ft)",
            "Modeled Walk Time (sec)",
        ]

        transaction_display[
            "Travel Distance (ft)"
        ] = (
            transaction_display[
                "Travel Distance (ft)"
            ]
            .round(1)
        )

        transaction_display[
            "Modeled Walk Time (sec)"
        ] = (
            transaction_display[
                "Modeled Walk Time (sec)"
            ]
            .round(2)
        )


        # =================================================
        # RESULT METRICS
        # =================================================

        average_walk_component = (
            display_results[
                "Modeled Walk Component"
            ]
            .mean()
        )

        largest_impact = (
            display_results[
                "Impact %"
            ]
            .max()
        )


        # =================================================
        # TABS
        # =================================================

        (
            overview_tab,
            results_tab,
            transactions_tab,
            architecture_tab,
        ) = st.tabs(
            [
                "Overview",
                "Results",
                "Transactions",
                "Architecture",
            ]
        )


        # =================================================
        # OVERVIEW
        # =================================================

        with overview_tab:

            st.write("")

            render_html(
                """
                <div class="section-eyebrow">
                    Model Output
                </div>

                <div class="section-title">
                    Run Summary
                </div>

                <div class="section-description">

                    The synthetic dataset has been processed
                    through the walking-analysis workflow.

                </div>
                """
            )

            (
                metric_1,
                metric_2,
                metric_3,
                metric_4,
            ) = st.columns(4)

            metric_1.metric(
                "Transactions",
                (
                    f"{transaction_summary['transaction_id'].nunique():,}"
                ),
            )

            metric_2.metric(
                "Pick Observations",
                f"{len(transactions):,}",
            )

            metric_3.metric(
                "Facility Locations",
                f"{len(locations):,}",
            )

            metric_4.metric(
                "Estimated Impact",
                f"{overall_impact:.2f}%",
            )


            st.write("")

            render_html(
                f"""
                <div class="result-explanation">

                    <div class="result-explanation-title">
                        What does {overall_impact:.2f}% impact mean?
                    </div>

                    <div class="result-explanation-text">

                        The proposed walking standard generated by
                        this synthetic demonstration is
                        <strong>{overall_impact:.2f}% higher</strong>
                        than the current demonstration standard.

                        A positive value means the modeled walking
                        requirement is greater than the current value.

                    </div>

                </div>
                """
            )


            render_html(
                """
                <div class="section-eyebrow">
                    Comparison
                </div>

                <div class="section-title">
                    Current vs Proposed Standard
                </div>

                <div class="section-description">

                    Longer orange bars represent the walking standard
                    generated by the synthetic model compared with
                    the current demonstration value.

                </div>
                """
            )

            render_standard_comparison(
                display_results
            )


        # =================================================
        # RESULTS
        # =================================================

        with results_tab:

            st.write("")

            render_html(
                """
                <div class="section-eyebrow">
                    Engineering Analysis
                </div>

                <div class="section-title">
                    Walking Standard Results
                </div>

                <div class="section-description">

                    Results are grouped by pallet configuration.
                    The modeled walking component is used to
                    calculate a proposed standard and resulting impact.

                </div>
                """
            )


            render_html(
                f"""
                <div class="results-summary-grid">

                    <div class="results-summary-card">

                        <div class="results-summary-label">
                            Overall Impact
                        </div>

                        <div class="results-summary-value">
                            +{overall_impact:.2f}%
                        </div>

                        <div class="results-summary-note">
                            Proposed versus current synthetic standard
                        </div>

                    </div>


                    <div class="results-summary-card">

                        <div class="results-summary-label">
                            Largest Segment Impact
                        </div>

                        <div class="results-summary-value">
                            +{largest_impact:.2f}%
                        </div>

                        <div class="results-summary-note">
                            Highest pallet-configuration difference
                        </div>

                    </div>


                    <div class="results-summary-card">

                        <div class="results-summary-label">
                            Avg Walk Component
                        </div>

                        <div class="results-summary-value">
                            {average_walk_component:.2f}
                        </div>

                        <div class="results-summary-note">
                            Average modeled walking-time component
                        </div>

                    </div>

                </div>
                """
            )


            render_standard_comparison(
                display_results
            )

            st.write("")

            st.caption(
                "Detailed result table"
            )

            st.dataframe(
                display_results,
                use_container_width=True,
                hide_index=True,
            )


        # =================================================
        # TRANSACTIONS
        # =================================================

        with transactions_tab:

            st.write("")

            render_html(
                """
                <div class="section-eyebrow">
                    Underlying Activity
                </div>

                <div class="section-title">
                    Transaction Analysis
                </div>

                <div class="section-description">

                    Each synthetic transaction represents an ordered
                    warehouse pick sequence. Travel is reconstructed
                    between consecutive locations.

                </div>
                """
            )

            st.dataframe(
                transaction_display,
                use_container_width=True,
                hide_index=True,
            )

            st.write("")

            with st.expander(
                "View processed pick-level data"
            ):

                walk_display = (
                    walk[
                        [
                            "transaction_id",
                            "sequence",
                            "location_id",
                            "aisle",
                            "pallet_count",
                            "weight_kg",
                            "walk_distance_ft",
                            "walk_time_sec",
                        ]
                    ]
                    .copy()
                )

                walk_display.columns = [
                    "Transaction",
                    "Sequence",
                    "Location",
                    "Aisle",
                    "Pallet Count",
                    "Weight (kg)",
                    "Walk Distance (ft)",
                    "Walk Time (sec)",
                ]

                walk_display[
                    "Walk Distance (ft)"
                ] = (
                    walk_display[
                        "Walk Distance (ft)"
                    ]
                    .round(1)
                )

                walk_display[
                    "Walk Time (sec)"
                ] = (
                    walk_display[
                        "Walk Time (sec)"
                    ]
                    .round(2)
                )

                st.dataframe(
                    walk_display,
                    use_container_width=True,
                    hide_index=True,
                )


        # =================================================
        # ARCHITECTURE
        # =================================================

        with architecture_tab:

            st.write("")

            render_html(
                """
                <div class="section-eyebrow">
                    Technical Design
                </div>

                <div class="section-title">
                    Demo Model Architecture
                </div>

                <div class="section-description">

                    The public portfolio implementation uses
                    synthetic data and intentionally simplified
                    analytical logic.

                </div>
                """
            )

            st.code(
                """
Synthetic Facility Layout
          │
          ▼
Synthetic Pick Transactions
          │
          ▼
Location Matching
          │
          ▼
Sequential Travel Calculation
          │
          ▼
Walking Time Component
          │
          ▼
Proposed Standard
          │
          ▼
Impact Comparison
                """,
                language=None,
            )


            st.write("")

            render_html(
                """
                <div class="section-eyebrow">
                    Cloud Deployment
                </div>

                <div class="section-title">
                    Target AWS Architecture
                </div>

                <div class="section-description">

                    This is the cloud deployment architecture
                    we will implement for the public portfolio
                    application.

                </div>
                """
            )

            st.code(
                """
GitHub Repository
       │
       ▼
Docker Container
       │
       ▼
Amazon ECR
       │
       ▼
Amazon ECS / Fargate
       │
       ▼
Streamlit Application
       │
       ├──────────────► Amazon CloudWatch
       │                  Logs / Monitoring
       │
       ▼
Public HTTPS Application
                """,
                language=None,
            )

            st.markdown(
                """
                **Deployment workflow**

                `VS Code`
                → `GitHub`
                → `Docker`
                → `Amazon ECR`
                → `Amazon ECS / Fargate`
                → `CloudWatch`
                → `Public Application`
                """
            )


    # =====================================================
    # ERRORS
    # =====================================================

    except FileNotFoundError as error:

        st.error(
            "A demo data file could not be found. "
            "Make sure locations.csv, transactions.csv "
            "and current_standards.csv are inside demo_data/."
        )

        st.code(
            str(error)
        )

    except Exception as error:

        st.error(
            "The demo model encountered an error."
        )

        st.exception(
            error
        )


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="custom-footer">

        Active Walk Model
        &nbsp;·&nbsp;
        Portfolio Demonstration
        &nbsp;·&nbsp;
        Python
        &nbsp;·&nbsp;
        Streamlit
        &nbsp;·&nbsp;
        AWS deployment planned

    </div>
    """
)