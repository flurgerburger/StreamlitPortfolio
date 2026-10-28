# CSIT 349 - Applied AI: Autobiography and Portfolio App

A clean, minimalist, and scrollable personal portfolio and autobiography web application built with **Streamlit**, **Pandas**, and **Python**.

---

## Highlights and Features

- **Academic Header Banner**: Prominently features your **Name**, **Course (CSIT 349 - Applied AI)**, and **Section** in the top identification header (satisfying the grading rubric requirement).
- **Single Scrollable Layout**: Clean, seamless page flow from top to bottom (no sidebar or tab fragmentation):
  1. Academic Identification and Quick Actions (Export JSON, Reset, Template Customizer)
  2. About Me (Profile photo stand-in, biography, key statistics, focus disciplines, social links)
  3. Autobiography and Academic Journey (Background narrative, education, optional chronological milestone nodes)
  4. Skills and Technical Proficiency (15 coding languages sliders, interactive bar graph, data table, category filter)
  5. Featured Projects (Auto-populated from inputted links, minimum 3 required for rubric credit)
  6. Certifications and Achievements (Credentials list, verification links, and entry form)
  7. Contact and Peer Feedback (Form with immediate response, receipt summary, and archived submissions)
- **Link-Driven Featured Projects**:
  - Instead of hand-writing big dictionaries, simply input your repository or deployment links (e.g., GitHub repos or web URLs).
  - The application automatically extracts and displays:
    - **Title**: Clean formatted name (e.g., `Backpropagation Neural Network`, `Washing Machine Timer (Fuzzy Logic)`, `SpendSync`)
    - **Role**: Automatically sets role (e.g., `Author and Lead Developer`)
    - **Tools Used**: Detected languages/frameworks from the repository (e.g., `C#`, `HTML`, `CSS`, `JavaScript`)
    - **Description**: Accurate, intelligent project summary
    - **Outcome**: Repository verification and stars/forks count
    - **Link**: Direct button to repository or demo
- **Academic Milestones Guidance & Toggle**:
  - The CSIT 349 activity sheet asks for *"background, education, interests, and a few milestones, in your own words"*.
  - Recommended format (one key milestone per academic year):
    - **Year 1 (2023 - 2024)**: Computer Science Foundations (C, C++, Java fundamentals)
    - **Year 2 (2024 - 2025)**: Software Architecture & CodeChum Java Certification
    - **Year 3 (2025 - 2026)**: Applied AI Projects (Backpropagation, Fuzzy Logic in CSIT 349)
- **15 Specific Coding Languages Bar Graph**:
  - Interactive sliders and bar chart for:
    `C`, `C++`, `C#`, `HTML`, `Django`, `.NET`, `Java`, `Figma`, `CSS`, `JS`, `Kotlin`, `SQL`, `Node`, `Python`, `Unity`.
  - Filterable by Domain Category and Minimum Competency Threshold.

---

## Rubric and Lecture Component Checklist

| Required Component | Implementation in App |
| :--- | :--- |
| **Title / Header / Subheader / Markdown** | Section headers, markdown content, bio narratives |
| **Table** | `st.dataframe` for Skills Breakdown and Project Table View |
| **Chart** | `st.bar_chart` for the 15 coding languages |
| **Button** | Update Project Links, Reset to Defaults, and Feedback Submission buttons |
| **Slider** | Skills competency sliders (0-100%) and Feedback rating score (1-5) |
| **Selectbox** | Skills domain category filter and Feedback inquiry category |
| **Checkbox** | Show milestones toggle, in-page template customizer toggle, and feedback copy checkbox |
| **Text Input** | Name, Section, URLs, Project links, Search bar |
| **Text Area** | Autobiography narrative, Bio, and Feedback message |
| **Radio Button** | Skills sort order and Project display mode (Card Grid vs Table) |
| **Multiselect** | Interest disciplines and project technologies filter |
| **Columns** | Multi-column grid layouts across all sections |
| **Extras** | `st.image`, `st.metric`, `st.form`, `st.session_state`, `st.download_button`, `st.expander`, `st.toast` |

---

## How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
streamlit run app.py
```
*(Or double-click `run.bat` on Windows!)*

Open your browser to: **`http://localhost:8501`**

---

## How to Configure Your Information and Projects

### Configuring Projects via Links:
In `app.py`, under `DEFAULT_PROFILE`:
```python
"project_links": [
    "https://github.com/flurgerburger/backpropagation",
    "https://github.com/flurgerburger/Washing_Machine_Timer-Fuzzy_Logic",
    "https://github.com/flurgerburger/SpendSync"
]
```
*(You can also edit or add links directly inside the running app under the **Featured Projects** expander!)*
