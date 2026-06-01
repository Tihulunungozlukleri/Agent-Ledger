# Agent-Ledger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

**Agent-Ledger** is a lightweight, zero-dependency, open-source Python library designed to track, log, and analyze autonomous AI agent (LLM) operations. It records API calls, token counts, execution latency, and custom actions in a local SQLite database using **only the Python standard library**.

Designed specifically for AI engineers, autonomous workflows, and research environments (such as submissions for the OpenAI OSS program), **Agent-Ledger** ensures you can monitor token expenditures and execution metrics locally without bloating your project dependencies.

---

## Key Features

- 🔋 **Zero External Dependencies**: Powered strictly by standard Python libraries (`sqlite3`, `csv`, `datetime`, etc.).
- 💾 **SQLite Local Datastore**: Stores runs in a robust local SQLite database with thread-safe, transactional commits.
- 📊 **Beautiful Console Summaries**: Features a highly polished, custom-built ASCII box-drawing visualizer to display agent metrics, total tokens, runs, and average latencies inside the terminal.
- 📥 **Instant CSV Exporting**: Includes automatic path-creation and seamless export of database logs to standard CSV files.
- 🔌 **Context Manager Support**: Supports Python's `with` statement for clean, safe database connection lifecycle management.
- 📐 **Clean Architecture**: Follows standard PEP 8 compliance, fully type-hinted, modular, and easy to extend.

---

## Directory Structure

```text
agent-ledger/
│
├── agent_ledger/
│   ├── __init__.py      # Package entry point
│   └── core.py          # SQLite database connection & analysis core
│
├── example.py           # Demonstration script
├── README.md            # Library documentation
├── LICENSE              # MIT License
└── .gitignore           # Git ignore list
```

---

## Installation

No `pip install` or internet connection is required. Simply clone the repository directly into your project's directory and import the package:

```bash
git clone https://github.com/your-username/Agent-Ledger.git
```

Move the `agent_ledger` folder into your Python source tree or make sure it is in your `PYTHONPATH`.

---

## Quick Start

### Basic Context Manager Usage (Recommended)

Using a context manager ensures database connections are safely finalized and committed even if runtime exceptions occur.

```python
from agent_ledger import AgentLedger

# Automatically establishes connection and initializes the SQLite schema
with AgentLedger("agent_performance.db") as ledger:
    
    # 1. Log a research task run
    ledger.log_run(
        agent_name="Research_Agent",
        action="Retrieve documents on quantum computing",
        prompt_tokens=1420,
        completion_tokens=512,
        execution_time_ms=782.4
    )
    
    # 2. Log a code-generation task run
    ledger.log_run(
        agent_name="Coding_Agent",
        action="Refactor core API endpoint",
        prompt_tokens=2100,
        completion_tokens=850,
        execution_time_ms=1420.1
    )

    # 3. Print a stunning console summary table grouped by agent
    ledger.get_summary()

    # 4. Export all logged runs to a CSV spreadsheet
    ledger.export_csv("reports/agent_activity.csv")
```

### Standard Connection Management

If you prefer manual control over when to close the database handle, you can initialize and close the logger explicitly:

```python
from agent_ledger import AgentLedger

ledger = AgentLedger("agent_performance.db")

try:
    ledger.log_run(
        agent_name="Planning_Agent",
        action="Select optimal execution graph",
        prompt_tokens=650,
        completion_tokens=150,
        execution_time_ms=210.0
    )
finally:
    ledger.close()
```

---

## Database Schema (`agent_logs` table)

The SQLite database structure is lightweight and efficient, designed to store run history cleanly:

| Column Name | SQLite Data Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key with auto-increment |
| `timestamp` | `DATETIME` | Time the log was recorded (ISO 8601 string) |
| `agent_name` | `TEXT` | Name of the agent execution context (e.g. `Research_Agent`) |
| `action` | `TEXT` | Specific operation being executed (e.g. `Summarize URL`) |
| `prompt_tokens` | `INTEGER` | Total number of prompt (input) tokens processed |
| `completion_tokens` | `INTEGER` | Total number of completion (output) tokens processed |
| `execution_time_ms` | `REAL` | Total time elapsed in milliseconds |

---

## API Reference

### `AgentLedger(db_path="agent_ledger.db")`
- **Description**: Instantiates a ledger logger. Creates the `agent_logs` table automatically inside the database. Creates any required subdirectories if they do not exist.
- **Arguments**:
  - `db_path` *(str)*: Target filepath for the SQLite file. Default: `"agent_ledger.db"`.

### `log_run(agent_name, action, prompt_tokens, completion_tokens, execution_time_ms, timestamp=None)`
- **Description**: Appends a new run to the SQLite database.
- **Arguments**:
  - `agent_name` *(str)*: The identifying label of the agent.
  - `action` *(str)*: Description of the task/call performed.
  - `prompt_tokens` *(int)*: Tokens consumed by prompt.
  - `completion_tokens` *(int)*: Tokens generated in completion.
  - `execution_time_ms` *(float)*: Latency duration of the API call or system execution in ms.
  - `timestamp` *(str, optional)*: ISO 8601 string representation. If omitted, defaults to the current system date and time (`YYYY-MM-DD HH:MM:SS`).

### `get_summary()`
- **Description**: Computes metrics (total runs, aggregated input/output tokens, total tokens, average latency) grouped per agent, and prints a polished ASCII table directly to stdout.

### `export_csv(filepath)`
- **Description**: Performs a raw extract of the log history, saving them to standard CSV. Create folder tree automatically if necessary.
- **Arguments**:
  - `filepath` *(str)*: Target filepath for the exported `.csv` file.

### `close()`
- **Description**: Closes the connection database socket safely.

---

## Terminal Visualizer Preview

When calling `get_summary()`, **Agent-Ledger** generates a premium box-drawing representation of your metrics directly in your workspace terminal:

```text
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AGENT PERFORMANCE SUMMARY                                  │
├──────────────────┬───────────┬───────────────┬───────────────────┬──────────────┬──────────┤
│ Agent Name       │ Runs      │ Prompt Tokens │ Completion Tokens │ Total Tokens │ Avg Time │
├──────────────────┼───────────┼───────────────┼───────────────────┼──────────────┼──────────┤
│ Research_Agent   │         3 │         7,700 │             3,450 │       11,150 │ 1,324.50 │
│ Coding_Agent     │         3 │         4,900 │             1,850 │        6,750 │   645.83 │
└──────────────────┴───────────┴───────────────┴───────────────────┴──────────────┴──────────┘
```

---

## License

This project is licensed under the standard MIT License - see the [LICENSE](LICENSE) file for details.
