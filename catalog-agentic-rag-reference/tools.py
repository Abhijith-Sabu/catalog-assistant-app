"""Tools the agent can call: read-only SQL over the catalogs, and the policy documents."""
import sqlite3
from pathlib import Path

from langchain.tools import tool

DB_PATH = Path(__file__).parent / "catalog.db"
POLICY_DIR = Path(__file__).parent.parent / "catalog-agentic-rag" / "data" / "policies"
MAX_ROWS = 50


def _connect_read_only():
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)


@tool
def list_tables() -> str:
    """List every table with its columns and row count. Call this first."""
    with _connect_read_only() as connection:
        table_names = [row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        lines = []
        for table_name in table_names:
            column_names = [row[1] for row in connection.execute(f"PRAGMA table_info({table_name})")]
            row_count = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            lines.append(f"{table_name} ({row_count} rows): {', '.join(column_names)}")
    return "\n".join(lines)


@tool
def run_sql(query: str) -> str:
    """Run one read-only SQLite SELECT query. Returns at most 50 rows.
    Use COUNT / GROUP BY for totals instead of fetching many rows."""
    if not query.strip().lower().startswith(("select", "with")):
        return "Error: only SELECT queries are allowed."
    try:
        with _connect_read_only() as connection:
            cursor = connection.execute(query)
            column_names = [description[0] for description in cursor.description]
            result_rows = cursor.fetchmany(MAX_ROWS + 1)
    except sqlite3.Error as sql_error:
        return f"SQL error: {sql_error}"
    if not result_rows:
        return "No rows found."
    truncated = len(result_rows) > MAX_ROWS
    lines = [" | ".join(column_names)]
    lines += [" | ".join(str(value) for value in row) for row in result_rows[:MAX_ROWS]]
    if truncated:
        lines.append(f"... more than {MAX_ROWS} rows, result cut off. Use COUNT or a narrower query.")
    return "\n".join(lines)


@tool
def list_policies() -> str:
    """List the policy documents and their section headings."""
    lines = []
    for policy_path in sorted(POLICY_DIR.glob("*.md")):
        headings = [line.strip() for line in policy_path.read_text(encoding="utf-8").splitlines()
                    if line.startswith("#")]
        lines.append(f"{policy_path.stem}: " + " / ".join(headings))
    return "\n".join(lines)


@tool
def read_policy(policy_name: str) -> str:
    """Read one full policy document, e.g. 'pricing-policy'."""
    policy_path = POLICY_DIR / f"{policy_name.removesuffix('.md')}.md"
    if not policy_path.exists():
        return f"Policy '{policy_name}' not found. Use list_policies."
    return policy_path.read_text(encoding="utf-8")


@tool
def search_policies(keyword: str) -> str:
    """Find policy lines containing a keyword (case-insensitive), with the policy name."""
    matches = []
    for policy_path in sorted(POLICY_DIR.glob("*.md")):
        for line in policy_path.read_text(encoding="utf-8").splitlines():
            if keyword.lower() in line.lower():
                matches.append(f"[{policy_path.stem}] {line.strip()}")
    return "\n".join(matches) if matches else f"No policy line mentions '{keyword}'."


ALL_TOOLS = [list_tables, run_sql, list_policies, read_policy, search_policies]
