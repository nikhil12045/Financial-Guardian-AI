from google.cloud import firestore
import datetime
from config import PROJECT_ID

db = firestore.Client(project=PROJECT_ID)

class BillAgent:
    @staticmethod
    def get_upcoming_bills():
        """Reads the 'bills' collection for unpaid obligations."""
        try:
            docs = db.collection("bills").stream()
            bill_list = [f"{d.to_dict().get('merchant')}: ${d.to_dict().get('amount')} (Due in {d.to_dict().get('days_left')} days)" for d in docs]
            return "Upcoming Bills: " + ", ".join(bill_list) if bill_list else "No upcoming bills found."
        except Exception as e:
            return f"Error reading bills: {str(e)}"

class ExpenseAgent:
    @staticmethod
    def get_expenses():
        docs = db.collection("transactions").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()
        expense_list = [f"{d.to_dict().get('merchant')}: ${d.to_dict().get('amount')}" for d in docs]
        return "Recent Expenses: " + ", ".join(expense_list) if expense_list else "No expenses found."

class AnomalyAgent:
    @staticmethod
    def detect_subscription_hikes():
        return "🕵️ Vampire Alert: 'Cloud Stream' increased from $15 to $22. Suggesting a review."

class MockFinancialDataTool:
    @staticmethod
    def get_balance():
        doc = db.collection("accounts").document("acc_123").get()
        return doc.to_dict().get('balance', 0) if doc.exists else 0

class FirestoreSeeder:
    @staticmethod
    def seed_all():
        # 1. Accounts
        db.collection("accounts").document("acc_123").set({"name": "Checking", "balance": 15000.00})
        # 2. Upcoming Bills
        db.collection("bills").document("rent").set({"merchant": "Property Mgmt", "amount": 1800, "days_left": 5})
        db.collection("bills").document("electric").set({"merchant": "City Power", "amount": 145, "days_left": 12})
        # 3. Sample Transactions
        db.collection("transactions").add({"amount": 45, "merchant": "Uber", "timestamp": datetime.datetime.now()})
        return "Full Demo Data Seeded (Balance + Bills + Expenses)!"