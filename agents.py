import vertexai
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration
from fin_tools import BillAgent, ExpenseAgent, MockFinancialDataTool, AnomalyAgent
from config import PROJECT_ID, LOCATION, MODEL_ID

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Define the full suite of Stable Specialist Tools
internal_funcs = [
    FunctionDeclaration(name="check_balance", description="Get user bank balance.", parameters={"type": "object", "properties": {}}),
    FunctionDeclaration(name="check_bills", description="Check upcoming bills and due dates.", parameters={"type": "object", "properties": {}}),
    FunctionDeclaration(name="read_expenses", description="Read recent spending history.", parameters={"type": "object", "properties": {}}),
    FunctionDeclaration(name="check_vampire_subs", description="Scan for subscription price hikes.", parameters={"type": "object", "properties": {}})
]

data_tool = Tool(function_declarations=internal_funcs)

class MoneyOrchestrator:
    def __init__(self):
        self.model = GenerativeModel(
            MODEL_ID, 
            tools=[data_tool],
            system_instruction=(
                "You are an Elite Financial Assistant. Use your tools to check balances, bills, and expenses. "
                "CRITICAL: Always remember the conversation context (Session Memory). "
                "If a user says 'Can I afford it?' and you just discussed a $1000 item, 'it' refers to that $1000."
            )
        )
        self.chat = self.model.start_chat(history=[])

    def run(self, prompt):
        response = self.chat.send_message(prompt)
        while response.candidates[0].function_calls:
            responses = []
            for call in response.candidates[0].function_calls:
                if call.name == "check_balance":
                    res = f"Balance: ${MockFinancialDataTool.get_balance()}"
                elif call.name == "check_bills":
                    res = BillAgent.get_upcoming_bills()
                elif call.name == "read_expenses":
                    res = ExpenseAgent.get_expenses()
                elif call.name == "check_vampire_subs":
                    res = AnomalyAgent.detect_subscription_hikes()
                
                responses.append(vertexai.generative_models.Part.from_function_response(name=call.name, response={"content": res}))
            response = self.chat.send_message(responses)
        return response.text