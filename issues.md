# Lab 5 – Static Code Analysis

## Identified Issues

The following issues were identified by analysing `pharmacy_system.py` using Pylint, Bandit and Flake8, along with manual testing.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL injection vulnerability | Security – Medium | 21 | User input is directly inserted into an SQL query, making it vulnerable to SQL injection. | Use parameterized SQL queries. |
| Bare exception handling | Code Quality | 38, 58 | Exceptions are caught without specifying their type, hiding possible errors. | Replace bare except blocks with specific exception handling. |
| Mutable default argument | Bug | 24 | The default list is shared across multiple function calls. | Use None as the default and initialize the list inside the function. |
| Negative stock dispensing | Functional Bug | 30–32 | The program allows dispensing more medicine than the available stock. | Check stock availability before dispensing. |
| Expired medicines included | Functional Bug | 43–45 | Already expired medicines can appear in the expiring-soon list. | Check that the expiry date is in the future. |
| Unsafe file handling | Code Quality | 50, 57 | Files are opened without context managers or explicit encoding. | Use with open() and specify UTF-8 encoding. |
| Unused import | Code Quality | 3 | The os module is imported but never used. | Remove the unused import. |
| Incorrect function naming | Style | 61 | printStock() does not follow Python's snake_case naming convention. | Rename it to print_stock(). |

## Summary

Static analysis helped identify security vulnerabilities, coding mistakes and formatting problems. Manual testing also revealed functional issues that were not directly reported by the tools. These findings will be addressed while maintaining the original functionality of the pharmacy stock and prescription tracker.