# /// script
# requires-python = ">=3.12"
# dependencies = ["click"]
# ///

import random
import csv
import click

# Initialize variables
year = 34
income = 254
tax_rate = 1 / 16
col_rate = 1 / 10
net = 0
savings = 254
roll_count = 0  # Counter for the number of rolls


# Function to generate random numbers based on the number of dice and calculate the sum
def calculate_income_and_expenses(year):
    global savings, roll_count
    dice_count = 2 + (roll_count // 5 // 2)  # Start with 2 dice, add one more every 15 rolls
    income = sum(random.randint(1, 8) for _ in range(dice_count))  # Sum of random numbers from the dice
    tax = round(tax_rate * income, ndigits=2)
    col = round(col_rate * income, ndigits=2)
    net = income - tax - col
    savings = net + savings
    roll_count += 1  # Increment roll count after each calculation
    return year, income, tax, col, net, savings


@click.command()
@click.option('--output', default='accounting.csv', help='Output CSV file name.')
@click.option('--start_year', default=34, help='Starting year.')
@click.option('--starting_savings', default=254, help='Initial savings amount.')
@click.option('--starting_income', default=254, help='Starting income amount.')
@click.option('--starting_tax_rate', default=1/16, type=float, help='Starting tax rate.')
@click.option('--starting_col_rate', default=1/10, type=float, help='Starting cost of living rate.')
@click.option('--max_years', default=100, help='Number of years to simulate.')
def generate_accounting_report(output, start_year, starting_savings, starting_income, starting_tax_rate, starting_col_rate, max_years):
    """
    Generate a CSV report of income, tax, cost of living, net income, and savings over time.
    """
    global year, income, tax_rate, col_rate, savings
    year = start_year
    income = starting_income
    tax_rate = starting_tax_rate
    col_rate = starting_col_rate
    savings = starting_savings

    # Open the CSV file and write the header
    with open(output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Year", "Income", "Tax", "Cost of Living", "Net Income", "Savings"])

        # Calculate and write the data for each year
        for _ in range(max_years):
            year, income, tax, col, net, savings = calculate_income_and_expenses(year)
            writer.writerow([year, income, tax, col, net, savings])
            year += 1


if __name__ == '__main__':
    generate_accounting_report()
