import gradio as gr
from accounts import Account

# Create a global account instance for the sake of simplicity
account = Account()

def create_account(initial_deposit: float):
    global account
    account = Account(initial_deposit)
    return f"Account created with an initial deposit of ${initial_deposit}"

def deposit_funds(amount: float):
    account.deposit(amount)
    return f"Deposited ${amount}. Current Balance: ${account.balance}"

def withdraw_funds(amount: float):
    if account.withdraw(amount):
        return f"Withdrew ${amount}. Current Balance: ${account.balance}"
    else:
        return f"Insufficient balance for withdrawal of ${amount}. Current Balance: ${account.balance}"

def buy_shares(symbol: str, quantity: int):
    if account.buy_shares(symbol, quantity):
        return f"Bought {quantity} shares of {symbol}. Current Balance: ${account.balance}"
    else:
        return "Failed to buy shares. Check balance or symbol."

def sell_shares(symbol: str, quantity: int):
    if account.sell_shares(symbol, quantity):
        return f"Sold {quantity} shares of {symbol}. Current Balance: ${account.balance}"
    else:
        return "Failed to sell shares. Check holdings or symbol."

def get_portfolio_value():
    return f"Total Portfolio Value: ${account.get_portfolio_value()}"

def get_profit_or_loss():
    profit_or_loss = account.get_profit_or_loss()
    return f"Profit/Loss from initial deposit: ${profit_or_loss}"

def get_holdings():
    return f"Current Holdings: {account.get_holdings()}"

def list_transactions():
    return f"Transactions: {account.list_transactions()}"

with gr.Blocks() as demo:
    gr.Markdown("# Account Management System")

    with gr.Tab("Create Account"):
        initial_deposit_input = gr.Number(label="Initial Deposit", value=0.0)
        create_account_btn = gr.Button("Create Account")
        create_account_output = gr.Textbox(label="Output")
        create_account_btn.click(create_account, initial_deposit_input, create_account_output)

    with gr.Tab("Deposit"):
        deposit_input = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Output")
        deposit_btn.click(deposit_funds, deposit_input, deposit_output)

    with gr.Tab("Withdraw"):
        withdraw_input = gr.Number(label="Withdrawal Amount")
        withdraw_btn = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Output")
        withdraw_btn.click(withdraw_funds, withdraw_input, withdraw_output)

    with gr.Tab("Buy Shares"):
        symbol_input_buy = gr.Textbox(label="Symbol")
        quantity_input_buy = gr.Number(label="Quantity")
        buy_btn = gr.Button("Buy")
        buy_output = gr.Textbox(label="Output")
        buy_btn.click(buy_shares, [symbol_input_buy, quantity_input_buy], buy_output)

    with gr.Tab("Sell Shares"):
        symbol_input_sell = gr.Textbox(label="Symbol")
        quantity_input_sell = gr.Number(label="Quantity")
        sell_btn = gr.Button("Sell")
        sell_output = gr.Textbox(label="Output")
        sell_btn.click(sell_shares, [symbol_input_sell, quantity_input_sell], sell_output)

    with gr.Tab("Reports"):
        portfolio_value_btn = gr.Button("Get Portfolio Value")
        portfolio_value_output = gr.Textbox(label="Portfolio Value")
        portfolio_value_btn.click(get_portfolio_value, None, portfolio_value_output)

        profit_loss_btn = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss")
        profit_loss_btn.click(get_profit_or_loss, None, profit_loss_output)

        holdings_btn = gr.Button("Get Holdings")
        holdings_output = gr.Textbox(label="Holdings")
        holdings_btn.click(get_holdings, None, holdings_output)

        transactions_btn = gr.Button("List Transactions")
        transactions_output = gr.Textbox(label="Transactions")
        transactions_btn.click(list_transactions, None, transactions_output)

demo.launch()