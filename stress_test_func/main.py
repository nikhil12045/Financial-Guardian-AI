def run_nightly_job(request):
    # 1. Scan for debt > 30 days
    overdue_docs = db.collection("bills").where("days_overdue", ">", 30).stream()
    
    for doc in overdue_docs:
        bill = doc.to_dict()
        # 2. Automatically create a "Debt-Payoff Sprint" in the habits collection
        db.collection("habits").add({
            "name": f"Sprint: Clear {bill['merchant']}",
            "type": "Debt-Payoff",
            "start_date": firestore.SERVER_TIMESTAMP,
            "status": "active",
            "daily_target": bill['amount'] / 30
        })
        
        # 3. Create a Google Task (Audit Log)
        db.collection("audit_logs").add({
            "action": "PROACTIVE_STRESS_TEST",
            "outcome": f"Created Debt-Payoff Sprint for {bill['merchant']}"
        })
    return "Stress Test Complete", 200
