# Portfolio Simulator

A Python desktop app for learning how to invest. You can buy and sell assets, see your profit or loss, and get advice from an AI coach.

Built with **PyQt6** and **Google Gemini AI**. Works on Windows, macOS, and Linux.

---

## How to Run

```powershell
# 1. Go to the project folder
cd C:\Users\kerem\portfolio-simulator

# 2. Create a virtual environment (do this only once)
python -m venv venv

# 3. Turn on the virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install the required packages (do this only once)
pip install -r requirements.txt

# 5. Start the app
python main.py
```

> **Note:** Next time, you only need to do steps 1, 3, and 5.

---

## What Can You Do?

### Buy and Sell
- Buy and sell assets with simulated prices (prices update every 3 seconds)
- See your open positions: average cost, current value, profit/loss
- See your portfolio value as a chart
- Track your cash balance and trade history

### Analysis
- Run a simulation with a selected date range
- See price predictions using a simple regression model
- See trend direction, price change, and volatility

### Load Data
- Load price data from CSV files
- The app finds the date and price columns automatically

### Learn Mode (15 Tasks, 3 Levels)
Complete tasks to earn XP and unlock new levels.

| Level | XP Needed | Tasks | Topics |
|-------|-----------|-------|--------|
| 🌱 Beginner | 0 XP | 5 tasks | First buy, sell, portfolio check, analysis, report |
| 📈 Intermediate | 300 XP | 5 tasks | Diversify, sell for profit, big buy, forecast, calculator |
| 🚀 Advanced | 700 XP | 5 tasks | Balanced portfolio, big profit, full cycle, multi-sell, big forecast |

- You must finish one level before the next one opens
- You earn XP, badges, and leaderboard points

### Learn from Mistakes
After every trade, the app checks if you made a common mistake:

| Rule | When it fires | Tip |
|------|--------------|-----|
| Too much in one asset | One asset > 55% of portfolio | Diversify |
| Too large single trade | Trade > 50% of your cash | Make smaller trades |
| Panic sell at a loss | Loss > -20% | Think long-term |
| Sell a winner too early | Profit < 5% | Hold the position |
| No diversification | Only 1 asset | Add different assets |
| Too much idle cash | Cash > 80% of portfolio | Consider investing |
| Too many trades | 10+ trades, win rate < 30% | Trade less often |

### AI Coach (Gemini + Rule-Based)
- **Rule-based mode:** Works without an API key. Gives advice based on your portfolio.
- **Gemini AI mode:** Gives detailed advice using your real portfolio data.
- **Q&A:** You can ask the AI questions about your portfolio.
- **Task hints:** The AI gives you hints for learning tasks (without giving the answer).
- **Non-blocking:** AI calls run in the background. The app does not freeze.

### Leaderboard
- Each session gets a random Turkish username (no login needed)
- Saved locally in `leaderboard.json`
- Sorted by profit/loss, trade count, win rate, risk score, and level
- Shows the top 10 players

---

## Pages

| # | Page | What it does |
|---|------|-------------|
| 0 | **Dashboard** | Portfolio summary, XP progress, active task, AI tip, risk badge |
| 1 | **Trade** | Buy/sell orders, open positions, account summary, task banner |
| 2 | **History** | Trade history table, win rate, profitable sales, risk score |
| 3 | **Data** | Load a CSV file and see column info |
| 4 | **Analysis** | Scenario simulation, trend analysis, AI Coach comment |
| 5 | **Learn** | Tasks, achievements, challenges, leaderboard, AI Coach |

---

## AI Coach Setup (Optional)

The AI Coach works in **rule-based mode** without any API key.  
To use Gemini AI:

**1. Get a free API key:**  
[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**2. Create a `.env` file:**
```powershell
Copy-Item .env.example .env
```

**3. Edit the file:**
```
GEMINI_API_KEY=paste_your_key_here
```

---

## Requirements

| Package | Version | Required | Description |
|---------|---------|----------|-------------|
| Python | >= 3.10 | Yes | The programming language |
| PyQt6 | >= 6.10.2 | Yes | Desktop UI framework |
| google-genai | latest | No | For Gemini AI support |

```powershell
pip install -r requirements.txt
```

---

## XP and Level System

```
0 XP ──────── 300 XP ──────── 700 XP ──────── 1200 XP
  🌱 Beginner   📈 Intermediate  🚀 Advanced      🏆 Master
  (5 tasks)     (5 tasks)        (5 tasks)
```

- Each task gives you **100–200 XP**
- Achievements give **50–150 XP**
- Challenges give **100–200 XP**
- You cannot open the next level until you finish the current one

---

## Project Structure

```
portfolio-simulator/
│
├── main.py                         # App entry point
├── requirements.txt                # Package list
├── .env.example                    # Example API key file
├── leaderboard.json                # Leaderboard data (auto-created)
│
└── src/
    ├── app.py                      # PyQt6 app setup
    │
    ├── ai/                         # AI Coach modules
    │   ├── gemini_service.py       # Gemini API connection (cache, async)
    │   ├── context_builder.py      # Builds AI context from portfolio data
    │   └── ai_coach.py             # Hybrid AI system + rule engine
    │
    ├── learning/                   # Learning system
    │   ├── manager.py              # LearningManager, Achievement, Challenge
    │   ├── level.py                # Level class
    │   ├── task.py                 # Task class and TaskStatus
    │   ├── mistake_detector.py     # Mistake detection and warnings
    │   ├── leaderboard.py          # LeaderboardManager, JSON storage
    │   └── system.py               # Backward compatibility aliases
    │
    ├── portfolio/                  # Portfolio logic
    │   ├── portfolio.py            # PortfolioState, trade engine
    │   ├── asset.py                # Position data model
    │   ├── trade.py                # Trade data model
    │   └── market.py               # PriceFeed, WATCHLIST, price simulation
    │
    ├── analysis/                   # Analysis engine
    │   ├── regression_model.py     # RegressionForecaster
    │   └── trend_analysis.py       # TrendAnalyzer, TrendSummary
    │
    ├── data_processing/            # CSV handling
    │   ├── data_loader.py          # DataLoader, DatasetInfo
    │   └── data_cleaner.py         # DataCleaner, CleanedDataset
    │
    ├── alerts/                     # Alert system
    │   └── alert_system.py         # AlertSystem
    │
    ├── education/                  # Education content
    │   ├── content.py              # GLOSSARY, TIPS, TOPICS, TUTORIAL_STEPS
    │   └── widgets.py              # Education widgets
    │
    ├── ui/                         # User interface
    │   ├── main_window.py          # Main window and all pages
    │   ├── learn_page.py           # Learn page (LevelPage, AICoachPage…)
    │   └── welcome_dialog.py       # Welcome screen
    │
    └── visualization/              # Chart components
        ├── charts.py               # ChartPlaceholder (line/pie chart)
        └── portfolio_chart.py      # Portfolio slice calculation
```

---

## Design Notes

- The app uses a **dark theme**. Background: `#0b0f1a`, accent: `#2563eb`, green: `#10b981`, red: `#ef4444`.
- `PortfolioState` holds all business logic. The UI depends on it, not the other way around.
- `GeminiWorker` runs API calls on a background thread so the UI never freezes.
- The leaderboard is saved in `leaderboard.json`. The API key is saved in `.env` (not committed to git).
- Portfolio data is kept in memory and resets each session.
