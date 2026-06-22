"""CLI Entrypoint utilizing Click Orchestrating Async Subsystem Runs"""
import click
import asyncio
from src.config.loader import load_config
from src.orbit.client import OrbitClient
from src.planner.agent import Planner, Goal
from src.executor.agent import Executor
from src.analysis.static import StaticAnalysisEngine

@click.group()
def cli():
    """Orbit Autonomous Agent System Framework Operations console Command Interface"""
    pass

async def run_audit_pipeline(repo: str, auto_fix: bool):
    config = load_config()
    orbit_client = OrbitClient(config.orbit)
        
    goal = Goal(
        id="audit-1",
        name="Full Repository Analysis Execution Strategy Flow",
        description="Detect structural software decay inside targeting infrastructure matrix",
        context={"strategy": "dead-code", "repo": repo, "auto_fix": auto_fix}
    )
        
    planner = Planner()
    tasks = planner.plan_goal(goal)
        
    analysis_engine = StaticAnalysisEngine()
    executor = Executor(orbit_client, analysis_engine)
        
    results = await executor.execute_tasks_concurrent(tasks)
    return results

@cli.command()
@click.option("--repo", required=True, help="Target GitLab reference endpoint address path")
@click.option("--auto-fix", is_flag=True, help="Automatically emit remediation tasks directly into pipeline merge rules")
def audit(repo: str, auto_fix: bool):
    """Run structural multi-layered codebase optimizations sweeps securely"""
    click.echo(f"Initializing repository execution target tracking path: {repo}")
    results = asyncio.run(run_audit_pipeline(repo, auto_fix))
    click.echo(f"🎯 Execution Sequence Dispatched. Process Chain Completed: {len(results)} task operations performed successfully.")

@cli.command()
@click.option("--repo", required=True, help="Target repository string location")
def dead_code(repo: str):
    """Pinpoint code isolation paths requiring automatic cleanup patches"""
    click.echo("Targeting unreferenced endpoints...")
    results = asyncio.run(run_audit_pipeline(repo, auto_fix=True))
    click.echo(f"Process complete. {len(results)} execution steps successfully executed.")

if __name__ == "__main__":
    cli()
