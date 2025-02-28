import pytest
from project import get_vested_stocks, get_date, get_current_rate, fetch_exchange_rate, calculate_tax, get_release_price
import sys
import re
import requests
from unittest.mock import patch, MagicMock

def test_get_vested_stocks_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "10")
    assert get_vested_stocks() == 10


def test_get_vested_stocks_invalid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "cat")
    with pytest.raises(SystemExit):
        get_vested_stocks()

def test_get_date_vdate_invform(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2000.09.11")
    with pytest.raises(SystemExit):
        get_date()

def test_get_date_invdate_vform(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2026-01-01")
    with pytest.raises(SystemExit):
        get_date()

def test_get_date_vdate_vform(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2000-09-11")
    assert get_date() == "2000-09-11"


def test_get_current_rate_api():
    assert get_current_rate('2025-01-06') == 499


def test_get_current_rate_fallback(monkeypatch):
    with patch('zeep.Client', side_effect=Exception("Simulated API failure")):
        with patch('project.requests.get') as mock_requests_get:
            mock_requests_get.return_value.text = '''
                <table>
                    <tr><td>GBP</td><td>488,90</td></tr>
                </table>
            '''
            exchange_rate = get_current_rate("2025-02-21")
            assert exchange_rate == 488.9


def test_calculate_tax():
    vested_stocks = 85
    rate = 479.85
    release_price = 6.940851

    expected_szja = vested_stocks*rate*release_price*0.15*0.89
    expected_szocho = vested_stocks*rate*release_price*0.13*0.89

    szja,szocho = calculate_tax(vested_stocks, rate, release_price)
    assert szja == pytest.approx(expected_szja, rel=1e-6)
    assert szocho == pytest.approx(expected_szocho, rel=1e-6)


def test_get_release_price_inv(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'cat')
    with pytest.raises(SystemExit):
        get_release_price()

def test_release_price_v(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '6.940851')
    assert get_release_price() == 6.940851



