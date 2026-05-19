"""
Market power analysis utilities.

This module provides functions to calculate key market concentration and
market power metrics for economic analysis.
"""

import pandas as pd
import numpy as np
from typing import Union


def calculate_hhi(market_shares: Union[pd.Series, np.ndarray, list]) -> float:
    """
    Calculate the Herfindahl-Hirschman Index (HHI).

    The HHI measures market concentration by summing the squared market shares.
    It ranges from 0 to 10,000 and is interpreted as follows:
        - HHI < 1500: Competitive market
        - 1500 <= HHI < 2500: Moderately concentrated
        - HHI >= 2500: Highly concentrated

    Args:
        market_shares: Market shares as fractions (must sum to 1.0).
            Can be a pandas Series, numpy array, or list.

    Returns:
        float: HHI value scaled to 0-10,000 range.

    Raises:
        ValueError: If market shares do not sum to approximately 1.0.
        TypeError: If market_shares is not a supported type.

    Example:
        >>> shares = pd.Series([0.3, 0.3, 0.2, 0.2])
        >>> hhi = calculate_hhi(shares)
        >>> print(f"HHI: {hhi:.2f}")
        HHI: 2600.00
    """
    # Convert to numpy array for uniform handling
    if isinstance(market_shares, pd.Series):
        shares_array = market_shares.values
    elif isinstance(market_shares, (list, np.ndarray)):
        shares_array = np.asarray(market_shares)
    else:
        raise TypeError(
            f"market_shares must be a pandas Series, numpy array, or list, "
            f"got {type(market_shares)}"
        )

    # Validate that shares sum to 1.0
    share_sum = shares_array.sum()
    if not np.isclose(share_sum, 1.0, atol=1e-6):
        raise ValueError(
            f"Market shares must sum to 1.0, but sum to {share_sum:.6f}"
        )

    # Calculate HHI: sum of squared shares (as fractions) * 10,000
    hhi = (shares_array ** 2).sum() * 10_000

    return float(hhi)


def calculate_lerner_index(
    price: Union[pd.Series, np.ndarray, list],
    marginal_cost: Union[pd.Series, np.ndarray, list],
) -> float:
    """
    Calculate the average Lerner Index across firms.

    The Lerner Index measures the degree of market power for individual firms.
    It is calculated as (Price - Marginal Cost) / Price and ranges from 0 to 1.
    A value of 0 indicates perfect competition, while higher values indicate
    greater market power.

    The average Lerner Index represents the average level of market power
    across all firms in the market.

    Args:
        price: Price for each firm. Can be a pandas Series, numpy array, or list.
        marginal_cost: Marginal cost for each firm. Can be a pandas Series,
            numpy array, or list.

    Returns:
        float: Average Lerner Index (value between 0 and 1).

    Raises:
        ValueError: If price and marginal_cost have different lengths.
        ValueError: If any price is <= 0.
        TypeError: If inputs are not supported types.

    Example:
        >>> prices = pd.Series([10.0, 15.0, 20.0])
        >>> costs = pd.Series([6.0, 9.0, 12.0])
        >>> lerner = calculate_lerner_index(prices, costs)
        >>> print(f"Average Lerner Index: {lerner:.4f}")
        Average Lerner Index: 0.4000
    """
    # Convert to numpy arrays for uniform handling
    if isinstance(price, pd.Series):
        price_array = price.values
    elif isinstance(price, (list, np.ndarray)):
        price_array = np.asarray(price)
    else:
        raise TypeError(
            f"price must be a pandas Series, numpy array, or list, "
            f"got {type(price)}"
        )

    if isinstance(marginal_cost, pd.Series):
        mc_array = marginal_cost.values
    elif isinstance(marginal_cost, (list, np.ndarray)):
        mc_array = np.asarray(marginal_cost)
    else:
        raise TypeError(
            f"marginal_cost must be a pandas Series, numpy array, or list, "
            f"got {type(marginal_cost)}"
        )

    # Validate that arrays have the same length
    if len(price_array) != len(mc_array):
        raise ValueError(
            f"price and marginal_cost must have the same length, "
            f"got {len(price_array)} and {len(mc_array)}"
        )

    # Validate that all prices are positive
    if (price_array <= 0).any():
        raise ValueError("All prices must be positive")

    # Calculate Lerner Index for each firm
    lerner_indices = (price_array - mc_array) / price_array

    # Return average Lerner Index
    average_lerner = float(lerner_indices.mean())

    return average_lerner
