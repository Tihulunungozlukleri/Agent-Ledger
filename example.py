import time
import random
from agent_ledger import AgentLedger

def simulate_llm_latency(min_ms: int = 150, max_ms: int = 800) -> float:
    """Simulates realistic network latency of an LLM API call."""
    latency = random.randint(min_ms, max_ms)
    time.sleep(latency / 1000.0) # Small pause to simulate real clock time
    return float(latency)

def main():
    print("=" * 80)
    print(" Agent-Ledger: Lightweight AI Agent SQLite Logger & Summarizer".center(80))
    print("=" * 80)
    
    db_name = "agent_performance.db"
    csv_name = "agent_logs_export.csv"
    
    print(f"\n[1/4] Initializing AgentLedger database at: '{db_name}'...")
    
    # Using the library via context manager for automatic connection cleanup
    with AgentLedger(db_name) as ledger:
        
        print("\n[2/4] Simulating autonomous agent actions & API calls...")
        
        # --- Simulating Research Agent ---
        print("\n  [Research_Agent] Started semantic search on target papers...")
        # simulate prompt, completion tokens and latency
        prompt_t = random.randint(800, 1200)
        completion_t = random.randint(250, 450)
        latency = simulate_llm_latency(300, 600)
        ledger.log_run(
            agent_name="Research_Agent",
            action="VectorDB Query & Context Retrieval",
            prompt_tokens=prompt_t,
            completion_tokens=completion_t,
            execution_time_ms=latency
        )
        print(f"    --> Logged: {prompt_t} prompt, {completion_t} completion tokens in {latency}ms.")

        print("  [Research_Agent] Generating research report draft...")
        prompt_t = random.randint(2500, 3500)
        completion_t = random.randint(800, 1500)
        latency = simulate_llm_latency(800, 1800)
        ledger.log_run(
            agent_name="Research_Agent",
            action="Synthesize PDF papers into markdown summary",
            prompt_tokens=prompt_t,
            completion_tokens=completion_t,
            execution_time_ms=latency
        )
        print(f"    --> Logged: {prompt_t} prompt, {completion_t} completion tokens in {latency}ms.")

        # --- Simulating Coding Agent ---
        print("\n  [Coding_Agent] Generating SQLite schema parsing models...")
        prompt_t = random.randint(1200, 1800)
        completion_t = random.randint(500, 950)
        latency = simulate_llm_latency(400, 900)
        ledger.log_run(
            agent_name="Coding_Agent",
            action="Implement Pydantic models for core database",
            prompt_tokens=prompt_t,
            completion_tokens=completion_t,
            execution_time_ms=latency
        )
        print(f"    --> Logged: {prompt_t} prompt, {completion_t} completion tokens in {latency}ms.")

        print("  [Coding_Agent] Compiling and running unit tests...")
        prompt_t = random.randint(2000, 2400)
        completion_t = random.randint(300, 600)
        latency = simulate_llm_latency(300, 750)
        ledger.log_run(
            agent_name="Coding_Agent",
            action="Fix test errors & re-run pytest suite",
            prompt_tokens=prompt_t,
            completion_tokens=completion_t,
            execution_time_ms=latency
        )
        print(f"    --> Logged: {prompt_t} prompt, {completion_t} completion tokens in {latency}ms.")

        print("  [Coding_Agent] Optimizing SQL index configuration...")
        prompt_t = random.randint(1500, 2200)
        completion_t = random.randint(150, 400)
        latency = simulate_llm_latency(200, 500)
        ledger.log_run(
            agent_name="Coding_Agent",
            action="Create DB composite indices for fast query lookups",
            prompt_tokens=prompt_t,
            completion_tokens=completion_t,
            execution_time_ms=latency
        )
        print(f"    --> Logged: {prompt_t} prompt, {completion_t} completion tokens in {latency}ms.")

        # --- Logging another action for Research Agent ---
        print("\n  [Research_Agent] Translating findings to localized user layout...")
        prompt_t = random.randint(3000, 4000)
        completion_t = random.randint(1000, 1800)
        latency = simulate_llm_latency(900, 2200)
        ledger.log_run(
            agent_name="Research_Agent",
            action="Generate local documentation page in Turkish",
            prompt_tokens=prompt_t,
            completion_tokens=completion_t,
            execution_time_ms=latency
        )
        print(f"    --> Logged: {prompt_t} prompt, {completion_t} completion tokens in {latency}ms.")

        print("\n[3/4] Fetching aggregated database summary table:")
        ledger.get_summary()

        print(f"[4/4] Exporting all database transaction records to: '{csv_name}'...")
        ledger.export_csv(csv_name)
        print("    --> CSV export successfully finished!")

    print("\n" + "=" * 80)
    print(" Demo Run Successfully Completed! ".center(80))
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
