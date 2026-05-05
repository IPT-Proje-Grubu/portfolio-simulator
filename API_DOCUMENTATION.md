# PortfolioSim — API Documentation

**Version:** 1.0  
**Language:** Python 3.13  
**Type:** Desktop Application (PyQt6)

This document explains the main modules and classes you can use in the PortfolioSim project.

---

## Table of Contents

1. [Portfolio State](#1-portfolio-state)
2. [AI Coach](#2-ai-coach)
3. [Gemini Service](#3-gemini-service)
4. [Learning Manager](#4-learning-manager)
5. [Data Loader](#5-data-loader)
6. [Trend Analyzer](#6-trend-analyzer)
7. [Regression Forecaster](#7-regression-forecaster)
8. [Error Reference](#8-error-reference)

---

## 1. Portfolio State

**File:** `src/portfolio/portfolio.py`  
**Class:** `PortfolioState`

This is the main data object. It holds all information about the user's portfolio — cash, positions, and trade history.

### Create a Portfolio

```python
from src.portfolio.portfolio import PortfolioState

# Create a new empty portfolio
state = PortfolioState()

# Create with a demo setup
state = PortfolioState.with_demo_data()
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `cash` | `float` | How much cash the user has (in TL) |
| `starting_balance` | `float` | The balance when the portfolio started. Default: `1,000,000.0` |
| `positions` | `list` | All open investment positions |
| `trade_history` | `list` | All past buy and sell actions |
| `value_history` | `list[float]` | Portfolio value over time |
| `simulation_status` | `str` | Status message from the last simulation |

### Computed Properties

| Property | Returns | Description |
|----------|---------|-------------|
| `portfolio_value` | `float` | Total value: cash + all open positions |
| `total_pnl` | `float` | Total profit or loss (current value minus starting balance) |
| `total_pnl_pct` | `float` | Total profit/loss as a percentage |
| `total_unrealized_pnl` | `float` | Profit/loss on positions that are still open |
| `total_realized_pnl` | `float` | Profit/loss from positions that were already closed |
| `invested_capital` | `float` | Total money currently in open positions |

### Methods

#### `execute_buy(symbol, quantity, price)`

Buy an asset.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | `str` | Yes | Asset name. Example: `"BTC"`, `"AAPL"` |
| `quantity` | `float` | Yes | How many units to buy |
| `price` | `float` | Yes | Price per unit in TL |

**Returns:** `Trade` object

**Example:**
```python
trade = state.execute_buy("BTC", quantity=0.5, price=120000.0)
```

---

#### `execute_sell(symbol, quantity, price)`

Sell an asset.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | `str` | Yes | Asset name |
| `quantity` | `float` | Yes | How many units to sell |
| `price` | `float` | Yes | Price per unit in TL |

**Returns:** `Trade` object

**Example:**
```python
trade = state.execute_sell("BTC", quantity=0.25, price=130000.0)
```

---

#### `update_prices(prices)`

Update the current market price for one or more assets.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prices` | `dict[str, float]` | Yes | A dictionary of symbol → price |

**Returns:** `None`

**Example:**
```python
state.update_prices({"BTC": 125000.0, "ETH": 8000.0})
```

---

#### `build_report(start_date, end_date)`

Create a text report of the portfolio.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | `date` | Yes | Report start date |
| `end_date` | `date` | Yes | Report end date |

**Returns:** `str` — a multi-line text report

---

#### `run_simulation(start_date, end_date)`

Run a scenario simulation using historical price data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | `date` | Yes | Simulation start date |
| `end_date` | `date` | Yes | Simulation end date |

**Returns:** `None` — updates the portfolio's `value_history` and `simulation_status`

---

## 2. AI Coach

**File:** `src/ai/ai_coach.py`  
**Class:** `AICoach`

The AI Coach gives personalized advice. It uses Gemini AI if available, or falls back to rule-based responses.

### Create an AI Coach

```python
from src.ai.gemini_service import GeminiService
from src.ai.context_builder import ContextBuilder
from src.ai.ai_coach import AICoach

gemini = GeminiService()
context_builder = ContextBuilder()
coach = AICoach(gemini=gemini, ctx_builder=context_builder)
```

### Properties

| Property | Returns | Description |
|----------|---------|-------------|
| `gemini_available` | `bool` | `True` if Gemini AI is connected and ready |
| `gemini_status` | `str` | A short status message about the Gemini connection |

### Methods

#### `get_action_suggestion(state, extra, ls, action, callback)`

Get a coaching suggestion after a user action (like a trade).

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | `PortfolioState` | Current portfolio state |
| `extra` | `Any` | Extra learning context |
| `ls` | `LearningManager` | The learning system |
| `action` | `str` | What the user just did. Example: `"Bought BTC"` |
| `callback` | `Callable[[str], None]` | A function that receives the suggestion text |
| `lb` | `Any` (optional) | Leaderboard manager |

**Returns:** `None` — the result is sent to the `callback` function

**Example:**
```python
def show_tip(text: str):
    print("AI says:", text)

coach.get_action_suggestion(state, extra, ls, "Bought BTC", callback=show_tip)
```

---

#### `answer_question(state, extra, ls, question, callback)`

Answer a question the user types about their portfolio.

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | `PortfolioState` | Current portfolio state |
| `extra` | `Any` | Extra learning context |
| `ls` | `LearningManager` | The learning system |
| `question` | `str` | The user's question in Turkish or English |
| `callback` | `Callable[[str], None]` | A function that receives the answer text |

**Returns:** `None`

**Example:**
```python
coach.answer_question(state, extra, ls, "How can I reduce my risk?", callback=print)
```

---

#### `get_learning_hint(state, extra, ls, task, callback)`

Get a hint for the current learning task.

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | `PortfolioState` | Current portfolio state |
| `extra` | `Any` | Extra learning context |
| `ls` | `LearningManager` | The learning system |
| `task` | `Task` | The current active task |
| `callback` | `Callable[[str], None]` | A function that receives the hint text |

**Returns:** `None`

---

#### `build_context(state, extra, ls, action, lb)`

Build the context dictionary that is sent to Gemini.

**Returns:** `dict` — contains portfolio, performance, risk, and learning data

---

## 3. Gemini Service

**File:** `src/ai/gemini_service.py`  
**Class:** `GeminiService`

This is the low-level connection to the Google Gemini AI API.

### Configuration

| Constant | Value | Description |
|----------|-------|-------------|
| `MODEL_NAME` | `"gemini-2.5-flash-lite"` | The Gemini model used |
| `MAX_OUTPUT_CHARS` | `2000` | Maximum length of an accepted response |
| `MIN_OUTPUT_CHARS` | `12` | Minimum length of an accepted response |
| `MAX_CACHE_SIZE` | `60` | Maximum number of cached responses |

### API Key Setup

The service reads the API key in this order:

1. The `api_key` argument passed to `__init__`
2. The `GEMINI_API_KEY` environment variable
3. The `.env` file in the project root

**`.env` file format:**
```
GEMINI_API_KEY=your_api_key_here
```

### Create a Gemini Service

```python
from src.ai.gemini_service import GeminiService

# Reads key from .env automatically
gemini = GeminiService()

# Or pass a key directly
gemini = GeminiService(api_key="YOUR_KEY")
```

### Properties

| Property | Returns | Description |
|----------|---------|-------------|
| `is_available` | `bool` | `True` if the API key is valid and the model is ready |
| `status_message` | `str` | Human-readable connection status or error message |
| `status_icon` | `str` | `"✓"` if connected, `"✗"` if not |

### Methods

#### `send_prompt(context, user_question)`

Send a prompt to Gemini and get a response.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `context` | `dict` | Yes | Portfolio data dictionary |
| `user_question` | `str` | No | A specific question from the user |

**Returns:** `str` if successful, `None` if the call fails or the response is too short/long

> **Note:** Responses are cached. The same context + question will not call the API twice.

---

#### `configure(api_key)`

Change the API key and reconnect.

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str` | The new Gemini API key |

**Returns:** `bool` — `True` if the new key works

---

#### `make_worker(context, question, fallback)`

Create an async worker for use in the UI. This runs the API call on a background thread so the UI does not freeze.

**Returns:** `GeminiWorker` (a `QThread` subclass)

**Signals on `GeminiWorker`:**
- `result_ready(str)` — fired when AI responds successfully
- `failed(str)` — fired with the fallback message when the call fails

---

## 4. Learning Manager

**File:** `src/learning/manager.py`  
**Class:** `LearningManager`

This manages the XP system, tasks, achievements, and challenges.

### Properties

| Property | Returns | Description |
|----------|---------|-------------|
| `xp` | `int` | The user's current experience points |
| `current_level` | `str` | The current level id (e.g. `"beginner"`) |
| `current_level_label` | `str` | The display name (e.g. `"Başlangıç"`) |
| `current_level_icon` | `str` | The level icon emoji |

### Key Methods

#### `check_all(state, extra)`

Check all tasks, achievements, and challenges. Award XP for completed ones and fire callbacks.

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | `PortfolioState` | Current portfolio |
| `extra` | `dict` | Extra state (pages visited, actions done) |

**Returns:** `list[str]` — IDs of newly completed tasks

---

#### `is_task_complete(task_id)`

Check if a task is already done.

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | `str` | The task ID |

**Returns:** `bool`

---

#### `is_level_unlocked(level_id)`

Check if the user has enough XP to access a level.

| Parameter | Type | Description |
|-----------|------|-------------|
| `level_id` | `str` | One of `"beginner"`, `"intermediate"`, `"advanced"` |

**Returns:** `bool`

---

#### `level_progress()`

Get the user's XP progress inside the current level.

**Returns:** `tuple[int, int]` — (current XP in level, total XP needed for next level)

**Example:**
```python
current, total = ls.level_progress()
print(f"{current} / {total} XP")  # e.g. "120 / 300 XP"
```

---

### Callbacks (Event Hooks)

Register functions to run when something happens:

```python
# When a task is completed
ls.on_task_complete(lambda task, xp: print(f"Done: {task.title}, +{xp} XP"))

# When an achievement is unlocked
ls.on_achievement_unlock(lambda ach: print(f"Achievement: {ach.title}"))

# When the user reaches a new level
ls.on_level_up(lambda level_id: print(f"New level: {level_id}"))

# When all tasks in a level are done
ls.on_level_complete(lambda level: print(f"Level complete: {level.name}"))
```

---

## 5. Data Loader

**File:** `src/data_processing/data_loader.py`  
**Class:** `DataLoader`

Loads historical price data from CSV files.

### Methods

#### `load_csv(file_path)`

Load one CSV file.

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | `str` | Full path to the CSV file |

**Returns:** `LoadedDataset`

| Field | Type | Description |
|-------|------|-------------|
| `path` | `Path` | File path |
| `symbol` | `str` | Asset symbol detected from the file |
| `df` | `DataFrame` | Full data as a pandas DataFrame |
| `date_column` | `str` | Name of the date column found |
| `price_columns` | `list[str]` | Names of the price columns found |
| `close_series` | `list[float]` | (property) List of closing prices |

**Example:**
```python
loader = DataLoader()
dataset = loader.load_csv("data/raw/coin_Bitcoin.csv")
print(dataset.symbol)       # "BTC"
print(dataset.close_series) # [45000.0, 46200.0, ...]
```

---

#### `load_raw_folder(folder)`

Load all CSV files from a folder at once.

| Parameter | Type | Description |
|-----------|------|-------------|
| `folder` | `Path` | Path to the folder |

**Returns:** `dict[str, LoadedDataset]` — symbol → dataset

**Example:**
```python
from pathlib import Path

loader = DataLoader()
datasets = loader.load_raw_folder(Path("data/raw"))
print(list(datasets.keys()))  # ["BTC", "ETH", "AAPL", ...]
```

---

#### `inspect_csv(file_path)`

Read only the header and row count of a CSV file (fast — does not load all data).

**Returns:** `DatasetInfo` with fields: `path`, `columns`, `row_count`

---

## 6. Trend Analyzer

**File:** `src/analysis/trend_analysis.py`  
**Class:** `TrendAnalyzer`

Analyzes a price series and tells you the trend direction.

### Method

#### `summarize(series)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `series` | `list[float]` | A list of prices, oldest first |

**Returns:** `TrendSummary`

| Field | Type | Description |
|-------|------|-------------|
| `direction` | `str` | `"up"`, `"down"`, `"flat"`, or `"not_enough_data"` |
| `change_pct` | `float` | Total percentage change from first to last price |
| `volatility_pct` | `float` | Average step-by-step volatility as a percentage |

**Example:**
```python
analyzer = TrendAnalyzer()
result = analyzer.summarize([100.0, 102.0, 99.0, 105.0, 108.0])
print(result.direction)     # "up"
print(result.change_pct)    # 8.0
print(result.volatility_pct)  # e.g. 2.5
```

---

## 7. Regression Forecaster

**File:** `src/analysis/regression_model.py`  
**Class:** `RegressionForecaster`

Predicts future prices using a simple linear regression model.

### Method

#### `predict_next(series, steps)`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `series` | `list[float]` | Yes | Historical prices, oldest first |
| `steps` | `int` | No | How many future steps to predict. Default: `3` |

**Returns:** `list[ForecastPoint]`

| Field | Type | Description |
|-------|------|-------------|
| `index` | `int` | Step number (1, 2, 3, …) |
| `value` | `float` | Predicted price at that step |

**Example:**
```python
forecaster = RegressionForecaster()
points = forecaster.predict_next([100.0, 102.0, 104.0, 103.0, 105.0], steps=3)
for p in points:
    print(f"Step {p.index}: {p.value:.2f}")
# Step 1: 106.40
# Step 2: 107.80
# Step 3: 109.20
```

---

## 8. Error Reference

### Common Errors

| Situation | What happens | How to fix |
|-----------|-------------|------------|
| No API key in `.env` | `GeminiService.is_available` is `False` | Add `GEMINI_API_KEY=your_key` to the `.env` file |
| API rate limit reached | `send_prompt()` returns `None` | Wait a few minutes and try again |
| Not enough cash to buy | `execute_buy()` raises an error | Check `state.cash` before buying |
| Selling more than you own | `execute_sell()` raises an error | Check the position quantity first |
| CSV file has no Date column | `load_csv()` raises an error | Make sure the file has a `Date`, `Timestamp`, or `Datetime` column |
| CSV file has no price column | `load_csv()` raises an error | Make sure the file has an `Open`, `High`, `Low`, `Close`, or `Price` column |

### Gemini HTTP Status Codes

| Code | Meaning | What to do |
|------|---------|------------|
| `200` | OK — request worked | Nothing |
| `401` | Unauthorized — bad API key | Check your API key in `.env` |
| `429` | Too many requests — rate limit hit | Wait and try again |
| `404` | Model not found | Check that `MODEL_NAME` is a valid model |

---

## Data Files

| File / Folder | Format | Description |
|---------------|--------|-------------|
| `data/raw/*.csv` | CSV | Historical daily prices for each asset. Columns: `Date`, `Open`, `High`, `Low`, `Close`, `Volume` |
| `data/portfoliosim.db` | SQLite | User accounts, portfolios, and trade history |
| `leaderboard.json` | JSON | Top 10 session scores, sorted by profit/loss |
| `.env` | Plain text | API keys. Format: `KEY=value` |

---

## Quick Start Example

```python
from src.portfolio.portfolio import PortfolioState
from src.ai.gemini_service import GeminiService
from src.ai.context_builder import ContextBuilder
from src.ai.ai_coach import AICoach

# 1. Create a portfolio
state = PortfolioState()

# 2. Buy an asset
state.execute_buy("BTC", quantity=0.1, price=100000.0)

# 3. Update prices
state.update_prices({"BTC": 105000.0})

# 4. Check profit
print(f"Profit: {state.total_pnl:+,.0f} TL")  # Profit: +500 TL

# 5. Ask AI for advice
gemini = GeminiService()  # reads key from .env
coach = AICoach(gemini=gemini, ctx_builder=ContextBuilder())

if gemini.is_available:
    coach.get_action_suggestion(state, {}, None, "bought BTC",
                                callback=lambda tip: print("AI:", tip))
```
