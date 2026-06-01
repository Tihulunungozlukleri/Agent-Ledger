import os
import sqlite3
import csv
from datetime import datetime
from pathlib import Path
from typing import Optional

class AgentLedger:
    """
    AgentLedger is a zero-dependency, lightweight Python library that logs
    AI agent operations, token counts, and execution times in a local SQLite database.
    """
    def __init__(self, db_path: str = "agent_ledger.db"):
        self.db_path = db_path
        
        # Ensure parent directories exist automatically
        db_dir = Path(db_path).parent
        if db_dir != Path(".") and db_dir != Path(""):
            db_dir.mkdir(parents=True, exist_ok=True)
            
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Initializes the SQLite database and creates the agent_logs table if not exists."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                agent_name TEXT NOT NULL,
                action TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL,
                completion_tokens INTEGER NOT NULL,
                execution_time_ms REAL NOT NULL
            )
        """)
        self.conn.commit()

    def log_run(
        self,
        agent_name: str,
        action: str,
        prompt_tokens: int,
        completion_tokens: int,
        execution_time_ms: float,
        timestamp: Optional[str] = None
    ) -> None:
        """
        Logs a single agent run, transaction, or API call.

        Args:
            agent_name: Name of the LLM agent (e.g. 'Research_Agent').
            action: Specific action performed (e.g. 'Code Generation').
            prompt_tokens: Number of prompt/input tokens.
            completion_tokens: Number of completion/output tokens.
            execution_time_ms: Duration of the run in milliseconds.
            timestamp: ISO 8601 datetime string. Defaults to current local datetime if None.
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO agent_logs (
                timestamp, agent_name, action, prompt_tokens, completion_tokens, execution_time_ms
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            agent_name,
            action,
            int(prompt_tokens),
            int(completion_tokens),
            float(execution_time_ms)
        ))
        self.conn.commit()

    def get_summary(self) -> None:
        """
        Queries the database to calculate total runs, total tokens, and average
        latency grouped by agent_name, then prints a highly polished table to the console.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                agent_name,
                COUNT(*) as run_count,
                SUM(prompt_tokens) as total_prompt,
                SUM(completion_tokens) as total_completion,
                SUM(prompt_tokens + completion_tokens) as total_tokens,
                AVG(execution_time_ms) as avg_execution_time
            FROM agent_logs
            GROUP BY agent_name
            ORDER BY total_tokens DESC
        """)
        rows = cursor.fetchall()

        if not rows:
            print("\n[Agent Ledger] No logs recorded yet.\n")
            return

        headers = ["Agent Name", "Runs", "Prompt Tokens", "Completion Tokens", "Total Tokens", "Avg Latency (ms)"]
        
        # Format metric values to string first (with thousands comma separators)
        formatted_rows = []
        for r in rows:
            agent_name = str(r[0])
            runs = f"{r[1]:,}"
            prompt = f"{r[2]:,}" if r[2] is not None else "0"
            completion = f"{r[3]:,}" if r[3] is not None else "0"
            total = f"{r[4]:,}" if r[4] is not None else "0"
            avg_time = f"{r[5]:,.2f}" if r[5] is not None else "0.00"
            formatted_rows.append([agent_name, runs, prompt, completion, total, avg_time])

        # Compute column widths based on maximum contents size
        col_widths = [len(h) for h in headers]
        for row in formatted_rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(val))

        # Add visual padding
        padding = 2
        col_widths = [w + padding for w in col_widths]

        # Attempt to draw utilizing beautiful Unicode box-drawing characters.
        # Fall back to safe standard ASCII delimiters (+, -, |) if stdout raised a UnicodeEncodeError
        # (common on regional Windows Command Prompts e.g., CP1254).
        try:
            self._print_table(formatted_rows, col_widths, headers, use_unicode=True)
        except UnicodeEncodeError:
            self._print_table(formatted_rows, col_widths, headers, use_unicode=False)

    def _print_table(self, rows: list, col_widths: list, headers: list, use_unicode: bool) -> None:
        if use_unicode:
            top_left, top_right = "┌", "┐"
            bottom_left, bottom_right = "└", "┘"
            horizontal, vertical = "─", "│"
            t_down, t_up = "┬", "┴"
            t_right, t_left = "├", "┤"
            cross = "┼"
        else:
            top_left, top_right = "+", "+"
            bottom_left, bottom_right = "+", "+"
            horizontal, vertical = "-", "|"
            t_down, t_up = "+", "+"
            t_right, t_left = "+", "+"
            cross = "+"

        # Construct borders and separators
        top_border = top_left + t_down.join(horizontal * w for w in col_widths) + top_right
        header_separator = t_right + cross.join(horizontal * w for w in col_widths) + t_left
        bottom_border = bottom_left + t_up.join(horizontal * w for w in col_widths) + bottom_right

        # Table Header Banner
        total_table_width = sum(col_widths) + len(col_widths) - 1
        title_text = " AGENT PERFORMANCE SUMMARY "
        title_padding_left = (total_table_width - len(title_text)) // 2
        title_padding_right = total_table_width - len(title_text) - title_padding_left
        
        title_border_top = top_left + (horizontal * total_table_width) + top_right
        title_row = vertical + (" " * title_padding_left) + title_text + (" " * title_padding_right) + vertical
        title_separator = t_right + t_down.join(horizontal * w for w in col_widths) + t_left

        # Print layout
        print("\n" + title_border_top)
        print(title_row)
        print(title_separator)

        # Print header
        header_str = vertical + vertical.join(
            f" {headers[i].ljust(w-1)}" if i == 0 else f" {headers[i].rjust(w-1)}"
            for i, w in enumerate(col_widths)
        ) + vertical
        print(header_str)
        print(header_separator)

        # Print rows (agent name is left-aligned, numeric statistics are right-aligned)
        for row in rows:
            row_str = vertical + vertical.join(
                f" {row[i].ljust(w-1)}" if i == 0 else f" {row[i].rjust(w-1)}"
                for i, w in enumerate(col_widths)
            ) + vertical
            print(row_str)

        print(bottom_border + "\n")


    def export_csv(self, filepath: str) -> None:
        """
        Exports all logged agent interactions from the database to a CSV file.

        Args:
            filepath: Destination filepath for the CSV. Parent folders will be created automatically.
        """
        path = Path(filepath)
        if path.parent != Path(".") and path.parent != Path(""):
            path.parent.mkdir(parents=True, exist_ok=True)

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, agent_name, action, prompt_tokens, completion_tokens, execution_time_ms
            FROM agent_logs
            ORDER BY id ASC
        """)
        rows = cursor.fetchall()

        headers = ["id", "timestamp", "agent_name", "action", "prompt_tokens", "completion_tokens", "execution_time_ms"]

        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def close(self) -> None:
        """Safely closes the SQLite connection."""
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self) -> "AgentLedger":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
