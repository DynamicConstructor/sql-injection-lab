# Case Study: Eliminating SQL Injection With Bound Parameters

## Problem

Constructing a SQL query from raw user input can turn data into executable query syntax. Authentication and search functions can return unintended records.

## Approach

The isolated SQLite demonstration creates three fictional accounts. An intentionally unsafe function concatenates text into a WHERE clause; two safe functions use SQLite placeholders and bound values. Regression tests compare both behaviors.

## Architecture

`User-supplied string → vulnerable concatenation OR bound parameter → SQLite → returned rows`

## Finding and fix

**SQLI-001 (local lab):** A controlled predicate changes the unsafe query and matches three records. In the fixed query, the exact same input is treated as one literal username and matches none.

The fundamental correction is parameterization. Validation and least-privilege database credentials are useful additional controls, not substitutes for bound values.

## Demonstrated outcome

Five tests passed in the cloud run. The reproduction is limited to an in-memory SQLite lab; it is not a deployed web application security assessment.

## Next personal contribution

Alexander can build a local HTTP interface, add a secure filter endpoint, and test valid and malicious inputs—only within his own lab.
