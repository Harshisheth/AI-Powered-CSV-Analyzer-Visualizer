import streamlit as st
import pandas as pd
import plotly.express as px
import io
import google.generativeai as genai
import pandas as pd
genai.configure(api_key="AIzaSyClHUjDfQwYWYxDGstsxZ4uCtzFSyEIlO0")  
model = genai.GenerativeModel("gemini-1.5-pro")  
def generate_insights_from_data(df):
    prompt = f"""
    You are a skilled data analyst. Given the following dataset:
    - Provide a brief summary of the dataset (e.g., type of data, columns, and general trends).
    - Give 2 business recommendations based on the data trends or patterns.
    Use a clear, concise, and professional tone.
    Data (first 50 rows):\n{df.head(50).to_csv(index=False)}
    """
    response = model.generate_content(prompt)  
    return response.text
st.set_page_config(page_title="CSV Data Visualizer", layout="wide")
st.title("CSV Data Visualizer")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
    st.subheader("Preview of Data")
    st.dataframe(df.head())
    st.subheader("Summary Statistics")
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    st.write(df[numeric_columns].describe())
    if len(numeric_columns) >= 2:
        st.subheader("Create a Chart")
        x_axis = st.selectbox("X-axis", numeric_columns)
        y_axis = st.selectbox("Y-axis", numeric_columns, index=1)
        chart_type = st.radio("Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"])
        if chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis)
        elif chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis)
        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis)
        elif chart_type == "Pie Chart":
            fig = px.pie(df, names=x_axis, values=y_axis)
        st.plotly_chart(fig, use_container_width=True)
        if st.button("💡 Generate AI Insights with Gemini"):
            with st.spinner("Analyzing CSV with Gemini..."):
                try:
                    insights = generate_insights_from_data(df)
                    st.subheader("🧠 AI Insights & Recommendations")
                    st.markdown(insights)
                except Exception as e:
                    st.error(f"Error generating insights: {e}")
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format="png")
        img_buffer.seek(0)
        st.download_button(
            label="📥 Download Chart as PNG",
            data=img_buffer,
            file_name="chart.png",
            mime="image/png"
        )
    else:
        st.warning("Not enough numeric columns to display a chart.")
else:
    st.info("Please upload a CSV file to get started.")
