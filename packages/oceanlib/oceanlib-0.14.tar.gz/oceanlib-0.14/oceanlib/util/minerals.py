# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 22:43:58 2017

@author: Sonam Srivastava
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
from math import ceil
from lxml import etree
import sqlite3
import pandas as pd
from get_data import *
import good_morning as gm

def create_components_db():
    '''
    This function pushes the coponents of S&P 500 into a database named
    SNP_COMPONENTS
    '''
    conn = sqlite3.connect('database.db')
    df = obtain_parse_wiki_snp500()
    df.to_sql("SNP_COMPONENTS", conn, if_exists="replace")
    conn.commit()
    conn.close()
    print('created database of S&P 500 components')


def create_daily_ohlc_db(num_years=5):
    '''
    This function downloads the daily OHLC for the coponents of S&P 500
    and pushes it into a database named
    DAILY_OHLC
    '''
    conn = sqlite3.connect('snp_database.db')
    for symbol in get_components().ticker:
        df = get_data_daily(symbol, num_years=num_years)
        df['symbol'] = symbol
        df.to_sql("DAILY_OHLC", conn, if_exists="append")
        print('added daily OHLC for {} {}'.format(symbol, len(df)))
    conn.close()


def create_minbin_ohlc_db(num_days=20):
    '''
    This function downloads the minute binned OHLC for the coponents of S&P 500
    and pushes it into a database named
    MINBIN_OHLC
    '''
    conn = sqlite3.connect('snp_database.db')
    for symbol in get_components().ticker:
        df = get_data_minutebinned(symbol, num_days=20)
        df['symbol'] = symbol
        df.to_sql("MINBIN_OHLC", conn, if_exists="append")
        print('added minute binned OHLC for {}'.format(symbol))
    conn.close()


def download_fundamentals(symbol='AAPL'):
    '''
    This function downloads the fundamental data for the coponents of S&P 500
    from morningstar API and pushes it into separate databases called
    CASH_FLOW, BALANCE_SHEET and INCOME_STATEMENT
    '''
    conn = sqlite3.connect('snp_database.db')
    kr = gm.FinancialsDownloader()
    kr_frames = kr.download('AAPL')
    cash_flow = kr_frames['cash_flow'].drop('parent_index', axis=1)
    cash_flow['symbol'] = symbol
    income_statement = kr_frames['income_statement'].drop(
        'parent_index', axis=1)
    income_statement['symbol'] = symbol
    balance_sheet = kr_frames['balance_sheet'].drop('parent_index', axis=1)
    balance_sheet['symbol'] = symbol
    cash_flow.to_sql("CASH_FLOW", conn, if_exists="append")
    income_statement.to_sql("INCOME_STATEMENT", conn, if_exists="append")
    balance_sheet.to_sql("BALANCE_SHEET", conn, if_exists="append")
    conn.close()
    print('added fundamentals for {}'.format(symbol))


def create_fundamentals_db():
    '''
    This function updates the fundamentaldb for all stocks
    '''
    for symbol in get_components().ticker:
        download_fundamentals(symbol)


def get_components():
    '''
    This function queries the SNP_COMPONETS and returns all components
    '''
    conn = sqlite3.connect('snp_database.db')
    df = pd.read_sql_query("SELECT * FROM SNP_COMPONENTS", conn)
    conn.close()
    return df


def get_daily_ohlc(symbol):
    '''
    This function queries the DAILY_OHLC to get daily OHLC for a symbol
    '''
    conn = sqlite3.connect('snp_database.db')
    df = pd.read_sql_query(
        'select * from DAILY_OHLC where symbol=\'{}\''.format(symbol), conn)
    conn.close()
    return df


def get_minbin_ohlc(symbol):
    '''
    This function queries the MINBIN_OHLC to get minute binned OHLC 
    for a symbol
    '''
    conn = sqlite3.connect('snp_database.db')
    df = pd.read_sql_query(
        'select * from MINBIN_OHLC where symbol=\'{}\''.format(symbol), conn)
    conn.close()
    return df


def get_cashflow(symbol):
    '''
    This function queries the CASH_FLOW to cash flow data for a symbol
    '''
    conn = sqlite3.connect('snp_database.db')
    df = pd.read_sql_query(
        'select * from CASH_FLOW where symbol=\'{}\''.format(symbol), conn)
    conn.close()
    return df


def get_balancesheet(symbol):
    '''
    This function queries the BALANCE_SHEET to balance sheet data for a symbol
    '''
    conn = sqlite3.connect('snp_database.db')
    df = pd.read_sql_query(
        'select * from BALANCE_SHEET where symbol=\'{}\''.format(symbol), conn)
    conn.close()
    return df


def get_incomestatement(symbol):
    '''
    This function queries the INCOME_STATEMENT to income statement data 
    for a symbol
    '''
    conn = sqlite3.connect('snp_database.db')
    df = pd.read_sql_query(
        'select * from INCOME_STATEMENT where symbol=\'{}\''.format(symbol), conn)
    conn.close()
    return df


if __name__ == '__main__':
    create_components_db()
    create_daily_ohlc_db(num_years=25)
    create_minbin_ohlc_db(num_days=20)
    create_fundamentals_db()
    print(get_daily_ohlc('AAPL'))
    print(get_minbin_ohlc('AAPL'))
    print(get_cashflow('AAPL'))
    print(get_balancesheet('AAPL'))
    print(get_incomestatement('AAPL'))
