import pandas as pd
import plotly.express as px
import streamlit as st

def generate_dashboard(df):
    """
    Generate an interactive dashboard using Plotly.
    - Detects numeric/categorical columns
    - Lets user customize chart type
    - Auto-suggests a visualization if user skips selection
    """

    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    if df.empty:
        st.warning("⚠️ Uploaded dataset is empty.")
        return None

    if not numeric_cols and not cat_cols:
        st.warning("⚠️ No valid columns found for visualization.")
        return None

    # --- User customization controls ---
    st.subheader("🧩 Customize Your Dashboard")

    with st.expander("Click to customize chart options"):
        cat_choice = st.selectbox(
            "Select a categorical column (optional)",
            ["None"] + cat_cols if cat_cols else ["None"],
            index=0,
        )

        num_choice = st.multiselect(
            "Select numeric columns to visualize",
            numeric_cols,
            default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols,
        )

        chart_type = st.selectbox(
            "Select chart type",
            ["Auto", "Bar", "Line", "Scatter", "Histogram", "Matrix"],
            index=0,
        )

    # --- Automatic suggestion logic ---
    fig = None

    # Auto mode
    if chart_type == "Auto":
        if cat_choice != "None" and num_choice:
            grouped = df.groupby(cat_choice)[num_choice].mean().reset_index()
            fig = px.bar(
                grouped,
                x=cat_choice,
                y=num_choice,
                barmode="group",
                title=f"Average values grouped by {cat_choice}",
                template="plotly_dark",
            )

        elif len(num_choice) > 2:
            fig = px.scatter_matrix(
                df,
                dimensions=num_choice[:4],
                title="Numeric Correlation Matrix",
                template="plotly_dark",
            )

        elif len(num_choice) == 1:
            fig = px.histogram(
                df,
                x=num_choice[0],
                nbins=25,
                title=f"Distribution of {num_choice[0]}",
                template="plotly_dark",
            )

        elif "date" in " ".join(df.columns).lower():
            date_col = [c for c in df.columns if "date" in c.lower()][0]
            fig = px.line(
                df,
                x=date_col,
                y=num_choice[0],
                title=f"Trend over time ({num_choice[0]} vs {date_col})",
                template="plotly_dark",
            )

        else:
            avg_series = df[numeric_cols].mean()
            fig = px.bar(
                x=avg_series.index,
                y=avg_series.values,
                title="Average of Numeric Columns",
                labels={"x": "Columns", "y": "Average Value"},
                template="plotly_dark",
            )

    # Manual chart selection
    elif chart_type == "Bar":
        if cat_choice != "None" and num_choice:
            grouped = df.groupby(cat_choice)[num_choice].mean().reset_index()
            fig = px.bar(
                grouped,
                x=cat_choice,
                y=num_choice,
                barmode="group",
                title=f"Bar Chart: {', '.join(num_choice)} by {cat_choice}",
                template="plotly_dark",
            )

    elif chart_type == "Line":
        if len(num_choice) >= 1:
            x_axis = st.selectbox("Select X-axis (numeric or date)", df.columns)
            fig = px.line(
                df,
                x=x_axis,
                y=num_choice,
                title=f"Line Chart: {', '.join(num_choice)} vs {x_axis}",
                template="plotly_dark",
            )

    elif chart_type == "Scatter":
        if len(num_choice) >= 2:
            fig = px.scatter(
                df,
                x=num_choice[0],
                y=num_choice[1],
                title=f"Scatter Plot: {num_choice[0]} vs {num_choice[1]}",
                template="plotly_dark",
            )

    elif chart_type == "Histogram":
        if num_choice:
            fig = px.histogram(
                df,
                x=num_choice[0],
                nbins=25,
                title=f"Histogram of {num_choice[0]}",
                template="plotly_dark",
            )

    elif chart_type == "Matrix":
        if len(num_choice) > 1:
            fig = px.scatter_matrix(
                df,
                dimensions=num_choice[:4],
                title="Correlation Matrix (Scatter)",
                template="plotly_dark",
            )

    # --- Final layout styling ---
    if fig:
        fig.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            height=500,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        return fig
    else:
        st.warning("⚠️ Not enough data or wrong column types for this chart.")
        return None
