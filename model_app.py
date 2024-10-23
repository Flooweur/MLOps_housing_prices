import streamlit as st
import joblib
import matplotlib.pyplot as plt

model = joblib.load("regression.joblib")

size = st.number_input("Enter the size of the house (in square meters)", min_value=0.0, step=0.1)
nb_rooms = st.number_input("Enter the number of bedrooms", min_value=0, step=1)
garden = st.number_input("Does the house have a garden? (0 for No, 1 for Yes)", min_value=0, max_value=1, step=1)

if st.button("Predict Price"):
    input_data = [[size, nb_rooms, garden]]
    
    prediction = model.predict(input_data)
    
    st.write(f"The predicted price of the house is: ${prediction[0]:,.2f}")
    
    # Store the input data in session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append({
        'size': size,
        'nb_rooms': nb_rooms,
        'garden': garden,
        'predicted_price': prediction[0]
    })
    
    # Display the history
    st.subheader("Prediction History")
    for i, entry in enumerate(st.session_state.history, 1):
        st.write(f"Request {i}:")
        st.write(f"Size: {entry['size']} sq m")
        st.write(f"Number of rooms: {entry['nb_rooms']}")
        st.write(f"Garden: {'Yes' if entry['garden'] == 1 else 'No'}")
        st.write(f"Predicted Price: ${entry['predicted_price']:,.2f}")
        st.write("---")

    # Create a graph of predicted prices vs house size
    if len(st.session_state.history) > 1:
        st.subheader("Predicted Prices vs House Size")
        
        sizes = [entry['size'] for entry in st.session_state.history]
        prices = [entry['predicted_price'] for entry in st.session_state.history]
        
        fig, ax = plt.subplots()
        ax.scatter(sizes, prices)
        ax.set_xlabel('House Size (sq m)')
        ax.set_ylabel('Predicted Price ($)')
        ax.set_title('Predicted House Prices vs Size')
        
        st.pyplot(fig)
