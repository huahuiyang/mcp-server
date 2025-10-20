"""
Simple prompts registry for veFaaS MCP Server tools.

Usage patterns:
- Programmatic registration (recommended): call add_prompts("tool_name", [...]) near tool definitions.
- Querying: call get_prompts() or get_prompts("tool_name") from code or expose via an MCP tool.

This module is intentionally small and dependency-free.
"""
from typing import Dict, List, Optional, Callable, Any

_PROMPTS: Dict[str, List[str]] = {}

def register_prompts_for(name: str, prompts: List[str]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register prompts for a tool function.

    Usage:
      @register_prompts_for("pull_function_code", ["下载函数代码到 /tmp/foo", "获取函数 abc 的代码并展现文件结构"])
      def pull_function_code(...):
          ...
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        _PROMPTS[name] = prompts
        return func
    return decorator

def add_prompts(name: str, prompts: List[str]) -> None:
    """Programmatically add or update prompts for a tool."""
    _PROMPTS[name] = prompts

def get_prompts(name: Optional[str] = None):
    """
    Return prompts for a specific tool or all prompts if name is None.

    Returns:
      If name provided: { name: [prompts...] }
      Otherwise: { tool_name: [prompts...], ... }
    """
    if name:
        return {name: _PROMPTS.get(name, [])}
    return dict(_PROMPTS)