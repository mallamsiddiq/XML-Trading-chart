import random
# from django.contrib.auth import get_user_model

# User = get_user_model()

def simulate_trader_data(num_traders, num_intervals):
    trader_data = []
    
    for trader_id in range(1, num_traders + 1):
        trader_name = f"Trader {trader_id}"
        trader_profit_loss = []
        
        for interval in range(num_intervals):
            # Simulate a random profit or loss value between -10 and 10.
            profit_loss = random.uniform(-10, 10)
            
            # Calculate the cumulative profit or loss.
            if interval == 0:
                cumulative_profit_loss = profit_loss
            else:
                cumulative_profit_loss += profit_loss
            
            # Create a data point with timestamp and profit/loss.
            data_point = {
                'timestamp': interval,  # You can use a timestamp format here if needed.
                'profit_loss': cumulative_profit_loss
            }
            
            trader_profit_loss.append(data_point)
        
        trader_data.append({'name': trader_name, 'data': trader_profit_loss})
    
    return trader_data

# Example usage:
num_traders = 10
num_intervals = 60  # Simulate data for 60 intervals (1 minute intervals).
simulated_data = simulate_trader_data(num_traders, num_intervals)

print(simulated_data[2])
