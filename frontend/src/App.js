import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

export default function App() {
  const [ticker, setTicker] = useState('');
  const [amount, setAmount] = useState('');
  const [buyDate, setBuyDate] = useState('');
  const [sellDate, setSellDate] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5001';
      const response = await axios.get(`${apiUrl}/api/investment`, {
        params: { ticker, amount, buyDate, sellDate }
      });
      console.log('Response:', response.data);
      setResult(response.data);
      setError(null);
    } catch (err) {
      console.error('Error:', err.message, err.response?.data, err.response?.status);
      setError(`Could not fetch investment data: ${err.response?.data?.error || err.message}`);
      setResult(null);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '700px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '1rem' }}>"What If?" Portfolio Simulator</h1>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1rem' }}>
        <input
          type="text"
          placeholder="Ticker (e.g. AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Amount (e.g. 1000)"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />
        <input
          type="date"
          value={buyDate}
          onChange={(e) => setBuyDate(e.target.value)}
          required
        />
        <input
          type="date"
          value={sellDate}
          onChange={(e) => setSellDate(e.target.value)}
        />
        <button
          type="submit"
          style={{ padding: '0.5rem', backgroundColor: '#2563EB', color: 'white', border: 'none', borderRadius: '5px' }}
        >
          Simulate
        </button>
      </form>

      {error && <div style={{ color: 'red', marginTop: '1rem' }}>{error}</div>}

      {result && (
        <div style={{ marginTop: '2rem' }}>
          <h2 style={{ fontSize: '1.4rem', fontWeight: '600', marginBottom: '0.5rem' }}>
            {result.isPrediction ? 'Predicted Investment Result' : 'Historical Investment Result'}
          </h2>
          <p><strong>Initial Investment:</strong> ${result.initialAmount}</p>
          <p><strong>Shares Bought:</strong> {result.shares}</p>
          <p><strong>Value on Sell Date:</strong> ${result.finalValue}</p>
          <p><strong>Return:</strong> {result.returnPercent}%</p>
          {result.isPrediction && (
            <p style={{ color: 'orange' }}>
              Note: This is a predicted result based on historical trends and may not reflect actual future performance.
            </p>
          )}
          <Line
            data={{
              labels: result.dates,
              datasets: [{
                label: `${ticker.toUpperCase()} Value Over Time${result.isPrediction ? ' (Predicted)' : ''}`,
                data: result.values,
                fill: false,
                borderColor: result.isPrediction ? 'orange' : 'blue'
              }]
            }}
          />
        </div>
      )}
    </div>
  );
}