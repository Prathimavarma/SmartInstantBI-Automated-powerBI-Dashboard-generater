import streamlit as st
import requests
import pandas as pd
import io
import contextlib
import traceback

st.set_page_config(page_title="💬 Chat Assistant", layout="centered")
st.title("💬 Chat with Your Data (Gemma3:1b via Ollama)")

# Sidebar
model = st.sidebar.selectbox(
    "Select Ollama Model",
    ["gemma3:1b", "llama3.2", "phi3:mini"],
    index=0
)
st.sidebar.info("🧠 Powered by Ollama on port 11434")

# Ensure df exists
if "df" not in st.session_state:
    st.warning("⚠️ Please upload your dataset first in the Dashboard page.")
    st.stop()

df = st.session_state.df

# --- Safe execution ---
def safe_exec(code, df):
    local_env = {"df": df, "pd": pd}
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        try:
            exec(code, {}, local_env)
            logs = buffer.getvalue().strip()
            result = local_env.get("result", None)
            if result is None and logs:
                result = logs
            return result
        except Exception:
            return traceback.format_exc()

# --- Build context ---
preview = df.head(5).to_markdown(index=False)
dtypes = df.dtypes.astype(str).to_dict()

context = f"""
You are a data assistant with access to a pandas DataFrame `df`.

Dataset info:
Columns: {', '.join(df.columns)}
Column types: {dtypes}
Sample rows:
{preview}

Rules:
- If computation is needed, output Python code (inside ```python ...```).
- Always assign your final result to variable 'result'.
- Do NOT just print; always store the answer in 'result'.
- If conceptual, reply in plain English.
"""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

if prompt := st.chat_input("Ask me anything about your data..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append(("user", prompt))

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                history = "\n".join([f"{r}: {m}" for r, m in st.session_state.chat_history[-5:]])
                full_prompt = f"{context}\n\n{history}\nAssistant:"
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": model, "prompt": full_prompt, "stream": False},
                    timeout=120,
                )
                reply = (
                    response.json().get("response", "").strip()
                    if response.ok
                    else f"⚠️ Error: {response.text}"
                )
            except Exception as e:
                reply = f"⚠️ Failed to reach Ollama API: {e}"

            if "```python" in reply:
                code = reply.split("```python")[1].split("```")[0].strip()
                result = safe_exec(code, df)

                if isinstance(result, (pd.DataFrame, pd.Series)):
                    st.dataframe(result)
                elif isinstance(result, (int, float, str)):
                    st.success(f"{result}")
                else:
                    st.text(result)

                with st.expander("🧩 Show generated code"):
                    st.code(code, language="python")
            else:
                st.markdown(reply)

            st.session_state.chat_history.append(("assistant", reply))
