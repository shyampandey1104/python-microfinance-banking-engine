"""Unit tests for CoreBankingEngine."""

from banking.engine import CoreBankingEngine, Account


def test_fund_transfer():
    engine = CoreBankingEngine()
    engine.accounts["ACC-101"] = Account(account_number="ACC-101", customer_name="Alice", balance=10000.0)
    engine.accounts["ACC-102"] = Account(account_number="ACC-102", customer_name="Bob", balance=2000.0)

    res = engine.transfer("ACC-101", "ACC-102", 3000.0)
    assert res["status"] == "Transferred"
    assert engine.accounts["ACC-101"].balance == 7000.0
    assert engine.accounts["ACC-102"].balance == 5000.0


def test_loan_amortization_schedule():
    # ₹100,000 principal at 12% annual interest for 12 months
    res = CoreBankingEngine.calculate_loan_amortization(
        principal=100000.0,
        annual_interest_rate_pct=12.0,
        tenure_months=12,
    )
    assert round(res["monthly_emi"]) == 8885.0
    assert len(res["schedule"]) == 12
    # Ending balance of last month must be 0.0
    assert res["schedule"][-1].ending_balance == 0.0
