"""Planner Agent - Multi-Agent Architecture Component
Breaks high-level goals into atomic tasks, prioritizes by impact/risk,
handles dependencies."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from src.utils.logging import get_logger

logger = get_logger("planner")

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    name: str
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None

@dataclass
class Goal:
    id: str
    name: str
    description: str
    context: Dict[str, Any] = field(default_factory=field)

class PlannerStrategy(ABC):
    @abstractmethod
    def plan(self, goal: Goal) -> List[Task]:
        pass

class DeadCodePlanner(PlannerStrategy):
    def plan(self, goal: Goal) -> List[Task]:
        tasks = [
            Task(
                id="dc-1-query",
                name="Query Orbit for unused files",
                description="Find files with no inbound edges",
                priority=TaskPriority.HIGH,
                metadata={"orbit_query_type": "inbound_edges"}
            ),
            Task(
                id="dc-2-static",
                name="Static analysis validation",
                description="Verify via AST parsing",
                priority=TaskPriority.HIGH,
                dependencies=["dc-1-query"]
            ),
            Task(
                id="dc-3-semantic",
                name="Semantic analysis validation",
                description="Check runtime traces",
                priority=TaskPriority.MEDIUM,
                dependencies=["dc-2-static"]
            ),
            Task(
                id="dc-4-patch",
                name="Generate removal patches",
                description="Create git patches",
                priority=TaskPriority.HIGH,
                dependencies=["dc-3-semantic"]
            ),
            Task(
                id="dc-5-mr",
                name="Create merge requests",
                description="Open MRs with patches",
                priority=TaskPriority.CRITICAL,
                dependencies=["dc-4-patch"]
            ),
        ]
        logger.info(f"Planned {len(tasks)} tasks for goal: {goal.name}")
        return tasks

class Planner:
    def __init__(self):
        self.strategies: Dict[str, PlannerStrategy] = {}
        self.register_strategy("dead-code", DeadCodePlanner())
        
    def register_strategy(self, name: str, strategy: PlannerStrategy):
        self.strategies[name] = strategy
        
    def plan_goal(self, goal: Goal) -> List[Task]:
        strategy_name = goal.context.get("strategy", "dead-code")
        strategy = self.strategies.get(strategy_name)
                
        if not strategy:
            raise ValueError(f"Unknown strategy: {strategy_name}")
                
        tasks = strategy.plan(goal)
        tasks.sort(key=lambda t: t.priority)
                
        logger.info(f"Planned {len(tasks)} tasks ordered by execution priority thresholds")
        return tasks
