import streamlit as st
import pandas as pd
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F3F7FC, #E5EDF7);
}

/* Selectbox styling */
div[data-baseweb="select"] > div {
    border: 1px solid #BFC9D9 !important;
    border-radius: 8px !important;
}

/* Remove red focus border */
div[data-baseweb="select"] > div:focus-within {
    border-color: #142D4E !important;
    box-shadow: 0 0 0 1px #142D4E !important;
}

h1 {
    color: #142D4E !important;
    font-family: Arial, sans-serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: center;'>Amazon End of Season Sales Analysis Dashboard</h1>",
    unsafe_allow_html=True
)
df = pd.read_csv("C:/Users/Asus/PythonProjects/Book 6(Amazon EndOf Season Sale).csv")
df = df[df["OrderID"] != "SUM OF SALES"]
col1, col2 = st.columns(2)


with col1:
    selected_state = st.selectbox(
   "Select State",
    ["All"] + sorted(df["State"].unique().tolist())
)

with col2:
    selected_category = st.selectbox(
      "Select Category",
      ["All"] + sorted(df["Category"].unique().tolist())
)

if selected_state != "All":
    df = df[df["State"] == selected_state]
if selected_category != "All":
     df = df[df["Category"] == selected_category]

df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")

st.write(df)
total_sales = df["Sales_INR"].str.replace(",", "", regex=False).astype(int).sum()


col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,}")
col2.metric("Total Orders", len(df))
col3.metric("Delivered Orders", (df["Status"] == "Delivered").sum())
col4.metric("Returned Orders", (df["Status"] == "Returned").sum())
status_sales = df.groupby("Status")["Sales_INR"].apply(
    lambda x: x.str.replace(",", "", regex=False).astype(int).sum()
)

st.subheader("Sales by Order Status")
st.bar_chart(status_sales)
state_sales = df.groupby("State")["Sales_INR"].apply(
    lambda x: x.str.replace(",", "", regex=False).astype(int).sum()
)

st.subheader("Sales by State")
st.bar_chart(state_sales)
category_sales = df.groupby("Category")["Sales_INR"].apply(
    lambda x: x.str.replace(",", "", regex=False).astype(int).sum()
)

st.subheader("Sales by Category")
st.bar_chart(category_sales)
payment_sales = df.groupby("PaymentMethod")["Sales_INR"].apply(
    lambda x: x.str.replace(",", "", regex=False).astype(int).sum()
)

st.subheader("Sales by Payment Method")
st.bar_chart(payment_sales)
daily_sales = df.groupby("Date")["Sales_INR"].apply(
    lambda x: x.str.replace(",", "", regex=False).astype(int).sum()
)

st.subheader("Sales over Time")
st.line_chart(daily_sales)


st.divider()
st.header("💡 Key Insights")

if not df.empty:
    # Find the leading category, state and payment method
    category_sales = df.groupby("Category")["Sales_INR"].apply(
        lambda x: x.astype(str).str.replace(",", "", regex=False).astype(int).sum()
    )
    state_sales = df.groupby("State")["Sales_INR"].apply(
        lambda x: x.astype(str).str.replace(",", "", regex=False).astype(int).sum()
    )
    payment_sales = df.groupby("PaymentMethod")["Sales_INR"].apply(
        lambda x: x.astype(str).str.replace(",", "", regex=False).astype(int).sum()
    )

    top_category = category_sales.idxmax()
    top_state = state_sales.idxmax()
    top_payment = payment_sales.idxmax()

    st.write(
        f"**Top sales category:** {top_category} "
        f"(₹{category_sales.max():,.0f})."
    )
    st.write(
        f"**Top sales state:** {top_state} "
        f"(₹{state_sales.max():,.0f})."
    )
    st.write(
        f"**Top payment method by sales:** {top_payment} "
        f"(₹{payment_sales.max():,.0f})."
    )

    st.caption(
        "These insights update based on the selected state and category filters."
    )
else:
    st.info("No data is available for the selected filters.")


st.divider()
st.header("✅ Conclusion & Learning")

st.write(
    "This project explores Amazon End of Season Sale data using Python "
    "and Pandas. It demonstrates data cleaning, filtering, KPI calculations, "
    "grouping, and interactive visualisation with Streamlit."
)

st.write(
    "The analysis helps compare sales across product categories, states, "
    "payment methods, and order statuses. The findings apply only to this "
    "practice dataset and should not be treated as official Amazon business results."
)

st.subheader("Skills Practised")
st.markdown("""
- Python and Pandas
- Data cleaning and type conversion
- Exploratory data analysis
- KPI calculations and data grouping
- Interactive dashboard development with Streamlit
""")

