from pathlib import Path
from typing import List
from common.solver_io import SolverInput, SolverResultCode

def get_run_command(s_input: SolverInput) -> List[str]:
    return [
        "bash", "/SMTS/smtcomp26-aws/run_parallel.sh",
        str(s_input.formula_file),
        # "-t", str(s_input.timeout_seconds)
    ]

def get_solver_result(stdout_path: Path) -> SolverResultCode:
    if not stdout_path.exists():
        return SolverResultCode.INDETERMINATE

    with open(stdout_path, 'r') as f:
        content = f.read().lower().splitlines()

    if "unsat" in content:
        return SolverResultCode.UNSAT
    if "sat" in content:
        return SolverResultCode.SAT
    if "unknown" in content:
        return SolverResultCode.UNKNOWN
    # if "error" in content or ";error" in content:
    #     return SolverResultCode.INDETERMINATE

    # SolverResultCode.TIMEOUT
    # SolverResultCode.CRASH

    return SolverResultCode.INDETERMINATE

def get_cleanup_command() -> List[str]:
    return ["pkill", "solver_opensmt"]
