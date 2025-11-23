import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from llama_cpp import Llama
from dashboard_generator import generate_dashboard
import requests
import os
import numpy as np
import io
import contextlib

# --- Streamlit Setup ---
st.set_page_config(page_title="📊 AI Dashboard (TinyLlama + Ollama)", layout="wide")
st.title("📊 Instant BI: Automated Power BI Dashboard Generator")

# -----------------------
# ⚙️ Safe Code Execution
# -----------------------
def safe_exec(code, df=None):
    local_env = {"np": np, "pd": pd}
    try:
        if df is not None:
            for col in df.columns:
                safe_name = col.strip().replace(" ", "_").lower()
                local_env[safe_name] = df[col].tolist()
            local_env["df"] = df

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(code, {}, local_env)
        output = buf.getvalue().strip()

        result = local_env.get("result", None)
        if result is None and output:
            result = output

        if result is None:
            return "⚠️ No result variable found. Try rephrasing your question."

        return result

    except NameError as e:
        missing_var = str(e).split("'")[1] if "'" in str(e) else "unknown"
        suggestions = ", ".join(df.columns.tolist()) if df is not None else "none"
        return f"⚠️ The variable or column '{missing_var}' was not found. Try using one of: {suggestions}"

    except Exception as e:
        return f"⚠️ Error while running generated code: {str(e)}"


# -----------------------
# 📂 File Upload
# -----------------------
uploaded_file = st.file_uploader("Upload your CSV or XLSX file", type=["csv", "xlsx"])

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1]
    df = pd.read_csv(uploaded_file) if ext == "csv" else pd.read_excel(uploaded_file)
    st.session_state.df = df

    st.write("### 📄 Preview:")
    st.dataframe(df.head())

    # -----------------------
    # 🧠 TinyLlama Dashboard Generation
    # -----------------------
    
    model_path = os.path.join(os.path.dirname(__file__), "models", "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

    try:
        llm = Llama(model_path=model_path)
    except Exception as e:
        st.error(f"⚠️ Could not load TinyLlama model:\n{e}")
        st.stop()

    os.makedirs("static", exist_ok=True)

    with st.spinner("📊 TinyLlama generating dashboard..."):
        fig = generate_dashboard(df)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -----------------------
    # 💡 Ollama Insights Generation
    # -----------------------
    model = "gemma3:1b"
    preview = df.head(5).to_markdown(index=False)
    columns = ", ".join(df.columns)

    insights_prompt = f"""
    You are a professional data analyst.
    Analyze this dataset and give 3–5 key insights and observations about trends, relationships, and patterns.
    Focus on interesting changes, possible causes, and implications.

    Columns: {columns}
    Sample data:
    {preview}
    """

    with st.spinner("🤖 Ollama generating insights..."):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": insights_prompt, "stream": False},
                timeout=60,
            )
            if response.ok:
                insights = response.json()["response"].strip()
            else:
                insights = f"⚠️ Error: {response.text}"
        except Exception as e:
            insights = f"⚠️ Ollama connection failed: {e}"

    st.markdown("### 💡 Ollama Insights:")
    st.markdown(insights)
    st.divider()

    # -----------------------
    # 💬 Integrated Chat Assistant
    # -----------------------
    st.subheader("💬 Chat with Your Data")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    dtypes = df.dtypes.astype(str).to_dict()
    columns = ", ".join(df.columns)

    context = f"""
    You are an advanced data assistant with Python and pandas knowledge.
    Dataset columns: {columns}
    Column types: {dtypes}
    Numeric columns: {numeric_cols}

    Rules:
    - If the question involves data analysis or prediction, return a Python code block using pandas/numpy.
    - Always assign your final computed answer to a variable named 'result'.
    - Do NOT only print — assign your final value to 'result', even if you also print it.
    - 'result' can be numeric, text, or a pandas object.
    - You may explain your reasoning textually **after** the code block.
    """

    if prompt := st.chat_input("Ask me anything about your data..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append(("user", prompt))

        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking..."):
                try:
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": model,
                            "prompt": f"{context}\n\nUser: {prompt}\nAssistant:",
                            "stream": False,
                        },
                        timeout=120,
                    )

                    if not response.ok:
                        reply = f"⚠️ Error: {response.text}"
                    else:
                        reply = response.json()["response"].strip()

                except Exception as e:
                    reply = f"⚠️ Failed to contact Ollama: {e}"

                if "```python" in reply:
                    code = reply.split("```python")[1].split("```")[0].strip()
                    # Hide code — just execute
                    result = safe_exec(code, df)

                    if isinstance(result, (pd.DataFrame, pd.Series)):
                        st.dataframe(result)
                    elif isinstance(result, (int, float, str)):
                        st.success(f"{result}")
                    else:
                        st.info(result)

                    # Optional: allow user to expand to see code
                    with st.expander("🧩 Show generated code"):
                        st.code(code, language="python")

                else:
                    st.markdown(reply)

                st.session_state.chat_history.append(("assistant", reply))
