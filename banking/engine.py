"""Core Banking & Microfinance Loan Engine in Python."""

import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class Account(BaseModel):
    account_number: str
    customer_name: str
    account_type: str = "Savings"  # Savings, Current, Loan
    balance: float = 0.0
    status: str = "Active"


class EMIScheduleRow(BaseModel):
    month_number: int
    beginning_balance: float
    emi_amount: float
    principal_component: float
    interest_component: float
    ending_balance: float


class CoreBankingEngine:
    """Core ledger transactions and loan amortization scheduler."""

    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def transfer(self, source_acc: str, dest_acc: str, amount: float) -> Dict[str, Any]:
        if source_acc not in self.accounts or dest_acc not in self.accounts:
            raise ValueError("Invalid source or destination account")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        src = self.accounts[source_acc]
        if src.balance < amount:
            raise ValueError("Insufficient funds")

        src.balance -= amount
        self.accounts[dest_acc].balance += amount

        return {
            "source_account": source_acc,
            "destination_account": dest_acc,
            "amount": amount,
            "source_new_balance": round(src.balance, 2),
            "status": "Transferred",
        }

    @staticmethod
    def calculate_loan_amortization(
        principal: float,
        annual_interest_rate_pct: float,
        tenure_months: int,
    ) -> Dict[str, Any]:
        """Compute exact monthly EMI and complete payment amortization schedule."""
        monthly_rate = (annual_interest_rate_pct / 100.0) / 12.0

        # EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
        r_pow = math.pow(1 + monthly_rate, tenure_months)
        emi = principal * monthly_rate * r_pow / (r_pow - 1)

        schedule: List[EMIScheduleRow] = []
        current_balance = principal
        total_interest_paid = 0.0

        for month in range(1, tenure_months + 1):
            interest = current_balance * monthly_rate
            principal_paid = emi - interest
            ending = max(0.0, current_balance - principal_paid)

            total_interest_paid += interest
            schedule.append(
                EMIScheduleRow(
                    month_number=month,
                    beginning_balance=round(current_balance, 2),
                    emi_amount=round(emi, 2),
                    principal_component=round(principal_paid, 2),
                    interest_component=round(interest, 2),
                    ending_balance=round(ending, 2),
                )
            )
            current_balance = ending

        return {
            "principal": principal,
            "annual_rate": annual_interest_rate_pct,
            "tenure_months": tenure_months,
            "monthly_emi": round(emi, 2),
            "total_interest_payable": round(total_interest_paid, 2),
            "total_amount_payable": round(principal + total_interest_paid, 2),
            "schedule": schedule,
        }
