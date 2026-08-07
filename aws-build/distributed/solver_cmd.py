from pathlib import Path
from typing import List
from common.solver_io import SolverInput, SolverResultCode
import os

def get_run_command(s_input: SolverInput) -> List[str]:
    def create_hostfile(worker_ips, leader_ip, request_dir):
        totalWorkerNodes = 0
        hostfile_path = os.path.join(request_dir, 'combined_hostfile')
        with open(hostfile_path, 'w+') as f:
            for ip in worker_ips:
                if ip != leader_ip:
                    totalWorkerNodes += 1
                    f.write(f'{ip}\n')
                    # f.write(f'{ip} slots=1\n')

        return hostfile_path, totalWorkerNodes

    # leader_ip = socket.gethostbyname(socket.gethostname())
    leader_ip = s_input.node_ip

    hostfile, totalWorkerNodes = create_hostfile(s_input.worker_node_ips, leader_ip, s_input.run_dir)


    return [
        "bash", "/SMTS/smtcomp26-aws/run_distributed.sh",
        str(hostfile),
        str(s_input.formula_file),
        str(totalWorkerNodes),
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
