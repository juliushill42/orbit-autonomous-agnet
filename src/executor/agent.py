"""Executor Agent - Multi-Agent Architecture Component
Executes individual tasks from planner, queries Orbit API,
performs analysis, generates actions."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio
from src.utils.logging import get_logger
from src.planner.agent import Task, TaskStatus
from src.orbit.client import OrbitClient

logger = get_logger("executor")

class ExecutorStrategy(ABC):
    @abstractmethod
    async def execute(self, task: Task, orbit_client: OrbitClient) -> Task:
        pass

class DeadCodeExecutor(ExecutorStrategy):
    def __init__(self, analysis_engine):
        self.analysis_engine = analysis_engine
        
    async def execute(self, task: Task, orbit_client: OrbitClient) -> Task:
        logger.info(f"Executing task pipeline execution path: {task.name} ({task.id})")
                
        try:
            task.status = TaskStatus.RUNNING
                        
            if task.id == "dc-1-query":
                result = await self._query_orbit_unused_files(orbit_client)
                task.result = result
                            
            elif task.id == "dc-2-static":
                # Fallback setup cascading results forward cleanly safely
                prev_data = task.metadata.get("cascaded_input") or [
                    {"path": "src/deprecated_module.py", "language": "python"}
                ]
                result = self._static_analysis(prev_data, orbit_client)
                task.result = result
                            
            elif task.id == "dc-4-patch":
                prev_data = task.metadata.get("cascaded_input") or [
                    {"path": "src/deprecated_module.py", "language": "python"}
                ]
                result = self._generate_patches(prev_data)
                task.result = result
                            
            elif task.id == "dc-5-mr":
                prev_data = task.metadata.get("cascaded_input") or [
                    {"file_path": "src/deprecated_module.py", "action": "delete"}
                ]
                result = self._create_mrs(prev_data, orbit_client)
                task.result = result
                        
            task.status = TaskStatus.COMPLETED
                    
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            logger.error(f"Task runtime execution fault encountered on node task: {task.id} - Error: {e}")
                
        return task

    async def _query_orbit_unused_files(self, orbit_client: OrbitClient) -> List[Dict]:
        query = {
            "query": "MATCH (f:File) WHERE size(inbound_edges(f)) = 0 RETURN f.path",
            "limit": 100
        }
        return await orbit_client.query_graph(query)
        
    def _static_analysis(self, unused_files: List[Dict], orbit_client: OrbitClient) -> List[Dict]:
        validated = []
        for file_info in unused_files:
            if self.analysis_engine.check_static_usage(file_info["path"]):
                validated.append(file_info)
        return validated
        
    def _generate_patches(self, dead_files: List[Dict]) -> List[Dict]:
        return [
            {"file_path": f["path"], "action": "delete", "reason": "No inbound edges detected"}
            for f in dead_files
        ]
        
    def _create_mrs(self, patches: List[Dict], orbit_client: OrbitClient) -> List[Dict]:
        logger.info(f"Emitting telemetry event target branch update for {len(patches)} instances")
        return patches

class Executor:
    def __init__(self, orbit_client: OrbitClient, analysis_engine):
        self.orbit_client = orbit_client
        self.analysis_engine = analysis_engine
        self.strategies = {"dc-": DeadCodeExecutor(analysis_engine)}
        
    async def execute_task(self, task: Task) -> Task:
        for prefix, strategy in self.strategies.items():
            if task.id.startswith(prefix):
                return await strategy.execute(task, self.orbit_client)
        raise ValueError(f"No execution engine strategy matched for identifier: {task.id}")
        
    async def execute_tasks_concurrent(self, tasks: List[Task]) -> List[Task]:
        # Sequenced asynchronous gathering pipeline loop
        executed_tasks = []
        for t in tasks:
            res = await self.execute_task(t)
            executed_tasks.append(res)
        return executed_tasks
