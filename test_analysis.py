"""
Test script for utils/analysis.py module
Tests calculate_hhi and calculate_lerner_index functions
"""

import sys
sys.path.insert(0, '.')

from utils.analysis import calculate_hhi, calculate_lerner_index
import pandas as pd
import numpy as np

print("="*60)
print("Testing utils/analysis.py Module")
print("="*60)

# Test 1: calculate_hhi with list
print("\n--- Test 1: calculate_hhi with list ---")
market_shares_list = [0.3, 0.3, 0.2, 0.2]
hhi_result = calculate_hhi(market_shares_list)
print(f"Market Shares: {market_shares_list}")
print(f"HHI Result: {hhi_result:.2f}")
print(f"Interpretation: ", end="")
if hhi_result < 1500:
    print("Competitive market")
elif hhi_result < 2500:
    print("Moderately concentrated")
else:
    print("Highly concentrated")

# Test 2: calculate_hhi with pandas Series
print("\n--- Test 2: calculate_hhi with pandas Series ---")
market_shares_series = pd.Series([0.5, 0.3, 0.2])
hhi_result2 = calculate_hhi(market_shares_series)
print(f"Market Shares: {list(market_shares_series)}")
print(f"HHI Result: {hhi_result2:.2f}")
print(f"Interpretation: ", end="")
if hhi_result2 < 1500:
    print("Competitive market")
elif hhi_result2 < 2500:
    print("Moderately concentrated")
else:
    print("Highly concentrated")

# Test 3: calculate_hhi with numpy array
print("\n--- Test 3: calculate_hhi with numpy array ---")
market_shares_array = np.array([0.6, 0.25, 0.15])
hhi_result3 = calculate_hhi(market_shares_array)
print(f"Market Shares: {list(market_shares_array)}")
print(f"HHI Result: {hhi_result3:.2f}")
print(f"Interpretation: ", end="")
if hhi_result3 < 1500:
    print("Competitive market")
elif hhi_result3 < 2500:
    print("Moderately concentrated")
else:
    print("Highly concentrated")

# Test 4: calculate_lerner_index with lists
print("\n--- Test 4: calculate_lerner_index with lists ---")
prices_list = [10.0, 15.0, 20.0]
costs_list = [6.0, 9.0, 12.0]
lerner_result = calculate_lerner_index(prices_list, costs_list)
print(f"Prices: {prices_list}")
print(f"Marginal Costs: {costs_list}")
print(f"Average Lerner Index: {lerner_result:.4f}")

# Test 5: calculate_lerner_index with pandas Series
print("\n--- Test 5: calculate_lerner_index with pandas Series ---")
prices_series = pd.Series([10.0, 15.0, 20.0])
costs_series = pd.Series([6.0, 9.0, 12.0])
lerner_result2 = calculate_lerner_index(prices_series, costs_series)
print(f"Prices: {list(prices_series)}")
print(f"Marginal Costs: {list(costs_series)}")
print(f"Average Lerner Index: {lerner_result2:.4f}")

# Test 6: calculate_lerner_index with numpy arrays
print("\n--- Test 6: calculate_lerner_index with numpy arrays ---")
prices_array = np.array([10.0, 15.0, 20.0])
costs_array = np.array([6.0, 9.0, 12.0])
lerner_result3 = calculate_lerner_index(prices_array, costs_array)
print(f"Prices: {list(prices_array)}")
print(f"Marginal Costs: {list(costs_array)}")
print(f"Average Lerner Index: {lerner_result3:.4f}")

# Test 7: Real-world scenario
print("\n--- Test 7: Real-world market scenario ---")
# Simulating a competitive market with 5 firms
market_shares_realistic = pd.Series([0.25, 0.22, 0.21, 0.18, 0.14])
prices_realistic = pd.Series([100.0, 105.0, 98.0, 102.0, 100.0])
costs_realistic = pd.Series([70.0, 72.0, 68.0, 75.0, 71.0])

hhi_realistic = calculate_hhi(market_shares_realistic)
lerner_realistic = calculate_lerner_index(prices_realistic, costs_realistic)

print(f"HHI: {hhi_realistic:.2f}")
print(f"Average Lerner Index: {lerner_realistic:.4f}")

print("\n" + "="*60)
print("All tests completed successfully!")
print("="*60)
