#!/usr/bin/env python3
"""Testa reinício real do piloto, com dois processos e SQLite temporário."""

import argparse
import json
import platform
import shutil
import socket
import sqlite3
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mathua", type=Path, required=True, help="Clone do Mathua com o patch aplicado")
    parser.add_argument("--binary", type=Path, default=Path("pilot-bin"))
    parser.add_argument("--node", default="node")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--previous-mathua", type=Path, help="Clone compilado da versão que cria o banco antes da atualização")
    args = parser.parse_args()
    root = args.mathua.resolve()
    binary = args.binary if args.binary.is_absolute() else root / args.binary
    if not binary.is_file():
        parser.error(f"Compile o piloto antes do teste. Executável ausente: {binary}")
    node = shutil.which(args.node)
    if not node:
        parser.error(f"Node não encontrado: {args.node}")

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    process = None
    log = None

    def stop():
        nonlocal process, log
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        if log is not None:
            log.close()
        process, log = None, None

    def request(method, path, body=None, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(base + path, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=15) as response:
            raw = response.read()
            return json.loads(raw), raw

    with tempfile.TemporaryDirectory(prefix="mathua-restart-") as temporary:
        work = Path(temporary)
        database = work / "pilot.db"

        def start(index):
            nonlocal process, log
            log = (work / f"process-{index}.log").open("w")
            checkout = args.previous_mathua.resolve() if index == 1 and args.previous_mathua else root
            executable = checkout / args.binary if checkout != root else binary
            content = Path(__file__).resolve().parents[3] / "conteudo/typescript-v1"
            process = subprocess.Popen(
                [str(executable), "-content", str(content), "-addr", f"127.0.0.1:{port}", "-db", str(database), "-node", node],
                cwd=checkout, stdout=log, stderr=subprocess.STDOUT,
            )
            deadline = time.monotonic() + 90
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(f"O processo terminou com código {process.returncode}")
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                        return
                except OSError:
                    time.sleep(0.1)
            raise RuntimeError("O servidor não iniciou dentro do prazo")

        try:
            start(1)
            guest, _ = request("POST", "/api/auth/guest", {})
            token = guest["token"]
            concept = "ts.type.number"
            served, _ = request("GET", f"/api/lessons/{concept}/practice?count=1", token=token)
            question = served["questions"][0]["question"]
            assert served["questions"][0]["answer_input_mode"] == "text"
            if args.previous_mathua:
                earlier = {"concept_id": concept, "question": question, "answer": "number",
                           "elapsed": 30, "submission_id": "before-upgrade"}
                graded, saved = request("POST", "/api/study/answer", earlier, token)
                assert graded["correct"]
                served, _ = request("GET", f"/api/lessons/{concept}/practice?count=1", token=token)
                question = served["questions"][0]["question"]
            stop()
            start(2)
            if args.previous_mathua:
                _, replay = request("POST", "/api/study/answer", earlier, token)
                assert replay == saved, "A atualização mudou uma resposta já gravada"

            payload = {"concept_id": concept, "question": question, "answer": "number",
                       "elapsed": 30, "submission_id": "process-restart-proof"}
            answer, raw = request("POST", "/api/study/answer", payload, token)
            assert answer["correct"] is True and answer.get("ungraded") is not True, answer
            _, retry = request("POST", "/api/study/answer", payload, token)
            assert retry == raw, "A repetição mudou a resposta gravada"
            with sqlite3.connect(database) as connection:
                attempts = connection.execute("SELECT count(*) FROM attempts").fetchone()[0]
            assert attempts == (2 if args.previous_mathua else 1), f"A repetição gravou {attempts} tentativas"
            result = {
                "passed": True,
                "test": "real_process_restart",
                "runtime": {"system": platform.system(), "release": platform.release(),
                            "machine": platform.machine(), "python": platform.python_version(),
                            "node": subprocess.check_output([node, "--version"], text=True).strip()},
                "processes_started": 2,
                "old_bearer_token_accepted": True,
                "pre_restart_question_graded": True,
                "retry_body_identical": True,
                "persisted_attempts": attempts,
                "previous_version_answer_replayed": bool(args.previous_mathua),
                "ungraded_key_present_in_normal_response": "ungraded" in answer,
                "normal_response": answer,
            }
        finally:
            stop()

    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
