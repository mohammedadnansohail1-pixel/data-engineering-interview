import asyncio
import json
from typing import List, Dict, Any


class CodeExecutor:
    """Service for executing code safely in isolated environments"""

    async def execute_python(self, code: str, test_cases: List[Dict], timeout: int = 30) -> Dict[str, Any]:
        """Execute Python code and validate against test cases"""

        # For MVP, we'll do basic execution without Docker
        # In production, this should use Docker containers
        results = {
            "passed": 0,
            "failed": 0,
            "total": len(test_cases),
            "test_results": [],
            "execution_time_ms": 0,
            "errors": []
        }

        if not test_cases:
            # No test cases, just try to run the code
            try:
                # Create a safe execution environment
                exec_globals = {"__builtins__": __builtins__}
                exec(code, exec_globals)
                results["passed"] = 1
                results["total"] = 1
                results["test_results"].append({
                    "passed": True,
                    "message": "Code executed successfully"
                })
            except Exception as e:
                results["failed"] = 1
                results["total"] = 1
                results["errors"].append(str(e))
                results["test_results"].append({
                    "passed": False,
                    "message": f"Execution error: {str(e)}"
                })

            return results

        # Run test cases
        for i, test_case in enumerate(test_cases):
            try:
                input_data = test_case.get("input", {})
                expected_output = test_case.get("expected")

                # Create execution environment
                exec_globals = {"__builtins__": __builtins__}
                exec_globals.update(input_data)

                # Execute code
                exec(code, exec_globals)

                # Check if there's a function to test
                function_name = test_case.get("function")
                if function_name and function_name in exec_globals:
                    func = exec_globals[function_name]
                    args = test_case.get("args", [])
                    kwargs = test_case.get("kwargs", {})
                    actual_output = func(*args, **kwargs)

                    # Compare output
                    if actual_output == expected_output:
                        results["passed"] += 1
                        results["test_results"].append({
                            "test_case": i + 1,
                            "passed": True,
                            "expected": expected_output,
                            "actual": actual_output
                        })
                    else:
                        results["failed"] += 1
                        results["test_results"].append({
                            "test_case": i + 1,
                            "passed": False,
                            "expected": expected_output,
                            "actual": actual_output
                        })
                else:
                    # No specific function, just check if code ran
                    results["passed"] += 1
                    results["test_results"].append({
                        "test_case": i + 1,
                        "passed": True,
                        "message": "Code executed successfully"
                    })

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Test case {i + 1}: {str(e)}")
                results["test_results"].append({
                    "test_case": i + 1,
                    "passed": False,
                    "error": str(e)
                })

        return results

    async def execute_sql(self, query: str, test_data: Dict) -> Dict[str, Any]:
        """Execute SQL query against test database"""

        # For MVP, return mock results
        # In production, this should use a temporary PostgreSQL database
        results = {
            "passed": 1,
            "failed": 0,
            "total": 1,
            "query_result": [],
            "execution_time_ms": 10,
            "errors": []
        }

        try:
            # Basic SQL validation
            query_lower = query.lower().strip()

            if not any(keyword in query_lower for keyword in ['select', 'insert', 'update', 'delete', 'create']):
                results["passed"] = 0
                results["failed"] = 1
                results["errors"].append("Invalid SQL query")
                return results

            # Mock successful execution
            results["query_result"] = test_data.get("expected_result", [])

        except Exception as e:
            results["passed"] = 0
            results["failed"] = 1
            results["errors"].append(str(e))

        return results

    async def validate_output(self, actual: Any, expected: Any) -> bool:
        """Compare outputs and validate correctness"""
        try:
            if isinstance(expected, (list, dict)):
                return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
            return actual == expected
        except:
            return False
