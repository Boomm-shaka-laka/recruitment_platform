import streamlit as st
from datetime import datetime

# 设置页面配置（必须在其他 st 命令之前）
st.set_page_config(
    page_title="甬才智聘",
    page_icon="🏢",
    layout="wide"
)

# === 1. 定义页面函数 ===
def home_page(current_category='国企招聘'):
    """首页 - 职位展示页面"""
    
    # 科技感样式 + 动画效果 (CSS 样式块)
    st.markdown("""
    <style>
        /* 移除默认边距 */
        .main > div {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* 导航栏样式 */
        .nav-bar {
            position: sticky;
            top: 0;
            z-index: 999;
            background: linear-gradient(135deg, #0f0c29, #302b63);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
            height: 64px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            margin-top: 45px;
            margin-bottom: 2rem;
            border-radius: 10px;
        }
        
        /* Logo 样式 */
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            white-space: nowrap;
            flex-shrink: 0;
            text-decoration: none;
        }
        
        .nav-logo-zh {
            font-family: 'Arial Black', 'Helvetica Neue', sans-serif;
            font-size: 1.4rem;
            font-weight: bold;
            background: linear-gradient(135deg, #f0d687, #e8b84d, #f5e29a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
        }
        
        .nav-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #f0d687;
            flex-shrink: 0;
            animation: pulseDot 2s infinite;
        }
        
        /* 导航链接列表 */
        .nav-links {
            display: flex;
            gap: 4px;
            list-style: none;
            align-items: center;
            margin: 0;
            padding: 0;
        }
        
        .nav-item {
            position: relative;
        }
        
        .nav-link {
            color: #b0bed8;
            text-decoration: none !important;
            font-size: 0.92rem;
            letter-spacing: 0.06em;
            padding: 8px 16px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: color 0.22s, background 0.22s;
            white-space: nowrap;
            cursor: pointer;
        }
        
        .nav-link:hover {
            color: #f0d687;
            background: rgba(240, 214, 135, 0.08);
            text-decoration: none;
        }
        
        /* 小箭头图标 */
        .nav-link .arrow {
            font-size: 0.55rem;
            opacity: 0.55;
            transition: transform 0.22s;
            margin-left: 2px;
        }
        
        .nav-item:hover > .nav-link .arrow {
            transform: rotate(180deg);
        }
        
        /* 下拉菜单 */
        .nav-dropdown {
            position: absolute;
            top: calc(100% + 6px);
            left: 50%;
            transform: translateX(-50%) translateY(-8px);
            background: linear-gradient(160deg, #0f0c29, #302b63);
            border: 1px solid rgba(240, 214, 135, 0.15);
            border-radius: 14px;
            padding: 8px;
            min-width: 180px;
            opacity: 0;
            pointer-events: none;
            transition: all 0.22s cubic-bezier(0.34, 1.48, 0.64, 1);
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.4);
            z-index: 1000;
        }
        
        /* 桥接层：防止鼠标滑向菜单时由于间隙导致消失 */
        .nav-dropdown::before {
            content: '';
            position: absolute;
            top: -12px;
            left: 0;
            right: 0;
            height: 14px;
        }
        
        .nav-item:hover > .nav-dropdown {
            opacity: 1;
            pointer-events: all;
            transform: translateX(-50%) translateY(0);
        }
        
        /* 下拉菜单单项 */
        .drop-item {
            display: flex;
            align-items: center;
            gap: 9px;
            padding: 9px 13px;
            border-radius: 9px;
            color: #8090b0;
            font-size: 0.87rem;
            text-decoration: none !important;
            white-space: nowrap;
            transition: all 0.15s;
        }
        
        .drop-item:hover {
            background: rgba(240, 214, 135, 0.1);
            color: #f0d687;
            text-decoration: none;
        }
        
        .drop-item.cur-tab {
            color: #f0d687;
            background: rgba(240, 214, 135, 0.08);
        }
        
        .drop-divider {
            height: 1px;
            background: rgba(240, 214, 135, 0.08);
            margin: 4px 0;
        }
        
        /* 动画定义 */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulseDot {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        /* 科技感封面样式 */
        .cover-container {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: white;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                0 0 30px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* 动态渐变动画 */
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* 添加光效 */
        .cover-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            pointer-events: none;
            animation: rotate 20s linear infinite;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .main-title {
            font-size: 4.5rem;
            font-weight: 800;
            margin-bottom: 1.5rem;
            text-shadow: 
                0 0 10px rgba(102, 126, 234, 0.8),
                0 0 20px rgba(102, 126, 234, 0.6),
                0 0 30px rgba(102, 126, 234, 0.4);
            letter-spacing: 2px;
            font-family: 'Arial Black', 'Helvetica Neue', sans-serif;
            position: relative;
            z-index: 2;
            animation: fadeInUp 1s ease-out;
        }
        
        .subtitle {
            font-size: 1.3rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto 2rem;
            line-height: 1.6;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
            position: relative;
            z-index: 2;
            font-weight: 300;
            animation: fadeInUp 1s ease-out 0.3s both;
        }
        
        /* 添加装饰线条 */
        .subtitle::before,
        .subtitle::after {
            content: '✦';
            display: inline-block;
            margin: 0 15px;
            opacity: 0.7;
            animation: pulse 2s infinite alternate;
        }
        
        @keyframes pulse {
            from { opacity: 0.5; transform: scale(0.9); }
            to { transform: scale(1.1); }
        }
        
        /* 卡片样式 */
        .job-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.1),
                inset 0 0 0 1px rgba(255, 255, 255, 0.2);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            opacity: 0;
            transform: translateY(50px);
            animation: slideInUp 0.8s forwards;
        }
        
        /* 为每个卡片设置不同的延迟时间 */
        .job-card:nth-child(1) { animation-delay: 0.1s; }
        .job-card:nth-child(2) { animation-delay: 0.2s; }
        .job-card:nth-child(3) { animation-delay: 0.3s; }
        .job-card:nth-child(4) { animation-delay: 0.4s; }
        .job-card:nth-child(5) { animation-delay: 0.5s; }
        .job-card:nth-child(6) { animation-delay: 0.6s; }
        .job-card:nth-child(7) { animation-delay: 0.7s; }
        .job-card:nth-child(8) { animation-delay: 0.8s; }
        .job-card:nth-child(9) { animation-delay: 0.9s; }
        .job-card:nth-child(10) { animation-delay: 1.0s; }
        
        .job-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 8px 30px rgba(0, 0, 0, 0.15),
                inset 0 0 0 1px rgba(102, 126, 234, 0.3);
        }
        
        .job-card:hover::before {
            opacity: 1;
        }
        
        .job-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            position: relative;
        }
        
        .job-overview {
            color: #5a6c7d;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        .job-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            display: inline-block;
            margin-top: 0.5rem;
            position: relative;
        }
        
        .job-link::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 1px;
            background: #667eea;
            transition: width 0.3s ease;
        }
        
        .job-link:hover::after {
            width: 100%;
        }
        
        .job-link:hover {
            color: #764ba2;
            text-decoration: none;
        }
        
        /* 滚动容器 */
        .scroll-container {
            max-height: 600px;
            overflow-y: auto;
            padding-right: 1rem;
            border-radius: 12px;
        }
        
        /* 滚动条样式 */
        .scroll-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .scroll-container::-webkit-scrollbar-track {
            background: rgba(241, 241, 241, 0.5);
            border-radius: 4px;
        }
        
        .scroll-container::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 4px;
        }
        
        .scroll-container::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #764ba2, #667eea);
        }
        
        /* 全宽容器 */
        .full-width-container {
            width: 100%;
            max-width: 100%;
            padding: 0 1rem;
        }
        
        /* 减少边距 */
        .block-container {
            padding-top: 1rem;
            max-width: 100% !important;
        }
        
        /* 动画定义 */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* 滚动触发动画的类 */
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-on-scroll.visible {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- 这里我们创建一个静态的、视觉上的导航栏，但它本身不处理跳转 ---
    # 它只是作为页面顶部的一个美观组件。
    # 实际的导航由 Streamlit 的 st.navigation() 控制。
    drops_html = """
        <a class="drop-item cur-tab" href="#">🏛️&nbsp; 国企招聘</a>
        <div class="drop-divider"></div>
        <a class="drop-item" href="#">🏛️&nbsp; 事业单位招聘</a>
    """
    st.markdown(f"""
    <div class="nav-bar">
      <div class="nav-logo">
        <div class="nav-dot"></div>
        <span class="nav-logo-zh">甬才智聘</span>
      </div>
      <ul class="nav-links">
        <li class="nav-item">
          <a class="nav-link" href="#">
            在招岗位 <span class="arrow">▼</span>
          </a>
          <div class="nav-dropdown">
            {drops_html}
          </div>
        </li>
        <li><a class="nav-link" href="#">关于我们</a></li>
        <li><a class="nav-link" href="#">刷新岗位</a></li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # --- 页面主体内容 ---
    # 封面
    st.markdown(f"""
    <div class="cover-container">
        <div class="main-title">甬才智聘</div>
        <div class="subtitle">汇聚宁波优质{current_category if current_category != '全部' else '国企'}岗位 · 精准匹配人才需求 · 助力职业腾飞</div>
    </div>
    """, unsafe_allow_html=True)

    # 示例职位数据
    all_jobs = {
        "国企招聘": [
            {
                "title": "高级软件工程师 - 国企数字化转型项目",
                "overview": "负责大型国有企业数字化转型项目的系统架构设计与开发，参与核心业务系统的重构与优化，要求5年以上Java开发经验，熟悉Spring Cloud微服务架构。",
                "link": "https://example.com/job1"
            },
            {
                "title": "财务主管 - 国有投资集团",
                "overview": "负责国有投资集团旗下子公司的财务管理与风险控制工作，制定财务管理制度，监督资金运作，要求CPA资格，8年以上财务管理经验。",
                "link": "https://example.com/job2"
            },
            {
                "title": "项目经理 - 基础设施建设",
                "overview": "负责宁波市重点基础设施建设项目的统筹管理，协调各方资源，确保项目按期保质完成，要求PMP认证，10年以上项目管理经验。",
                "link": "https://example.com/job3"
            },
            {
                "title": "人力资源专员 - 市属国企",
                "overview": "负责市属国有企业人才招聘、培训发展及绩效管理工作，协助建立完善的人力资源管理体系，要求人力资源相关专业，3年以上工作经验。",
                "link": "https://example.com/job4"
            },
            {
                "title": "电气工程师 - 国有能源公司",
                "overview": "负责电力设备运行维护及技术改造工作，保障电网安全稳定运行，要求电气工程专业，具备注册电气工程师资格者优先。",
                "link": "https://example.com/job5"
            },
            {
                "title": "数据分析师 - 国有银行分行",
                "overview": "运用大数据技术分析客户行为及市场趋势，为业务决策提供数据支持，要求统计学或相关专业，熟练掌握Python/R等分析工具。",
                "link": "https://example.com/job6"
            },
            {
                "title": "供应链管理专员 - 国有贸易集团",
                "overview": "负责供应链体系优化及供应商管理工作，降低采购成本，提高运营效率，要求物流管理或相关专业，3年以上供应链管理经验。",
                "link": "https://example.com/job7"
            },
            {
                "title": "法律顾问 - 国有资本运营公司",
                "overview": "为国有资本运营提供法律咨询服务，审核各类合同协议，处理法律纠纷，要求法学专业，通过国家司法考试，5年以上法务工作经验。",
                "link": "https://example.com/job8"
            }
        ],
        "事业单位招聘": [
            {
                "title": "教育研究员 - 市教育研究院",
                "overview": "从事教育教学改革研究工作，制定教育政策建议，要求教育学硕士及以上学历，5年以上相关工作经验。",
                "link": "https://example.com/job9"
            },
            {
                "title": "医疗专家 - 市中心医院",
                "overview": "担任临床科室主任，负责医疗团队管理和疑难病例诊治，要求医学博士学位，副主任医师以上职称。",
                "link": "https://example.com/job10"
            },
            {
                "title": "科研工程师 - 市科学院",
                "overview": "开展前沿科学研究项目，发表高质量学术论文，要求相关专业博士学位，有海外留学经历优先。",
                "link": "https://example.com/job11"
            },
            {
                "title": "文化策划师 - 市博物馆",
                "overview": "策划组织各类展览活动，负责文化项目运营管理，要求文博、历史等相关专业，有策展经验者优先。",
                "link": "https://example.com/job12"
            },
            {
                "title": "审计师 - 市审计局下属单位",
                "overview": "执行政府投资项目审计工作，撰写审计报告，要求会计、审计专业，具备注册会计师资格。",
                "link": "https://example.com/job13"
            },
            {
                "title": "规划师 - 市规划院",
                "overview": "参与城市规划编制工作，提供专业技术支持，要求城乡规划专业，具备注册规划师资格。",
                "link": "https://example.com/job14"
            },
            {
                "title": "图书馆员 - 市图书馆",
                "overview": "负责图书资料管理和服务工作，开展读者服务活动，要求图书情报专业，有图书馆工作经验者优先。",
                "link": "https://example.com/job15"
            },
            {
                "title": "环境监测员 - 市环保局监测站",
                "overview": "开展环境质量监测工作，编制监测报告，要求环境科学相关专业，熟悉环境监测标准规范。",
                "link": "https://example.com/job16"
            }
        ]
    }

    # 根据分类筛选职位
    if current_category == '全部':
        jobs_data = all_jobs["国企招聘"] + all_jobs["事业单位招聘"]
    else:
        jobs_data = all_jobs.get(current_category, [])

    # 职位展示区域
    st.subheader(f"{current_category if current_category != '全部' else '全部'}招聘信息")

    # 直接使用全宽度容器
    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

    # 显示职位卡片
    for i, job in enumerate(jobs_data):
        st.markdown(f"""
        <div class="job-card animate-on-scroll" data-index="{i}">
            <div class="job-title">{job['title']}</div>
            <div class="job-overview">{job['overview']}</div>
            <a href="{job['link']}" target="_blank" class="job-link">查看详情 →</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def about_page():
    """关于我们页面"""
    # 我们在这里也渲染一个静态的导航栏，以保持视觉一致性
    st.markdown("""
    <style>
        .nav-bar {
            position: sticky;
            top: 0;
            z-index: 999;
            background: linear-gradient(135deg, #0f0c29, #302b63);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
            height: 64px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            margin-top: 45px;
            margin-bottom: 2rem;
            border-radius: 10px;
        }
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            white-space: nowrap;
            flex-shrink: 0;
            text-decoration: none;
        }
        .nav-logo-zh {
            font-family: 'Arial Black', 'Helvetica Neue', sans-serif;
            font-size: 1.4rem;
            font-weight: bold;
            background: linear-gradient(135deg, #f0d687, #e8b84d, #f5e29a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
        }
        .nav-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #f0d687;
            flex-shrink: 0;
            animation: pulseDot 2s infinite;
        }
        .nav-links {
            display: flex;
            gap: 4px;
            list-style: none;
            align-items: center;
            margin: 0;
            padding: 0;
        }
        .nav-item {
            position: relative;
        }
        .nav-link {
            color: #b0bed8;
            text-decoration: none !important;
            font-size: 0.92rem;
            letter-spacing: 0.06em;
            padding: 8px 16px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: color 0.22s, background 0.22s;
            white-space: nowrap;
            cursor: pointer;
        }
        .nav-link:hover {
            color: #f0d687;
            background: rgba(240, 214, 135, 0.08);
            text-decoration: none;
        }
        .nav-link .arrow {
            font-size: 0.55rem;
            opacity: 0.55;
            transition: transform 0.22s;
            margin-left: 2px;
        }
        .nav-item:hover > .nav-link .arrow {
            transform: rotate(180deg);
        }
        .nav-dropdown {
            position: absolute;
            top: calc(100% + 6px);
            left: 50%;
            transform: translateX(-50%) translateY(-8px);
            background: linear-gradient(160deg, #0f0c29, #302b63);
            border: 1px solid rgba(240, 214, 135, 0.15);
            border-radius: 14px;
            padding: 8px;
            min-width: 180px;
            opacity: 0;
            pointer-events: none;
            transition: all 0.22s cubic-bezier(0.34, 1.48, 0.64, 1);
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.4);
            z-index: 1000;
        }
        .nav-dropdown::before {
            content: '';
            position: absolute;
            top: -12px;
            left: 0;
            right: 0;
            height: 14px;
        }
        .nav-item:hover > .nav-dropdown {
            opacity: 1;
            pointer-events: all;
            transform: translateX(-50%) translateY(0);
        }
        .drop-item {
            display: flex;
            align-items: center;
            gap: 9px;
            padding: 9px 13px;
            border-radius: 9px;
            color: #8090b0;
            font-size: 0.87rem;
            text-decoration: none !important;
            white-space: nowrap;
            transition: all 0.15s;
        }
        .drop-item:hover {
            background: rgba(240, 214, 135, 0.1);
            color: #f0d687;
            text-decoration: none;
        }
        .drop-item.cur-tab {
            color: #f0d687;
            background: rgba(240, 214, 135, 0.08);
        }
        .drop-divider {
            height: 1px;
            background: rgba(240, 214, 135, 0.08);
            margin: 4px 0;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulseDot {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)

    drops_html = """
        <a class="drop-item" href="#">🏛️&nbsp; 国企招聘</a>
        <div class="drop-divider"></div>
        <a class="drop-item" href="#">🏛️&nbsp; 事业单位招聘</a>
    """
    st.markdown(f"""
    <div class="nav-bar">
      <div class="nav-logo">
        <div class="nav-dot"></div>
        <span class="nav-logo-zh">甬才智聘</span>
      </div>
      <ul class="nav-links">
        <li class="nav-item">
          <a class="nav-link" href="#">
            在招岗位 <span class="arrow">▼</span>
          </a>
          <div class="nav-dropdown">
            {drops_html}
          </div>
        </li>
        <li><a class="nav-link" href="#">关于我们</a></li>
        <li><a class="nav-link" href="#">刷新岗位</a></li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # 关于页面内容
    st.markdown("<h1 style='text-align: center; color: #302b63;'>关于我们</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2>甬才智聘简介</h2>
        <p>甬才智聘是专注于宁波地区优质国企和事业单位招聘信息的专业平台。</p>
        <p>我们致力于为求职者提供精准的岗位匹配服务，助力每一位人才实现职业梦想。</p>
        <h3>我们的优势</h3>
        <ul>
            <li>汇聚宁波最优质的国企和事业单位招聘信息</li>
            <li>智能匹配系统，精准推荐适合的岗位</li>
            <li>专业的职业规划指导服务</li>
            <li>便捷的在线申请流程</li>
        </ul>
        <h3>联系方式</h3>
        <p>电话：0574-12345678</p>
        <p>邮箱：info@yongcaizhipin.com</p>
        <p>地址：宁波市鄞州区</p>
    </div>
    """, unsafe_allow_html=True)


# === 2. 创建一个侧边栏，用于实现带跳转功能的下拉菜单 ===
# 这个侧边栏是隐藏的，只用来存放下拉选择框
with st.sidebar:
    st.subheader("切换岗位类型")
    # 当用户在侧边栏选择时，会触发页面重载
    new_category = st.selectbox("", options=["国企招聘", "事业单位招聘"], label_visibility="collapsed")
    
    # 如果侧边栏的选择改变了，就跳转回主页并传递参数
    if new_category != st.session_state.get('current_category_for_home', '国企招聘'):
        st.session_state.current_category_for_home = new_category
        # 重定向到 home 页面
        st.switch_page(st.Page(home_page))

# === 3. 定义导航（必须在页面内容之前，且是第一个 st 命令）===
# 获取当前存储的分类，如果没有则默认为 '国企招聘'
current_cat = st.session_state.get('current_category_for_home', '国企招聘')

pages = [
    st.Page(lambda: home_page(current_category=current_cat), title="在招岗位", icon="💼"),
    st.Page(about_page, title="关于我们", icon="ℹ️"),
]

# 显式指定为顶部导航
st.navigation(pages, position="top")

# === 4. 页脚（在所有页面底部显示）===
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**甬才智聘**")
    st.markdown("宁波市人才服务一站式平台")

with footer_col2:
    st.markdown("**服务范围**")
    st.markdown("• 国企招聘信息")
    st.markdown("• 事业单位招聘")
    st.markdown("• 人才精准匹配")

with footer_col3:
    st.markdown("**联系我们**")
    st.markdown("• 地址：宁波市鄞州区")
    st.markdown("• 电话：0574-12345678")
    st.markdown("• 邮箱：info@yongcaizhipin.com")

st.markdown(f"<div style='text-align: center; padding: 2rem;'>© {datetime.now().year} 甬才智聘 - 汇聚宁波优质{st.session_state.get('current_category_for_home', '国企')}岗位</div>", unsafe_allow_html=True)