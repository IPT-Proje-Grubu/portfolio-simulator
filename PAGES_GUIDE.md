# PortfolioSim — Pages Guide

This file explains what every page in the app does.

---

## Main Pages

There are 5 main pages. You can switch between them using the buttons on the left side.

---

### ◎ Summary (Dashboard)

This is the **home page**. You can see everything about your portfolio here.

**What you can see:**
- **5 number boxes** — your portfolio value, profit/loss, and learning level
- **A line chart** — shows how your portfolio value changed over time
- **Live market prices** — all assets with their current price; updates every 3 seconds
- **Recent trades** — your last buy and sell actions
- **Learning panel** — shows your current task and XP progress bar
- **AI Coach tip** — a short suggestion from Gemini AI about your portfolio
- **Quick buttons** — go to Trade or Analysis page fast

---

### ⇄ Trade

This is where you **buy and sell assets**.

**What you can do:**
- See a list of all assets (crypto, stocks, gold) with live prices
- Click on an asset to select it
- See information about the asset — its name, symbol, and risk level
- Choose **BUY** or **SELL** mode
- Enter how much you want to buy or sell
- Use the **"Maximum"** button to use all your money or close your full position
- See a summary before you confirm the trade
- See a table of all your open positions with profit/loss for each
- See **warnings** if your portfolio has too much risk

---

### ≡ History

This page shows **all your past trades**.

**What you can see:**
- A table with every trade — date, type (BUY/SELL), asset name, quantity, price, and total amount
- Summary numbers — total trades, best trade, worst trade
- You can filter by asset name or date

---

### ⊙ Analysis

This page lets you **test your portfolio with real past prices** and see future price predictions.

**What you can do:**
- Pick a start date and end date
- Press **"Run Scenario"** — the app calculates what your portfolio would be worth in that time period
- See a **price forecast** for the next 30 days (uses a regression model)
- See **trend analysis** — is each asset going up or down? How volatile is it?
- See a chart of your portfolio value after the scenario
- See a summary — total profit/loss, best and worst performing asset

---

### 📚 Learn

This is the **learning mode**. It teaches you how to invest through tasks and challenges.

It has 9 sections inside:

---

#### 🌱 Beginner

Tasks for people who are new to investing.

**Example tasks:** Buy your first asset, look at your portfolio summary, make your first sell, check your trade history.

Each task has a description, a hint button, a link to the right page, and **automatic checking** — the app knows when you finish a task. You get XP when you complete a task.

---

#### 📈 Intermediate

This opens after you finish the Beginner level. The tasks are a little harder.

**Example tasks:** Add 3 different assets to your portfolio, keep your risk level low, close a trade with profit.

---

#### 🚀 Advanced

This opens after you finish the Intermediate level. You use the analysis tools here.

**Example tasks:** Run a scenario simulation, look at the price forecast, use the calculator tools.

---

#### 🏆 Achievements

These are **badges** you get automatically when you do something special.

**Examples:** First buy, first profitable sell, reach a certain XP level, diversify your portfolio. Each achievement gives you extra XP.

---

#### ⚡ Challenges

These are **special tasks** that need real investment decisions. They give more XP than regular tasks.

**Examples:** Reach a profit goal, lower your risk level, make many trades.

---

#### 📊 My Analytics

This page shows **how well you are doing** as a learner and trader.

**What you can see:**
- Total number of trades, buys, and sells
- Total volume (how much money you traded)
- Total profit/loss, realized profit/loss, unrealized profit/loss
- Your risk level
- Your best and worst sell

---

#### 🏅 Leaderboard

This is a **ranking table** for all users. Scores are saved in the `leaderboard.json` file.

**What you can see:**
- Your rank, username, profit/loss, trade count, and XP
- Top 10 users sorted by profit/loss
- A **"Save Score"** button to save your current session to the list

---

#### 🧮 Tools

Two **interactive calculators** to help you learn.

**Profit/Loss Calculator:**
Enter the buy price, current price, and quantity. The app shows your profit or loss amount and percentage.

**DCA Simulator (Dollar Cost Averaging):**
Enter a monthly investment amount and number of months. The app shows the total value you would have. This helps you understand the power of investing a small amount regularly.

> Using these tools will automatically complete the **"Use the Calculators"** task in the Advanced level.

---

#### 🤖 AI Coach

This is your **personal AI coach**, powered by Gemini AI. All suggestions are based on your real portfolio data.

**What you can do:**
- See the Gemini connection status (green = connected, yellow = not connected)
- See a **smart suggestion** — automatically created after each trade; press "↻ Refresh" to get a new one
- **Ask a question** — type any question about your portfolio in the big text box and press "Ask"
  - Quick question buttons: *How do I lower my risk?*, *What is my best trade?*, *What should I buy?*, *Why am I losing money?*
- See the **AI answer** — Gemini gives a detailed, data-based answer in Turkish
- Get a **task hint** — AI gives you a small hint for your current learning task
- See a **portfolio snapshot** — quick summary of your value, cash, profit/loss, and risk

---

## Start-up Screens

### Welcome Screen

This appears the **first time you open the app**. You can choose:
- **Start with Learning Mode** → goes directly to the Learn page
- **Explore** → starts from the home page

### Login / Register Screen

Enter a username and password to log in or create a new account. Your data is saved locally in a database file (`data/portfoliosim.db`). Every user has their own portfolio and trade history.

---

## Files in the Project

| File / Folder | What it does |
|---------------|-------------|
| `data/raw/*.csv` | Historical price data for crypto and stocks |
| `data/portfoliosim.db` | User accounts, portfolios, and trade history |
| `leaderboard.json` | Saved leaderboard scores |
| `.env` | Gemini API key |
| `src/ui/` | All page layouts and designs |
| `src/ai/` | Gemini service and AI coach logic |
| `src/portfolio/` | Portfolio state and trade management |
| `src/analysis/` | Trend analysis and price prediction model |
| `src/learning/` | XP system, tasks, and achievements |
