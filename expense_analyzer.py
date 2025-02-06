import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

class ExpenseAnalyzer:
    def __init__(self, expenses):
        self.expenses = pd.DataFrame(expenses)
        
    def get_monthly_summary(self):
        """Generate monthly expense summary"""
        monthly = self.expenses.groupby(['category', pd.Grouper(key='date', freq='M')])['amount'].sum()
        return monthly.to_dict()
    
    def get_category_breakdown(self):
        """Get expense breakdown by category"""
        return self.expenses.groupby('category')['amount'].sum().to_dict()
    
    def generate_trend_graph(self):
        """Generate expense trend visualization"""
        fig = px.line(self.expenses, x='date', y='amount', color='category')
        return fig.to_json()
    
    def predict_future_expenses(self):
        """Simple prediction for next month's expenses"""
        recent_avg = self.expenses.groupby('category')['amount'].mean()
        return recent_avg.to_dict()
        
    def get_spending_alerts(self):
        """Generate spending alerts based on patterns"""
        alerts = []
        category_limits = {
            'food': 1000,
            'entertainment': 500,
            'shopping': 2000
        }
        
        for category, limit in category_limits.items():
            total = self.expenses[
                (self.expenses['category'] == category) & 
                (self.expenses['date'] >= datetime.now() - timedelta(days=30))
            ]['amount'].sum()
            
            if total > limit:
                alerts.append(f"Warning: {category} spending (₹{total}) exceeds monthly limit of ₹{limit}")
                
        return alerts