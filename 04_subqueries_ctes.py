"""
04. Subqueries and Common Table Expressions (CTEs) in DuckDB
This script demonstrates subqueries and CTEs for complex data analysis.

Topics covered:
- Scalar subqueries
- Column subqueries (IN, EXISTS)
- Correlated subqueries
- Common Table Expressions (CTEs)
- Recursive CTEs
- Multiple CTEs
- Subqueries in different clauses
"""

from db_utils import print_query_results

def scalar_subquery_examples():
    """Demonstrate scalar subqueries (return single value)."""
    print("=== Scalar Subquery Examples ===")
    
    # 1. Employees earning more than the average salary
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary,
            (SELECT ROUND(AVG(salary), 2) FROM employees) AS company_avg_salary,
            ROUND(salary - (SELECT AVG(salary) FROM employees), 2) AS diff_from_avg
        FROM employees
        WHERE salary > (SELECT AVG(salary) FROM employees)
        ORDER BY salary DESC
        """,
        "1. Employees Above Average Salary"
    )
    
    # 2. Department with the highest average salary
    print_query_results(
        """
        SELECT 
            d.department_name,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            (SELECT MAX(avg_sal) FROM 
                (SELECT AVG(salary) AS avg_sal 
                 FROM employees 
                 GROUP BY department_id)
            ) AS highest_dept_avg
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        HAVING AVG(e.salary) = (
            SELECT MAX(avg_sal) FROM 
                (SELECT AVG(salary) AS avg_sal 
                 FROM employees 
                 GROUP BY department_id)
        )
        """,
        "2. Department with Highest Average Salary"
    )

def column_subquery_examples():
    """Demonstrate column subqueries (IN, EXISTS, NOT IN, NOT EXISTS)."""
    print("\n=== Column Subquery Examples ===")
    
    # 1. Employees in departments located in the US
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        WHERE e.department_id IN (
            SELECT d.department_id
            FROM departments d
            JOIN locations l ON d.location_id = l.location_id
            WHERE l.country_id = 'US'
        )
        ORDER BY e.employee_id
        """,
        "1. Employees in US-Located Departments (IN)"
    )
    
    # 2. Managers (employees who manage others)
    print_query_results(
        """
        SELECT 
            m.employee_id,
            m.first_name || ' ' || m.last_name AS manager_name,
            COUNT(e.employee_id) AS direct_reports
        FROM employees m
        WHERE EXISTS (
            SELECT 1 
            FROM employees e 
            WHERE e.manager_id = m.employee_id
        )
        LEFT JOIN employees e ON m.employee_id = e.manager_id
        GROUP BY m.employee_id, m.first_name, m.last_name
        ORDER BY direct_reports DESC
        """,
        "2. Managers with Direct Reports (EXISTS)"
    )
    
    # 3. Employees with no dependents
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.salary
        FROM employees e
        WHERE NOT EXISTS (
            SELECT 1 
            FROM dependents d 
            WHERE d.employee_id = e.employee_id
        )
        ORDER BY e.salary DESC
        LIMIT 10
        """,
        "3. Employees with No Dependents (NOT EXISTS)"
    )
    
    # 4. Jobs not currently held by any employee
    print_query_results(
        """
        SELECT 
            j.job_id,
            j.job_title,
            j.min_salary,
            j.max_salary
        FROM jobs j
        WHERE j.job_id NOT IN (
            SELECT DISTINCT e.job_id 
            FROM employees e 
            WHERE e.job_id IS NOT NULL
        )
        ORDER BY j.job_title
        """,
        "4. Vacant Job Positions (NOT IN)"
    )

def correlated_subquery_examples():
    """Demonstrate correlated subqueries."""
    print("\n=== Correlated Subquery Examples ===")
    
    # 1. Employees earning more than their department average
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name,
            e.salary,
            (SELECT ROUND(AVG(e2.salary), 2) 
             FROM employees e2 
             WHERE e2.department_id = e.department_id) AS dept_avg_salary
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        WHERE e.salary > (
            SELECT AVG(e2.salary) 
            FROM employees e2 
            WHERE e2.department_id = e.department_id
        )
        ORDER BY d.department_name, e.salary DESC
        """,
        "1. Employees Above Department Average"
    )
    
    # 2. Top 2 highest paid employees in each department
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name,
            e.salary
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        WHERE (
            SELECT COUNT(*)
            FROM employees e2
            WHERE e2.department_id = e.department_id
            AND e2.salary > e.salary
        ) < 2
        ORDER BY d.department_name, e.salary DESC
        """,
        "2. Top 2 Earners per Department"
    )
    
    # 3. Departments with all employees earning above company average
    print_query_results(
        """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS dept_avg_salary
        FROM departments d
        JOIN employees e ON d.department_id = e.department_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM employees e2
            WHERE e2.department_id = d.department_id
            AND e2.salary <= (SELECT AVG(salary) FROM employees)
        )
        GROUP BY d.department_id, d.department_name
        ORDER BY dept_avg_salary DESC
        """,
        "3. Departments with All High Earners"
    )

def basic_cte_examples():
    """Demonstrate basic Common Table Expressions."""
    print("\n=== Basic CTE Examples ===")
    
    # 1. Simple CTE for department statistics
    print_query_results(
        """
        WITH dept_stats AS (
            SELECT 
                d.department_id,
                d.department_name,
                COUNT(e.employee_id) AS employee_count,
                ROUND(AVG(e.salary), 2) AS avg_salary,
                MIN(e.salary) AS min_salary,
                MAX(e.salary) AS max_salary
            FROM departments d
            LEFT JOIN employees e ON d.department_id = e.department_id
            GROUP BY d.department_id, d.department_name
        )
        SELECT 
            department_name,
            employee_count,
            avg_salary,
            CASE 
                WHEN avg_salary > 10000 THEN 'High Pay'
                WHEN avg_salary > 6000 THEN 'Medium Pay'
                ELSE 'Lower Pay'
            END AS pay_category
        FROM dept_stats
        WHERE employee_count > 0
        ORDER BY avg_salary DESC
        """,
        "1. Department Statistics with CTE"
    )
    
    # 2. CTE for employee hierarchy
    print_query_results(
        """
        WITH employee_hierarchy AS (
            SELECT 
                e.employee_id,
                e.first_name || ' ' || e.last_name AS employee_name,
                e.manager_id,
                CASE 
                    WHEN e.manager_id IS NULL THEN 'CEO'
                    ELSE m.first_name || ' ' || m.last_name
                END AS manager_name,
                e.salary
            FROM employees e
            LEFT JOIN employees m ON e.manager_id = m.employee_id
        )
        SELECT 
            manager_name,
            COUNT(*) AS direct_reports,
            ROUND(AVG(salary), 2) AS avg_team_salary
        FROM employee_hierarchy
        WHERE manager_name != 'CEO'
        GROUP BY manager_name
        ORDER BY direct_reports DESC
        """,
        "2. Manager Performance Analysis"
    )

def multiple_cte_examples():
    """Demonstrate multiple CTEs in one query."""
    print("\n=== Multiple CTE Examples ===")
    
    # 1. Regional analysis with multiple CTEs
    print_query_results(
        """
        WITH regional_employees AS (
            SELECT 
                r.region_name,
                e.employee_id,
                e.salary,
                e.department_id
            FROM regions r
            JOIN countries c ON r.region_id = c.region_id
            JOIN locations l ON c.country_id = l.country_id
            JOIN departments d ON l.location_id = d.location_id
            JOIN employees e ON d.department_id = e.department_id
        ),
        regional_stats AS (
            SELECT 
                region_name,
                COUNT(*) AS employee_count,
                ROUND(AVG(salary), 2) AS avg_salary,
                COUNT(DISTINCT department_id) AS dept_count
            FROM regional_employees
            GROUP BY region_name
        ),
        company_stats AS (
            SELECT 
                COUNT(*) AS total_employees,
                ROUND(AVG(salary), 2) AS company_avg_salary
            FROM employees
        )
        SELECT 
            rs.region_name,
            rs.employee_count,
            ROUND(100.0 * rs.employee_count / cs.total_employees, 1) AS pct_of_workforce,
            rs.avg_salary,
            rs.avg_salary - cs.company_avg_salary AS diff_from_company_avg,
            rs.dept_count
        FROM regional_stats rs
        CROSS JOIN company_stats cs
        ORDER BY rs.employee_count DESC
        """,
        "1. Comprehensive Regional Analysis"
    )
    
    # 2. Salary analysis with multiple CTEs
    print_query_results(
        """
        WITH salary_quartiles AS (
            SELECT 
                employee_id,
                first_name || ' ' || last_name AS full_name,
                salary,
                NTILE(4) OVER (ORDER BY salary) AS salary_quartile
            FROM employees
        ),
        dept_quartile_stats AS (
            SELECT 
                e.department_id,
                d.department_name,
                sq.salary_quartile,
                COUNT(*) AS employee_count,
                ROUND(AVG(sq.salary), 2) AS avg_salary
            FROM salary_quartiles sq
            JOIN employees e ON sq.employee_id = e.employee_id
            JOIN departments d ON e.department_id = d.department_id
            GROUP BY e.department_id, d.department_name, sq.salary_quartile
        )
        SELECT 
            department_name,
            SUM(CASE WHEN salary_quartile = 4 THEN employee_count ELSE 0 END) AS top_quartile_count,
            SUM(CASE WHEN salary_quartile = 1 THEN employee_count ELSE 0 END) AS bottom_quartile_count,
            SUM(employee_count) AS total_employees
        FROM dept_quartile_stats
        GROUP BY department_name
        HAVING SUM(employee_count) >= 3
        ORDER BY top_quartile_count DESC
        """,
        "2. Department Salary Distribution Analysis"
    )

def recursive_cte_examples():
    """Demonstrate recursive CTEs for hierarchical data."""
    print("\n=== Recursive CTE Examples ===")
    
    # 1. Organization hierarchy
    print_query_results(
        """
        WITH RECURSIVE org_hierarchy AS (
            -- Base case: CEO (no manager)
            SELECT 
                employee_id,
                first_name || ' ' || last_name AS full_name,
                manager_id,
                0 AS level,
                CAST(first_name || ' ' || last_name AS VARCHAR) AS hierarchy_path
            FROM employees 
            WHERE manager_id IS NULL
            
            UNION ALL
            
            -- Recursive case: employees with managers
            SELECT 
                e.employee_id,
                e.first_name || ' ' || e.last_name AS full_name,
                e.manager_id,
                oh.level + 1 AS level,
                CAST(oh.hierarchy_path || ' > ' || e.first_name || ' ' || e.last_name AS VARCHAR) AS hierarchy_path
            FROM employees e
            JOIN org_hierarchy oh ON e.manager_id = oh.employee_id
        )
        SELECT 
            level,
            REPEAT('  ', level) || full_name AS indented_name,
            hierarchy_path
        FROM org_hierarchy
        ORDER BY level, full_name
        LIMIT 20
        """,
        "1. Organization Hierarchy Tree"
    )

def cte_performance_examples():
    """Demonstrate CTEs for performance optimization."""
    print("\n=== CTE Performance Examples ===")
    
    # 1. Avoiding repeated subqueries with CTE
    print_query_results(
        """
        WITH high_performers AS (
            SELECT 
                e.employee_id,
                e.first_name || ' ' || e.last_name AS full_name,
                e.department_id,
                e.salary,
                j.job_title
            FROM employees e
            JOIN jobs j ON e.job_id = j.job_id
            WHERE e.salary > (SELECT AVG(salary) * 1.2 FROM employees)
        ),
        dept_high_performer_stats AS (
            SELECT 
                d.department_name,
                COUNT(hp.employee_id) AS high_performer_count,
                ROUND(AVG(hp.salary), 2) AS avg_high_performer_salary
            FROM departments d
            LEFT JOIN high_performers hp ON d.department_id = hp.department_id
            GROUP BY d.department_id, d.department_name
        )
        SELECT 
            department_name,
            high_performer_count,
            avg_high_performer_salary,
            CASE 
                WHEN high_performer_count = 0 THEN 'No High Performers'
                WHEN high_performer_count = 1 THEN 'One High Performer'
                ELSE CAST(high_performer_count AS VARCHAR) || ' High Performers'
            END AS performance_status
        FROM dept_high_performer_stats
        ORDER BY high_performer_count DESC
        """,
        "1. High Performer Analysis by Department"
    )

def run_all_examples():
    """Run all subquery and CTE examples."""
    scalar_subquery_examples()
    column_subquery_examples()
    correlated_subquery_examples()
    basic_cte_examples()
    multiple_cte_examples()
    recursive_cte_examples()
    cte_performance_examples()

if __name__ == "__main__":
    print("DuckDB SQL Practice: Subqueries and CTEs")
    print("=" * 40)
    run_all_examples()
    print("\n" + "=" * 40)
    print("Practice complete! Try creating complex CTEs for your own analysis.")