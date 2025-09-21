"""
01. Introduction to DuckDB SQL Practice
This script demonstrates basic DuckDB operations and SELECT statements.

Topics covered:
- Connecting to DuckDB
- Basic SELECT statements
- Filtering with WHERE
- Sorting with ORDER BY
- Limiting results with LIMIT
- Column selection and aliases
"""

from db_utils import get_connection, print_query_results, table_info
import duckdb

def basic_connection_demo():
    """Demonstrate basic DuckDB connection and database exploration."""
    print("=== DuckDB Connection and Database Exploration ===")
    
    # Show database information
    print("Database Information:")
    info = table_info()
    for table_name, table_data in info.items():
        print(f"  {table_name}: {table_data['count']} records")
    
    # Show a simple query
    print_query_results(
        "SELECT 'Hello from DuckDB!' as message, CURRENT_DATE as today",
        "Basic DuckDB Query"
    )

def basic_select_examples():
    """Demonstrate basic SELECT operations."""
    print("\n=== Basic SELECT Operations ===")
    
    # 1. Select all from a small table
    print_query_results(
        "SELECT * FROM regions",
        "1. All Regions"
    )
    
    # 2. Select specific columns
    print_query_results(
        "SELECT region_id, region_name FROM regions",
        "2. Specific Columns from Regions"
    )
    
    # 3. Column aliases
    print_query_results(
        "SELECT region_id AS id, region_name AS name FROM regions",
        "3. Column Aliases"
    )
    
    # 4. Select with expressions
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary,
            salary * 12 AS annual_salary
        FROM employees 
        LIMIT 5
        """,
        "4. Expressions and Concatenation"
    )

def where_clause_examples():
    """Demonstrate WHERE clause filtering."""
    print("\n=== WHERE Clause Examples ===")
    
    # 1. Simple equality filter
    print_query_results(
        "SELECT * FROM countries WHERE region_id = 1",
        "1. Countries in Region 1 (Europe)",
        limit=15
    )
    
    # 2. String comparison
    print_query_results(
        "SELECT * FROM jobs WHERE job_title LIKE '%Manager%'",
        "2. Jobs with 'Manager' in Title"
    )
    
    # 3. Numeric comparisons
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary
        FROM employees 
        WHERE salary > 10000
        """,
        "3. High-Salary Employees (> 10,000)"
    )
    
    # 4. Multiple conditions (AND)
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary,
            department_id
        FROM employees 
        WHERE salary > 8000 AND department_id = 5
        """,
        "4. High-Salary Employees in Department 5"
    )
    
    # 5. Multiple conditions (OR)
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            department_id
        FROM employees 
        WHERE department_id = 3 OR department_id = 6
        """,
        "5. Employees in Departments 3 or 6"
    )
    
    # 6. IN clause
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            department_id
        FROM employees 
        WHERE department_id IN (3, 6, 9)
        """,
        "6. Employees in Departments 3, 6, or 9"
    )
    
    # 7. BETWEEN clause
    print_query_results(
        """
        SELECT 
            job_id,
            job_title,
            min_salary,
            max_salary
        FROM jobs 
        WHERE min_salary BETWEEN 4000 AND 8000
        """,
        "7. Jobs with Min Salary Between 4,000 and 8,000"
    )
    
    # 8. IS NULL / IS NOT NULL
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            phone_number
        FROM employees 
        WHERE phone_number IS NULL
        """,
        "8. Employees with No Phone Number"
    )

def order_by_examples():
    """Demonstrate ORDER BY clause."""
    print("\n=== ORDER BY Examples ===")
    
    # 1. Simple ascending sort
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary
        FROM employees 
        ORDER BY salary
        LIMIT 10
        """,
        "1. Employees by Salary (Ascending)"
    )
    
    # 2. Descending sort
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary
        FROM employees 
        ORDER BY salary DESC
        LIMIT 10
        """,
        "2. Employees by Salary (Descending)"
    )
    
    # 3. Multiple column sort
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            department_id,
            salary
        FROM employees 
        ORDER BY department_id, salary DESC
        LIMIT 15
        """,
        "3. Employees by Department, then Salary (Desc)"
    )

def limit_offset_examples():
    """Demonstrate LIMIT and OFFSET for pagination."""
    print("\n=== LIMIT and OFFSET Examples ===")
    
    # 1. Simple limit
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary
        FROM employees 
        ORDER BY employee_id
        LIMIT 5
        """,
        "1. First 5 Employees"
    )
    
    # 2. Limit with offset (pagination)
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary
        FROM employees 
        ORDER BY employee_id
        LIMIT 5 OFFSET 5
        """,
        "2. Next 5 Employees (Offset 5)"
    )

def distinct_examples():
    """Demonstrate DISTINCT clause."""
    print("\n=== DISTINCT Examples ===")
    
    # 1. Distinct values
    print_query_results(
        "SELECT DISTINCT department_id FROM employees ORDER BY department_id",
        "1. Distinct Departments"
    )
    
    # 2. Distinct combinations
    print_query_results(
        """
        SELECT DISTINCT 
            department_id,
            job_id
        FROM employees 
        ORDER BY department_id, job_id
        """,
        "2. Distinct Department-Job Combinations"
    )

def case_when_examples():
    """Demonstrate CASE WHEN conditional logic."""
    print("\n=== CASE WHEN Examples ===")
    
    # 1. Simple case
    print_query_results(
        """
        SELECT 
            employee_id,
            first_name || ' ' || last_name AS full_name,
            salary,
            CASE 
                WHEN salary < 5000 THEN 'Low'
                WHEN salary < 10000 THEN 'Medium'
                ELSE 'High'
            END AS salary_category
        FROM employees 
        ORDER BY salary
        LIMIT 10
        """,
        "1. Salary Categories"
    )
    
    # 2. Case with multiple conditions
    print_query_results(
        """
        SELECT 
            r.region_name,
            COUNT(*) AS country_count,
            CASE 
                WHEN COUNT(*) < 5 THEN 'Small Region'
                WHEN COUNT(*) < 10 THEN 'Medium Region'
                ELSE 'Large Region'
            END AS region_size
        FROM regions r
        JOIN countries c ON r.region_id = c.region_id
        GROUP BY r.region_id, r.region_name
        ORDER BY country_count DESC
        """,
        "2. Region Sizes by Country Count"
    )

def run_all_examples():
    """Run all SELECT examples."""
    basic_connection_demo()
    basic_select_examples()
    where_clause_examples()
    order_by_examples()
    limit_offset_examples()
    distinct_examples()
    case_when_examples()

if __name__ == "__main__":
    print("DuckDB SQL Practice: Introduction and SELECT Statements")
    print("=" * 60)
    run_all_examples()
    print("\n" + "=" * 60)
    print("Practice complete! Try modifying the queries above to explore further.")