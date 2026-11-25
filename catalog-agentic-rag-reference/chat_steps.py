"""Pure helpers for the chat app (no Streamlit import, so they can be unit-tested)."""


def step_label(tool_name, tool_args):
    if tool_name == "list_tables":
        return "📋 Looking at the tables"
    if tool_name == "run_sql":
        return "📊 Querying the data"
    if tool_name == "list_policies":
        return "📚 Listing the policies"
    if tool_name == "read_policy":
        return f"📄 Reading {tool_args.get('policy_name', 'a policy')}"
    if tool_name == "search_policies":
        return f"🔎 Searching policies for '{tool_args.get('keyword', '')}'"
    return f"🔧 {tool_name}"


def history_messages(chat_history, new_question):
    """Earlier questions and final answers only (no tool messages), then the new question."""
    messages = []
    for turn in chat_history:
        if turn["answer"] is None:  # the model call failed: nothing to send back
            continue
        messages.append({"role": "user", "content": turn["question"]})
        messages.append({"role": "assistant", "content": turn["answer"]})
    messages.append({"role": "user", "content": new_question})
    return messages


def cost_line(tool_call_count, total_tokens, seconds):
    return f"{tool_call_count} tool call{'' if tool_call_count == 1 else 's'} · {total_tokens:,} tokens · {seconds:.1f} s"
