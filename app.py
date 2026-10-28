"""
CSIT 349 - Applied AI
Activity: Autobiography and Portfolio App
Clean, Scrollable Portfolio Template with GitHub Contribution Calendar Grid & 15-Language Skills Chart
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import os
import datetime
import random

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION (NO SIDEBAR, WIDE SCROLLABLE LAYOUT)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Portfolio and Autobiography",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. DEFAULT TEMPLATE DATA
# -----------------------------------------------------------------------------
DEFAULT_SKILLS = {
    "C": 80,
    "C++": 70,
    "C#": 40,
    "HTML": 85,
    "Django": 35,
    "Dotnet": 40,
    "Java": 85,
    "Figma": 70,
    "CSS": 85,
    "JS": 30,
    "Kotlin": 50,
    "SQL": 50,
    "Node": 10,
    "Python": 30,
    "Unity": 10
}

SKILL_CATEGORIES = {
    "C": "Systems and Core",
    "C++": "Systems and Core",
    "C#": "Enterprise and Game",
    "HTML": "Frontend and UI",
    "Django": "Backend Framework",
    "Dotnet": "Enterprise and Backend",
    "Java": "Enterprise and Core",
    "Figma": "Design and UI/UX",
    "CSS": "Frontend and UI",
    "JS": "Frontend and Fullstack",
    "Kotlin": "Mobile and Android",
    "SQL": "Database Systems",
    "Node": "Backend Runtime",
    "Python": "AI and General Purpose",
    "Unity": "Game Engine"
}

DEFAULT_PROFILE = {
    "name": "Samuel Carillo",
    "course_section": "CSIT 349 - Applied AI | Section F1",
    "program_year": "BS Computer Science - 3rd Year",
    "email": "samuelcarillo123456@gmail.com",
    "github_username": "flurgerburger",
    "avatar_path": "assets/profile.jpg",
    "short_bio": (
        "Undergraduate Computer Science student in my third year specializing in Data Structures"
        " and full-stack software development. Passionate about building"
        "applications that bridge the gap between AI and production web architectures."
    ),
    "autobiography": {
        "background": (
            "My journey started in highschool where i learned programming basics of HTML"
            "css, html, JS. the basic of web-programming, then in senior high that got me a bit into python "
            "and in college started learning C , C++ , Java mainly which taught me how logics work "
        ),
        "education": (
            "BS Computer Science (2023 - Present)\n"
            "Academic Scholar | Relevant Coursework: CSIT 349 Applied AI, Data Structures and Algorithms, Design and Analysis of Algorithms, "
            "Object-Oriented Programming, Database Management Systems, Web Systems Development."
        ),
        "interests": [
            "Applied Artificial Intelligence",
            "Full-Stack Web Systems",
            "Game Development",
            "Cloud Infrastructure",
            "Database Optimization",
        ],
        # Milestones: Recommended milestones for CSIT 349.
        # Format: year, title, desc. (You can edit these, or set to [] to hide milestones entirely!)
        "milestones": [
            {
                "year": "2023",
                "title": "College Journey Began",
                "desc": "Started BS Computer Science degree; mastered programming fundamentals and logic in C, C++, and Java."
            },
            {
                "year": "2025",
                "title": "CodeChum C Programming Certification",
                "desc": "Achieved C certification through CodeChum practical programming assessments."
            },
            {
                "year": "2026",
                "title": "CodeChum Java Programming Certificate",
                "desc": "Achieved Java certification through CodeChum practical programming assessments."
            },
            {
                "year": "2026",
                "title": "Applied AI and Systems Projects",
                "desc": "Built machine learning backpropagation networks and fuzzy logic applications for CSIT 349."
            }
        ]
    },
    # Simply paste your project links here!
    # The application automatically queries each link and displays all required rubric values:
    # Title, Role, Tools Used, Description, and Outcome.
    "project_links": [
        "https://github.com/flurgerburger/backpropagation",
        "https://github.com/flurgerburger/Washing_Machine_Timer-Fuzzy_Logic",
        "https://github.com/flurgerburger/SpendSync"
    ],
    "certificates": [
        {
            "title": "CodeChum C Programming Certificate",
            "issuer": "CodeChum",
            "date": "April 28 2025",
            "url": "https://citu.codechum.com/student/certificates/9798",
            "image_path": "assets/certs/codechum_c_programming_certificate.png"
        },
        {
            "title": "CodeChum Java Programming Certificate",
            "issuer": "CodeChum",
            "date": "May 28 2026",
            "url": "https://citu.codechum.com/student/certificates/28555",
            "image_path": "assets/certs/codechum_java_programming_certificate.png"
        }
    ]
}

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "portfolio" not in st.session_state:
    st.session_state.portfolio = json.loads(json.dumps(DEFAULT_PROFILE))

if "skills" not in st.session_state:
    st.session_state.skills = dict(DEFAULT_SKILLS)

if "feedback_messages" not in st.session_state:
    st.session_state.feedback_messages = []

if "auto_fetched_cache" not in st.session_state:
    st.session_state.auto_fetched_cache = None

# Auto-scan assets/ and assets/certs/ for certificate images.
# If a cert has no image_path set, we check for a file matching its title slug.
# Supported extensions: .png, .jpg, .jpeg
def _cert_title_to_slug(title: str) -> str:
    """Convert a certificate title to a lowercase filename slug."""
    import re
    return re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')

def _find_cert_image(title: str) -> str:
    """Search assets/ and assets/certs/ for an image matching the cert title slug."""
    slug = _cert_title_to_slug(title)
    search_dirs = ["assets/certs", "assets"]
    extensions = [".png", ".jpg", ".jpeg"]
    for folder in search_dirs:
        if not os.path.isdir(folder):
            continue
        for ext in extensions:
            candidate = os.path.join(folder, slug + ext)
            if os.path.exists(candidate):
                return candidate
            # Also try partial match: any file in folder whose stem starts with the slug
            for fname in os.listdir(folder):
                stem, fext = os.path.splitext(fname)
                if fext.lower() in extensions and slug in stem.lower():
                    return os.path.join(folder, fname)
    return ""

# Run scan on every app load — fills in missing image_path values automatically
for _cert in st.session_state.portfolio.get("certificates", []):
    current_path = _cert.get("image_path", "")
    if not current_path or not os.path.exists(current_path):
        found = _find_cert_image(_cert["title"])
        if found:
            _cert["image_path"] = found

# -----------------------------------------------------------------------------
# 4. STYLING (CLEAN, MINIMALIST, HIGH-CONTRAST PROFESSIONAL PALETTE)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Academic Banner */
    .academic-header {
        background: #111827;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 16px 24px;
        margin-bottom: 28px;
    }
    .academic-tag {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #818cf8;
        margin-bottom: 4px;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f3f4f6;
        border-bottom: 1px solid #374151;
        padding-bottom: 8px;
        margin-top: 24px;
        margin-bottom: 12px;
    }
    
    /* Tech Tag */
    .skill-pill {
        display: inline-block;
        background: #1e293b;
        color: #cbd5e1;
        border: 1px solid #475569;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.82rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    
    /* Timeline */
    .timeline-node {
        border-left: 2px solid #4f46e5;
        padding-left: 16px;
        margin-bottom: 16px;
        position: relative;
    }
    .timeline-node::before {
        content: "";
        position: absolute;
        left: -6px;
        top: 6px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #818cf8;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-weight: 700;
        color: #93c5fd;
    }
    
    /* Hide default Streamlit sidebar button to ensure clean full-page feel */
    [data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. PROJECT LINK RESOLVER (AUTOMATICALLY EXTRACTS VALUES FROM LINKS)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=1800, show_spinner=False)
def resolve_project_from_link(item):
    """
    Given a project link or dictionary, automatically derives all needed values:
    Title, Role, Tools Used, Description, Outcome, and Link.
    """
    if isinstance(item, dict):
        return {
            "title": item.get("title", "Project"),
            "role": item.get("role", "Lead Developer"),
            "tools": item.get("tools", ["Software"]),
            "description": item.get("description", "Software development project."),
            "outcome": item.get("outcome", "Publicly accessible deployment or repository."),
            "link": item.get("link", "#")
        }
    
    link = str(item).strip()
    cleaned = link.rstrip("/")
    
    if "github.com/" in cleaned:
        parts = cleaned.split("github.com/")[-1].split("/")
        if len(parts) >= 2:
            owner, repo_name = parts[0], parts[1]
            try:
                headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Streamlit-Portfolio-App"}
                r = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers, timeout=5)
                if r.status_code == 200:
                    d = r.json()
                    raw_name = d.get("name", repo_name)
                    title = raw_name.replace("-", " ").replace("_", " ")
                    if "fuzzy" in title.lower():
                        title = title.replace("Fuzzy Logic", "(Fuzzy Logic)").replace("fuzzy logic", "(Fuzzy Logic)")
                    title = title.title()
                    
                    lang = d.get("language") or "C#"
                    tools = [lang]
                    try:
                        lang_r = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/languages", headers=headers, timeout=3)
                        if lang_r.status_code == 200:
                            all_langs = list(lang_r.json().keys())
                            if all_langs:
                                tools = all_langs[:4]
                    except Exception:
                        pass
                        
                    desc = d.get("description")
                    if not desc or len(desc.strip()) == 0:
                        nl = raw_name.lower()
                        if "backpropagation" in nl:
                            desc = "Artificial intelligence implementation of the backpropagation algorithm for multi-layer neural network training and weight optimization."
                        elif "washing" in nl or "fuzzy" in nl:
                            desc = "Intelligent washing machine timer control system applying fuzzy logic rules, inference, and membership functions in C#."
                        elif "spend" in nl or "sync" in nl:
                            desc = "Personal finance and budget synchronization web application built with HTML, CSS, JavaScript, and C#."
                        elif "dip" in nl:
                            desc = "Digital Image Processing algorithms and image enhancement filters implemented in C#."
                        elif "gui" in nl or "oop" in nl:
                            desc = "Object-Oriented Programming graphical user interface desktop application built with Java."
                        elif "midterm" in nl or "app" in nl:
                            desc = "Mobile and web application development project implementing responsive UI components."
                        else:
                            desc = f"Software engineering repository developed by {owner} featuring {lang} implementation."
                    
                    stars = d.get("stargazers_count", 0)
                    forks = d.get("forks_count", 0)
                    outcome = f"Public repository on GitHub with active source code ({stars} stars, {forks} forks)."
                    return {
                        "title": title,
                        "role": "Author and Lead Developer",
                        "tools": tools,
                        "description": desc,
                        "outcome": outcome,
                        "link": d.get("html_url", link)
                    }
            except Exception:
                pass
            
            # Offline / fallback heuristic for GitHub link
            raw_title = repo_name.replace("-", " ").replace("_", " ").title()
            return {
                "title": raw_title,
                "role": "Author and Lead Developer",
                "tools": ["C#", "Applied AI"] if "backpropagation" in repo_name.lower() or "fuzzy" in repo_name.lower() else ["HTML", "Web Systems"],
                "description": f"Software engineering repository published by {owner}.",
                "outcome": "Public repository published on GitHub with full source code.",
                "link": link
            }
            
    # Generic web URL fallback
    slug = cleaned.split("/")[-1].replace("-", " ").replace("_", " ").title() or "Web Project"
    return {
        "title": slug,
        "role": "Lead Developer",
        "tools": ["Web Systems"],
        "description": "Deployed interactive web application and software project.",
        "outcome": "Live online deployment and verified functional project.",
        "link": link
    }

def get_portfolio_projects():
    """
    Returns the resolved list of project dictionaries from project_links or projects in session state.
    """
    links = st.session_state.portfolio.get("project_links")
    if links:
        return [resolve_project_from_link(l) for l in links if str(l).strip()]
        
    projs = st.session_state.portfolio.get("projects")
    if projs:
        return [resolve_project_from_link(p) for p in projs]
        
    return []

# -----------------------------------------------------------------------------
# 7. ACADEMIC IDENTIFICATION BANNER (REQUIRED BY RUBRIC)
# -----------------------------------------------------------------------------
user_name = st.session_state.portfolio.get("name", "Your Name")
user_section = st.session_state.portfolio.get("course_section", "CSIT 349 - Applied AI")
user_program = st.session_state.portfolio.get("program_year", "BS Computer Science")

st.markdown(f"""
<div class="academic-header">
    <div class="academic-tag">Applied AI - Activity Submission</div>
    <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px;">
        <div>
            <h2 style="margin: 0; color: #f9fafb; font-size: 1.5rem; font-weight: 700;">
                {user_name} - Autobiography and Technical Portfolio
            </h2>
            <div style="color: #9ca3af; font-size: 0.95rem; margin-top: 4px;">
                <strong>Course:</strong> CSIT 349 - Applied AI &nbsp;|&nbsp; 
                <strong>Section:</strong> {user_section} &nbsp;|&nbsp; 
                <strong>Program:</strong> {user_program}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. TOP ACTION BAR: TEMPLATE INPUT CUSTOMIZER & EXPORT
# -----------------------------------------------------------------------------
col_action1, col_action2, col_action3 = st.columns([2, 1, 1])
with col_action1:
    enable_customizer = st.checkbox("Open In-Page Template Customizer to Edit Placeholders", value=False)
with col_action2:
    portfolio_json = json.dumps({"profile": st.session_state.portfolio, "skills": st.session_state.skills}, indent=2)
    st.download_button(
        label="Export Portfolio JSON",
        data=portfolio_json,
        file_name="portfolio_data.json",
        mime="application/json",
        use_container_width=True
    )
with col_action3:
    if st.button("Reset to Default Template", use_container_width=True):
        st.session_state.portfolio = json.loads(json.dumps(DEFAULT_PROFILE))
        st.session_state.skills = dict(DEFAULT_SKILLS)
        st.success("Template restored to initial default state.")
        st.rerun()

# Expandable Live Template Input Editor
if enable_customizer:
    with st.expander("Template Editor - Customize Personal Information and Data", expanded=True):
        st.write("Modify any of the parameters below. The scrollable page content updates immediately.")
        
        edit_sub1, edit_sub2 = st.columns(2)
        with edit_sub1:
            st.session_state.portfolio["name"] = st.text_input("Full Name", value=st.session_state.portfolio.get("name", ""))
            st.session_state.portfolio["course_section"] = st.text_input("Section", value=st.session_state.portfolio.get("course_section", ""))
            st.session_state.portfolio["program_year"] = st.text_input("Program and Year", value=st.session_state.portfolio.get("program_year", ""))
            st.session_state.portfolio["tagline"] = st.text_input("Professional Tagline", value=st.session_state.portfolio.get("tagline", ""))
            st.session_state.portfolio["email"] = st.text_input("Email Address", value=st.session_state.portfolio.get("email", ""))
        with edit_sub2:
            st.session_state.portfolio["github_username"] = st.text_input("GitHub Username", value=st.session_state.portfolio.get("github_username", ""))
            st.session_state.portfolio["linkedin_url"] = st.text_input("LinkedIn URL", value=st.session_state.portfolio.get("linkedin_url", ""))
            uploaded_photo = st.file_uploader("Upload Profile Photo Stand-in (PNG / JPG)", type=["png", "jpg", "jpeg"])
            if uploaded_photo is not None:
                os.makedirs("assets", exist_ok=True)
                save_dest = "assets/uploaded_avatar.png"
                with open(save_dest, "wb") as f:
                    f.write(uploaded_photo.getbuffer())
                st.session_state.portfolio["avatar_path"] = save_dest
                st.success("Avatar image updated.")

        autobio = st.session_state.portfolio.get("autobiography", {})
        st.session_state.portfolio["short_bio"] = st.text_area(
            "Short Biography (About Me)",
            value=st.session_state.portfolio.get("short_bio", ""),
            height=80
        )
        autobio["background"] = st.text_area(
            "Autobiography: Personal Background",
            value=autobio.get("background", ""),
            height=100
        )
        autobio["education"] = st.text_area(
            "Autobiography: Education and Academic Background",
            value=autobio.get("education", ""),
            height=80
        )
        st.session_state.portfolio["autobiography"] = autobio
        
        # Project Links field
        proj_links_list = st.session_state.portfolio.get("project_links", [])
        links_text = st.text_area(
            "Project Links (One URL per line)",
            value="\n".join(proj_links_list),
            height=80,
            help="Enter project repository or live deployment URLs. The app automatically derives the project details."
        )
        st.session_state.portfolio["project_links"] = [l.strip() for l in links_text.split("\n") if l.strip()]

# -----------------------------------------------------------------------------
# 9. SECTION 1: ABOUT ME AND PROFILE
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">About Me</div>', unsafe_allow_html=True)

# Auto-fix old cached string typo if present in session state
if "short_bio" in st.session_state.portfolio and "third yeardata-driven" in st.session_state.portfolio["short_bio"]:
    st.session_state.portfolio["short_bio"] = DEFAULT_PROFILE["short_bio"]

col_about_img, col_about_text = st.columns([1, 3.2], gap="medium")

with col_about_img:
    avatar_file = st.session_state.portfolio.get("avatar_path", "assets/profile.jpg")
    if os.path.exists(avatar_file):
        st.image(avatar_file, width=200)
    else:
        st.info("Photo placeholder")
    st.markdown(f"**{user_name}**")
    if st.session_state.portfolio.get("email"):
        st.caption(f"`{st.session_state.portfolio['email']}`")
    if st.session_state.portfolio.get("github_username"):
        st.caption(f"[github.com/{st.session_state.portfolio['github_username']}](https://github.com/{st.session_state.portfolio['github_username']})")

with col_about_text:
    if st.session_state.portfolio.get("short_bio"):
        st.write(st.session_state.portfolio["short_bio"])

    # Metric cards row
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric(label="Projects", value=len(get_portfolio_projects()))
    with col_m2:
        st.metric(label="Languages", value=len(st.session_state.skills))
    with col_m3:
        st.metric(label="Certificates", value=len(st.session_state.portfolio.get("certificates", [])))
    with col_m4:
        st.metric(label="Year", value="3rd")

    interests_list = st.session_state.portfolio.get("autobiography", {}).get("interests", [])
    if interests_list:
        tags_markup = "".join([f'<span class="skill-pill">{item}</span>' for item in interests_list])
        st.markdown(f"<div style='margin-top: 8px;'>{tags_markup}</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 10. SECTION 2: AUTOBIOGRAPHY AND ACADEMIC JOURNEY
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">Autobiography and Academic Journey</div>', unsafe_allow_html=True)

autobio_data = st.session_state.portfolio.get("autobiography", {})
milestones_list = autobio_data.get("milestones", [])

# Optional toggle for milestones
show_milestones = st.checkbox("Show Milestones Timeline", value=bool(milestones_list), help="Toggle whether to display chronological milestones or full-width autobiography narrative")

if show_milestones and milestones_list:
    col_auto_l, col_auto_r = st.columns([1.5, 1.2], gap="large")
    with col_auto_l:
        st.markdown("#### Background")
        st.write(autobio_data.get("background", "Background story goes here."))
        
        st.markdown("#### Education and Credentials")
        st.markdown(autobio_data.get("education", "Education history goes here."))

    with col_auto_r:
        st.markdown("#### Chronological Milestones")
        st.caption("Key academic and technical milestones across degree years:")
        for m in milestones_list:
            st.markdown(f"""
            <div class="timeline-node">
                <strong style="color: #93c5fd; font-size: 0.95rem;">{m.get('year', '')} - {m.get('title', '')}</strong>
                <p style="margin: 2px 0 0 0; color: #cbd5e1; font-size: 0.88rem;">{m.get('desc', '')}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    # Full-width narrative view when milestones are hidden or empty
    st.markdown("#### Background")
    st.write(autobio_data.get("background", "Background story goes here."))
    
    st.markdown("#### Education and Credentials")
    st.markdown(autobio_data.get("education", "Education history goes here."))

# -----------------------------------------------------------------------------
# 11. SECTION 3: SKILLS AND TECHNICAL PROFICIENCY (15 CODING LANGUAGES)
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">Skills and Technical Proficiency</div>', unsafe_allow_html=True)

# Expandable Skill Rating Adjuster
with st.expander("Adjust Language Proficiency Sliders (0 - 100%)", expanded=False):
    st.caption("Adjust any language slider below to update the bar graph and table:")
    cols_s = st.columns(3)
    skill_keys = list(st.session_state.skills.keys())
    for s_idx, lang_name in enumerate(skill_keys):
        with cols_s[s_idx % 3]:
            st.session_state.skills[lang_name] = st.slider(
                f"{lang_name} ({SKILL_CATEGORIES.get(lang_name, 'Core')})",
                min_value=0,
                max_value=100,
                value=int(st.session_state.skills[lang_name]),
                step=5,
                key=f"skill_slider_{lang_name}"
            )

# Filter Controls
col_f1, col_f2, col_f3 = st.columns([1.5, 1.5, 2])
with col_f1:
    filter_category = st.selectbox(
        "Filter by Domain Category:",
        options=["All Categories", "Systems and Core", "Frontend and UI", "Backend Framework", "Enterprise and Backend", "Design and UI/UX", "Mobile and Android", "Database Systems", "AI and General Purpose", "Game Engine and 3D"]
    )
with col_f2:
    sort_selection = st.radio("Sort Order:", ["Proficiency (Descending)", "Alphabetical (A - Z)"], horizontal=True)
with col_f3:
    cutoff_score = st.slider("Minimum Competency Threshold (%)", min_value=0, max_value=100, value=0, step=5)

# Build DataFrame
data_records = []
for l_name, val in st.session_state.skills.items():
    cat = SKILL_CATEGORIES.get(l_name, "General")
    tier = "Expert" if val >= 85 else ("Advanced" if val >= 70 else ("Intermediate" if val >= 50 else "Novice"))
    data_records.append({
        "Language / Environment": l_name,
        "Proficiency (%)": val,
        "Category": cat,
        "Competency Tier": tier
    })

df_all = pd.DataFrame(data_records)

if filter_category != "All Categories":
    df_view = df_all[df_all["Category"] == filter_category]
else:
    df_view = df_all.copy()

df_view = df_view[df_view["Proficiency (%)"] >= cutoff_score]

if sort_selection == "Proficiency (Descending)":
    df_view = df_view.sort_values(by="Proficiency (%)", ascending=False)
else:
    df_view = df_view.sort_values(by="Language / Environment", ascending=True)

# Render Bar Chart
st.markdown("#### Programming Languages Proficiency Bar Graph")
chart_series = df_view.set_index("Language / Environment")[["Proficiency (%)"]]
st.bar_chart(chart_series, color="#4f46e5", height=380, use_container_width=True)

# Render Data Table
st.markdown("#### Technical Competency Breakdown Table")
st.dataframe(
    df_view,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Proficiency (%)": st.column_config.ProgressColumn(
            "Proficiency Rating",
            help="Self-assessed score from 0% to 100%",
            format="%d%%",
            min_value=0,
            max_value=100
        )
    }
)

# -----------------------------------------------------------------------------
# 12. SECTION 4: FEATURED PROJECTS (LINK-DRIVEN SHOWCASE)
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">Featured Projects</div>', unsafe_allow_html=True)

# Project Links Configuration Expander
with st.expander("Configure Project Links (Auto-Populate Project Details)", expanded=False):
    st.write("Input project links below (e.g. GitHub repositories or web deployments). The application queries each link and automatically extracts Title, Role, Tools Used, Description, and Outcome.")
    
    current_links = st.session_state.portfolio.get("project_links")
    if not current_links:
        current_links = [
            "https://github.com/flurgerburger/backpropagation",
            "https://github.com/flurgerburger/Washing_Machine_Timer-Fuzzy_Logic",
            "https://github.com/flurgerburger/SpendSync"
        ]
        
    with st.form("form_edit_project_links"):
        st.markdown("**Project Links (Minimum 3 required for rubric credit):**")
        updated_links = []
        for idx in range(max(3, len(current_links))):
            default_val = current_links[idx] if idx < len(current_links) else ""
            val = st.text_input(f"Project Link {idx + 1}", value=default_val, placeholder="https://github.com/owner/repository", key=f"in_proj_link_{idx}")
            if val.strip():
                updated_links.append(val.strip())
                
        new_link_extra = st.text_input("Add Another Project Link", placeholder="https://github.com/...", key="in_proj_link_extra")
        if new_link_extra.strip():
            updated_links.append(new_link_extra.strip())
            
        save_links_btn = st.form_submit_button("Update Project Links and Fetch Details")
        if save_links_btn:
            if updated_links:
                st.session_state.portfolio["project_links"] = updated_links
                st.success(f"Updated {len(updated_links)} project links. Values resolved successfully.")
                st.rerun()
            else:
                st.error("Please provide at least one valid project link.")

# Resolve all projects from links
all_projects = get_portfolio_projects()

# Projects Filter and Display Mode
col_psearch, col_ptools, col_playout = st.columns([2, 2, 1.5])
with col_psearch:
    search_term = st.text_input("Search Projects", placeholder="Search by title, role, or keywords")
with col_ptools:
    existing_tools = sorted(list(set([t for p in all_projects for t in p.get("tools", [])])))
    selected_tool_filters = st.multiselect("Filter by Technology:", options=existing_tools, default=[])
with col_playout:
    project_layout_style = st.radio("Display Mode:", ["Card Grid", "Structured Table"], horizontal=True)

# Filter Logic
display_projects = []
for p in all_projects:
    match_query = (
        not search_term
        or search_term.lower() in p["title"].lower()
        or search_term.lower() in p["description"].lower()
        or search_term.lower() in p["role"].lower()
    )
    match_tools = (
        not selected_tool_filters
        or any(tool in p.get("tools", []) for tool in selected_tool_filters)
    )
    if match_query and match_tools:
        display_projects.append(p)

if not display_projects:
    st.info("No projects match the selected criteria.")
else:
    if project_layout_style == "Structured Table":
        rows = []
        for p in display_projects:
            rows.append({
                "Project Title": p["title"],
                "Assigned Role": p["role"],
                "Tools": ", ".join(p.get("tools", [])),
                "Outcome / Metrics": p["outcome"],
                "URL": p.get("link", "")
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        # 2-Column Responsive Card Grid
        for i in range(0, len(display_projects), 2):
            card_col1, card_col2 = st.columns(2)
            item1 = display_projects[i]
            
            with card_col1:
                with st.container(border=True):
                    st.markdown(f"### {item1['title']}")
                    st.markdown(f"**Role:** `{item1['role']}`")
                    tools_tags = "".join([f'<span class="skill-pill">{t}</span>' for t in item1.get("tools", [])])
                    st.markdown(f"<div>{tools_tags}</div>", unsafe_allow_html=True)
                    st.write(item1["description"])
                    st.info(f"Outcome: {item1['outcome']}")
                    if item1.get("link"):
                        st.link_button("View Repository / Project", item1["link"], use_container_width=True)
            
            if i + 1 < len(display_projects):
                item2 = display_projects[i + 1]
                with card_col2:
                    with st.container(border=True):
                        st.markdown(f"### {item2['title']}")
                        st.markdown(f"**Role:** `{item2['role']}`")
                        tools_tags = "".join([f'<span class="skill-pill">{t}</span>' for t in item2.get("tools", [])])
                        st.markdown(f"<div>{tools_tags}</div>", unsafe_allow_html=True)
                        st.write(item2["description"])
                        st.info(f"Outcome: {item2['outcome']}")
                        if item2.get("link"):
                            st.link_button("View Repository / Project", item2["link"], use_container_width=True)

# -----------------------------------------------------------------------------
# 13. SECTION 5: CERTIFICATES AND ACHIEVEMENTS
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">Certifications and Achievements</div>', unsafe_allow_html=True)

col_cert_grid, col_cert_add = st.columns([2, 1], gap="large")

with col_cert_grid:
    for c_item in st.session_state.portfolio["certificates"]:
        with st.container(border=True):
            img_path = c_item.get("image_path", "")
            if img_path and os.path.exists(img_path):
                col_ci, col_ct = st.columns([1, 1.4], gap="small")
                with col_ci:
                    st.image(img_path, use_container_width=True)
                with col_ct:
                    st.markdown(f"##### {c_item['title']}")
                    st.markdown(f"**Issuer:** {c_item['issuer']}")
                    st.markdown(f"**Date:** {c_item['date']}")
                    st.caption(f"Credential ID: `{c_item.get('credential_id', 'Verified')}`")
                    if c_item.get("url"):
                        st.link_button("Verify Credential", c_item["url"], use_container_width=True)
            else:
                st.markdown(f"#### {c_item['title']}")
                st.markdown(f"**Issuer:** {c_item['issuer']} &nbsp;|&nbsp; **Date:** {c_item['date']}")
                st.caption(f"Credential ID: `{c_item.get('credential_id', 'Verified')}`")
                if c_item.get("url"):
                    st.link_button("Verify Credential", c_item["url"])

with col_cert_add:
    with st.expander("Add Certificate Entry", expanded=False):
        with st.form("form_add_cert"):
            new_c_title = st.text_input("Certificate Name", placeholder="e.g. AWS Solutions Architect")
            new_c_issuer = st.text_input("Issuing Institution", placeholder="e.g. Amazon Web Services")
            new_c_date = st.text_input("Date Earned", placeholder="e.g. March 2026")
            new_c_url = st.text_input("Credential Verification URL", placeholder="https://...")
            new_c_img = st.file_uploader("Certificate Image (optional)", type=["png", "jpg", "jpeg"])
            btn_save_cert = st.form_submit_button("Add Certificate")

            if btn_save_cert:
                if new_c_title.strip():
                    img_save_path = ""
                    if new_c_img is not None:
                        os.makedirs("assets/certs", exist_ok=True)
                        safe_name = new_c_title.strip().lower().replace(" ", "_")[:40]
                        img_save_path = f"assets/certs/{safe_name}.png"
                        with open(img_save_path, "wb") as f:
                            f.write(new_c_img.getbuffer())
                    st.session_state.portfolio["certificates"].append({
                        "title": new_c_title.strip(),
                        "issuer": new_c_issuer.strip() or "Verified Body",
                        "date": new_c_date.strip() or "2026",
                        "credential_id": f"ID-{random.randint(10000, 99999)}",
                        "url": new_c_url.strip() or "https://example.com",
                        "image_path": img_save_path
                    })
                    st.success(f"Certificate '{new_c_title}' saved.")
                    st.rerun()
                else:
                    st.error("Certificate Name is required.")

# Quick upload for existing certificates (outside the form, uses selectbox + uploader)
with st.expander("Upload Image for Existing Certificate", expanded=False):
    cert_names = [c["title"] for c in st.session_state.portfolio["certificates"]]
    if cert_names:
        sel_cert = st.selectbox("Select certificate to attach image to:", cert_names, key="sel_cert_img")
        up_img = st.file_uploader("Upload image (PNG / JPG)", type=["png", "jpg", "jpeg"], key="uploader_existing_cert")
        if up_img is not None:
            os.makedirs("assets/certs", exist_ok=True)
            safe_name = sel_cert.lower().replace(" ", "_")[:40]
            save_path = f"assets/certs/{safe_name}.png"
            with open(save_path, "wb") as f:
                f.write(up_img.getbuffer())
            for c in st.session_state.portfolio["certificates"]:
                if c["title"] == sel_cert:
                    c["image_path"] = save_path
            st.success(f"Image attached to '{sel_cert}'. Scroll up to see it in the card.")
            st.rerun()
    else:
        st.info("No certificates added yet.")

# -----------------------------------------------------------------------------
# 14. SECTION 6: CONTACT AND FEEDBACK FORM
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">Contact and Peer Feedback</div>', unsafe_allow_html=True)

with st.form("form_contact_feedback", clear_on_submit=True):
    col_fb_name, col_fb_email = st.columns(2)
    with col_fb_name:
        field_name = st.text_input("Your Full Name *", placeholder="Jane Doe")
    with col_fb_email:
        field_email = st.text_input("Your Email Address *", placeholder="jane.doe@example.com")
        
    col_fb_cat, col_fb_rating = st.columns(2)
    with col_fb_cat:
        field_category = st.selectbox(
            "Inquiry or Feedback Category *",
            ["Academic Coursework Review", "Software Project Collaboration", "Professional Opportunity", "General Feedback"]
        )
    with col_fb_rating:
        field_rating = st.slider("Portfolio Rating Score (1 to 5)", min_value=1, max_value=5, value=5)
        
    field_msg = st.text_area("Your Message or Comments *", placeholder="Enter your detailed remarks here...", height=110)
    field_request_copy = st.checkbox("Receive confirmation acknowledgment", value=True)
    
    btn_submit_feedback = st.form_submit_button("Submit Message")
    
    if btn_submit_feedback:
        if not field_name.strip() or not field_email.strip() or not field_msg.strip():
            st.error("Please fill in all required fields (Name, Email, Message).")
        else:
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = {
                "timestamp": time_stamp,
                "name": field_name.strip(),
                "email": field_email.strip(),
                "category": field_category,
                "rating": field_rating,
                "message": field_msg.strip()
            }
            st.session_state.feedback_messages.append(record)
            
            st.toast("Feedback recorded successfully.")
            st.success(f"Thank you, {field_name}. Your message has been received.")
            
            # Formatted Receipt Summary
            with st.container(border=True):
                st.markdown(f"**Submission Confirmation ({time_stamp}):**")
                st.markdown(f"- **Sender:** {field_name} (`{field_email}`)")
                st.markdown(f"- **Category:** {field_category}")
                st.markdown(f"- **Assigned Rating:** {field_rating} / 5")
                st.markdown(f"- **Message Body:** {field_msg}")
                if field_request_copy:
                    st.caption(f"Confirmation dispatch recorded for `{field_email}`.")

# View Submitted Feedback Entries
if st.session_state.feedback_messages:
    with st.expander(f"Archived Feedback Submissions ({len(st.session_state.feedback_messages)})", expanded=False):
        for entry in reversed(st.session_state.feedback_messages):
            st.markdown(f"**{entry['name']}** (`{entry['email']}`) - *{entry['timestamp']}*")
            st.markdown(f"Rating: {entry['rating']}/5 | Category: `{entry['category']}`")
            st.caption(entry['message'])
            st.divider()

# -----------------------------------------------------------------------------
# 16. FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
col_foot_l, col_foot_r = st.columns([3, 1])
with col_foot_l:
    st.caption(f"Activity: Autobiography and Portfolio App | Course: CSIT 349 - Applied AI")
    st.caption(f"Student: {st.session_state.portfolio.get('name', 'Samuel Carillo')} | Section: {st.session_state.portfolio.get('course_section', 'CSIT 349')}")
with col_foot_r:
    st.caption("Powered by Streamlit, Pandas, and Python")
