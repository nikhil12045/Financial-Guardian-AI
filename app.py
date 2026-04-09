import streamlit as st
from agents import MoneyOrchestrator
from fin_tools import FirestoreSeeder, MockFinancialDataTool, BillAgent

st.set_page_config(page_title="Guardian AI", layout="wide")

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = MoneyOrchestrator()
    st.session_state.messages = []

# --- DASHBOARD METRICS ---
st.title("🛡️ Financial Guardian AI")
curr_balance = MockFinancialDataTool.get_balance()

c1, c2, c3 = st.columns(3)
c1.metric("Available Liquidity", f"${curr_balance:,.2f}", "+$2,300")
c2.metric("Intelligence Status", "Proactive Agents")
c3.info("Context Memory: **Active** 🧠")

st.divider()

# --- THE "ATTRACTIVE" DASHBOARD VIEW ---
col_chat, col_data = st.columns([2, 1])

with col_chat:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("What bills do I have coming up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.spinner("Analyzing Accounts & Debt..."):
            response = st.session_state.orchestrator.run(prompt)
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with col_data:
    st.subheader("📋 Proactive Monitor")
    st.write("**Upcoming Debt Deadlines:**")
    st.warning(BillAgent.get_upcoming_bills())
    
    st.divider()
    if st.button("Run Subscription Audit"):
        from fin_tools import AnomalyAgent
        st.error(AnomalyAgent.detect_subscription_hikes())

with st.sidebar:
    st.header("Admin")
    if st.button("Initialize Full Demo"):
        st.success(FirestoreSeeder.seed_all())
    st.write("Enabled Agents: **Liquidity, Debt/Bills, Spending, Anomaly**")