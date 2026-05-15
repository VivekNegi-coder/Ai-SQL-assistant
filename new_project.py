import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time

# Page Config
st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🧠",
    layout="wide"
)

# Sidebar
with st.sidebar:

    st.title("🧠 AI SQL Assistant")

    st.write("### Features")
    st.write("✔ Natural Language Queries")
    st.write("✔ SQL Generation")
    st.write("✔ Data Analytics")
    st.write("✔ Interactive Charts")

    st.write("---")

    st.write("### Built With")
    st.write("🐍 Python")
    st.write("⚡ Streamlit")
    st.write("🗄 SQLite")
    st.write("📊 Pandas")
    st.write("📈 Matplotlib")

# Custom CSS
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.stApp {
    background-color: #0E1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #161B22, #1F2937);
    border: 1px solid #2D3748;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
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

# Title
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

st.info("🚀 Convert natural language into SQL queries and analytics instantly.")

st.caption(
    "Suggested queries: top customers • total revenue • highest revenue city • best selling products"
)

# Quick Questions
st.write("### Quick Questions")

c1, c2, c3, c4, c5 = st.columns([1,2,2,2,1])

with c2:
    if st.button("Top Customers"):
        st.session_state.question = "top customers"

with c3:
    if st.button("Total Revenue"):
        st.session_state.question = "total revenue"

with c4:
    if st.button("Best Selling Products"):
        st.session_state.question = "best selling products"

# Input Box
question = st.text_input(
    "Ask your database question:",
    placeholder="Try: top customers",
    key="question"
)

# Generate Button
run_query = st.button("Generate SQL")

# Run Query
if question and run_query:

    # SQL Logic
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
    st.subheader("🧾 Generated SQL")
    st.code(sql, language="sql")

    # Connect Database
    conn = sqlite3.connect("company.db")

    # Query Timer
    start = time.time()

    # Execute Query
    df = pd.read_sql_query(sql, conn)

    end = time.time()

    st.divider()

    # Show Results
    st.subheader("📊 Query Results")
    st.dataframe(df)

    st.success("Query executed successfully ✅")

    st.caption(f"⚡ Query executed in {round(end-start, 2)} seconds")

    # Dynamic Charts
    if "total_spent" in df.columns:

        fig, ax = plt.subplots(figsize=(8,4))

        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#161B22')

        ax.bar(df["name"], df["total_spent"])

        ax.set_title("Top Customers", color='white')
        ax.set_xlabel("Customers", color='white')
        ax.set_ylabel("Amount", color='white')

        ax.tick_params(colors='white')

        st.pyplot(fig)

    elif "revenue" in df.columns:

        fig, ax = plt.subplots(figsize=(8,4))

        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#161B22')

        ax.bar(df["city"], df["revenue"])

        ax.set_title("Revenue By City", color='white')
        ax.set_xlabel("City", color='white')
        ax.set_ylabel("Revenue", color='white')

        ax.tick_params(colors='white')

        st.pyplot(fig)

    elif "total_sales" in df.columns:

        fig, ax = plt.subplots(figsize=(8,4))

        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#161B22')

        ax.bar(df["product_name"], df["total_sales"])

        ax.set_title("Best Selling Products", color='white')
        ax.set_xlabel("Products", color='white')
        ax.set_ylabel("Sales", color='white')

        ax.tick_params(colors='white')

        st.pyplot(fig)

    conn.close()

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
