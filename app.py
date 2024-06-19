import streamlit as st
import pickle
import numpy as np
import pandas as pd

# import the model
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

st.title("Laptop Price Predictor")

# brand
company = st.selectbox('Brand', df['Company'].unique())

# type of laptop
type = st.selectbox('Type', df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM(in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])

# weight
weight = st.number_input('Weight of the Laptop')

# Touchscreen
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])

# IPS
ips = st.selectbox('IPS', ['No', 'Yes'])

# screen size
screen_size = st.number_input('Screen Size')

# resolution
resolution = st.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800',
    '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])

# CPU
cpu = st.selectbox('CPU', df['Cpu brand'].unique())

# HDD
hdd = st.selectbox('HDD(in GB)', [0, 128, 256, 512, 1024, 2048])

# SSD
ssd = st.selectbox('SSD(in GB)', [0, 8, 128, 256, 512, 1024])

# GPU
gpu = st.selectbox('GPU', df['Gpu brand'].unique())

# OS
os = st.selectbox('OS', df['os'].unique())

if st.button('Predict Price'):
    # Convert inputs to the correct format
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    # Calculate PPI
    x_res, y_res = map(int, resolution.split('x'))
    ppi = ((x_res**2 + y_res**2)**0.5) / screen_size

    # Prepare the query DataFrame
    query = pd.DataFrame({
        'Company': [company],
        'TypeName': [type],
        'Ram': [ram],
        'Weight': [weight],
        'Touchscreen': [touchscreen],
        'Ips': [ips],
        'Cpu brand': [cpu],
        'HDD': [hdd],
        'SSD': [ssd],
        'Gpu brand': [gpu],
        'os': [os],
        'ppi': [ppi]
    })

    # Predict the price
    try:
        predicted_price_usd = np.exp(pipe.predict(query))[0]
        exchange_rate = 14500  # Fixed exchange rate from USD to IDR
        predicted_price_idr = predicted_price_usd * exchange_rate
        st.title(f"The predicted price for the laptop with the specified configuration is Rp {int(predicted_price_idr):,} ")
    except Exception as e:
        st.error(f"An error occurred: {e}")
