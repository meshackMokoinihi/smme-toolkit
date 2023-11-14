import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import numpy_financial as npf
from flask import Flask, render_template, request
# import request



app = Flask(__name__)



returns = ''
plot=''
total=''


# @app.route('/upload', methods=['POST'])

@app.route('/')
def index():

    global plot, total
    # Load Bank Statement 1
    df1 = pd.read_csv('bank_statement_1.csv', parse_dates=['Date'])

    # Load Bank Statement 2
    df2 = pd.read_csv('bank_statement_2.csv', parse_dates=['Date'])

    df3 = pd.read_csv('bank_statement_3.csv', parse_dates=['Date'])


    # Combine both statements
    combined_df = pd.concat([df1, df2, df3])

    # Create subplots within a single figure
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))

    # Plot all transactions over time as a pie chart
    axs[0, 0].pie(combined_df.groupby('Date')['Amount'].sum(), labels=combined_df.groupby('Date').sum().index, autopct='%1.1f%%', colors=['blue', 'green'])
    axs[0, 0].set_title('Bank Transactions Over Time')
    axs[0, 0].legend(labels=['Deposit', 'Withdrawal'], loc="upper right")

    # Extract features (for simplicity, we're using only one feature: Amount)
    features = combined_df[['Amount']]

    # Train KMeans model
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(features)

    # Add a new column to the DataFrame indicating the cluster
    combined_df['Cluster'] = kmeans.labels_

    # Plot spending by cluster as a pie chart with meaningful labels
    axs[0, 1].pie(combined_df.groupby('Cluster')['Amount'].sum(), labels=['Essential Expenses', 'Balanced Spending', 'Non-Essential Items'], autopct='%1.1f%%', colors=['purple', 'orange', 'green'])
    axs[0, 1].set_title('Spending by Cluster')

    # Provide advice based on cluster analysis
    most_spent_cluster = combined_df.groupby('Cluster')['Amount'].sum().idxmax()
    if most_spent_cluster == 0:
        advice = "You tend to spend a lot on essential expenses. Consider optimizing your budget or finding ways to save on necessities."
    elif most_spent_cluster == 1:
        advice = "Your spending is well-distributed across various categories. Keep up the good work in maintaining a balanced budget."
    else:
        advice = "A significant portion of your spending is on non-essential items. Consider identifying areas where you can cut back to save more."

    # axs[0, 1].text(0.5, 0.5, advice, horizontalalignment='center', verticalalignment='bottom', transform=axs[0, 1].transAxes)

    # Identify the month with the highest spending
    combined_df['Month'] = combined_df['Date'].dt.month
    monthly_spending = combined_df.groupby('Month')['Amount'].sum()

    # Reindex to include all months (1 to 12)
    monthly_spending = monthly_spending.reindex(range(1, 13), fill_value=0)

    # Plot monthly spending as a bar chart with meaningful labels
    axs[1, 0].bar(monthly_spending.index, monthly_spending, color=['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'black', 'red'])
    axs[1, 0].set_title('Monthly Spending')
    axs[1, 0].set_xlabel('Month')
    axs[1, 0].set_ylabel('Total Spending')
    axs[1, 0].set_xticks(monthly_spending.index)
    axs[1, 0].set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], rotation=45)

    # Add a fourth chart: Histogram of Transaction Amounts
    axs[1, 1].hist(combined_df['Amount'], bins=20, color='skyblue', edgecolor='black')
    axs[1, 1].set_title('Distribution of Transaction Amounts')
    axs[1, 1].set_xlabel('Transaction Amount')
    axs[1, 1].set_ylabel('Frequency')

    # Adjust layout for better spacing
    plt.tight_layout()

    # Display all charts on the same window
    # plt.show()

    # Identify the month with the highest spending
    highest_spending_month = monthly_spending.idxmax()
    # print(f"The month with the highest spending is: {highest_spending_month}")

    plot_path = 'static/plot.png'  # Assuming 'static' is the folder to store static files
    plt.savefig(plot_path)
    plt.close()
    plot=plot_path

    monthly_spending = combined_df.groupby('Month')['Amount'].sum()

    # Reindex to include all months (1 to 12)
    monthly_spending = monthly_spending.reindex(range(1, 13), fill_value=0)

    # Total spending per month information
    total = monthly_spending.reset_index(name='Total Spending')


    # Render the HTML template with the image path
    return render_template('index.html',plot_path=plot_path )


@app.route("/businessanalysis.html", methods=["POST", "GET"])
def analyze():
    global plot, total
    plot=plot
    total =total
    return render_template("businessanalysis.html", plot=plot, total=total)


@app.route("/education.html", methods=["POST", "GET"])
def education():
    return render_template("education.html")


@app.route("/calculator.html", methods=["POST", "GET"])
def calculator():
    return render_template("calculator.html")



@app.route("/funding.html", methods=["POST", "GET"])
def funding():
    return render_template("funding.html")




@app.route("/form.html", methods=["POST", "GET"])
def form():
    returns = None

    if request.method == "POST":
        try:
            # Retrieve form data
            amount = float(request.form["amount"])
            rate = float(request.form["rate"]) / 100  # Assuming rate is in percentage
            period = float(request.form["period"])
            
            # Validate input values
            if amount <= 0 or rate <= 0 or period <= 0:
                raise ValueError("Please enter positive values for amount, rate, and period.")
            
            # Calculate returns
            returns = investment_calculator(amount, rate, period)
            
        except ValueError as e:
            returns = f"Error: {str(e)}"

    return render_template("form.html", returns=returns)

def investment_calculator(principal, rate, periods):
    # Calculate future value using numpy_financial.fv
    future_value = npf.fv(rate, periods, 0, -principal)
    
    return future_value

if __name__ == '__main__':
    app.run(debug=False)