import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="Bangalore Real Estate Price Prediction",
    page_icon=":house:",
    # layout="wide",
    initial_sidebar_state="expanded",
)

# Set background color using custom CSS
st.markdown(
    """
    <style>
        .css-fg4pbf {
    position: absolute;
    color: white;
    background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(100,43,115,1) 0%, rgba(4,0,4,1) 90% );
}
    p,span{
    color: white;
}
    button{
    color:black;
    }
   .css-1vbkxwb p {
   color:black;
   margin:auto;
   }
   .stButton{
   display: flex;
    align-items: center;
    justify-content: center;
   }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load the column data
columns_data = pd.read_json("columns.json", typ='series')

# Load the trained model
model = joblib.load("./Banglore_price_predictor.model")

# Function for price prediction
def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = columns_data.data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(columns_data.data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

# Streamlit app
st.title("Bangalore Real Estate Price Prediction")



# Components
selected_location = st.selectbox("Select Location", columns_data.data_columns[3:])
bedrooms = st.selectbox("Number of Bedrooms", [1, 2, 3, 4, 5, 6])
bathrooms = st.selectbox("Number of Bathrooms", [1, 2, 3, 4, 5, 6])
sqft = st.slider("Select Square Footage", 300, 5000, 1000)

# Predict button
if st.button("Predict Price"):
    # Get the estimated price
    estimated_price = get_estimated_price(selected_location, sqft, bedrooms, bathrooms)
    int_price = int(estimated_price)
    def format_price(price):
        if price < 100:
            return f"₹{price:,.2f} Lakhs"
        else:
            return f"₹{price/100:.2f} Crores"
    # st.success(format_price(int_price))
    st.success(f"The estimated real estate price is: {format_price(int_price)}")
    



