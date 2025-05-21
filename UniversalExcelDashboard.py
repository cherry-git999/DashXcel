import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit app configuration
st.set_page_config(page_title="DashXcel - Universal Excel Analyzer", layout="wide")
st.title(":bar_chart:  DashXcel - Universal Excel Dashboard")

# Upload Excel file
file = st.file_uploader("Upload any Excel file", type=["xlsx"], key="uploader_main")

if file:
    try:
        df = pd.read_excel(file)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
    else:
        st.success("File uploaded successfully!")
        st.subheader("🔍 Raw Data Preview")
        st.dataframe(df.head())

        # Identify column types
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()
        object_cols = df.select_dtypes(include=['object']).columns.tolist()

        # Try to convert object columns to datetime
        for col in object_cols:
            try:
                df[col] = pd.to_datetime(df[col])
                date_cols.append(col)
            except:
                continue

        # Re-identify column types after conversion
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        date_cols = list(set(date_cols))
        object_cols = df.select_dtypes(include=['object']).columns.tolist()

        # Sidebar options
        st.sidebar.header("📊 Chart Options")
        st.sidebar.markdown("Auto-selected based on data types")

        # Time series plot
        if date_cols and numeric_cols:
            date_col = st.sidebar.selectbox("Choose a date column", date_cols)
            y_col = st.sidebar.selectbox("Numeric column for time series", numeric_cols)
            df_sorted = df.sort_values(by=date_col)
            fig = px.line(df_sorted, x=date_col, y=y_col, title=f"{y_col} Over Time")
            st.plotly_chart(fig, use_container_width=True)

        # Bar chart for categorical + numeric
        if object_cols and numeric_cols:
            cat_col = st.sidebar.selectbox("Choose a categorical column", object_cols)
            num_col = st.sidebar.selectbox("Choose a numeric column", numeric_cols, index=0)
            if cat_col and num_col:
                bar_data = df.groupby(cat_col)[num_col].sum().reset_index()
                fig = px.bar(bar_data, x=cat_col, y=num_col, title=f"{num_col} by {cat_col}", height=400)
                st.plotly_chart(fig, use_container_width=True)

                # Pie chart
                pie_data = df.groupby(cat_col)[num_col].sum().reset_index()
                fig = px.pie(pie_data, values=num_col, names=cat_col, title=f"{num_col} Distribution by {cat_col}")
                st.plotly_chart(fig, use_container_width=True)

        # Scatter plot
        if len(numeric_cols) >= 2:
            x_col = st.sidebar.selectbox("X-axis for Scatter", numeric_cols, index=0)
            y_col = st.sidebar.selectbox("Y-axis for Scatter", numeric_cols, index=1)
            fig = px.scatter(df, x=x_col, y=y_col, size=df[numeric_cols[0]],
                             title=f"{y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)

        # Treemap
        if len(object_cols) >= 2 and numeric_cols:
            level_1 = st.sidebar.selectbox("Treemap Level 1", object_cols, index=0)
            level_2 = st.sidebar.selectbox("Treemap Level 2", object_cols, index=1)
            value_col = st.sidebar.selectbox("Treemap Value", numeric_cols)
            tree_data = df.groupby([level_1, level_2])[value_col].sum().reset_index()
            fig = px.treemap(tree_data, path=[level_1, level_2], values=value_col,
                             title=f"Treemap of {value_col} by {level_1} and {level_2}")
            st.plotly_chart(fig, use_container_width=True)

        # Data download button
        st.download_button("Download Processed Data", data=df.to_csv(index=False).encode('utf-8'),
                           file_name="Processed_Data.csv", mime="text/csv")
        st.markdown("### Note: This is a basic version of the dashboard. More features will be added soon.")
        st.markdown("### For any issues, please contact: [A SRI SAI CHARAN](mailto:cherry2544t@gmail.com )")

else:
    st.warning("Please upload an Excel file to proceed.")

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 14px; color: gray;'>
        Made with ❤️ using Streamlit | DashXcel © 2025<br>
        Developed by [A SRI SAI CHARAN]
    </div>
    """,
    unsafe_allow_html=True
)
