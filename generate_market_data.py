"""
Generate synthetic market data for market power analysis.

This module provides functions to create synthetic market datasets and calculate
market concentration metrics including the Herfindahl-Hirschman Index (HHI) and
the Lerner Index.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def generate_synthetic_market_data(n_companies: int = 10, seed: int = 42) -> pd.DataFrame:
    """
    Generate a synthetic DataFrame simulating a market with multiple companies.

    Args:
        n_companies: Number of companies to generate. Defaults to 10.
        seed: Random seed for reproducibility. Defaults to 42.

    Returns:
        A pandas DataFrame with columns:
        - company_name: Name of the company
        - market_share: Market share as a fraction (sums to 1.0)
        - price: Unit price for the product
        - marginal_cost: Marginal cost of production

    Raises:
        ValueError: If n_companies is less than 1.
    """
    if n_companies < 1:
        raise ValueError("n_companies must be at least 1")

    np.random.seed(seed)

    # Generate company names
    company_names = [f"Company_{chr(65 + i)}" for i in range(n_companies)]

    # Generate market shares using Dirichlet distribution
    # This ensures shares sum to 1.0 and have realistic variation
    market_shares_raw = np.random.dirichlet(np.ones(n_companies))
    market_shares = market_shares_raw / market_shares_raw.sum()  # Normalize to ensure sum = 1.0

    # Generate prices: uniformly distributed between 10 and 50
    prices = np.random.uniform(10, 50, n_companies)

    # Generate marginal costs: uniformly distributed between 5 and 40,
    # ensuring they're less than prices for economic realism
    marginal_costs = np.random.uniform(5, 40, n_companies)
    marginal_costs = np.minimum(marginal_costs, prices * 0.95)  # Ensure MC < Price

    # Create DataFrame
    data = {
        "company_name": company_names,
        "market_share": market_shares,
        "price": prices,
        "marginal_cost": marginal_costs,
    }

    df = pd.DataFrame(data)

    return df


def calculate_hhi(market_shares: pd.Series) -> float:
    """
    Calculate the Herfindahl-Hirschman Index (HHI).

    HHI measures market concentration. It is calculated as the sum of squared
    market shares (expressed as percentages, scaled by 10,000).
    - HHI < 1500: Competitive market
    - 1500 <= HHI < 2500: Moderate concentration
    - HHI >= 2500: Highly concentrated

    Args:
        market_shares: A pandas Series containing market shares as fractions.

    Returns:
        HHI value (scaled to 0-10,000 range).

    Raises:
        ValueError: If market shares do not sum to approximately 1.0.
    """
    if not np.isclose(market_shares.sum(), 1.0, atol=1e-6):
        raise ValueError(
            f"Market shares must sum to 1.0, but sum to {market_shares.sum()}"
        )

    # HHI is calculated as sum of squared market shares (as percentages) * 100
    # Which is equivalent to (sum of squared shares as fractions) * 10,000
    hhi = (market_shares ** 2).sum() * 10_000

    return hhi


def calculate_average_lerner_index(
    prices: pd.Series, marginal_costs: pd.Series
) -> float:
    """
    Calculate the average Lerner Index across all firms.

    The Lerner Index measures market power for individual firms:
    L_i = (P_i - MC_i) / P_i

    The average Lerner Index is the mean across all firms, representing
    the average level of market power in the market.

    Args:
        prices: A pandas Series containing prices for each firm.
        marginal_costs: A pandas Series containing marginal costs for each firm.

    Returns:
        Average Lerner Index (value between 0 and 1).

    Raises:
        ValueError: If any price is <= 0.
        ValueError: If Series lengths don't match.
    """
    if len(prices) != len(marginal_costs):
        raise ValueError("prices and marginal_costs must have the same length")

    if (prices <= 0).any():
        raise ValueError("All prices must be positive")

    lerner_indices = (prices - marginal_costs) / prices
    average_lerner = lerner_indices.mean()

    return average_lerner


def analyze_market(df: pd.DataFrame) -> None:
    """
    Analyze and print market concentration metrics from a market dataset.

    Args:
        df: DataFrame containing market data with columns:
            'market_share', 'price', 'marginal_cost'
    """
    # Verify required columns
    required_columns = {"market_share", "price", "marginal_cost"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")

    # Calculate metrics
    hhi = calculate_hhi(df["market_share"])
    avg_lerner = calculate_average_lerner_index(df["price"], df["marginal_cost"])

    # Display results
    print("Market Analysis Results")
    print("=" * 50)
    print(f"\nMarket Data Summary:")
    print(f"  Number of firms: {len(df)}")
    print(f"  Total market share: {df['market_share'].sum():.6f}")
    print(f"\nMarket Concentration:")
    print(f"  HHI: {hhi:.2f}")
    if hhi < 1500:
        concentration_level = "Competitive"
    elif hhi < 2500:
        concentration_level = "Moderately Concentrated"
    else:
        concentration_level = "Highly Concentrated"
    print(f"  Concentration Level: {concentration_level}")
    print(f"\nMarket Power:")
    print(f"  Average Lerner Index: {avg_lerner:.4f}")
    print(f"\n" + "=" * 50)
    print("\nDetailed Firm Data:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    # Generate synthetic market data
    market_data = generate_synthetic_market_data(n_companies=10, seed=42)

    # Analyze the market
    analyze_market(market_data)

    # Save to CSV for later use
    market_data.to_csv("synthetic_market_data.csv", index=False)
    print("\nData saved to: synthetic_market_data.csv")
