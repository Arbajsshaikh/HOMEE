import streamlit as st
import pandas as pd

# Function to create or load the data frame
@st.cache
def load_data():
    return pd.DataFrame(columns=['Expense Type', 'Amount'])

# Function to update and display the data frame
def update_data(data):
    st.write("## Construction Site Tracker")
    st.table(data)

# Function to add new expenses to the data frame
def add_expense(data, expense_type, amount):
    data = data.append({'Expense Type': expense_type, 'Amount': amount}, ignore_index=True)
    return data

# Main Streamlit app
def main():
    st.title("Construction Site Tracker")

    # Load existing data or create a new data frame
    data = load_data()

    # Sidebar for adding new expenses
    st.sidebar.header("Add New Expense")
    expense_type = st.sidebar.text_input("Expense Type")
    amount = st.sidebar.number_input("Amount", min_value=0.0)

    if st.sidebar.button("Add Expense"):
        if expense_type and amount:
            data = add_expense(data, expense_type, amount)

    # Display the updated data frame
    update_data(data)

    # Calculate and display the total expenses
    total_expenses = data['Amount'].sum()
    st.write(f"## Total Expenses: ${total_expenses:.2f}")

# Run the app
if __name__ == "__main__":
    main()
