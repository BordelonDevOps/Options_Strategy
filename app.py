from flask import Flask, render_template, request, jsonify
import datetime as dt
import json
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
from optionlab import run_strategy, Inputs, plot_pl
from optionlab.models import Option, Stock, ClosedPosition

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_strategy():
    try:
        data = request.json
        
        # Parse basic inputs
        stock_ticker = data.get('stock_ticker', 'UNKNOWN')
        stock_price = float(data['stock_price'])
        volatility = float(data['volatility'])
        interest_rate = float(data.get('interest_rate', 0.0))
        start_date = dt.datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        target_date = dt.datetime.strptime(data['target_date'], '%Y-%m-%d').date()
        
        # Calculate price range
        price_range = float(data.get('price_range', 0.5))
        min_stock = stock_price - round(stock_price * price_range, 2)
        max_stock = stock_price + round(stock_price * price_range, 2)
        
        # Parse strategy legs
        strategy = []
        for leg in data['strategy']:
            if leg['type'] == 'stock':
                strategy.append({
                    'type': 'stock',
                    'n': int(leg['n']),
                    'action': leg['action']
                })
            elif leg['type'] in ['call', 'put']:
                strategy.append({
                    'type': leg['type'],
                    'strike': float(leg['strike']),
                    'premium': float(leg['premium']),
                    'n': int(leg['n']),
                    'action': leg['action']
                })
        
        # Create inputs object
        inputs = Inputs(
            stock_price=stock_price,
            start_date=start_date,
            target_date=target_date,
            volatility=volatility,
            interest_rate=interest_rate,
            min_stock=min_stock,
            max_stock=max_stock,
            profit_target=data.get('profit_target'),
            loss_limit=data.get('loss_limit'),
            model='black-scholes',
            strategy=strategy
        )
        
        # Run calculation
        outputs = run_strategy(inputs)
        
        # Generate plot
        plt.figure(figsize=(12, 8))
        plot_pl(outputs)
        if stock_ticker != 'UNKNOWN':
            plt.title(f'{stock_ticker} Options Strategy Analysis', fontsize=16, fontweight='bold')
        else:
            plt.title('Profit/Loss Diagram', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Save plot to base64 string
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plot_url = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        # Helper function to handle infinite values
        def safe_round(value, decimals=2):
            if value is None:
                return None
            if not np.isfinite(value):
                return None  # Convert infinite values to None
            return round(value, decimals)
        
        # Prepare results
        results = {
            'success': True,
            'plot': plot_url,
            'metrics': {
                'probability_of_profit': safe_round(outputs.probability_of_profit * 100) if outputs.probability_of_profit else None,
                'max_profit': safe_round(outputs.maximum_return_in_the_domain) if outputs.maximum_return_in_the_domain else None,
                'max_loss': safe_round(outputs.minimum_return_in_the_domain) if outputs.minimum_return_in_the_domain else None,
                'profit_ranges': [[safe_round(r[0]), safe_round(r[1])] for r in outputs.profit_ranges] if outputs.profit_ranges else [],
                'expected_profit': safe_round(outputs.expected_profit) if outputs.expected_profit else None,
                'expected_loss': safe_round(outputs.expected_loss) if outputs.expected_loss else None,
                'strategy_cost': safe_round(outputs.strategy_cost) if outputs.strategy_cost else None
            }
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/preset/<strategy_name>')
def get_preset_strategy(strategy_name):
    """Get preset strategy configurations"""
    presets = {
        'covered_call': {
            'name': 'Covered Call',
            'description': 'Buy stock and sell call option',
            'strategy': []
        },
        'protective_put': {
            'name': 'Protective Put',
            'description': 'Buy stock and buy put option',
            'strategy': []
        },
        'bull_call_spread': {
            'name': 'Bull Call Spread',
            'description': 'Buy lower strike call, sell higher strike call',
            'strategy': []
        },
        'bear_put_spread': {
            'name': 'Bear Put Spread',
            'description': 'Buy higher strike put, sell lower strike put',
            'strategy': []
        },
        'iron_condor': {
            'name': 'Iron Condor',
            'description': 'Sell call spread and put spread',
            'strategy': []
        },
        'straddle': {
            'name': 'Long Straddle',
            'description': 'Buy call and put at same strike',
            'strategy': []
        }
    }
    
    if strategy_name in presets:
        return jsonify(presets[strategy_name])
    else:
        return jsonify({'error': 'Strategy not found'}), 404

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    """Fetch real-time stock data using yfinance"""
    try:
        # Create ticker object
        stock = yf.Ticker(ticker.upper())
        
        # Get stock info and history
        info = stock.info
        hist = stock.history(period="1mo")  # Get 1 month of data for volatility calculation
        
        if hist.empty or len(hist) < 2:
            return jsonify({
                'success': False, 
                'error': f'No data found for ticker {ticker.upper()}'
            })
        
        # Get current price (most recent close)
        current_price = float(hist['Close'].iloc[-1])
        
        # Calculate historical volatility (annualized)
        returns = hist['Close'].pct_change().dropna()
        if len(returns) > 1:
            volatility = float(returns.std() * np.sqrt(252))  # Annualized volatility
        else:
            volatility = 0.25  # Default volatility if calculation fails
        
        # Get company name
        company_name = info.get('longName', ticker.upper())
        
        return jsonify({
            'success': True,
            'data': {
                'ticker': ticker.upper(),
                'company_name': company_name,
                'current_price': round(current_price, 2),
                'volatility': round(volatility, 4),
                'currency': info.get('currency', 'USD'),
                'market_cap': info.get('marketCap'),
                'sector': info.get('sector', 'Unknown')
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching data for {ticker.upper()}: {str(e)}'
        })

@app.route('/api/stock/<ticker>/chart', methods=['GET'])
def get_stock_chart(ticker):
    """Fetch stock chart data using yfinance"""
    try:
        # Get period parameter (default to 3mo)
        period = request.args.get('period', '3mo')
        
        # Create ticker object
        stock = yf.Ticker(ticker.upper())
        
        # Get historical data
        hist = stock.history(period=period)
        
        if hist.empty:
            return jsonify({
                'success': False, 
                'error': f'No chart data found for ticker {ticker.upper()}'
            })
        
        # Generate stock price chart
        plt.figure(figsize=(10, 6))
        plt.plot(hist.index, hist['Close'], linewidth=2, color='#4facfe')
        plt.title(f'{ticker.upper()} Stock Price Chart ({period})', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot to base64 string
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        chart_url = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'chart': chart_url,
            'period': period
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generating chart for {ticker.upper()}: {str(e)}'
        })

@app.route('/api/options/<ticker>', methods=['GET'])
def get_options_data(ticker):
    """Fetch options chain data using yfinance"""
    
    # Helper functions to safely convert values
    def safe_float(value, default=0.0):
        try:
            if value is None or str(value).lower() in ['nan', 'none', '']:
                return default
            return float(value)
        except (ValueError, TypeError):
            return default

    def safe_int(value, default=0):
        try:
            if value is None or str(value).lower() in ['nan', 'none', '']:
                return default
            return int(float(value))
        except (ValueError, TypeError):
            return default
    
    try:
        # Create ticker object
        stock = yf.Ticker(ticker.upper())
        
        # Get available expiration dates
        expirations = stock.options
        
        if not expirations:
            return jsonify({
                'success': False,
                'error': f'No options data found for ticker {ticker.upper()}'
            })
        
        # Get current stock price for reference
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 100)
        
        # Get options data for the first few expiration dates
        options_data = []
        for exp_date in expirations[:6]:  # Limit to first 6 expiration dates
            try:
                option_chain = stock.option_chain(exp_date)
                
                # Process calls
                calls = option_chain.calls
                calls_data = []
                for _, row in calls.iterrows():
                    calls_data.append({
                        'strike': safe_float(row['strike']),
                        'lastPrice': safe_float(row['lastPrice']),
                        'bid': safe_float(row['bid']),
                        'ask': safe_float(row['ask']),
                        'volume': safe_int(row['volume']),
                        'openInterest': safe_int(row['openInterest']),
                        'impliedVolatility': safe_float(row['impliedVolatility'])
                    })
                
                # Process puts
                puts = option_chain.puts
                puts_data = []
                for _, row in puts.iterrows():
                    puts_data.append({
                        'strike': safe_float(row['strike']),
                        'lastPrice': safe_float(row['lastPrice']),
                        'bid': safe_float(row['bid']),
                        'ask': safe_float(row['ask']),
                        'volume': safe_int(row['volume']),
                        'openInterest': safe_int(row['openInterest']),
                        'impliedVolatility': safe_float(row['impliedVolatility'])
                    })
                
                options_data.append({
                    'expiration': exp_date,
                    'calls': calls_data,
                    'puts': puts_data
                })
                
            except Exception as e:
                print(f"Error processing expiration {exp_date}: {e}")
                continue
        
        return jsonify({
            'success': True,
            'data': {
                'ticker': ticker.upper(),
                'current_price': round(current_price, 2),
                'expirations': options_data
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching options data for {ticker.upper()}: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True, port=9100, host='0.0.0.0')