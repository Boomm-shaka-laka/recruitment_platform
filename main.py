import streamlit as st

import interface

st.set_page_config(
    page_title="甬才智聘 · State-owned Intelligence Recruitment",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

/* ── Keyframe Animations ── */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
@keyframes rotateSeal {
  from { transform: translateY(-50%) rotate(0deg); }
  to   { transform: translateY(-50%) rotate(360deg); }
}
@keyframes pulseDot {
  0%, 100% { box-shadow: 0 0 0 0 rgba(240,214,135,0.6); }
  50%       { box-shadow: 0 0 0 9px rgba(240,214,135,0); }
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(22px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes gradientFlow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes floatBubble {
  0%, 100% { transform: translateY(0px) scale(1); opacity: 0.5; }
  50%       { transform: translateY(-20px) scale(1.05); opacity: 0.9; }
}
@keyframes waveBar {
  0%, 100% { transform: scaleY(0.35); }
  50%       { transform: scaleY(1); }
}

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] {
    background: #eef2f7 !important;
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 17px;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAV BAR ── */
.nav-bar {
    position: sticky; top: 0; z-index: 999;
    background: linear-gradient(100deg, #0d1b3e 0%, #1a2f6b 60%, #0d2452 100%);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 52px; height: 64px;
    box-shadow: 0 4px 28px rgba(13,27,62,0.45);
    animation: fadeIn 0.6s ease both;
}
.nav-logo {
    display: flex; align-items: center; gap: 10px;
    font-family: 'Playfair Display', serif;
    color: #f0d687; font-size: 1.2rem; letter-spacing: 0.04em;
    white-space: nowrap;
}
.nav-logo-zh {
    font-family: 'Noto Serif SC', serif;
    font-size: 1.35rem; font-weight: 700;
    background: linear-gradient(135deg, #f0d687, #e8b84d, #f5e29a);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.nav-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #f0d687; flex-shrink: 0;
    animation: pulseDot 2s infinite;
}
.nav-links { display: flex; gap: 28px; list-style: none; }
.nav-links li a {
    color: #b0bed8; text-decoration: none; font-size: 0.95rem;
    letter-spacing: 0.07em; text-transform: uppercase;
    padding: 6px 0; border-bottom: 2px solid transparent;
    transition: color 0.25s, border-color 0.25s;
}
.nav-links li a:hover { color: #f0d687; border-bottom-color: #f0d687; }

/* ── HERO ── */
.hero {
    position: relative; width: 100%; height: 460px;
    overflow: hidden;
    background: linear-gradient(130deg, #0a1628 0%, #0d2452 35%, #183a7a 65%, #0a2240 100%);
    background-size: 300% 300%;
    animation: gradientFlow 12s ease infinite;
    display: flex; align-items: center; justify-content: center;
}
.hero-particles {
    position: absolute; inset: 0; overflow: hidden; pointer-events: none;
}
.hero-particles span {
    position: absolute; border-radius: 50%;
    background: radial-gradient(circle, rgba(240,214,135,0.18), transparent 70%);
    animation: floatBubble ease-in-out infinite;
}
.hero-particles span:nth-child(1) { width:280px;height:280px; top:5%;  left:3%;  animation-duration:7s; }
.hero-particles span:nth-child(2) { width:190px;height:190px; top:50%; left:72%; animation-duration:9s; animation-delay:1.2s; }
.hero-particles span:nth-child(3) { width:130px;height:130px; top:18%; left:55%; animation-duration:6s; animation-delay:2s; }
.hero-particles span:nth-child(4) { width:100px;height:100px; top:68%; left:22%; animation-duration:8.5s; animation-delay:0.5s; }
.hero-grid {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(240,214,135,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(240,214,135,0.07) 1px, transparent 1px);
    background-size: 54px 54px;
}
.hero-content {
    position: relative; text-align: center; color: white;
    padding: 0 32px;
    animation: fadeSlideUp 0.9s ease 0.2s both;
}
.hero-badge {
    display: inline-block;
    background: rgba(240,214,135,0.13);
    border: 1px solid rgba(240,214,135,0.32);
    border-radius: 30px; padding: 5px 20px; margin-bottom: 18px;
    font-size: 0.85rem; letter-spacing: 0.2em; color: #f0d687;
    text-transform: uppercase;
}
.hero-title-zh {
    font-family: 'Noto Serif SC', serif;
    font-size: 4rem; font-weight: 700;
    background: linear-gradient(135deg, #f5e29a, #e8b84d, #f0d687, #fff3c0);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.2em; margin-bottom: 10px;
    filter: drop-shadow(0 2px 22px rgba(232,184,77,0.4));
}
.hero-title-en {
    font-family: 'Playfair Display', serif;
    font-size: 1.18rem; color: #7a9abf;
    letter-spacing: 0.22em; text-transform: uppercase; margin-bottom: 22px;
}
.hero-divider {
    display: flex; align-items: center; justify-content: center;
    gap: 10px; margin-bottom: 20px;
}
.hero-divider-line { width: 64px; height: 1px; background: linear-gradient(90deg, transparent, #f0d687); }
.hero-divider-line.right { background: linear-gradient(90deg, #f0d687, transparent); }
.hero-divider-diamond { width: 8px; height: 8px; background: #f0d687; transform: rotate(45deg); }
.hero-subtitle {
    font-size: 1.05rem; color: #6a90b8;
    letter-spacing: 0.07em; max-width: 530px; margin: 0 auto;
}
.hero-seal {
    position: absolute; right: 90px; top: 50%;
    transform: translateY(-50%);
    width: 132px; height: 132px;
    animation: fadeIn 1.2s ease 0.7s both;
}
.hero-seal-outer {
    position: absolute; inset: 0;
    border: 1.5px solid rgba(240,214,135,0.38);
    border-radius: 50%;
    animation: rotateSeal 20s linear infinite;
}
.hero-seal-outer::before {
    content: ''; position: absolute; inset: 8px;
    border: 1px dashed rgba(240,214,135,0.2); border-radius: 50%;
}
.hero-seal-inner {
    position: absolute; inset: 22px;
    border: 1px solid rgba(240,214,135,0.28);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
}
.hero-seal-text {
    font-family: 'Noto Serif SC', serif;
    color: rgba(240,214,135,0.72);
    font-size: 0.85rem; text-align: center; line-height: 1.9;
}

/* ── STATS RIBBON ── */
.stats-ribbon {
    background: linear-gradient(90deg, #14255c, #1e3a8a, #2a4aae, #1e3a8a, #14255c);
    background-size: 300% 100%;
    animation: gradientFlow 10s ease infinite;
    display: flex; justify-content: center; gap: 0;
}
.stat-item {
    flex: 1; max-width: 230px;
    padding: 20px 24px; text-align: center;
    border-right: 1px solid rgba(255,255,255,0.07);
    animation: fadeSlideUp 0.7s ease both;
}
.stat-item:last-child { border-right: none; }
.stat-item:nth-child(1) { animation-delay: 0.1s; }
.stat-item:nth-child(2) { animation-delay: 0.2s; }
.stat-item:nth-child(3) { animation-delay: 0.3s; }
.stat-item:nth-child(4) { animation-delay: 0.4s; }
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem; font-weight: 700; color: #f0d687;
    display: block; line-height: 1.2;
}
.stat-label { font-size: 0.85rem; color: #7090c0; letter-spacing: 0.06em; margin-top: 3px; }

/* ── TABS ── */
[data-testid="stTabs"] { background: transparent !important; }
[data-testid="stTabs"] > div:first-child {
    background: white !important;
    border-bottom: none !important;
    padding: 0 44px;
    box-shadow: 0 3px 20px rgba(13,27,62,0.1);
    gap: 0 !important;
    position: sticky; top: 64px; z-index: 998;
}
button[data-baseweb="tab"] {
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    color: #7080a0 !important;
    padding: 18px 28px !important;
    border-bottom: 3px solid transparent !important;
    border-radius: 0 !important;
    letter-spacing: 0.04em;
    transition: all 0.25s ease !important;
}
button[data-baseweb="tab"]:hover {
    color: #1a2f6b !important;
    background: rgba(26,47,107,0.05) !important;
}
button[aria-selected="true"][data-baseweb="tab"] {
    color: #1a2f6b !important;
    border-bottom: 3px solid #e8b84d !important;
    font-weight: 700 !important;
    background: rgba(232,184,77,0.06) !important;
}
[data-testid="stTabContent"] { padding: 0 !important; }

/* ── CONTENT AREA ── */
.content-area { max-width: 960px; margin: 46px auto; padding: 0 28px 90px; }

/* ── SECTION HEADER ── */
.section-header {
    display: flex; align-items: center; gap: 16px; margin-bottom: 34px;
}
.section-icon {
    width: 48px; height: 48px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    background: linear-gradient(135deg, #1a2f6b, #2a50b8);
    box-shadow: 0 6px 18px rgba(26,47,107,0.32);
    flex-shrink: 0;
}
.section-title {
    font-family: 'Noto Serif SC', serif;
    font-size: 1.6rem; font-weight: 700; color: #0d1b3e;
}
.section-count {
    font-size: 0.85rem; color: #94a8c8;
    background: #f0f4fc; border-radius: 20px;
    padding: 4px 14px; margin-left: auto;
    border: 1px solid #d4dff0;
}

/* ── POST CARD ── */
.post-card {
    background: white;
    border: 1px solid #dde6f5;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    transition: all 0.32s cubic-bezier(0.34, 1.48, 0.64, 1);
    position: relative; overflow: hidden;
    animation: cardIn 0.55s ease both;
    box-shadow: 0 2px 12px rgba(13,27,62,0.05);
}
.post-card:nth-child(1) { animation-delay: 0.05s; }
.post-card:nth-child(2) { animation-delay: 0.13s; }
.post-card:nth-child(3) { animation-delay: 0.21s; }
.post-card:nth-child(4) { animation-delay: 0.29s; }
.post-card:nth-child(5) { animation-delay: 0.37s; }
.post-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #1a2f6b, #4a7adb, #e8b84d, #1a2f6b);
    background-size: 300% 100%;
    border-radius: 20px 20px 0 0;
    opacity: 0; transition: opacity 0.3s ease;
    animation: shimmer 2.4s linear infinite paused;
}
.post-card:hover::before { opacity: 1; animation-play-state: running; }
.post-card:hover {
    transform: translateY(-6px) scale(1.005);
    box-shadow: 0 18px 52px rgba(13,27,62,0.13);
    border-color: #b8cce8;
}
.post-card::after {
    content: '';
    position: absolute; bottom: 0; right: 0;
    width: 64px; height: 64px;
    background: radial-gradient(circle at bottom right, rgba(232,184,77,0.1), transparent 70%);
    border-radius: 0 0 20px 0;
    transition: all 0.3s;
}
.post-card:hover::after { width: 90px; height: 90px; background: radial-gradient(circle at bottom right, rgba(232,184,77,0.22), transparent 70%); }

.post-meta { display: flex; align-items: center; gap: 11px; margin-bottom: 12px; flex-wrap: wrap; }
.post-tag {
    font-size: 0.78rem; font-weight: 600;
    letter-spacing: 0.07em; padding: 4px 13px;
    border-radius: 22px; text-transform: uppercase;
    transition: transform 0.2s ease, box-shadow 0.2s;
}
.post-tag:hover { transform: scale(1.07); box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
.tag-state   { background: linear-gradient(135deg,#dbeafe,#bfdbfe); color: #1d4ed8; border: 1px solid #bfdbfe; }
.tag-finance { background: linear-gradient(135deg,#fee2e2,#fecaca); color: #b91c1c; border: 1px solid #fecaca; }
.tag-tech    { background: linear-gradient(135deg,#dcfce7,#bbf7d0); color: #15803d; border: 1px solid #bbf7d0; }
.tag-energy  { background: linear-gradient(135deg,#ffedd5,#fed7aa); color: #c2410c; border: 1px solid #fed7aa; }
.tag-general { background: linear-gradient(135deg,#f3e8ff,#e9d5ff); color: #7e22ce; border: 1px solid #e9d5ff; }

.post-date { font-size: 0.82rem; color: #98a8c0; display: flex; align-items: center; gap: 4px; }
.post-title {
    font-family: 'Noto Serif SC', serif;
    font-size: 1.18rem; font-weight: 600; color: #0d1b3e;
    text-decoration: none; display: block;
    margin-bottom: 12px; line-height: 1.7;
    transition: color 0.22s ease;
    position: relative;
}
.post-title::after {
    content: ' ↗'; font-size: 0.88em;
    opacity: 0; transition: opacity 0.2s, transform 0.2s;
    display: inline-block; color: #4a7adb;
}
.post-title:hover { color: #2040a0; }
.post-title:hover::after { opacity: 1; transform: translate(3px, -2px); }
.post-summary {
    font-size: 0.98rem; color: #4a5a72; line-height: 1.95;
    margin-bottom: 16px; padding: 14px 18px;
    background: linear-gradient(135deg, #f6f9ff, #f0f4fc);
    border-radius: 12px;
    border-left: 4px solid #b8d0f0;
}
.post-footer { display: flex; align-items: center; justify-content: space-between; }
.post-source { font-size: 0.82rem; color: #98a8c0; display: flex; align-items: center; gap: 6px; }
.read-more {
    font-size: 0.85rem; font-weight: 600; color: #2a46a8;
    letter-spacing: 0.06em; text-decoration: none;
    display: flex; align-items: center; gap: 5px;
    padding: 7px 18px;
    border: 1.5px solid #c0d4f0;
    border-radius: 22px;
    transition: all 0.26s ease;
    background: white;
}
.read-more:hover {
    background: linear-gradient(135deg, #1a2f6b, #2a50b8);
    color: #f0d687; border-color: #1a2f6b;
    transform: translateX(3px);
    box-shadow: 0 4px 14px rgba(26,47,107,0.28);
}

/* ── EMPTY ── */
.empty-state {
    text-align: center; padding: 72px 20px;
    color: #b0c0d8; font-size: 1.05rem; letter-spacing: 0.06em;
}

/* ── PAGINATION ── */
.pagination-hint {
    text-align: center; padding: 26px;
    font-size: 0.88rem; color: #b0c0d8;
    letter-spacing: 0.09em;
    display: flex; align-items: center; justify-content: center; gap: 14px;
}
.pagination-hint::before, .pagination-hint::after {
    content: ''; flex: 1; max-width: 88px; height: 1px;
    background: linear-gradient(90deg, transparent, #c8d8ee);
}
.pagination-hint::after { background: linear-gradient(90deg, #c8d8ee, transparent); }
</style>
""", unsafe_allow_html=True)


# ─── Nav ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-logo">
    <div class="nav-dot"></div>
    <span class="nav-logo-zh">甬才智聘</span>
    <span style="color:#4a6090;font-size:0.88rem;letter-spacing:0.06em;">State-owned Intelligence Recruitment</span>
  </div>
  <ul class="nav-links">
    <li><a href="#">首页</a></li>
    <li><a href="#">职位速递</a></li>
    <li><a href="#">政策解读</a></li>
    <li><a href="#">关于我们</a></li>
  </ul>
</div>
""", unsafe_allow_html=True)


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-grid"></div>
  <div class="hero-particles">
    <span></span><span></span><span></span><span></span>
  </div>
  <div class="hero-content">
    <div class="hero-badge">✦ 宁波国企人才招聘平台 ✦</div>
    <div class="hero-title-zh">甬才智聘</div>
    <div class="hero-title-en">State-owned Intelligence Recruitment</div>
    <div class="hero-divider">
      <div class="hero-divider-line"></div>
      <div class="hero-divider-diamond"></div>
      <div class="hero-divider-line right"></div>
    </div>
    <div class="hero-subtitle">汇聚宁波优质国企岗位 · 精准匹配人才需求 · 助力职业腾飞</div>
  </div>
  <div class="hero-seal">
    <div class="hero-seal-outer"></div>
    <div class="hero-seal-inner">
      <div class="hero-seal-text">宁波<br>国企<br>人才</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Stats Ribbon ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-ribbon">
  <div class="stat-item">
    <span class="stat-num">200<span style="font-size:1.1rem">+</span></span>
    <div class="stat-label">在招岗位</div>
  </div>
  <div class="stat-item">
    <span class="stat-num">58</span>
    <div class="stat-label">合作国企</div>
  </div>
  <div class="stat-item">
    <span class="stat-num">12,400<span style="font-size:1.1rem">+</span></span>
    <div class="stat-label">注册求职者</div>
  </div>
  <div class="stat-item">
    <span class="stat-num">96<span style="font-size:1.1rem">%</span></span>
    <div class="stat-label">用户满意度</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Data ─────────────────────────────────────────────────────────────────────
SECTION_ICONS = {
    "宁波国企": "🏛️"
}

POSTS = {
    "宁波国企": [
        {
            "title": "宁波钢铁有限公司2025年春季校园招聘公告",
            "summary": "宁波钢铁有限公司面向全国高校开展2025年春季校园招聘，计划招募冶金工程、机械工程、计算机科学等专业应届本科及硕士毕业生共计120余名，提供有竞争力的薪资待遇及完善的职业发展通道。",
            "date": "2025-03-28", "tag": "tag-state", "tag_label": "制造业",
            "source": "宁波钢铁官网", "url": "https://www.nbsteel.com.cn",
        },
        {
            "title": "宁波市轨道交通集团招募运营管理岗位人才",
            "summary": "宁波轨道交通集团现面向社会公开招聘运营管理、信号维保、供电技术等多个岗位，要求具有相关专业背景及2年以上工作经验，薪资区间15,000—30,000元/月，含五险一金及住房补贴。",
            "date": "2025-03-22", "tag": "tag-state", "tag_label": "交通",
            "source": "宁波轨道交通", "url": "https://www.nbmetro.com",
        },
        {
            "title": "宁波港集团2025届毕业生招募启动，需求岗位超200个",
            "summary": "作为全球货物吞吐量前列的港口集团，宁波港集团本年度将招募物流管理、港口工程、国际贸易等专业人才，应届生起薪不低于8,000元/月，并提供丰富的出海交流机会与晋升空间。",
            "date": "2025-03-15", "tag": "tag-state", "tag_label": "港航物流",
            "source": "宁波港集团HR", "url": "https://www.nbport.com.cn",
        },
        {
            "title": "宁波市建设投资集团招聘工程技术管理人才",
            "summary": "宁波建投集团面向全国招聘土木工程、项目管理、BIM技术等专业人才，提供稳定的国有企业待遇，年薪20万元起，含多项福利补贴，适合有志于城市建设领域发展的求职者。",
            "date": "2025-03-10", "tag": "tag-state", "tag_label": "建设投资",
            "source": "宁波建投集团", "url": "https://www.nbcig.com",
        },
        {
            "title": "宁波城市发展集团城市更新项目招聘策划人才",
            "summary": "宁波城发集团结合旧城改造与城市更新重大项目，广泛招募城市规划、品牌策划、商业运营等专业人才，欢迎有城市运营相关经验人士踊跃报名，享受国企福利待遇。",
            "date": "2025-03-05", "tag": "tag-state", "tag_label": "城市发展",
            "source": "宁波城发集团", "url": "https://www.nbudc.com",
        },
    ],
    "金融国企": [
        {
            "title": "宁波银行2025年春招社会招聘正式开启",
            "summary": "宁波银行股份有限公司面向全国招募金融分析、风险管理、数字金融等岗位人才，要求金融、经济、计算机等相关专业背景，提供完善的培训体系和晋升机制，综合薪酬具有较强市场竞争力。",
            "date": "2025-03-26", "tag": "tag-finance", "tag_label": "银行",
            "source": "宁波银行官网", "url": "https://www.nbcb.com.cn",
        },
        {
            "title": "宁波市财政局下属国有资本运营公司招聘投资分析师",
            "summary": "宁波国资运营公司面向社会公开招募3名投资分析师，要求具备CFA证书或相关从业资格，熟悉PE/VC投资逻辑，年薪25—45万元，参与市级重大股权投资项目决策。",
            "date": "2025-03-18", "tag": "tag-finance", "tag_label": "投资",
            "source": "宁波国资委", "url": "http://gzw.ningbo.gov.cn",
        },
        {
            "title": "甬舟保险有限公司扩招理赔与精算专业人才",
            "summary": "甬舟保险2025年计划扩充理赔核损、精算建模、数据分析等核心岗位团队，薪资依经验面议，提供国有企业标准福利及灵活的工作时间安排，欢迎保险精算师及相关从业者投递。",
            "date": "2025-03-12", "tag": "tag-finance", "tag_label": "保险",
            "source": "甬舟保险", "url": "#",
        },
    ],
    "科技国企": [
        {
            "title": "中芯国际宁波基地2025年大规模招募芯片工程师",
            "summary": "中芯国际宁波基地持续扩产，面向全国招募芯片制造工艺、设备工程、品质管理等方向工程师逾300名，提供行业具有竞争力的薪资和驻宁波补贴，硕士起薪可达18,000元/月以上。",
            "date": "2025-03-29", "tag": "tag-tech", "tag_label": "半导体",
            "source": "中芯国际官网", "url": "https://www.smics.com",
        },
        {
            "title": "宁波市数字经济发展集团人工智能岗位专项招聘",
            "summary": "宁波数字经济集团面向AI大模型应用、数据治理、智慧城市平台开发等领域招募10名核心技术人才，提供优厚薪酬及充裕的科研资金支持，欢迎具有产学研背景的优秀人才加盟。",
            "date": "2025-03-20", "tag": "tag-tech", "tag_label": "数字经济",
            "source": "宁波数字经济集团", "url": "#",
        },
        {
            "title": "海天集团智能制造研究院招募机器人算法研究员",
            "summary": "海天集团智能制造研究院计划引进机器人运动控制、机器视觉、强化学习方向研究员5名，要求相关专业博士学历或同等研究经验，薪资待遇优厚，提供独立课题经费支持。",
            "date": "2025-03-08", "tag": "tag-tech", "tag_label": "智能制造",
            "source": "海天集团", "url": "https://www.htmould.com",
        },
    ],
    "能源国企": [
        {
            "title": "国网宁波供电公司2025年社会招聘正式启动",
            "summary": "国家电网宁波供电公司面向全社会招聘电力工程、变电运维、电力调度等专业技术人才，提供国有企业标准福利体系，稳定性强，五险一金齐全，欢迎有志于电力行业发展的人士报名。",
            "date": "2025-03-25", "tag": "tag-energy", "tag_label": "电力",
            "source": "国网宁波供电", "url": "https://nb.sgcc.com.cn",
        },
        {
            "title": "宁波市燃气集团招募管网工程与安全管理人才",
            "summary": "宁波燃气集团面向社会公开招聘管网工程设计、安全管理、客户服务等岗位，要求具备相关专业背景，注重经验积累与团队协作，提供完善的员工培训和职业发展规划。",
            "date": "2025-03-14", "tag": "tag-energy", "tag_label": "燃气",
            "source": "宁波燃气集团", "url": "#",
        },
    ],
    "政策资讯": [
        {
            "title": "宁波市出台高层次人才引进专项政策，最高补贴200万元",
            "summary": "宁波市人力资源和社会保障局近日发布《宁波市高层次人才引进专项实施细则（2025版）》，对引进的顶尖人才、领军人才分别给予100—200万元安家补贴，同时提供科研启动经费、子女教育等配套支持。",
            "date": "2025-03-27", "tag": "tag-general", "tag_label": "政策",
            "source": "宁波市人社局", "url": "http://hrss.ningbo.gov.cn",
        },
        {
            "title": "《宁波市国有企业薪酬制度改革指导意见》正式印发",
            "summary": "宁波市国资委印发最新薪酬改革文件，推动国有企业建立与市场接轨的薪酬体系，允许科技类国企参照市场标准设定核心技术人才薪资，打破传统薪酬天花板限制，提升竞争力。",
            "date": "2025-03-19", "tag": "tag-general", "tag_label": "改革",
            "source": "宁波市国资委", "url": "http://gzw.ningbo.gov.cn",
        },
        {
            "title": "宁波市2025年国企实习生计划启动，面向全国高校",
            "summary": "宁波市国资委联合多家市属国企推出2025年度国企实习生计划，面向在校本科及研究生，提供为期3个月的带薪实习机会，优秀实习生可纳入正式招聘绿色通道，报名截止日期为2025年4月30日。",
            "date": "2025-03-10", "tag": "tag-general", "tag_label": "实习",
            "source": "宁波市国资委", "url": "http://gzw.ningbo.gov.cn",
        },
    ],
}


def render_posts(tab_name: str):
    # posts = POSTS.get(tab_name, [])
    posts = interface.get_soe_data()
    for post in posts:
        post["tag"] = "tag-general"
        post["tag_label"] = "制造业"
        post["date"] = post["public_time"]
        post["url"] = post["href"]
    icon = SECTION_ICONS.get(tab_name, "📌")
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="section-header">
      <div class="section-icon">{icon}</div>
      <span class="section-title">{tab_name}</span>
      <span class="section-count">共 {len(posts)} 条资讯</span>
    </div>
    """, unsafe_allow_html=True)

    if not posts:
        st.markdown('<div class="empty-state">暂无相关资讯，敬请期待 🔍</div>', unsafe_allow_html=True)
    else:
        for p in posts:
            st.markdown(f"""
            <div class="post-card">
              <div class="post-meta">
                <span class="post-tag {p['tag']}">{p['tag_label']}</span>
                <span class="post-date">🗓&nbsp;{p['date']}</span>
              </div>
              <a class="post-title" href="{p['url']}" target="_blank">{p['title']}</a>
              <div class="post-summary">{p['summary']}</div>
              <div class="post-footer">
                <span class="post-source">📌&nbsp;{p['source']}</span>
                <a class="read-more" href="{p['url']}" target="_blank">查看详情 →</a>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f'<div class="pagination-hint">已加载全部 {len(posts)} 条内容</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Tabs ─────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏛️ 宁波国企", "💰 金融国企", "💡 科技国企", "⚡ 能源国企", "📋 政策资讯"])
tab_names = ["宁波国企", "金融国企", "科技国企", "能源国企", "政策资讯"]

for tab, name in zip(tabs, tab_names):
    with tab:
        render_posts(name)