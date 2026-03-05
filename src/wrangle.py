import os
import numpy as np
import pandas as pd


COLS_TO_USE = [
    'Fiscal Year',
    'Agency Name',
    'Last Name',
    'First Name',
    'Mid Init',
    'Agency Start Date',
    'Title Description',
    'Leave Status as of June 30',
    'Base Salary',
    'Total Other Pay',
]

COLS_ORDER = [
    'Fiscal Year',
    'Employee ID',
    'Hire Date',
    'Hire Year',
    'Years of Employment',
    'Employment Category',
    'Salary',
    'Additional Pay',
    'UFT Dues',
    'Net Salary',
    'Previous Salary',
    'Total Pay',
    'Salary Category',
    'Fiscal Year Rate',
    'Effective Rate',
    'Salary Delta',
    'Net Salary Delta',
    'Total Pay to Previous Salary Delta',
    'Salary Monetary Diff',
    'Net Salary Monetary Diff',
    'Contract Period',
    'Additional Pay Category',
    'Salary Delta Category',
    'Delta Category',
    'Compensation Category',
    'Salary Monetary Diff Category',
    'Salary at or Above Schedule Rate',
    'Compensation at or Above Schedule Rate',
    'Salary Monetary Diff Covers UFT Dues',
    'Total Pay Covers UFT Dues',
]

UNION_DUES_BY_YEAR = {
    2014: 51.87 * 24,
    2015: 53.95 * 24,
    2016: 56.10 * 24,
    2017: 57.19 * 24,
    2018: 58.31 * 24,
    2019: 59.64 * 24,
    2020: 61 * 24,
    2021: 62.39 * 24,
    2022: 63.81 * 24,
    2023: 65.50 * 24,
    2024: 65.60 + 66.94 * 23,  # 1 check @ $65.60 + 23 checks @ $66.94
    2025: 66.94 * 3 + 68.97 * 14 + 70.70 * 7,  # 3 + 14 + 7 checks across rate tiers
}

FISCAL_YEAR_RATES = {
    2014: 1,
    2015: 3,
    2016: 3.5,
    2017: 4.5,
    2018: 5,
    2019: 2,
    2020: 2.5,
    2021: 3,
    2022: 0,
    2023: 3,
    2024: 3,
    2025: 3,
}

# Bin definitions
EMPLOYMENT_BINS = [-1, 5, 70]
EMPLOYMENT_LABELS = ['0-5', '6+']

CONTRACT_BINS = [2009, 2018, 2021, 2027]
CONTRACT_LABELS = ["2009-2018", "2019-2021", "2022-2027"]

SALARY_BINS = [40000, 60000, 80000, 100000, 120000, 200000]
SALARY_LABELS = ['40k-60k', '60k-80k', '80k-100k', '100k-120k', '120k+']

ADDITIONAL_PAY_BINS = [-1, 0, 1000, 300000]
ADDITIONAL_PAY_LABELS = ['$0', '0-$1K', '$1k+']

DELTA_BINS = [-1, 0, 5, 10, 90]
DELTA_LABELS = ['0%', '0-5%', '5-10%', '10+%']

SIMPLIFIED_DELTA_BINS = [-1, 0, 90]
SIMPLIFIED_DELTA_LABELS = ['No Change', 'Salary Increased']

MONETARY_DIFF_BINS = [-1, 0, 5000, 10000, 70000]
MONETARY_DIFF_LABELS = ['0', '0-$5k', '$5k-$10k', '$10k+']

EFFECTIVE_RATE_BINS = [-1, -0.0004, 0, 90]
EFFECTIVE_RATE_LABELS = ['Compensation Decreased', 'No Change', 'Compensation Increased']


def read_teacher_data(cached_file='./data/teachers_payroll.parquet'):
    '''
    Reads and returns the NYC teachers payroll data from a parquet file.

    Parameters:
    - cached_file (str): Path to the cached parquet file containing NYC teachers payroll data.

    Returns:
    - pd.DataFrame: DataFrame containing NYC teachers payroll data.
    '''
    df = pd.read_parquet(cached_file)

    df['Fiscal Year'] = df['Fiscal Year'].astype('Int16')
    df['Hire Date'] = pd.to_datetime(df['Hire Date'])
    df['Salary'] = df['Salary'].astype('Int32')
    df['Hire Year'] = df['Hire Year'].astype('Int16')
    df['Years of Employment'] = df['Years of Employment'].astype('Int16')
    df['Employee ID'] = df['Employee ID'].astype('O')
    df['Salary at or Above Schedule Rate'] = df['Salary at or Above Schedule Rate'].astype('Int8')
    df['Compensation at or Above Schedule Rate'] = df['Compensation at or Above Schedule Rate'].astype('Int8')
    df['Salary Monetary Diff Covers UFT Dues'] = df['Salary Monetary Diff Covers UFT Dues'].astype('Int8')
    df['Total Pay Covers UFT Dues'] = df['Total Pay Covers UFT Dues'].astype('Int8')

    df['Employment Category'] = pd.Categorical(df['Employment Category'], categories=EMPLOYMENT_LABELS, ordered=True)
    df['Contract Period'] = pd.Categorical(df['Contract Period'], categories=CONTRACT_LABELS, ordered=True)
    df['Salary Category'] = pd.Categorical(df['Salary Category'], categories=SALARY_LABELS, ordered=True)
    df['Additional Pay Category'] = pd.Categorical(df['Additional Pay Category'], categories=ADDITIONAL_PAY_LABELS, ordered=True)
    df['Salary Delta Category'] = pd.Categorical(df['Salary Delta Category'], categories=DELTA_LABELS, ordered=True)
    df['Delta Category'] = pd.Categorical(df['Delta Category'], categories=SIMPLIFIED_DELTA_LABELS, ordered=True)
    df['Salary Monetary Diff Category'] = pd.Categorical(df['Salary Monetary Diff Category'],
                                                         categories=MONETARY_DIFF_LABELS, ordered=True)
    df['Compensation Category'] = pd.Categorical(df['Compensation Category'], categories=EFFECTIVE_RATE_LABELS, ordered=True)

    return df


def _load_and_filter_payroll(file_path):
    '''Reads city payroll CSV and filters to full-time teachers.'''
    data = pd.read_csv(file_path, usecols=COLS_TO_USE, engine='pyarrow')

    # Handle dollar-formatted columns (e.g., "$65,921.00" → 65921.0)
    for col in ['Base Salary', 'Total Other Pay']:
        if data[col].dtype == object:
            data[col] = data[col].str.replace(r'[$,]', '', regex=True).astype(float)

    conditions = (
        (data['Agency Name'] == 'DEPT OF ED PEDAGOGICAL') &
        (data['Title Description'] == 'TEACHER') &
        (data['Leave Status as of June 30'] != 'CEASED')
    )

    cols_to_drop = ['Agency Name', 'Title Description', 'Leave Status as of June 30']
    df = data[conditions].drop(columns=cols_to_drop)

    df = df.rename(columns={
        'Agency Start Date': 'Hire Date',
        'Base Salary': 'Salary',
        'Total Other Pay': 'Additional Pay',
    })

    return df


def _clean_teacher_data(df):
    '''Parses dates, calculates tenure, removes outliers, and creates employee keys.'''
    df['Hire Date'] = pd.to_datetime(df['Hire Date'], errors='coerce')
    df['Hire Year'] = df['Hire Date'].dt.year.astype('Int16')
    df['Years of Employment'] = (df['Fiscal Year'] - df['Hire Year']).astype('Int8')

    df = df[df['Years of Employment'] <= 65]\
            .sort_values('Fiscal Year')\
            .reset_index(drop=True)

    df[['Last Name', 'First Name', 'Mid Init']] = df[['Last Name', 'First Name', 'Mid Init']].apply(
        lambda x: x.str.replace(' ', '').str.strip().str.title().fillna('None')
    )
    df['FirstMidLastStart'] = df['First Name'] + df['Mid Init'] + df['Last Name'] + df['Hire Date'].astype(str)
    df = df.drop(columns=['Last Name', 'First Name', 'Mid Init'])
    df = df.sort_values(by=['FirstMidLastStart', 'Fiscal Year']).reset_index(drop=True)

    return df


def _engineer_salary_features(df):
    '''Calculates salary deltas, union dues, and filters out salary decreases.'''
    df['UFT Dues'] = df['Fiscal Year'].map(UNION_DUES_BY_YEAR)
    df['Additional Pay'] = np.where(df['Additional Pay'] < 0, np.nan, df['Additional Pay'])
    df['Net Salary'] = df['Salary'] - df['UFT Dues']
    df['Total Pay'] = df['Salary'] + df['Additional Pay']

    df['Salary Delta'] = df.groupby(by=['FirstMidLastStart'])['Salary'].pct_change() * 100
    df['Salary Monetary Diff'] = df.groupby(by=['FirstMidLastStart'])['Salary'].diff()
    df['Net Salary Delta'] = df.groupby(by=['FirstMidLastStart'])['Net Salary'].pct_change() * 100
    df['Net Salary Monetary Diff'] = df.groupby(by=['FirstMidLastStart'])['Net Salary'].diff()

    delta_cols = ['Salary Delta', 'Salary Monetary Diff', 'Net Salary Delta', 'Net Salary Monetary Diff']
    df[delta_cols] = df[delta_cols].round(4)

    df['Previous Salary'] = df.groupby('FirstMidLastStart')['Salary'].shift()
    df['Total Pay to Previous Salary Delta'] = (((df['Total Pay'] / df['Previous Salary']) - 1) * 100).round(4)

    # Remove teachers with any YoY salary decrease
    df['Salary Delta Flag'] = np.where((df['Salary Delta'] >= 0) | (df['Salary Delta'].isna()), 1, 0)
    df_salary_filter = df.groupby('FirstMidLastStart')['Salary Delta Flag'].all().reset_index()
    df = df.merge(df_salary_filter, left_on='FirstMidLastStart', right_on='FirstMidLastStart', how='left')
    df = df[df['Salary Delta Flag_y'] == True]
    df = df.dropna(subset=['Salary Delta']).reset_index(drop=True).sort_values(by=['FirstMidLastStart', 'Fiscal Year'])

    # Assign unique Employee IDs
    df['Employee ID'], _ = pd.factorize(df['FirstMidLastStart'], sort=True)
    df['Employee ID'] = df['Employee ID'].astype('O')
    df = df.drop(columns=['FirstMidLastStart', 'Salary Delta Flag_x', 'Salary Delta Flag_y'])
    df = df.sort_values(by=['Employee ID', 'Fiscal Year']).reset_index(drop=True)

    df['Fiscal Year Rate'] = df['Fiscal Year'].map(FISCAL_YEAR_RATES.get)
    df['Effective Rate'] = np.where(
        (df['Salary Delta'] == 0) | (df['Salary Delta'].round(1) < df['Fiscal Year Rate']),
        df['Total Pay to Previous Salary Delta'].round(),
        df['Salary Delta'].round(1),
    )

    return df


def _create_categorical_features(df):
    '''Creates binned categorical features from numeric columns.'''
    df['Employment Category'] = pd.cut(df['Years of Employment'], bins=EMPLOYMENT_BINS, labels=EMPLOYMENT_LABELS)
    df['Contract Period'] = pd.cut(df['Fiscal Year'], bins=CONTRACT_BINS, labels=CONTRACT_LABELS)
    df['Salary Category'] = pd.cut(df['Salary'], bins=SALARY_BINS, labels=SALARY_LABELS)
    df['Additional Pay Category'] = pd.cut(df['Additional Pay'], bins=ADDITIONAL_PAY_BINS, labels=ADDITIONAL_PAY_LABELS)
    df['Salary Delta Category'] = pd.cut(df['Salary Delta'], bins=DELTA_BINS, labels=DELTA_LABELS)
    df['Delta Category'] = pd.cut(df['Salary Delta'], bins=SIMPLIFIED_DELTA_BINS, labels=SIMPLIFIED_DELTA_LABELS)
    df['Salary Monetary Diff Category'] = pd.cut(df['Salary Monetary Diff'], bins=MONETARY_DIFF_BINS, labels=MONETARY_DIFF_LABELS)
    df['Compensation Category'] = pd.cut(df['Effective Rate'], bins=EFFECTIVE_RATE_BINS, labels=EFFECTIVE_RATE_LABELS)

    df['Employment Category'] = pd.Categorical(df['Employment Category'], categories=EMPLOYMENT_LABELS, ordered=True)
    df['Contract Period'] = pd.Categorical(df['Contract Period'], categories=CONTRACT_LABELS, ordered=True)
    df['Salary Category'] = pd.Categorical(df['Salary Category'], categories=SALARY_LABELS, ordered=True)
    df['Additional Pay Category'] = pd.Categorical(df['Additional Pay Category'], categories=ADDITIONAL_PAY_LABELS, ordered=True)
    df['Salary Delta Category'] = pd.Categorical(df['Salary Delta Category'], categories=DELTA_LABELS, ordered=True)
    df['Delta Category'] = pd.Categorical(df['Delta Category'], categories=SIMPLIFIED_DELTA_LABELS, ordered=True)
    df['Salary Monetary Diff Category'] = pd.Categorical(df['Salary Monetary Diff Category'], categories=MONETARY_DIFF_LABELS, ordered=True)
    df['Compensation Category'] = pd.Categorical(df['Compensation Category'], categories=EFFECTIVE_RATE_LABELS, ordered=True)

    return df


def _add_rate_flags(df):
    '''Adds boolean flags comparing salary increases to schedule rates and union dues.'''
    df['Salary at or Above Schedule Rate'] = np.where((df['Salary Delta'].round(2) >= df['Fiscal Year Rate']), 1, 0)
    df['Compensation at or Above Schedule Rate'] = np.where(df['Effective Rate'] >= df['Fiscal Year Rate'], 1, 0)
    df['Salary Monetary Diff Covers UFT Dues'] = np.where(df['Salary Monetary Diff'] >= df['UFT Dues'], 1, 0)
    df['Total Pay Covers UFT Dues'] = np.where((df['Salary Monetary Diff'] + df['Additional Pay']) >= df['UFT Dues'], 1, 0)

    return df


def read_and_filter_data(file_path='city_payroll_data.csv', cached_file='./data/teachers_payroll.parquet'):
    '''
    Reads, filters, and returns NYC teachers payroll data.
    If a cached parquet file exists, it is used; otherwise, the data is loaded from CSV and processed.

    Parameters:
    - file_path (str): Path to the city payroll data CSV file.
    - cached_file (str): Path to the cached parquet file for teachers payroll data.

    Returns:
    - pd.DataFrame: DataFrame containing filtered and processed NYC teachers payroll data.
    '''
    if os.path.exists(cached_file):
        return read_teacher_data(cached_file)

    df = _load_and_filter_payroll(file_path)
    df = _clean_teacher_data(df)
    df = _engineer_salary_features(df)
    df = _create_categorical_features(df)
    df = _add_rate_flags(df)

    df = df[COLS_ORDER]
    df.to_parquet('./data/teachers_payroll.parquet', index=False)

    return df
