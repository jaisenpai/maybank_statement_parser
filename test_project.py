import pytest
import os
from project import data_clean, calculate_initial_balance,rename_csv, data_calculation, generate_csv

def test_data_clean():

    assert data_clean("1,200.50+") == 1200.50
    assert data_clean("74.65-") == -74.65
    assert data_clean("") == 0.0
    assert data_clean(None) == 0.0
    assert data_clean("cat") == 0.0

def test_calculate_initial_balance():

    mock_data1 = {"transaction": -50.0,"balance": 100.0}
    assert calculate_initial_balance(mock_data1) == 150

    mock_data2 = {"transaction": -5.43,"balance": 241.56}
    assert calculate_initial_balance(mock_data2) == 246.99

    mock_data3 = {"transaction": 249.00,"balance": 1231.02}
    assert calculate_initial_balance(mock_data3) == 982.02

def test_data_calculation () :

    #generate mock data for test
    mock_data = [
        {"transaction": 0.0, "balance": 1000.0},   # Opening
        {"transaction": 500.0, "balance": 1500.0},  # Deposit
        {"transaction": -200.0, "balance": 1300.0}, # Withdrawal
        {"transaction": -50.0, "balance": 1250.0}   # Withdrawal
    ]

    assert data_calculation (mock_data) == (500.0, 250.0)

def test_generate_csv_availability(tmp_path):

    #create temporary path and mock data
    test_csv = tmp_path / "output_check.csv"
    mock_data = [{"date": "01/01",
                  "description": "Test",
                  "transaction": 0.0,
                  "balance": 0.0}
                  ]

    #run function and check availability
    generate_csv(mock_data, test_csv)
    assert os.path.exists(test_csv)

