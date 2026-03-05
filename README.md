![nyc-teacher-pay-header](./visuals/nyc-teacher-pay-header.png)

![nyc-teacher-compensation-summary](./visuals/nyc-teacher-compensation-summary.png)

## Project Description

This project aims to provide NYC teachers with a comprehensive understanding of their expected annual salary growth, factoring in the impact of United Federation of Teachers salary contracts from 2014 to 2023. By offering insights into the relationship between salary contracts and individual compensation, the objective is to empower teachers to improve their financial well-being and evaluate the value they receive from UFT-negotiated contracts.

## Table of Contents

- [Getting Started](#getting-started)
- [Data Sources](#acquire)
- [Data Dictionary](#data-dictionary)
- [Data Cleaning](#data-cleaning)
- [Analysis](#analysis)
- [Results](#results)
- [Visualizations](#visualizations)
- [License](#license)
- [Acknowledgments](#acknowledgments)

### Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/promeos/Teacher_Payroll_Analysis.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Teacher_Payroll_Analysis
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

6. Download the dataset from [NYC Citywide Payroll Data (Fiscal Year)](https://data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e/about_data) and place it in the project directory.

7. Open `nyc_teacher_salary_analysis.ipynb` and run the cells to reproduce the analysis.

### Data Dictionary

| Column Name              | Description                                            | Type       |
|--------------------------|--------------------------------------------------------|------------|
| Fiscal Year              | Fiscal Year                                            | Number     |
| Payroll Number           | Payroll Number                                         | Number     |
| Agency Name              | The Payroll agency that the employee works for         | Plain Text |
| Last Name                | Last name of employee                                  | Plain Text |
| First Name               | First name of employee                                 | Plain Text |
| Mid Init                 | Middle initial of employee                             | Plain Text |
| Agency Start Date        | Date which employee began working for their current agency | Date & Time |
| Work Location Borough    | Borough of employee's primary work location            | Plain Text |
| Title Description        | Civil service title description of the employee        | Plain Text |
| Leave Status as of June 30| Status of employee as of the close of the relevant fiscal year: Active, Ceased, or On Leave | Plain Text |
| Base Salary              | Base Salary assigned to the employee                    | Number     |
| Pay Basis                | Lists whether the employee is paid on an hourly, per diem, or annual basis | Plain Text |
| Regular Hours            | Number of regular hours employee worked in the fiscal year | Number     |
| Regular Gross Paid       | The amount paid to the employee for base salary during the fiscal year | Number     |
| OT Hours                 | Overtime Hours worked by employee in the fiscal year    | Number     |
| Total OT Paid            | Total overtime pay paid to the employee in the fiscal year | Number     |
| Total Other Pay          | Includes any compensation in addition to gross salary and overtime pay, i.e., Differentials, lump sums, uniform allowance, meal allowance, retroactive pay increases, settlement amounts, and bonus pay, if applicable | Number     |


### Data Cleaning

- Filtered the NYC Citywide Payroll dataset to full-time teachers employed by the Department of Education (Pedagogical).
- Removed teachers who ceased employment and those with year-over-year salary decreases to focus on typical career progression.
- Created anonymized Employee IDs from name and hire date combinations for longitudinal tracking.
- Engineered salary delta features (year-over-year percentage and monetary changes) and computed UFT union dues by fiscal year.
- Treated negative Additional Pay values as null to avoid skewing compensation calculations.

### Analysis

- Compared year-over-year salary increases against UFT contract schedule rates across three contract periods (2009-2018, 2019-2021, 2022-2027).
- Analyzed whether annual salary monetary increases cover UFT union dues.
- Segmented all analyses by employment tenure (0-5 years vs. 6+ years) to identify differences between newer and experienced teachers.
- Examined both cumulative and year-over-year salary growth trends using median values to reduce the effect of outliers.

### Results

- Most teachers receive salary increases at or above the UFT schedule rate each year.
- Teachers with 0-5 years of tenure see larger percentage salary increases than their tenured (6+) peers, reflecting step increases on the salary schedule.
- The 2022-2027 contract period shows improved total compensation outcomes compared to prior periods.
- Annual salary monetary increases typically exceed UFT union dues, meaning teachers retain a net benefit from negotiated raises.
- New teachers can reach $100K in base salary with fewer years of service under the current contract.

### Visualizations

All visualizations are available in the analysis notebook [`nyc_teacher_salary_analysis.ipynb`](nyc_teacher_salary_analysis.ipynb), including:
- Salary distributions by contract period and employment category
- Year-over-year salary increase comparisons against UFT schedule rates
- Cumulative and annual compensation growth trends by tenure group
- Proportion of teachers receiving salary increases each fiscal year

### License

This project is licensed under the MIT License.

### Acknowledgments

- [NYC Open Data](https://opendata.cityofnewyork.us/) for the Citywide Payroll Data (Fiscal Year) dataset.
- [United Federation of Teachers (UFT)](https://www.uft.org/) salary schedules and contract documents (2009-2018, 2018-2027).
