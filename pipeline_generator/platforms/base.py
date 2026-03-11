"""Base class for platform pipeline generators."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import PipelineSpec


class BasePlatform(ABC):
    """Abstract base class for CI/CD platform generators."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable platform name."""

    @property
    @abstractmethod
    def icon(self) -> str:
        """Emoji icon for the platform."""

    @property
    @abstractmethod
    def filename(self) -> str:
        """Default output filename (relative path)."""

    @abstractmethod
    def generate(self, spec: PipelineSpec) -> str:
        """Generate the complete pipeline config file content."""

    @staticmethod
    def _gh(expr: str) -> str:
        """Format a GitHub Actions / CI expression: ${{ expr }}."""
        return "${{ " + expr + " }}"

    @staticmethod
    def _quote_versions(versions: list[str]) -> str:
        """Quote version strings for YAML (prevents 3.10 -> 3.1)."""
        return "[" + ", ".join(f'"{v}"' for v in versions) + "]"
