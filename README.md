# NYC Teacher Union Value Analysis

**Do UFT union dues pay for themselves?** This project analyzes ~492,000 salary records for NYC public school teachers (FY2015-2025) to measure whether UFT-negotiated raises exceed the cost of union membership.

## Key Findings

| Finding | Detail |
|---|---|
| Raises exceed dues | Median annual increase ($2,300-$7,500) vs. UFT dues ($1,295-$1,661) |
| New teachers benefit most | 88% received raises even in the 0% contract year (FY2022), vs. 44% of tenured teachers |
| 2022-2027 contract improved outcomes | Consistent 3%+ annual raises after a flat FY2022; new teachers reach $100K faster |
| Additional Pay bridges gaps | Lump sums, settlements, and retroactive pay keep total compensation growing even when base salary is flat |

## Methodology

- **Dataset:** [NYC Citywide Payroll Data](https://data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e/about_data), filtered to full-time DOE teachers
- **Scope:** Three UFT contract periods (2009-2018, 2019-2021, 2022-2027)
- **Approach:** Year-over-year salary deltas compared against UFT contract schedule rates, segmented by tenure (0-5 years vs. 6+)
- **Metrics:** Median values used throughout to reduce the effect of outliers

### Data Cleaning

- Filtered to full-time teachers employed by the Department of Education (Pedagogical)
- Removed teachers who ceased employment and those with year-over-year salary decreases to focus on typical career progression
- Created anonymized Employee IDs from name and hire date combinations for longitudinal tracking
- Engineered salary delta features and computed UFT union dues by fiscal year
- Treated negative Additional Pay values as null to avoid skewing compensation calculations

## Getting Started

```bash
git clone https://github.com/Promeos/nyc-teacher-union-value-analysis.git
cd nyc-teacher-union-value-analysis
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Download the dataset from [NYC Citywide Payroll Data (Fiscal Year)](https://data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e/about_data) and place it in the project directory, then open [`nyc_teacher_salary_analysis.ipynb`](nyc_teacher_salary_analysis.ipynb) to reproduce the analysis.

## Data Dictionary

| Column | Description | Type |
|---|---|---|
| Fiscal Year | Fiscal year of the payroll record | Number |
| Agency Name | Payroll agency the employee works for | Text |
| Agency Start Date | Date employee began at their current agency | Date |
| Work Location Borough | Borough of primary work location | Text |
| Title Description | Civil service title description | Text |
| Leave Status as of June 30 | Active, Ceased, or On Leave at fiscal year close | Text |
| Base Salary | Base salary assigned to the employee | Number |
| Pay Basis | Hourly, per diem, or annual | Text |
| Regular Hours | Regular hours worked in the fiscal year | Number |
| Regular Gross Paid | Base salary amount paid during the fiscal year | Number |
| OT Hours | Overtime hours worked | Number |
| Total OT Paid | Total overtime pay | Number |
| Total Other Pay | Differentials, lump sums, retroactive pay, settlements, bonuses, etc. | Number |

## License

This project is licensed under the MIT License.

## Acknowledgments

- [NYC Open Data](https://opendata.cityofnewyork.us/) for the Citywide Payroll Data (Fiscal Year) dataset
- [United Federation of Teachers (UFT)](https://www.uft.org/) salary schedules and contract documents (2009-2018, 2018-2027)
