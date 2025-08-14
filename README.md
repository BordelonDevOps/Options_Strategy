# Professional Options Strategy Calculator

> A sophisticated web-based options trading analysis platform built with Flask and modern web technologies

## 🚀 Overview

This is a professional-grade web application designed for options traders who need powerful strategy analysis tools. Built from the ground up with a focus on user experience, real-time data integration, and comprehensive risk analysis.

## ✨ Key Features

### 🎯 **Interactive Strategy Builder**
- Drag-and-drop interface for building complex options strategies
- Support for stocks, calls, and puts with unlimited combinations
- Real-time validation and error handling
- Professional-grade UI with gradient designs and smooth animations

### 📊 **Advanced Analytics**
- Probability of profit calculations
- Maximum profit/loss analysis
- Expected profit/loss projections
- Strategy cost analysis
- Profit range identification

### 📈 **Real-Time Market Data**
- Live stock price feeds via Yahoo Finance API
- Historical volatility calculations
- Options chain data with bid/ask spreads
- Interactive stock price charts
- Company information and market metrics

### 🎨 **Modern Web Interface**
- Responsive design that works on all devices
- Professional gradient color schemes
- Smooth animations and transitions
- Bootstrap 5 integration
- Font Awesome icons
- Custom CSS with modern design patterns

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5, Custom CSS with CSS Variables
- **Charts**: Matplotlib with base64 encoding
- **Data**: Yahoo Finance API, Pandas, NumPy
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter)

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip or Poetry

### Quick Start

```bash
# Clone the repository
git clone https://github.com/BordelonDevOps/Options_Strategy.git
cd Options_Strategy

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:9100`

### Using Poetry (Recommended)

```bash
# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell

# Run the application
python app.py
```

## 🎮 Usage

### Web Interface
1. Open your browser to `http://localhost:9100`
2. Enter stock ticker and basic parameters
3. Add strategy legs (stocks, calls, puts)
4. Click "Calculate Strategy" to see results
5. View profit/loss diagram and key metrics

### API Endpoints

#### Strategy Calculation
```http
POST /calculate
Content-Type: application/json

{
  "stock_ticker": "AAPL",
  "stock_price": 150.00,
  "volatility": 0.25,
  "interest_rate": 0.05,
  "start_date": "2024-01-01",
  "target_date": "2024-02-01",
  "strategy": [
    {
      "type": "call",
      "strike": 155.0,
      "premium": 3.50,
      "n": 1,
      "action": "buy"
    }
  ]
}
```

#### Real-Time Stock Data
```http
GET /api/stock/{ticker}
```

#### Stock Charts
```http
GET /api/stock/{ticker}/chart?period=3mo
```

#### Options Chain Data
```http
GET /api/options/{ticker}
```

## 🎨 Design Philosophy

This application was built with a focus on:

- **Professional Aesthetics**: Modern gradient designs and clean typography
- **User Experience**: Intuitive interface with helpful validation messages
- **Performance**: Optimized API calls and efficient data processing
- **Reliability**: Comprehensive error handling and timeout protection
- **Scalability**: Modular code structure for easy expansion

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `PORT`: Custom port (default: 9100)
- `HOST`: Custom host (default: 0.0.0.0)

### Customization
- Modify CSS variables in `templates/index.html` for color schemes
- Adjust chart styling in the matplotlib configuration
- Update API endpoints in `app.py` for additional features

## 📊 Supported Strategies

- **Basic Positions**: Long/Short Stock, Long/Short Calls/Puts
- **Spreads**: Bull/Bear Call/Put Spreads
- **Straddles & Strangles**: Long/Short variations
- **Complex Strategies**: Iron Condors, Butterflies, Custom combinations

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:9100 app:app

# Using Docker
docker build -t options-calculator .
docker run -p 9100:9100 options-calculator
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and informational purposes only. It should not be considered as financial advice. Options trading involves substantial risk and is not suitable for all investors. Always consult with a qualified financial advisor before making investment decisions.

## 📞 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Contact: [Your Contact Information]

---

**Built with ❤️ for the trading community**
