-- HR Database Schema for DuckDB
-- This schema creates tables for regions, countries, locations, departments, jobs, employees, and dependents
-- Note: DuckDB doesn't support CASCADE operations in foreign keys, so we use basic foreign keys

CREATE TABLE regions (
	region_id INTEGER PRIMARY KEY,
	region_name TEXT NOT NULL
);

CREATE TABLE countries (
	country_id TEXT NOT NULL,
	country_name TEXT NOT NULL,
	region_id INTEGER NOT NULL,
	PRIMARY KEY (country_id),
	FOREIGN KEY (region_id) REFERENCES regions (region_id)
);

CREATE TABLE locations (
	location_id INTEGER PRIMARY KEY,
	street_address TEXT,
	postal_code TEXT,
	city TEXT NOT NULL,
	state_province TEXT,
	country_id TEXT NOT NULL,
	FOREIGN KEY (country_id) REFERENCES countries (country_id)
);

CREATE TABLE departments (
	department_id INTEGER PRIMARY KEY,
	department_name TEXT NOT NULL,
	location_id INTEGER NOT NULL,
	FOREIGN KEY (location_id) REFERENCES locations (location_id)
);

CREATE TABLE jobs (
	job_id INTEGER PRIMARY KEY,
	job_title TEXT NOT NULL,
	min_salary DOUBLE NOT NULL,
	max_salary DOUBLE NOT NULL
);

CREATE TABLE employees (
	employee_id INTEGER PRIMARY KEY,
	first_name TEXT,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL,
	phone_number TEXT,
	hire_date TEXT NOT NULL,
	job_id INTEGER NOT NULL,
	salary DOUBLE NOT NULL,
	manager_id INTEGER,
	department_id INTEGER NOT NULL,
	FOREIGN KEY (job_id) REFERENCES jobs (job_id),
	FOREIGN KEY (department_id) REFERENCES departments (department_id),
	FOREIGN KEY (manager_id) REFERENCES employees (employee_id)
);

CREATE TABLE dependents (
	dependent_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	relationship TEXT NOT NULL,
	employee_id INTEGER NOT NULL,
	FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);