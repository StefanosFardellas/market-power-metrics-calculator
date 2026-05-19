"""
Market Power Metrics Calculator - Streamlit Application.

This Streamlit app allows users to upload market data and calculate
key economic metrics including the Herfindahl-Hirschman Index (HHI)
and the Lerner Index for market power analysis.
"""

import io
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from typing import Tuple, Optional
from utils.analysis import calculate_hhi, calculate_lerner_index

# Configure Streamlit page settings
st.set_page_config(
    page_title="Market Power Metrics Calculator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("📊 Market Power Metrics Calculator")


def render_sidebar_explanations() -> None:
    """
    Render explanations of HHI and Lerner Index in the sidebar.
    """
    with st.sidebar:
        st.header("📖 Metric Explanations")
        
        with st.expander("HHI (Herfindahl-Hirschman Index)", expanded=True):
            st.markdown(
                """
                **What is HHI?**
                
                The Herfindahl-Hirschman Index measures market concentration by 
                summing the squared market shares of all firms.
                
                **Formula:** HHI = Σ(market_share)²
                
                **Interpretation:**
                - **HHI < 1,500**: Competitive market
                - **1,500 ≤ HHI < 2,500**: Moderately concentrated
                - **HHI ≥ 2,500**: Highly concentrated market
                
                A higher HHI indicates greater market concentration and 
                reduced competition. The index ranges from 0 to 10,000.
                """
            )
        
        with st.expander("Lerner Index", expanded=True):
            st.markdown(
                """
                **What is the Lerner Index?**
                
                The Lerner Index measures the degree of market power for firms.
                It represents how much a firm can mark up its price above 
                marginal cost.
                
                **Formula:** L = (P - MC) / P
                
                where P = Price and MC = Marginal Cost
                
                **Interpretation:**
                - **L = 0**: Perfect competition (price equals marginal cost)
                - **L → 1**: Higher market power (more markup over cost)
                - **Range**: 0 to 1
                
                The average Lerner Index across all firms indicates the 
                average level of market power in the industry.
                """
            )


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
    """
    Validate that the uploaded DataFrame has required columns.
    
    Args:
        df: The uploaded DataFrame to validate.
        
    Returns:
        A tuple of (is_valid: bool, error_message: Optional[str]).
    """
    required_columns = {"market_share", "price", "marginal_cost"}
    
    if not required_columns.issubset(set(df.columns)):
        missing = required_columns - set(df.columns)
        error_msg = (
            f"Missing required columns: {', '.join(sorted(missing))}. "
            f"Your CSV must include: market_share, price, marginal_cost"
        )
        return False, error_msg
    
    # Check for null values
    if df[list(required_columns)].isnull().any().any():
        return False, "Data contains missing values (NaN). Please ensure all values are present."
    
    # Check for non-numeric values
    for col in required_columns:
        try:
            pd.to_numeric(df[col])
        except (ValueError, TypeError):
            return False, f"Column '{col}' contains non-numeric values."
    
    # Check that market shares sum to approximately 1.0
    market_share_sum = df["market_share"].sum()
    if not np.isclose(market_share_sum, 1.0, atol=0.01):
        return (
            False,
            f"Market shares must sum to 1.0 (or very close). "
            f"Current sum: {market_share_sum:.4f}"
        )
    
    # Check that prices and marginal costs are positive
    if (df["price"] <= 0).any():
        return False, "All prices must be positive values."
    
    if (df["marginal_cost"] <= 0).any():
        return False, "All marginal costs must be positive values."
    
    return True, None


def calculate_metrics(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate HHI and average Lerner Index from the DataFrame.
    
    Args:
        df: DataFrame with market_share, price, and marginal_cost columns.
        
    Returns:
        A tuple of (hhi: float, avg_lerner: float).
        
    Raises:
        ValueError: If calculation fails.
    """
    try:
        hhi = calculate_hhi(df["market_share"])
        avg_lerner = calculate_lerner_index(df["price"], df["marginal_cost"])
        return hhi, avg_lerner
    except Exception as e:
        raise ValueError(f"Error calculating metrics: {str(e)}")


def interpret_hhi(hhi: float) -> str:
    """
    Provide textual interpretation of HHI value.
    
    Args:
        hhi: The HHI value to interpret.
        
    Returns:
        A string describing the market concentration level.
    """
    if hhi < 1500:
        return "🟢 **Competitive Market** - Low concentration, healthy competition"
    elif hhi < 2500:
        return "🟡 **Moderately Concentrated** - Medium market concentration"
    else:
        return "🔴 **Highly Concentrated** - High concentration, limited competition"


def create_market_share_chart(df: pd.DataFrame) -> plt.Figure:
    """
    Create a bar chart showing market shares per company.
    
    Args:
        df: DataFrame with company names and market shares.
        
    Returns:
        A matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use company names if available, otherwise use indices
    if "company_name" in df.columns:
        companies = df["company_name"]
    else:
        companies = [f"Firm {i+1}" for i in range(len(df))]
    
    shares = df["market_share"]
    colors = plt.cm.viridis(np.linspace(0, 1, len(shares)))
    
    ax.bar(companies, shares, color=colors, edgecolor="black", linewidth=1.2)
    ax.set_ylabel("Market Share", fontsize=12, fontweight="bold")
    ax.set_xlabel("Companies", fontsize=12, fontweight="bold")
    ax.set_title("Market Share Distribution", fontsize=14, fontweight="bold")
    ax.set_ylim([0, max(shares) * 1.1])
    
    # Add value labels on bars
    for i, (company, share) in enumerate(zip(companies, shares)):
        ax.text(i, share + 0.01, f"{share:.1%}", ha="center", va="bottom", fontweight="bold")
    
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    return fig


def generate_csv_report(
    df: pd.DataFrame,
    hhi: float,
    avg_lerner: float
) -> bytes:
    """
    Generate a CSV report with data and calculated metrics.
    
    Args:
        df: Original DataFrame.
        hhi: Calculated HHI value.
        avg_lerner: Calculated average Lerner Index.
        
    Returns:
        CSV file content as bytes.
    """
    # Create a report DataFrame
    report_df = df.copy()
    
    # Add calculated metrics as a summary section
    summary_data = {
        "Metric": ["Market Concentration Index (HHI)", "Average Lerner Index"],
        "Value": [f"{hhi:.2f}", f"{avg_lerner:.4f}"],
        "Interpretation": [
            interpret_hhi(hhi).replace("**", "").replace("🟢", "").replace("🟡", "").replace("🔴", ""),
            "Market power level (0=perfect competition, 1=monopoly)"
        ]
    }
    
    # Convert to CSV
    buffer = io.StringIO()
    report_df.to_csv(buffer, index=False)
    buffer.write("\n\n")
    buffer.write("SUMMARY METRICS\n")
    pd.DataFrame(summary_data).to_csv(buffer, index=False)
    
    return buffer.getvalue().encode("utf-8")


def main() -> None:
    """
    Main function to run the Streamlit application.
    """
    # Render sidebar explanations
    render_sidebar_explanations()
    
    # Main content area
    st.markdown(
        """
        Welcome to the Market Power Metrics Calculator! 
        Upload your market data CSV file to analyze market concentration and market power metrics.
        """
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📁 Upload CSV File",
        type=["csv"],
        help="CSV must contain: market_share, price, marginal_cost columns"
    )
    
    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Validate the DataFrame
            is_valid, error_message = validate_dataframe(df)
            
            if not is_valid:
                st.error(f"❌ {error_message}")
                st.info("💡 **Required columns:** market_share, price, marginal_cost")
                st.write("**Sample data format:**")
                sample_df = pd.DataFrame({
                    "market_share": [0.3, 0.25, 0.2, 0.15, 0.1],
                    "price": [15.0, 18.0, 12.0, 20.0, 14.0],
                    "marginal_cost": [8.0, 10.0, 7.0, 12.0, 8.5]
                })
                st.dataframe(sample_df)
            else:
                # Show success message
                st.success("✅ File uploaded successfully!")
                
                # Display the uploaded data
                with st.expander("📋 View Uploaded Data", expanded=False):
                    st.dataframe(df, use_container_width=True)
                
                # Calculate metrics
                try:
                    hhi, avg_lerner = calculate_metrics(df)
                    
                    # Display metrics in columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(
                            label="📈 HHI (Market Concentration Index)",
                            value=f"{hhi:.2f}",
                            help="Range: 0-10,000. Higher values indicate more concentration."
                        )
                        st.write(interpret_hhi(hhi))
                    
                    with col2:
                        st.metric(
                            label="💰 Average Lerner Index",
                            value=f"{avg_lerner:.4f}",
                            help="Range: 0-1. Higher values indicate more market power."
                        )
                        lerner_pct = avg_lerner * 100
                        st.write(
                            f"Firms mark up prices by an average of **{lerner_pct:.1f}%** "
                            f"above marginal cost."
                        )
                    
                    # Create and display market share chart
                    st.subheader("📊 Market Share Distribution")
                    fig = create_market_share_chart(df)
                    st.pyplot(fig, use_container_width=True)
                    
                    # Detailed analysis section
                    st.subheader("📑 Detailed Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Market Summary Statistics:**")
                        summary_stats = pd.DataFrame({
                            "Metric": [
                                "Number of Firms",
                                "Largest Market Share",
                                "Smallest Market Share",
                                "Average Market Share"
                            ],
                            "Value": [
                                len(df),
                                f"{df['market_share'].max():.2%}",
                                f"{df['market_share'].min():.2%}",
                                f"{df['market_share'].mean():.2%}"
                            ]
                        })
                        st.dataframe(summary_stats, use_container_width=True, hide_index=True)
                    
                    with col2:
                        st.write("**Price & Cost Summary:**")
                        price_cost_stats = pd.DataFrame({
                            "Metric": [
                                "Average Price",
                                "Average Marginal Cost",
                                "Average Markup",
                                "Price Range"
                            ],
                            "Value": [
                                f"${df['price'].mean():.2f}",
                                f"${df['marginal_cost'].mean():.2f}",
                                f"${(df['price'] - df['marginal_cost']).mean():.2f}",
                                f"${df['price'].min():.2f} - ${df['price'].max():.2f}"
                            ]
                        })
                        st.dataframe(price_cost_stats, use_container_width=True, hide_index=True)
                    
                    # Download report section
                    st.subheader("📥 Download Report")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv_report = generate_csv_report(df, hhi, avg_lerner)
                        st.download_button(
                            label="📥 Download CSV Report",
                            data=csv_report,
                            file_name="market_power_report.csv",
                            mime="text/csv",
                            help="Download analysis results as CSV"
                        )
                    
                    with col2:
                        # Excel export option
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                            df.to_excel(writer, sheet_name="Data", index=False)
                            
                            # Add metrics sheet
                            metrics_df = pd.DataFrame({
                                "Metric": ["HHI", "Average Lerner Index"],
                                "Value": [hhi, avg_lerner]
                            })
                            metrics_df.to_excel(writer, sheet_name="Metrics", index=False)
                        
                        excel_buffer.seek(0)
                        st.download_button(
                            label="📊 Download Excel Report",
                            data=excel_buffer,
                            file_name="market_power_report.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            help="Download analysis results as Excel"
                        )
                
                except ValueError as e:
                    st.error(f"❌ Error calculating metrics: {str(e)}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
        
        except pd.errors.ParserError:
            st.error("❌ Error reading CSV file. Please ensure it's a valid CSV format.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    else:
        # Show sample data if no file uploaded
        st.info("👆 Upload a CSV file to get started!")
        
        with st.expander("📝 See Example Data Format"):
            example_df = pd.DataFrame({
                "company_name": ["Company_A", "Company_B", "Company_C", "Company_D"],
                "market_share": [0.40, 0.30, 0.20, 0.10],
                "price": [25.0, 22.0, 20.0, 18.0],
                "marginal_cost": [15.0, 13.0, 12.0, 11.0]
            })
            st.dataframe(example_df, use_container_width=True)
            
            st.markdown(
                """
                **Notes:**
                - `market_share`: Must be decimal fractions summing to 1.0 (or very close)
                - `price`: Unit price of the product
                - `marginal_cost`: Marginal cost of production
                - `company_name`: (Optional) Company identifiers for better visualization
                """
            )


if __name__ == "__main__":
    main()
