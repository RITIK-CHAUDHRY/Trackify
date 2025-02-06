import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

class ExpenseAnalyzer:
    def __init__(self, expenses):
        # Convert expenses to DataFrame, handle empty case
        if expenses:
            self.expenses = pd.DataFrame(expenses)
        else:
            # Create empty DataFrame with required columns
            self.expenses = pd.DataFrame(columns=['category', 'date', 'amount'])
        
    def get_monthly_summary(self):
        """Generate monthly expense summary"""
        if self.expenses.empty:
            return {}
        monthly = self.expenses.groupby(['category', pd.Grouper(key='date', freq='M')])['amount'].sum()
        return monthly.to_dict()
    
    def get_category_breakdown(self):
        """Get expense breakdown by category"""
        if self.expenses.empty:
            return {}
        return self.expenses.groupby('category')['amount'].sum().to_dict()
    
    def generate_trend_graph(self):
        """Generate expense trend visualization"""
        if self.expenses.empty:
            # Create a simple empty graph
            df = pd.DataFrame({'date': [datetime.now()], 'amount': [0], 'category': ['No Data']})
            fig = px.line(df, x='date', y='amount', color='category')
            return fig.to_json()
        fig = px.line(self.expenses, x='date', y='amount', color='category')
        return fig.to_json()
    
    def predict_future_expenses(self):
        """Simple prediction for next month's expenses"""
        if self.expenses.empty:
            return {}
        recent_avg = self.expenses.groupby('category')['amount'].mean()
        return recent_avg.to_dict()
        
    def get_spending_alerts(self):
        """Generate spending alerts based on patterns"""
        if self.expenses.empty:
            return ["No expenses recorded yet. Start tracking your spending!"]
            
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
                
        return alerts if alerts else ["Your spending is within normal limits."]