# main.py
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import APP_NAME, VERSION, TARGET_MODELS
from connectors.ollama_connector import AdvancedOllamaConnector
from modules.semantic_evaluator import SemanticLLMJudge

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def run_benchmark_suite():
    console.print(Panel(f"[bold green]{APP_NAME} | v{VERSION}[/bold green]\n[dim]Semantic Architecture Model Benchmarking Matrix[/dim]", expand=False))

    dataset_path = os.path.join("datasets", "owasp_atlas_suite.json")
    if not os.path.exists(dataset_path):
        console.print("[bold red][X] Dataset Missing! Ensure datasets/owasp_atlas_suite.json exists.[/bold red]")
        return
        
    with open(dataset_path, "r", encoding="utf-8") as f:
        attack_dataset = json.load(f)

    console.print("[bold yellow][*] Initializing Semantic LLM Judge System...[/bold yellow]")
    judge = SemanticLLMJudge()
    if not judge.judge_connector.connect():
        console.print("[bold red][X] Evaluator Judge Node unable to reach Ollama Server.[/bold red]")
        return

    benchmark_matrix = {model: {"total": 0, "exploited": 0} for model in TARGET_MODELS}
    detailed_matrix_logs = []

    for model_name in TARGET_MODELS:
        console.print(f"\n[bold cyan][➔] Deploying Testing Vectors Against Target Model: [{model_name}][/bold cyan]")
        connector = AdvancedOllamaConnector(model_name=model_name)
        
        if not connector.connect():
            console.print(f" [bold red][X] Model '{model_name}' not available. Skipping...[/bold red]")
            continue

        for case in attack_dataset:
            response = connector.send_query(case["prompt"])
            verdict = judge.evaluate_attack_success(case["prompt"], response)
            
            benchmark_matrix[model_name]["total"] += 1
            if verdict == "FAIL":
                benchmark_matrix[model_name]["exploited"] += 1

            detailed_matrix_logs.append({
                "model": model_name,
                "id": case["vector_id"],
                "owasp": case["owasp_category"],
                "atlas": case["mitre_atlas_id"],
                "verdict": verdict
            })

    console.print("\n[bold magenta]📊 CROSS-MODEL ROBUSTNESS BENCHMARKING DASHBOARD[/bold magenta]\n")
    comparison_table = Table(title="Model Robustness Summary Matrix", border_style="cyan", header_style="bold white")
    comparison_table.add_column("Target LLM Model", style="yellow")
    comparison_table.add_column("Total Attack Vectors", justify="center")
    comparison_table.add_column("Successful Bypasses", justify="center")
    comparison_table.add_column("Attack Success Rate (ASR %)", justify="center", style="bold red")
    comparison_table.add_column("Defense Resilience Rate %", justify="center", style="bold green")

    for model, stats in benchmark_matrix.items():
        if stats["total"] > 0:
            asr = round((stats["exploited"] / stats["total"]) * 100, 2)
            drr = round(100.0 - asr, 2)
            comparison_table.add_row(model.upper(), str(stats["total"]), str(stats["exploited"]), f"{asr}%", f"{drr}%")
    console.print(comparison_table)

    console.print("\n[bold magenta]📋 MITRE ATLAS & OWASP VECTOR MAPPING LOGS[/bold magenta]\n")
    logs_table = Table(border_style="dim")
    logs_table.add_column("Model", style="yellow")
    logs_table.add_column("Vector ID", style="dim")
    logs_table.add_column("OWASP Category", style="cyan")
    logs_table.add_column("MITRE ATLAS ID", style="blue")
    logs_table.add_column("Judge Verdict", justify="center")

    for log in detailed_matrix_logs:
        tag = "[bold black on green] PASS [/bold black on green]" if log["verdict"] == "PASS" else "[bold white on red] FAIL [/bold white on red]"
        logs_table.add_row(log["model"].upper(), log["id"], log["owasp"], log["atlas"], tag)
    console.print(logs_table)

if __name__ == "__main__":
    run_benchmark_suite()