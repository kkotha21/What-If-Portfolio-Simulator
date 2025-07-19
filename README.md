What If? Portfolio Simulator is a full- web application that lets users simulate hypothetical investments and predict future stock prices using real historical data and machine learning.

 Features
- Simulate returns for any stock by entering a ticker, amount, buy date, and (optional) sell date

- Visualize investment growth over time using interactive charts

- Predict the next 30 days of stock prices using linear regression

- Built with a Python/Flask backend and a React frontend

- Tech Stack
Frontend: React, Axios, Chart.js

Backend: Flask, Python, yFinance, scikit-learn, Pandas

Tools: Git, VS Code, Node.js, npm

- Getting Started
1. Clone the repo
git clone https://github.com/kkotha21/What-If-Portfolio-Simulator.git
cd What-If-Portfolio-Simulator
2. Start the backend (Flask)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # or install manually
python app.py
3. Start the frontend (React)
cd ../frontend
npm install
npm start
App will run at: http://localhost:3000

- Example Usage
“What if I invested $500 in TSLA on Jan 1, 2020?”
→ See how that investment would have performed over time
→ Plus, view a 30-day prediction of future prices
