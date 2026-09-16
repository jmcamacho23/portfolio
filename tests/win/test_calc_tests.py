"""
Desktop application tests using Pywinauto and Pytest
Application: Calculator (Windows)
Author: Jose Camacho
"""

import pytest
from helpers.winapp_helper import CalculatorPage


@pytest.fixture(scope="function")
def calc_page():
    page = CalculatorPage(app_name='Calculator').wait_for_ready()
    yield page

    page.close()

@pytest.mark.calcy
def test_calculator_addition(calc_page, first_num='Seven', second_num='Eight', result='15'):
    calc_page.click_button_by_name(first_num)
    calc_page.click_button_by_name("Plus")
    calc_page.click_button_by_name(second_num)
    calc_page.click_button_by_name("Equals")

    assert calc_page.get_calculator_result() == result

@pytest.mark.calcy
def test_calculator_subtraction(calc_page, first_num='Nine', second_num='Two', result='7'):
    calc_page.click_button_by_name(first_num)
    calc_page.click_button_by_name('Minus')
    calc_page.click_button_by_name(second_num)
    calc_page.click_button_by_name('Equals')

    assert calc_page.get_calculator_result() == result
