![OptionLab](optionlab.png)

# Options Strategy Calculator Web Application

A comprehensive web-based options trading strategy calculator built with Flask and the OptionLab Python library. This application provides professional traders and enthusiasts with powerful tools to analyze complex options strategies, visualize profit/loss diagrams, and make informed trading decisions.

## 🚀 Features

### Web Application Features
- **Interactive Web Interface**: Modern, responsive UI for strategy configuration
- **Real-time Stock Data**: Integration with Yahoo Finance for live stock prices and volatility
- **Strategy Visualization**: Dynamic profit/loss charts with customizable parameters
- **Multiple Strategy Types**: Support for stocks, calls, puts, and complex multi-leg strategies
- **Preset Strategies**: Quick access to common strategies (Covered Call, Bull Call Spread, Iron Condor, etc.)
- **Options Chain Data**: Real-time options pricing and Greeks
- **Stock Charts**: Historical price charts with multiple timeframes
- **Risk Metrics**: Comprehensive analysis including probability of profit, max profit/loss, breakeven points

### OptionLab Library Features
- **Black-Scholes Pricing**: Accurate options pricing using the Black-Scholes model
- **Greeks Calculation**: Delta, Gamma, Theta, Vega, and Rho for each strategy leg
- **Probability Analysis**: Analytical probability of profit calculations
- **Flexible Strategy Building**: Support for complex multi-leg strategies
- **Previously Opened Positions**: Include existing positions in new strategies
- **Custom Price Arrays**: Use alternative pricing models beyond Black-Scholes

## 📋 Requirements

- Python 3.10+
- Flask
- OptionLab library
- yfinance (for real-time data)
- matplotlib (for chart generation)
- pandas, numpy, scipy
- Other dependencies listed in `pyproject.toml`

## 🛠️ Installation

### Option 1: Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/BordelonDevOps/Options_Strategy.git
cd Options_Strategy

# Install dependencies using Poetry
poetry install

# Activate the virtual environment
poetry shell

# Run the application
python app.py
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/BordelonDevOps/Options_Strategy.git
cd Options_Strategy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask optionlab yfinance matplotlib pandas numpy scipy pydantic holidays

# Run the application
python app.py
```

## 🚀 Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://localhost:9100`

### Web Interface

1. **Stock Data Input**:
   - Enter a stock ticker symbol
   - The application will automatically fetch current price and volatility
   - View historical stock charts

2. **Strategy Configuration**:
   - Add multiple strategy legs (stocks, calls, puts)
   - Configure strike prices, premiums, quantities, and actions
   - Set target dates and risk parameters

3. **Analysis**:
   - Click "Calculate Strategy" to generate analysis
   - View profit/loss diagram
   - Review key metrics and risk parameters

### API Endpoints

- `GET /` - Main web interface
- `POST /calculate` - Calculate strategy metrics
- `GET /preset/<strategy_name>` - Get preset strategy configurations
- `GET /api/stock/<ticker>` - Get real-time stock data
- `GET /api/stock/<ticker>/chart` - Get stock price charts
- `GET /api/options/<ticker>` - Get options chain data

## 📊 Supported Strategies

### Basic Strategies
- **Long/Short Stock**: Direct equity positions
- **Long/Short Calls**: Basic call option strategies
- **Long/Short Puts**: Basic put option strategies

### Spread Strategies
- **Bull Call Spread**: Buy lower strike call, sell higher strike call
- **Bear Put Spread**: Buy higher strike put, sell lower strike put
- **Calendar Spreads**: Same strike, different expirations

### Income Strategies
- **Covered Call**: Own stock + sell call
- **Cash-Secured Put**: Sell put with cash backing
- **Iron Condor**: Sell call spread + sell put spread

### Protection Strategies
- **Protective Put**: Own stock + buy put
- **Collar**: Own stock + buy put + sell call

### Volatility Strategies
- **Long Straddle**: Buy call + buy put (same strike)
- **Short Straddle**: Sell call + sell put (same strike)
- **Strangle**: Buy/sell call and put (different strikes)

## 🧮 Key Metrics Calculated

- **Probability of Profit (PoP)**: Likelihood of profitable outcome
- **Maximum Profit**: Highest possible return
- **Maximum Loss**: Worst-case scenario loss
- **Breakeven Points**: Stock prices where strategy breaks even
- **Expected Profit/Loss**: Probability-weighted outcomes
- **Strategy Cost**: Net debit or credit
- **Profit Ranges**: Price ranges where strategy is profitable
- **Greeks**: Risk sensitivities (Delta, Gamma, Theta, Vega, Rho)

## 🏗️ Project Structure

```
Options_Strategy/
├── app.py                 # Flask web application
├── templates/
│   └── index.html        # Main web interface
├── optionlab/            # Core options calculation library
│   ├── __init__.py
│   ├── engine.py         # Main calculation engine
│   ├── models.py         # Data models and types
│   ├── black_scholes.py  # Black-Scholes implementation
│   ├── plot.py           # Plotting utilities
│   ├── support.py        # Support functions
│   └── utils.py          # Utility functions
├── examples/             # Jupyter notebook examples
├── tests/                # Unit tests
├── docs/                 # API documentation
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Using Poetry
poetry run pytest

# Using pip
pytest
```

Run specific test categories:

```bash
pytest tests/test_core.py      # Core functionality tests
pytest tests/test_models.py    # Data model tests
pytest tests/test_misc.py      # Miscellaneous tests
```

## 📚 Examples

The `examples/` directory contains Jupyter notebooks demonstrating various strategies:

- `black_scholes_calculator.ipynb` - Basic Black-Scholes calculations
- `covered_call.ipynb` - Covered call strategy example
- `call_spread.ipynb` - Bull call spread example
- `calendar_spread.ipynb` - Calendar spread strategy
- `naked_call.ipynb` - Short call strategy

## 🔧 Development

### Setting up Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Install pre-commit hooks
pre-commit install

# Run code formatting
black .

# Run linting
ruff check .

# Run type checking
mypy optionlab/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📖 API Documentation

Detailed API documentation is available in the `docs/` directory and can be accessed at the [project's GitHub Pages site](https://rgaveiga.github.io/optionlab).

## ⚠️ Disclaimer

**Important**: This software is provided for educational and research purposes only. 

- The author makes no guarantee that results are accurate
- The author is not responsible for any losses caused by the use of this code
- Options trading involves significant risk and requires due diligence
- Always consult with a qualified financial advisor before making trading decisions
- Past performance does not guarantee future results

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Support

If you have questions, corrections, comments, or suggestions:

- Open an issue on GitHub
- Contact: [roberto.veiga@ufabc.edu.br](mailto:roberto.veiga@ufabc.edu.br)
- LinkedIn: [Roberto Gomes, PhD](https://www.linkedin.com/in/roberto-gomes-phd-8a718317b/)
- Twitter/X: [@rgaveiga](https://x.com/rgaveiga)
- Medium: [@rgaveiga](https://medium.com/@rgaveiga)

## 💝 Sponsorship

If you find this project useful and want to support its development, consider becoming a [sponsor on GitHub](https://github.com/sponsors/rgaveiga).

## 🏷️ Version

Current version: 1.4.3

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Built with ❤️ using Python, Flask, and the OptionLab library**
