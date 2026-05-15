import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

div[data-testid="metric-container"] {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #333;
    text-align: center;
}

.stButton>button {
    background-color: #7C3AED;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

.stButton>button:hover {
    background-color: #6D28D9;
}

.stTextInput>div>div>input {
    background-color: #1E1E1E;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# Sidebar
st.markdown(
    """
    <h1 style='text-align: center;'>
        🧠 AI SQL Assistant
    </h1>

    <p style='text-align: center; font-size:20px;'>
        Ask business questions in natural language and get analytics instantly.
    </p>
    """,
    unsafe_allow_html=True
)



st.caption(
    "Suggested queries: top customers • total revenue • highest revenue city • best selling products"
)
# Button
st.write("### Quick Questions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Top Customers"):
        question = "top customers"

with c2:
    if st.button("Total Revenue"):
        question = "total revenue"

with c3:
    if st.button("Best Selling Products"):
        question = "best selling products"



question = st.text_input(
    "Ask your database question:",
    placeholder="Try: top customers"
)

run_query = st.button("Generate SQL")

if question and run_query:
    if "top customers" in question.lower():

        sql = """
        SELECT customers.name,
               SUM(orders.amount) AS total_spent
        FROM customers
        JOIN orders
        ON customers.id = orders.customer_id
        GROUP BY customers.name
        ORDER BY total_spent DESC;
        """

    elif "products" in question.lower():

        sql = "SELECT * FROM products;"

    elif "orders" in question.lower():

        sql = "SELECT * FROM orders;"

    elif "pune" in question.lower():

        sql = """
        SELECT * FROM customers
        WHERE city='Pune';
        """

    elif "delhi" in question.lower():

        sql = """
        SELECT * FROM customers
        WHERE city='Delhi';
        """

    elif "mumbai" in question.lower():

        sql = """
        SELECT * FROM customers
        WHERE city='Mumbai';
        """

    elif "total revenue" in question.lower():

        sql = """
        SELECT SUM(amount) AS total_revenue
        FROM orders;
        """

    elif "highest revenue city" in question.lower():

        sql = """
        SELECT customers.city,
               SUM(orders.amount) AS revenue
        FROM customers
        JOIN orders
        ON customers.id = orders.customer_id
        GROUP BY customers.city
        ORDER BY revenue DESC;
        """

    elif "best selling products" in question.lower():

        sql = """
        SELECT products.product_name,
               SUM(orders.amount) AS total_sales
        FROM products
        JOIN orders
        ON products.product_id = orders.product_id
        GROUP BY products.product_name
        ORDER BY total_sales DESC;
        """

    elif "average order value" in question.lower():

        sql = """
        SELECT AVG(amount) AS average_order_value
        FROM orders;
        """

    elif "total orders" in question.lower():

        sql = """
        SELECT COUNT(*) AS total_orders
        FROM orders;
        """

    else:

        sql = "SELECT * FROM customers;"





    # Show SQL
    st.subheader("Generated SQL:")
    st.code(sql, language="sql")

# Connect database
    conn = sqlite3.connect("company.db")
    
    # Execute query
    df = pd.read_sql_query(sql, conn)
    st.divider()
    
    # Show Results
    st.subheader("Query Results:")
    st.dataframe(df)
    st.success("Query executed successfully ✅")
  

# Dynamic Charts
if "total_spent" in df.columns:

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["name"], df["total_spent"])
    ax.set_title("Top Customers")
    ax.set_xlabel("Customers")
    ax.set_ylabel("Amount")

    st.pyplot(fig)

elif "revenue" in df.columns:

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["city"], df["revenue"])
    ax.set_title("Revenue By City")
    ax.set_xlabel("City")
    ax.set_ylabel("Revenue")

    st.pyplot(fig)

elif "total_sales" in df.columns:

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["product_name"], df["total_sales"])
    ax.set_title("Best Selling Products")
    ax.set_xlabel("Products")
    ax.set_ylabel("Sales")

    st.pyplot(fig)


# KPI Cards
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value="₹3,33,000"
    )

with col2:
    st.metric(
        label="📦 Total Orders",
        value="12"
    )

with col3:
    st.metric(
        label="🛒 Products",
        value="8"
    )
# Footer
st.write("---")
st.caption("Built with Python, Streamlit, SQLite, Pandas, and Matplotlib")
