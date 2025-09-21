"""
03. Aggregation Functions and GROUP BY in DuckDB
This script demonstrates aggregation functions, GROUP BY, and HAVING clauses.

Topics covered:
- Basic aggregation functions (COUNT, SUM, AVG, MIN, MAX)
- GROUP BY operations
- HAVING clause
- Multiple column grouping
- Window functions
- String aggregation
- Statistical functions
"""

from db_utils import print_query_results

def basic_aggregation_examples():
    """Demonstrate basic aggregation functions."""
    print("=== Basic Aggregation Functions ===")
    
    # 1. Count all employees
    print_query_results(
        "SELECT COUNT(*) AS total_employees FROM employees",
        "1. Total Employee Count"
    )
    
    # 2. Count non-null values
    print_query_results(
        """
        SELECT 
            COUNT(*) AS total_employees,
            COUNT(phone_number) AS employees_with_phone,
            COUNT(manager_id) AS employees_with_manager
        FROM employees
        """,
        "2. Count with NULL handling"
    )
    
    # 3. Basic statistical functions
    print_query_results(
        """
        SELECT 
            COUNT(*) AS employee_count,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_salary
        FROM employees
        """,
        "3. Salary Statistics"
    )
    
    # 4. DISTINCT counts
    print_query_results(
        """
        SELECT 
            COUNT(DISTINCT department_id) AS unique_departments,
            COUNT(DISTINCT job_id) AS unique_jobs,
            COUNT(DISTINCT manager_id) AS unique_managers
        FROM employees
        """,
        "4. Distinct Counts"
    )

def group_by_examples():
    """Demonstrate GROUP BY operations."""
    print("\n=== GROUP BY Examples ===")
    
    # 1. Group by single column
    print_query_results(
        """
        SELECT 
            department_id,
            COUNT(*) AS employee_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY department_id
        ORDER BY department_id
        """,
        "1. Employees by Department"
    )
    
    # 2. Group by with JOINs
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY employee_count DESC
        """,
        "2. Department Statistics with Names"
    )
    
    # 3. Multiple column grouping
    print_query_results(
        """
        SELECT 
            d.department_name,
            j.job_title,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        JOIN jobs j ON e.job_id = j.job_id
        GROUP BY d.department_id, d.department_name, j.job_id, j.job_title
        HAVING COUNT(e.employee_id) > 0
        ORDER BY d.department_name, employee_count DESC
        """,
        "3. Employees by Department and Job"
    )

def having_clause_examples():
    """Demonstrate HAVING clause for filtering groups."""
    print("\n=== HAVING Clause Examples ===")
    
    # 1. Departments with more than 3 employees
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        HAVING COUNT(e.employee_id) > 3
        ORDER BY employee_count DESC
        """,
        "1. Departments with > 3 Employees"
    )
    
    # 2. High-paying departments (average salary > 8000)
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        HAVING AVG(e.salary) > 8000
        ORDER BY avg_salary DESC
        """,
        "2. High-Paying Departments (Avg > 8000)"
    )
    
    # 3. Combined WHERE and HAVING
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        WHERE e.salary > 5000  -- Filter individual records first
        GROUP BY d.department_id, d.department_name
        HAVING COUNT(e.employee_id) >= 2  -- Then filter groups
        ORDER BY avg_salary DESC
        """,
        "3. Well-Paid Employees by Department (Combined WHERE and HAVING)"
    )

def advanced_aggregation_examples():
    """Demonstrate advanced aggregation techniques."""
    print("\n=== Advanced Aggregation Examples ===")
    
    # 1. Percentiles and quartiles
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(MIN(e.salary), 2) AS min_salary,
            ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY e.salary), 2) AS q1_salary,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY e.salary), 2) AS median_salary,
            ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY e.salary), 2) AS q3_salary,
            ROUND(MAX(e.salary), 2) AS max_salary
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        HAVING COUNT(e.employee_id) >= 3
        ORDER BY median_salary DESC
        """,
        "1. Salary Quartiles by Department"
    )
    
    # 2. String aggregation
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            STRING_AGG(e.first_name || ' ' || e.last_name, ', ' ORDER BY e.salary DESC) AS employees
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        HAVING COUNT(e.employee_id) BETWEEN 2 AND 5
        ORDER BY employee_count DESC
        """,
        "2. Employee Names by Department"
    )
    
    # 3. Conditional aggregation
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS total_employees,
            COUNT(CASE WHEN e.salary > 8000 THEN 1 END) AS high_earners,
            COUNT(CASE WHEN e.salary <= 8000 THEN 1 END) AS regular_earners,
            ROUND(100.0 * COUNT(CASE WHEN e.salary > 8000 THEN 1 END) / COUNT(e.employee_id), 1) AS high_earner_percentage
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY high_earner_percentage DESC
        """,
        "3. High Earner Analysis by Department"
    )

def window_function_examples():
    """Demonstrate window functions for advanced analytics."""
    print("\n=== Window Function Examples ===")
    
    # 1. Running totals
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name,
            e.salary,
            SUM(e.salary) OVER (PARTITION BY e.department_id ORDER BY e.salary) AS running_salary_total,
            ROW_NUMBER() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS salary_rank_in_dept
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        WHERE e.department_id IN (3, 5, 6)  -- Limit to a few departments
        ORDER BY e.department_id, e.salary DESC
        """,
        "1. Running Totals and Rankings by Department"
    )
    
    # 2. Salary percentiles within department
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name,
            e.salary,
            ROUND(PERCENT_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary) * 100, 1) AS salary_percentile,
            NTILE(4) OVER (PARTITION BY e.department_id ORDER BY e.salary) AS salary_quartile
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        WHERE e.department_id IN (5, 6, 10)  -- Focus on departments with multiple employees
        ORDER BY e.department_id, e.salary DESC
        """,
        "2. Salary Percentiles and Quartiles"
    )
    
    # 3. Compare to averages
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name,
            e.salary,
            ROUND(AVG(e.salary) OVER (PARTITION BY e.department_id), 2) AS dept_avg_salary,
            ROUND(e.salary - AVG(e.salary) OVER (PARTITION BY e.department_id), 2) AS diff_from_dept_avg,
            ROUND(AVG(e.salary) OVER (), 2) AS company_avg_salary,
            ROUND(e.salary - AVG(e.salary) OVER (), 2) AS diff_from_company_avg
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        ORDER BY d.department_name, e.salary DESC
        LIMIT 20
        """,
        "3. Salary Comparison to Averages"
    )

def regional_analysis_examples():
    """Demonstrate complex aggregation across multiple tables."""
    print("\n=== Regional Analysis Examples ===")
    
    # 1. Employee distribution by region
    print_query_results(
        """
        SELECT 
            r.region_name,
            COUNT(e.employee_id) AS employee_count,
            COUNT(DISTINCT d.department_id) AS department_count,
            COUNT(DISTINCT l.location_id) AS location_count,
            ROUND(AVG(e.salary), 2) AS avg_salary
        FROM regions r
        JOIN countries c ON r.region_id = c.region_id
        JOIN locations l ON c.country_id = l.country_id
        JOIN departments d ON l.location_id = d.location_id
        JOIN employees e ON d.department_id = e.department_id
        GROUP BY r.region_id, r.region_name
        ORDER BY employee_count DESC
        """,
        "1. Employee Distribution by Region"
    )
    
    # 2. Detailed location analysis
    print_query_results(
        """
        SELECT 
            l.city,
            c.country_name,
            r.region_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            STRING_AGG(DISTINCT d.department_name, ', ') AS departments
        FROM locations l
        JOIN countries c ON l.country_id = c.country_id
        JOIN regions r ON c.region_id = r.region_id
        JOIN departments d ON l.location_id = d.location_id
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY l.location_id, l.city, c.country_name, r.region_name
        ORDER BY employee_count DESC
        """,
        "2. Detailed Location Analysis"
    )

def date_analysis_examples():
    """Demonstrate date-based aggregations."""
    print("\n=== Date Analysis Examples ===")
    
    # 1. Hiring trends by year
    print_query_results(
        """
        SELECT 
            EXTRACT(YEAR FROM CAST(hire_date AS DATE)) AS hire_year,
            COUNT(*) AS employees_hired,
            ROUND(AVG(salary), 2) AS avg_starting_salary
        FROM employees
        GROUP BY EXTRACT(YEAR FROM CAST(hire_date AS DATE))
        ORDER BY hire_year
        """,
        "1. Hiring Trends by Year"
    )
    
    # 2. Tenure analysis
    print_query_results(
        """
        SELECT 
            CASE 
                WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(hire_date AS DATE)) < 5 THEN '0-4 years'
                WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(hire_date AS DATE)) < 10 THEN '5-9 years'
                WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(hire_date AS DATE)) < 20 THEN '10-19 years'
                ELSE '20+ years'
            END AS tenure_group,
            COUNT(*) AS employee_count,
            ROUND(AVG(salary), 2) AS avg_salary
        FROM employees
        GROUP BY 
            CASE 
                WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(hire_date AS DATE)) < 5 THEN '0-4 years'
                WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(hire_date AS DATE)) < 10 THEN '5-9 years'
                WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(hire_date AS DATE)) < 20 THEN '10-19 years'
                ELSE '20+ years'
            END
        ORDER BY 
            CASE tenure_group
                WHEN '0-4 years' THEN 1
                WHEN '5-9 years' THEN 2
                WHEN '10-19 years' THEN 3
                ELSE 4
            END
        """,
        "2. Employee Tenure Analysis"
    )

def run_all_examples():
    """Run all aggregation examples."""
    basic_aggregation_examples()
    group_by_examples()
    having_clause_examples()
    advanced_aggregation_examples()
    window_function_examples()
    regional_analysis_examples()
    date_analysis_examples()

if __name__ == "__main__":
    print("DuckDB SQL Practice: Aggregation Functions and GROUP BY")
    print("=" * 55)
    run_all_examples()
    print("\n" + "=" * 55)
    print("Practice complete! Try creating your own aggregation queries.")