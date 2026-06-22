"""Configuration Management via Pydantic Settings"""
import os
import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class OrbitConfig(BaseModel):
    api_url: str = "https://gitlab.com/api/v4/orbit"
    token: str = "DEFAULT_TOKEN"

class GitLabConfig(BaseModel):
    api_url: str = "https://gitlab.com/api/v4"
    token: str = "DEFAULT_TOKEN"

class AgentSettings(BaseModel):
    max_concurrent_tasks: int = 5
    auto_create_mrs: bool = True
    risk_threshold: str = "medium"

class AppConfig(BaseSettings):
    orbit: OrbitConfig = OrbitConfig()
    gitlab: GitLabConfig = GitLabConfig()
    agent: AgentSettings = AgentSettings()

def load_config() -> AppConfig:
    config_path = os.path.join("config", "orbit-agent.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            yaml_data = yaml.safe_load(f) or {}
            return AppConfig(**yaml_data)
    return AppConfig()
