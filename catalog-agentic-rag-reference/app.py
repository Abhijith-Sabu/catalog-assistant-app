"""Catalog Assistant chat app. Run: python -m streamlit run app.py"""
import time

import streamlit as st

from agent import build_agent
from chat_steps import cost_line, history_messages, step_label

SAMPLE_QUESTIONS = {
    "S1": "Is product EP-1023 export-controlled? And where is it made?",
    "S2": "A customer asks what the SVC-14 service plan covers. What do I tell them?",
    "S3": "How many CircuitNova prices are missing and need fixing?",
    "S4": "Can I quote option EO-10029 to a customer in the US?",
    "S5": "Which CircuitNova products are we still selling even though they've expired?",
    "S6": "A customer wants EP-5000 delivered to Germany. What's the price?",
}

st.set_page_config(page_title="Catalog Assistant (presales)", page_icon="💬")
st.title("Catalog Assistant (presales)")
st.caption("Ask a presales question about CircuitNova or Hearthwell.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


@st.cache_resource
def get_agent():
    return build_agent()


def clear_chat():
    st.session_state.chat_history = []


def draw_answer(turn):
    if turn["answer"] is None:
        st.error(turn["error"])
        return
    st.markdown(turn["answer"])
    with st.expander("How I got this"):
        for label, detail, kind in turn["steps"]:
            st.markdown(f"**{label}**")
            if detail:
                st.code(detail, language="sql" if kind == "sql" else None)
    st.caption(turn["cost"])


st.sidebar.header("Sample questions")
sample_clicks = [st.sidebar.button(f"{code}: {text}", key=code) for code, text in SAMPLE_QUESTIONS.items()]
st.sidebar.button("Clear chat", on_click=clear_chat)

for past_turn in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(past_turn["question"])
    with st.chat_message("assistant"):
        draw_answer(past_turn)

question = st.chat_input("Ask a presales question")
for was_clicked, sample_text in zip(sample_clicks, SAMPLE_QUESTIONS.values()):
    if was_clicked:
        question = sample_text

if question:
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        status = st.status("Working on it…", expanded=True)
        turn = {"question": question, "answer": None, "error": None, "steps": [], "cost": ""}
        tool_call_count, total_tokens, final_answer = 0, 0, ""
        start_time = time.time()
        try:
            inputs = {"messages": history_messages(st.session_state.chat_history, question)}
            for update in get_agent().stream(inputs, {"recursion_limit": 40}, stream_mode="updates"):
                for node_name, node_update in update.items():
                    for message in (node_update or {}).get("messages", []):
                        if message.type != "ai":
                            continue
                        total_tokens += (message.usage_metadata or {}).get("total_tokens", 0)
                        if not message.tool_calls:
                            final_answer = message.text
                        for call in message.tool_calls:
                            tool_args = call.get("args") or {}
                            label = step_label(call.get("name"), tool_args)
                            status.write(label)
                            if call.get("name") == "run_sql":
                                turn["steps"].append((label, tool_args.get("query", ""), "sql"))
                            else:
                                turn["steps"].append((label, ", ".join(str(value) for value in tool_args.values()), "text"))
                            tool_call_count += 1
            turn["answer"] = final_answer or "No answer (the agent stopped early)."
            turn["cost"] = cost_line(tool_call_count, total_tokens, time.time() - start_time)
            status.update(label="Done", state="complete", expanded=False)
        except Exception as run_error:
            turn["error"] = f"The model call failed: {type(run_error).__name__}: {run_error}"
            status.update(label="Failed", state="error")
        draw_answer(turn)
    st.session_state.chat_history.append(turn)
