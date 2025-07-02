from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from prophet import Prophet
from datetime import datetime, date, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/api/investment')
def simulate_investment():
    ticker = request.args.get('ticker')
    amount = request.args.get('amount')
    buy_date = request.args.get('buyDate')
    sell_date = request.args.get('sellDate')

    # Validate inputs
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400
    ticker = ticker.upper()

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount'}), 400

    try:
        buy_date_dt = datetime.strptime(buy_date, '%Y-%m-%d')
        sell_date_dt = datetime.strptime(sell_date, '%Y-%m-%d') if sell_date else datetime.today()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if buy_date_dt.date() > date.today():
        return jsonify({'error': 'Buy date cannot be in the future'}), 400
    if sell_date_dt.date() <= buy_date_dt.date():
        return jsonify({'error': 'Sell date must be after buy date'}), 400

    try:
        # Download historical data (up to today or sell_date if in past)
        end_date = min(sell_date_dt, datetime.today()).strftime('%Y-%m-%d')
        data = yf.download(ticker, start=buy_date, end=end_date)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if data.empty or 'Close' not in data.columns:
            return jsonify({'error': f'No data found for ticker {ticker} in the specified date range'}), 400

        buy_price = float(data.iloc[0]['Close'])
        shares = amount / buy_price

        if sell_date_dt.date() <= date.today():
            # Historical calculation
            final_price = float(data.iloc[-1]['Close'])
            final_value = round(shares * final_price, 2)
            return_percent = round(((final_value - amount) / amount) * 100, 2)
            return jsonify({
                'initialAmount': round(amount, 2),
                'shares': round(shares, 4),
                'finalValue': final_value,
                'returnPercent': return_percent,
                'dates': data.index.strftime('%Y-%m-%d').tolist(),
                'values': [round(float(price) * shares, 2) for price in data['Close']],
                'isPrediction': False
            })
        else:
            # Prediction for future sell_date
            df = data[['Close']].reset_index().rename(columns={'Date': 'ds', 'Close': 'y'})
            model = Prophet(daily_seasonality=True)
            model.fit(df)

            # Create future dates
            future_days = (sell_date_dt.date() - date.today()).days + 1
            future = model.make_future_dataframe(periods=future_days, freq='D')
            forecast = model.predict(future)

            # Filter forecast from buy_date to sell_date
            forecast = forecast[forecast['ds'] >= buy_date_dt][['ds', 'yhat']]
            forecast['yhat'] = forecast['yhat'].clip(lower=0)  # Ensure non-negative prices
            final_price = float(forecast.iloc[-1]['yhat'])
            final_value = round(shares * final_price, 2)
            return_percent = round(((final_value - amount) / amount) * 100, 2)

            return jsonify({
                'initialAmount': round(amount, 2),
                'shares': round(shares, 4),
                'finalValue': final_value,
                'returnPercent': return_percent,
                'dates': forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
                'values': [round(float(price) * shares, 2) for price in forecast['yhat']],
                'isPrediction': True
            })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)