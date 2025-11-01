# 🏅 Olympics Data Analysis Dashboard

An interactive **Streamlit web application** that visualizes over 120 years of Olympic Games history — analyzing medals, athletes, countries, and sports performance trends.  
Built with **Python**, **Pandas**, **Plotly**, **Seaborn**, and **Streamlit**.


**Live Demo:** 
* 🔗 [View Project on Render](https://olympics-data-analysis-zywx.onrender.com)

* 🔗 [View Project on Streamlit](https://olympics-data-analysis-st.streamlit.app)

---

## 📊 Overview

This project aims to provide data-driven insights into the **Olympic Games** using visual analytics.  
Users can explore data through dynamic dashboards, including medal tallies, athlete-wise analysis, country comparisons, and overall trends.

It helps users answer questions like:
- Which country has performed the best over time?
- What is the age distribution of gold medalists?
- How has gender participation evolved across years?
- What are the most successful sports for each nation?

---

## 🧠 Features

### 🥇 Medal Tally
- View medal counts by **year** and **country**
- Compare overall and year-specific performance
- Interactive filters for easy exploration

### 🌍 Country-wise Analysis
- Visualize a country’s performance trend over the years
- Identify top athletes and sports per nation
- Medal trend line chart for quick insights

### 🧍 Athlete-wise Analysis
- Analyze age distributions for all athletes and medal winners
- Compare gold medalists’ ages across different sports
- Explore **height vs. weight** relationships with gender and medal style

### 📈 Overall Analysis
- Total statistics: athletes, sports, events, and participating nations
- Interactive charts showing overall Olympic evolution
- Year-wise trends for sports and participation

---

## 🧩 Dataset Used

**Dataset Source:** [Kaggle - 120 years of Olympic history: athletes and results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

- `athlete_events.csv` → contains details of every athlete and event (1896–2016)
- `noc_regions.csv` → maps NOC codes to country/region names

---

## 🛠️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Frontend** | Streamlit |
| **Data Handling** | Pandas, NumPy |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **Environment** | Python 3.10+ |
| **Deployment** | Streamlit Cloud / Render |

---

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/olympics-data-analysis.git
   cd olympics-data-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # (Windows)
   source venv/bin/activate       # (Mac/Linux)
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

5. **View the dashboard**
   - The app will open automatically in your browser (default: http://localhost:8501)

---

## 🧑‍💻 Author

**Rishikesh Moon**  
Full Stack Developer | Data Science Enthusiast  
📧 [rishikeshmoon@gmail.com](mailto:rishikeshmoon@gmail.com)  

---

⭐ **If you like this project, don’t forget to star the repo!**
