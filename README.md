# Market Power Metrics Calculator

## Project Description

The **Market Power Metrics Calculator** is an interactive web application designed for economic analysis and research. This tool enables researchers, economists, and policy analysts to upload market data and calculate key metrics for assessing market concentration and competitive dynamics. Built with Streamlit, the application provides real-time computation of the Herfindahl-Hirschman Index (HHI) and the Lerner Index, with intuitive visualizations to support informed decision-making in market structure analysis.

The application is particularly useful for:
- **Market concentration assessment** in industrial organization research
- **Regulatory compliance analysis** for antitrust and competition law
- **Academic research** in energy economics and industrial economics
- **Policy evaluation** and market monitoring studies

---

## Key Features

- **CSV Data Upload**: Upload market data in CSV format with firm names, market shares, prices, and marginal costs
- **Real-time Metric Calculation**: Instantly compute HHI and Lerner Index with comprehensive error handling
- **Interactive Visualizations**: Explore market structure through charts, heatmaps, and distribution plots
- **Detailed Interpretations**: In-app explanations of metrics and their economic significance
- **Report Generation**: Export analysis results with formatted tables and statistics
- **Batch Processing**: Analyze multiple datasets with comparative metrics
- **User-Friendly Interface**: Intuitive sidebar navigation and responsive design

---

## How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/market-power-metrics-calculator.git
   cd market-power-metrics-calculator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - The app will open in your default browser at `http://localhost:8501`
   - If not, navigate to the URL displayed in the terminal

### Sample Data
A sample dataset (`synthetic_market_data.csv`) is included in the repository to help you get started with testing the application.

---

## Methodology

### Herfindahl-Hirschman Index (HHI)

The **Herfindahl-Hirschman Index** is a widely-used measure of market concentration employed by competition authorities and researchers worldwide.

**Mathematical Formulation:**

$$\text{HHI} = \sum_{i=1}^{n} s_i^2 \times 10,000$$

Where:
- $s_i$ is the market share of firm $i$ (expressed as a decimal fraction)
- $n$ is the number of firms in the market
- The index ranges from $\frac{10,000}{n}$ (perfect competition) to 10,000 (monopoly)

**Interpretation Guidelines:**
- **HHI < 1,500**: Competitive market with low concentration
- **1,500 ≤ HHI < 2,500**: Moderately concentrated market
- **HHI ≥ 2,500**: Highly concentrated market with significant market power concerns

The HHI is particularly sensitive to changes in shares of large firms and is preferred by the U.S. Department of Justice and Federal Trade Commission for merger analysis.

---

### Lerner Index

The **Lerner Index** measures the degree of market power possessed by an individual firm, representing the markup over marginal cost.

**Mathematical Formulation:**

$$L_i = \frac{P_i - MC_i}{P_i}$$

Where:
- $P_i$ is the price charged by firm $i$
- $MC_i$ is the marginal cost of firm $i$
- $L_i$ ranges from 0 (perfect competition) to 1 (monopoly power)

**Interpretation:**
- **L = 0**: Firm operates in perfect competition (P = MC)
- **0 < L < 0.5**: Moderate market power
- **L ≥ 0.5**: Substantial market power

The **average Lerner Index** reported in this application is the mean across all firms:

$$\bar{L} = \frac{1}{n}\sum_{i=1}^{n} L_i$$

This aggregate measure reflects the average level of market power across the entire market, providing complementary information to the HHI.

---

## Screenshots Placeholder

*Screenshots of the application interface will be added here, including:*
- *Main dashboard with data upload interface*
- *HHI and Lerner Index calculation results*
- *Market concentration visualizations*
- *Comparative analysis charts*
- *Report generation sample*

---

## Project Structure

```
market-power-metrics-calculator/
├── app.py                           # Main Streamlit application
├── generate_market_data.py          # Script for generating synthetic test data
├── synthetic_market_data.csv        # Sample dataset for testing
├── test_analysis.py                 # Unit tests for analysis functions
├── utils/
│   ├── __init__.py
│   └── analysis.py                  # Core analysis functions (HHI, Lerner Index)
├── requirements.txt                 # Python dependencies
└── README.md                         # This file
```

---

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib**: Data visualization
- **scipy**: Scientific computing utilities

See `requirements.txt` for a complete list of dependencies and versions.

---

## Usage Example

1. Prepare your market data in CSV format with the following columns:
   - `firm_name`: Name or identifier of the firm
   - `market_share`: Market share as a percentage or decimal (0-1)
   - `price`: Price charged by the firm
   - `marginal_cost`: Marginal cost of the firm

2. Launch the application and use the sidebar to upload your CSV file

3. View real-time calculations of:
   - Herfindahl-Hirschman Index (HHI)
   - Average Lerner Index
   - Market concentration classification
   - Detailed firm-level analysis

4. Generate visualizations and export results for further analysis

---

## Contact & Credits

**Author:** Stefanos Fardellas  
**Affiliation:** PhD Candidate, Department of Economics, University of Patras, Greece  
**Research Focus:** Energy Economics, Industrial Organization (IO)

**Research Interests:**
- Market structure and competition in energy markets
- Industrial organization and antitrust analysis
- Economic regulation and policy evaluation
- Quantitative methods in applied microeconomics

For inquiries, collaboration opportunities, or feedback regarding this project, please contact:
- **Email:** [sfardellas@ac.upatras.gr](mailto:sfardellas@ac.upatras.gr)
- **GitHub:** [@StefanosFardellas](https://github.com/StefanosFardellas)
- **University Profile:** [https://www.econ.upatras.gr/en/person/fardellas-stefanos/]

---

## License

This project is provided for academic and research purposes. Please refer to the LICENSE file for specific terms.

---

## Disclaimer

This tool is designed for educational and research purposes. Users are responsible for ensuring that their data and analysis comply with applicable laws and regulations, particularly regarding antitrust and competition law in their jurisdictions. The calculations provided are based on standard economic methodologies but should be verified independently before use in regulatory or policy contexts.

---

## Acknowledgments

This project was developed as part of research in industrial economics and market structure analysis at the University of Patras. Special thanks to all contributors and the open-source community for the excellent libraries and tools that made this project possible.

