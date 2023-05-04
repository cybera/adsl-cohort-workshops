import streamlit as st
import pandas as pd
import plotly.express as px
import os

os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_AUTH"]
API_URL = "https://api-inference.huggingface.co/models/hustvl/yolos-tiny"
headers = {"Authorization": f"Bearer {os.environ['HF_AUTH']}"}


# Function to load the dataset
def load_data(url):
    data = pd.read_csv(url)
    return data


# Page 1: Display the dataset
def display_data_page(data):
    st.header("Country Indicators Dataset")

    st.subheader("Dataset using st.write()")
    st.write("st.write() displays the dataset in an interactive table format, which allows you to scroll, search, and sort columns.")
    st.write(data)

    st.subheader("Dataset using st.dataframe() \n Documents: https://docs.streamlit.io/library/api-reference/data/st.dataframe")
    st.write("st.dataframe() also displays the dataset in an interactive table format, similar to st.write(). However, it offers more customization options, such as width and height.")
    st.dataframe(data, width=900, height=300)

    st.subheader("Dataset using st.table() \n Documents:https://docs.streamlit.io/library/api-reference/data/st.table")
    st.write("st.table() displays the dataset in a static table format. It has a cleaner look, but does not offer interactivity like scrolling, searching, or sorting.")
    st.table(data.head(10))

# Page 2: Create and display the plot
def plot_page(data):
    def plot_indicator(data, selected_countries, selected_indicator, year_range):
        filtered_data = data[(data['Country Name'].isin(selected_countries)) &
                            (data['Indicator Name'] == selected_indicator) &
                            (data['Year'].between(year_range[0], year_range[1]))]

        fig = px.line(filtered_data, x='Year', y='Value', color='Country Name',
                    title=f"{selected_indicator} for {', '.join(selected_countries)} over time")

        return fig

    st.header("Interactive Visualization \n Ducoments:https://docs.streamlit.io/library/api-reference/charts")
    st.subheader("Select countries, indicator, and year range to plot over time")
    all_countries = data['Country Name'].unique()
    all_indicators = data['Indicator Name'].unique()

    selected_countries = st.multiselect("Choose countries", options=all_countries, default=['United States', 'China'])
    selected_indicator = st.selectbox("Choose indicator", options=all_indicators, index=0)

    min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
    year_range = st.slider("Choose year range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    if selected_countries:
        fig = plot_indicator(data, selected_countries, selected_indicator, year_range)
        st.plotly_chart(fig)
    else:
        st.write("No countries selected. Please select at least one country to plot the selected indicator over time.")
# Page 3: Layout Examples
def layout_examples_page():
    st.header("Streamlit Layout Examples \n Document: https://docs.streamlit.io/library/api-reference/layout")

    st.subheader("Columns")
    st.write("You can create columns in Streamlit using `st.columns()`. This allows you to arrange widgets or content side by side.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Column 1")
        st.button("Button 1")
    with col2:
        st.write("Column 2")
        st.button("Button 2")
    with col3:
        st.write("Column 3")
        st.button("Button 3")

    st.subheader("Expander")
    st.write("You can create expanders in Streamlit using `st.xpander()`. This allows you to show or hide content in a collapsible section.")
    
    with st.expander("Expandable Section"):
        st.write("This is an expandable section.")
        st.button("Button inside Expander")

    st.subheader("Container")
    st.write("You can create containers in Streamlit using `st.container()`. This allows you to group and organize content or widgets.")
    
    
    with st.container():
        st.write("This is a container.")
        st.button("Button inside Container")
    st.write('This is outside a container')
    # Page 4: Styling Examples
def styling_examples_page():
    # Add custom CSS styles
    st.markdown("""
    <style>
        .custom-header {
            color: #4a148c;
            font-weight: bold;
        }
        .custom-text {
            color: #388e3c;
            font-style: italic;
        }
        .custom-button button {
            background-color: #ff9800;
            border: 2px solid #f57c00;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        }
        .custom-button:hover button {
            background-color: #f57c00;
            border-color: #ff9800;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='custom-header'>Custom Styled Header</h1>", unsafe_allow_html=True)
    st.markdown("<p class='custom-text'>This is custom styled text.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-button'>", unsafe_allow_html=True)
    st.button("Custom Styled Button")
    st.markdown("</div>", unsafe_allow_html=True)

#Page 5 chatbot assistant
import openai
import os 

# Set the OPENAI_API_KEY environment variable

class Prompter:
    def __init__(self, gpt_model):
        if not os.environ.get("OPENAI_API_KEY"):
            raise Exception("Please set the OPENAI_API_KEY environment variable")

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.gpt_model = gpt_model

    def prompt_model_return(self, messages: list):
        response = openai.ChatCompletion.create(model=self.gpt_model, messages=messages)
        return response["choices"][0]["message"]["content"]

# Initialize the prompter with the GPT-3.5-turbo model
prompter = Prompter("gpt-3.5-turbo")

# Add a chatbot page function
def chatbot_page():
    st.header("Chatbot Assistant")
    st.write("Interact with the chatbot assistant below.")

    user_input = st.text_input("Type your message here:")
    if st.button("Send"):
        if user_input:
            messages = [
                {"role": "system", "content": "You are a helpful assistant named Bera"},
                {"role": "user", "content": user_input},
            ]
            response = prompter.prompt_model_return(messages)
            st.write(f"Bera: {response}")
        else:
            st.write("Please type a message before sending.")

# Page 6 Object  detection model
import requests
from PIL import Image, ImageDraw
import numpy as np
import io
import base64




def query(filename):
    data = filename.getvalue()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
    
def draw_boxes(image, boxes):
    draw = ImageDraw.Draw(image)

    for box in boxes:
        xmin = int(box['box']['xmin'])
        ymin = int(box['box']['ymin'])
        xmax = int(box['box']['xmax'])
        ymax = int(box['box']['ymax'])
        label = box['label']
        score = box['score']

        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=(255, 0, 0), width=2)
        draw.text((xmin, ymin - 15), f"{label} {score:.2f}", fill=(255, 0, 0))

    return image

def object_detection_page():
    st.title("Object Detection")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.write("")

        if st.button("Detect Objects"):
            with st.spinner("Detecting..."):
                output = query(uploaded_file)
                with st.expander("Expandable Section"):
                    st.write(output)  # Add this line to print the output
                detected_image = draw_boxes(image, output)
                st.image(detected_image, caption="Detected Objects", use_column_width=True)

def main():
    # Read in the dataset
    DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/country_indicators.csv"
    data = load_data(DATA_URL)

    # Define pages and their corresponding functions
    pages = {
        "Display Data": display_data_page,
        "Plot Data": plot_page,
        "Layout Examples": layout_examples_page,
        "Styling Examples": styling_examples_page,
        "Chatbot Assistant Bera": chatbot_page,
        "Object Detection": object_detection_page,
    }

    # Show a selection box in the sidebar to choose a page
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))

    # Call the corresponding function for the selected page
    if selected_page in ["Display Data", "Plot Data"]:
        pages[selected_page](data)
    else:
        pages[selected_page]()

if __name__ == "__main__":
    main()