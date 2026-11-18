"""
Lab 6 - BankAccount tests (student version)

Every test below starts with the annotation  @pytest.mark.skip(reason=TODO).
For each test:
    1. Remove the @pytest.mark.skip line.
    2. Replace `pass` with real test code.
    3. Run pytest and read the coverage report.

If a test fails because of a real bug in src/, you found one of the 9 bugs.
Document it by adding this annotation above the test:

    @pytest.mark.xfail(reason="BUG #N: what is wrong", strict=True)
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.bank_account import BankAccount

TODO = "TODO: remove this annotation once you write the test"

# Marks every test in this file. Run only these with: pytest -m bank
pytestmark = pytest.mark.bank


# ---------------------------------------------------------------- fixtures

@pytest.fixture
def account():
    """An empty account owned by Alice."""
    return BankAccount("Alice")


@pytest.fixture
def funded_account(account):
    """Alice's account with 500.0 already deposited."""
    account.deposit(500.0)
    return account


@pytest.fixture
def bob():
    """A second, empty account - used by the transfer tests."""
    return BankAccount("Bob")


# ----------------------------------------------------------------- deposit

@pytest.mark.parametrize("amount", [1, 100.0, 0.01, 999_999])
def test_deposit_increases_balance(account, amount):
    """Deposit `amount` and check the balance equals `amount`."""
    account.deposit(amount)

    assert account.get_balance() == amount


def test_deposit_records_transaction(account):
    """After one deposit, get_transaction_count() should be 1."""
    account.deposit(100.0)

    assert account.get_transaction_count() == 1


@pytest.mark.xfail(
    reason="BUG: deposit() does not raise ValueError for zero or negative amounts",
    strict=True
)
@pytest.mark.parametrize("bad_amount", [0, -1, -100])
@pytest.mark.edge
def test_deposit_invalid_amount_raises(account, bad_amount):
    """Depositing zero or a negative amount should raise ValueError."""
    with pytest.raises(ValueError):
        account.deposit(bad_amount)


# ---------------------------------------------------------------- withdraw

@pytest.mark.parametrize("amount, expected_balance", [
    (100.0, 400.0),
    (0.5, 499.5),
    (500.0, 0.0),
])
def test_withdraw_reduces_balance(funded_account, amount, expected_balance):
    """Withdraw `amount` from 500.0 and check the balance."""
    funded_account.withdraw(amount)

    assert funded_account.get_balance() == expected_balance


@pytest.mark.edge
def test_withdraw_negative_raises(funded_account):
    """Withdrawing a negative amount should raise ValueError."""
    with pytest.raises(ValueError):
        funded_account.withdraw(-10)


@pytest.mark.xfail(
    reason="BUG: withdraw() allows withdrawals greater than the account balance",
    strict=True
)
@pytest.mark.parametrize("amount", [501, 600, 1000])
@pytest.mark.edge
def test_withdraw_overdraft_raises(funded_account, amount):
    """Withdrawing more than the balance should raise ValueError."""
    with pytest.raises(ValueError):
        funded_account.withdraw(amount)


@pytest.mark.xfail(
    reason="BUG: withdraw() does not reject overdrafts, so the balance changes instead of remaining 500.0",
    strict=True
)
@pytest.mark.edge
def test_balance_unchanged_after_failed_withdraw(funded_account):
    """Try to withdraw 600 from 500. Whether or not it raises,
    the balance should still be 500.0 afterwards."""
    with pytest.raises(ValueError):
        funded_account.withdraw(600)

    assert funded_account.get_balance() == 500.0




# ---------------------------------------------------------------- transfer

def test_transfer_reduces_sender_balance(funded_account, bob):
    """After transferring 200 to bob, Alice should have 300."""
    funded_account.transfer(bob, 200)

    assert funded_account.get_balance() == 300.0

@pytest.mark.xfail(
    reason="BUG: transfer() withdraws from the sender but never deposits the amount into the target account",
    strict=True
)
def test_transfer_increases_receiver_balance(funded_account, bob):
    """After transferring 200 to bob, Bob should have 200."""
    funded_account.transfer(bob, 200)

    assert bob.get_balance() == 200.0


# ------------------------------------------------------- owner and summary

def test_get_owner(account):
    """get_owner() should return "Alice"."""
    assert account.get_owner() == "Alice"


def test_summary_contains_owner(account):
    """The summary string should contain "Alice"."""
    assert "Alice" in account.get_summary()


@pytest.mark.xfail(
    reason="BUG: get_summary() puts Balance before Owner instead of starting with Owner",
    strict=True
)
def test_summary_starts_with_owner(account):
    """The summary should start with "Owner:"."""
    assert account.get_summary().startswith("Owner:")


@pytest.mark.parametrize("amount", [10, 100, 500])
def test_summary_contains_balance(account, amount):
    """After depositing an amount, the summary should contain that number."""
    account.deposit(amount)

    assert str(amount) in account.get_summary()