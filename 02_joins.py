"""
02. JOIN Operations in DuckDB
This script demonstrates various types of JOIN operations.

Topics covered:
- INNER JOIN
- LEFT JOIN (LEFT OUTER JOIN)
- RIGHT JOIN (RIGHT OUTER JOIN)  
- FULL OUTER JOIN
- CROSS JOIN
- SELF JOIN
- Multiple table joins
- JOIN with aggregations
"""

from db_utils import print_query_results

def inner_join_examples():
    """Demonstrate INNER JOIN operations."""
    print("=== INNER JOIN Examples ===")
    
    # 1. Basic INNER JOIN - Employees with their departments
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.department_id
        ORDER BY e.employee_id
        LIMIT 10
        """,
        "1. Employees with Departments (INNER JOIN)"
    )
    
    # 2. INNER JOIN with WHERE clause
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.salary,
            j.job_title
        FROM employees e
        INNER JOIN jobs j ON e.job_id = j.job_id
        WHERE e.salary > 8000
        ORDER BY e.salary DESC
        """,
        "2. High-Salary Employees with Job Titles"
    )
    
    # 3. Multiple INNER JOINs
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            j.job_title,
            d.department_name,
            l.city
        FROM employees e
        INNER JOIN jobs j ON e.job_id = j.job_id
        INNER JOIN departments d ON e.department_id = d.department_id
        INNER JOIN locations l ON d.location_id = l.location_id
        ORDER BY e.employee_id
        LIMIT 10
        """,
        "3. Employees with Job, Department, and Location"
    )

def left_join_examples():
    """Demonstrate LEFT JOIN operations."""
    print("\n=== LEFT JOIN Examples ===")
    
    # 1. All employees with their managers (including employees without managers)
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS employee_name,
            m.first_name || ' ' || m.last_name AS manager_name
        FROM employees e
        LEFT JOIN employees m ON e.manager_id = m.employee_id
        ORDER BY e.employee_id
        LIMIT 15
        """,
        "1. Employees with Managers (LEFT JOIN)"
    )
    
    # 2. All employees with their dependents (including employees without dependents)
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS employee_name,
            dep.first_name || ' ' || dep.last_name AS dependent_name,
            dep.relationship
        FROM employees e
        LEFT JOIN dependents dep ON e.employee_id = dep.employee_id
        ORDER BY e.employee_id, dep.dependent_id
        LIMIT 20
        """,
        "2. Employees with Dependents (LEFT JOIN)"
    )
    
    # 3. Departments with employee counts (including departments with no employees)
    print_query_results(
        """
        SELECT 
            d.department_id,
            d.department_name,
            COUNT(e.employee_id) AS employee_count
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY employee_count DESC, d.department_name
        """,
        "3. Departments with Employee Counts"
    )

def right_join_examples():
    """Demonstrate RIGHT JOIN operations."""
    print("\n=== RIGHT JOIN Examples ===")
    
    # Note: RIGHT JOIN is less commonly used, but equivalent to swapping tables in LEFT JOIN
    
    # 1. All jobs with employees (including jobs with no employees)
    print_query_results(
        """
        SELECT 
            j.job_id,
            j.job_title,
            COUNT(e.employee_id) AS employee_count
        FROM employees e
        RIGHT JOIN jobs j ON e.job_id = j.job_id
        GROUP BY j.job_id, j.job_title
        ORDER BY employee_count DESC, j.job_title
        """,
        "1. All Jobs with Employee Counts (RIGHT JOIN)"
    )

def full_outer_join_examples():
    """Demonstrate FULL OUTER JOIN operations."""
    print("\n=== FULL OUTER JOIN Examples ===")
    
    # 1. All regions and countries (showing regions without countries and countries without regions)
    print_query_results(
        """
        SELECT 
            r.region_id,
            r.region_name,
            c.country_id,
            c.country_name
        FROM regions r
        FULL OUTER JOIN countries c ON r.region_id = c.region_id
        ORDER BY r.region_id, c.country_id
        """,
        "1. All Regions and Countries (FULL OUTER JOIN)"
    )

def cross_join_examples():
    """Demonstrate CROSS JOIN operations."""
    print("\n=== CROSS JOIN Examples ===")
    
    # 1. Cross join (Cartesian product) - Use with caution!
    print_query_results(
        """
        SELECT 
            r.region_name,
            'can expand to' AS relationship,
            c.country_name
        FROM regions r
        CROSS JOIN countries c
        WHERE r.region_id = 1  -- Limiting to avoid too many results
        ORDER BY r.region_name, c.country_name
        LIMIT 10
        """,
        "1. Cross Join Example (Limited)"
    )

def self_join_examples():
    """Demonstrate SELF JOIN operations."""
    print("\n=== SELF JOIN Examples ===")
    
    # 1. Employee hierarchy (employees and their managers)
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS employee_name,
            e.salary AS employee_salary,
            m.employee_id AS manager_id,
            m.first_name || ' ' || m.last_name AS manager_name,
            m.salary AS manager_salary
        FROM employees e
        INNER JOIN employees m ON e.manager_id = m.employee_id
        ORDER BY m.employee_id, e.employee_id
        """,
        "1. Employee-Manager Relationships (SELF JOIN)"
    )
    
    # 2. Employees earning more than their managers
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS employee_name,
            e.salary AS employee_salary,
            m.first_name || ' ' || m.last_name AS manager_name,
            m.salary AS manager_salary,
            e.salary - m.salary AS salary_difference
        FROM employees e
        INNER JOIN employees m ON e.manager_id = m.employee_id
        WHERE e.salary > m.salary
        ORDER BY salary_difference DESC
        """,
        "2. Employees Earning More Than Managers"
    )
    
    # 3. Employees in the same department
    print_query_results(
        """
        SELECT 
            e1.first_name || ' ' || e1.last_name AS employee1,
            e2.first_name || ' ' || e2.last_name AS employee2,
            d.department_name
        FROM employees e1
        INNER JOIN employees e2 ON e1.department_id = e2.department_id
        INNER JOIN departments d ON e1.department_id = d.department_id
        WHERE e1.employee_id < e2.employee_id  -- Avoid duplicates and self-pairs
        ORDER BY d.department_name, e1.employee_id
        LIMIT 15
        """,
        "3. Employee Pairs in Same Department"
    )

def complex_join_examples():
    """Demonstrate complex JOIN scenarios."""
    print("\n=== Complex JOIN Examples ===")
    
    # 1. Complete employee information
    print_query_results(
        """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS full_name,
            j.job_title,
            d.department_name,
            l.city,
            c.country_name,
            r.region_name,
            e.salary,
            m.first_name || ' ' || m.last_name AS manager_name
        FROM employees e
        INNER JOIN jobs j ON e.job_id = j.job_id
        INNER JOIN departments d ON e.department_id = d.department_id
        INNER JOIN locations l ON d.location_id = l.location_id
        INNER JOIN countries c ON l.country_id = c.country_id
        INNER JOIN regions r ON c.region_id = r.region_id
        LEFT JOIN employees m ON e.manager_id = m.employee_id
        ORDER BY e.employee_id
        LIMIT 10
        """,
        "1. Complete Employee Information"
    )
    
    # 2. Department summary with location and region
    print_query_results(
        """
        SELECT 
            d.department_name,
            l.city,
            c.country_name,
            r.region_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM departments d
        INNER JOIN locations l ON d.location_id = l.location_id
        INNER JOIN countries c ON l.country_id = c.country_id
        INNER JOIN regions r ON c.region_id = r.region_id
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name, l.city, c.country_name, r.region_name
        ORDER BY employee_count DESC
        """,
        "2. Department Summary with Geography"
    )
    
    # 3. Jobs with salary ranges and current employees
    print_query_results(
        """
        SELECT 
            j.job_title,
            j.min_salary,
            j.max_salary,
            COUNT(e.employee_id) AS current_employees,
            ROUND(AVG(e.salary), 2) AS avg_current_salary,
            CASE 
                WHEN AVG(e.salary) < j.min_salary THEN 'Below Range'
                WHEN AVG(e.salary) > j.max_salary THEN 'Above Range'
                ELSE 'Within Range'
            END AS salary_status
        FROM jobs j
        LEFT JOIN employees e ON j.job_id = e.job_id
        GROUP BY j.job_id, j.job_title, j.min_salary, j.max_salary
        ORDER BY current_employees DESC
        """,
        "3. Job Salary Analysis"
    )

def join_performance_tips():
    """Demonstrate JOIN performance considerations."""
    print("\n=== JOIN Performance Tips ===")
    
    print("""
    Performance Tips for JOINs in DuckDB:
    
    1. Use appropriate indexes on join columns (DuckDB handles this automatically)
    2. Filter early with WHERE clauses before joins when possible
    3. Use INNER JOIN when you only need matching records
    4. Consider the order of tables in multi-table joins
    5. Use EXPLAIN to analyze query execution plans
    
    Example of filtering before join:
    """)
    
    # Example: Filter before join vs filter after join
    print_query_results(
        """
        SELECT 
            e.first_name || ' ' || e.last_name AS full_name,
            d.department_name,
            e.salary
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.department_id
        WHERE e.salary > 10000  -- Filter after join
        ORDER BY e.salary DESC
        """,
        "Filtering After Join"
    )

def run_all_examples():
    """Run all JOIN examples."""
    inner_join_examples()
    left_join_examples()
    right_join_examples()
    full_outer_join_examples()
    cross_join_examples()
    self_join_examples()
    complex_join_examples()
    join_performance_tips()

if __name__ == "__main__":
    print("DuckDB SQL Practice: JOIN Operations")
    print("=" * 40)
    run_all_examples()
    print("\n" + "=" * 40)
    print("Practice complete! Try creating your own join combinations.")