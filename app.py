import streamlit as st

st.title("🛍️ E-Commerce Recommendation App")
st.markdown(
   "Find products based on your preferences"
)
st.subheader("👤 Customer Details")
name = st.text_input("Enter Your Name")
age = st.number_input(
    "Enter Your Age",
    min_value=10,
    max_value=100,
    value=20
)
city = st.selectbox(
    "Select Your City",
    [
        "Pune",
        "Mumbai",
        "Nagpur",
        "Wardha",
        "Delhi",
        "Bangalore"
    ]
)
st.subheader("🛒 Shopping Preferences")
category = st.selectbox(
    "Select Product Category",
    [
        "Clothing",
        "Footwear",
        "Beauty",
        "Electronics",
        "Accessories"
    ]
)
brand = st.selectbox(
    "Select Preferred Brand",
    [
        "Any Brand",
        "Nike",
        "Puma",
        "Adidas",
        "Levis",
        "Samsung"
    ]
)
price = st.slider(
    "Select Maximum Price (₹)",
    min_value=100,
    max_value=100000,
    value=5000,
    step=100
)
rating = st.slider(
    "Select Minimum Rating",
    min_value=1,
    max_value=5,
    value=3
)
st.subheader("💳 Preferences")
payment = st.radio(
    "Select Payment Mode",
    [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Cash on Delivery"
    ]
)
discount = st.checkbox(
    "Show only discounted products"
)
st.subheader("🔮 Get Recommendations")
if st.button("🔮 Recommend Products"):

    st.success("✅ Recommendations generated!")

    st.subheader("📦 Recommended Products")

    st.write("👟 Sports Shoes")
    st.write("⭐ Rating: 4.5")
    st.write("💰 Price: ₹2,499")

    st.write("👕 Casual T-Shirt")
    st.write("⭐ Rating: 4.3")
    st.write("💰 Price: ₹999")

    st.write("🎒 Backpack")
    st.write("⭐ Rating: 4.2")
    st.write("💰 Price: ₹1,499") 
