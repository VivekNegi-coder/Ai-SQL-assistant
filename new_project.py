import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt



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
    
    # Dynamic Charts
    if "total_spent" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(df["name"], df["total_spent"])
        ax.set_title("Top Customers")
        st.pyplot(fig)
    elif "revenue" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(df["city"], df["revenue"])
        ax.set_title("Revenue By City")
        st.pyplot(fig)
    elif "total_sales" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(df["product_name"], df["total_sales"])
        ax.set_title("Best Selling Products")
        st.pyplot(fig)
    conn.close()



# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <h5>Total Revenue</h5>
        <h3>₹3,33,000</h3>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <h5>Total Orders</h5>
        <h3>12</h3>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <h5>Products</h5>
        <h3>8</h3>
        """,
        unsafe_allow_html=True
    )
# Footer
st.write("---")
st.caption("Built with Python, Streamlit, SQLite, Pandas, and Matplotlib")