"""Rich terminal output for pipeline-generator."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

if TYPE_CHECKING:
    from ..detector import DetectionResult
    from ..models import PipelineSpec

# Force UTF-8 on Windows to prevent emoji encoding errors
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

console = Console()


def print_header(spec: "PipelineSpec") -> None:
    """Print the generation header banner."""
    framework = f" / {spec.project.framework}" if spec.project.framework else ""
    subtitle = (
        f"Generating CI/CD pipelines for: [bold]{spec.project.name}[/bold] "
        f"({spec.project.language.title()} {spec.project.version}{framework})"
    )
    console.print()
    console.print(
        Panel(
            f"[bold cyan]\U0001f680  PIPELINE GENERATOR v1.0.0[/bold cyan]\n\n{subtitle}",
            border_style="cyan",
            padding=(1, 2),
        )
    )


def print_stages(stages: list[str]) -> None:
    """Print the pipeline stages flow."""
    flow = " \u2192 ".join(f"[bold]{s}[/bold]" for s in stages)
    console.print(f"\n\U0001f4cb Stages: {flow}\n")


def print_platform_result(
    icon: str,
    name: str,
    filename: str,
    content: str,
    dry_run: bool = False,
) -> None:
    """Print the result for a single platform generation."""
    console.print(
        "\u2500" * 78,
        style="dim",
    )
    console.print(f"\n{icon}  [bold]{name}[/bold]  \u2192  [cyan]{filename}[/cyan]\n")

    # Preview: first 12 lines
    preview_lines = content.split("\n")[:12]
    remaining = len(content.split("\n")) - 12
    preview = "\n".join(preview_lines)
    if remaining > 0:
        preview += f"\n# ... ({remaining} more lines)"

    console.print(
        Panel(
            Syntax(preview, "yaml", theme="monokai", line_numbers=False),
            title="[dim]Preview[/dim]",
            border_style="dim",
            padding=(0, 1),
        )
    )

    total_lines = len(content.split("\n"))
    if dry_run:
        console.print(f"  \U0001f4dd Would write to [cyan]{filename}[/cyan] ({total_lines} lines)")
    else:
        console.print(f"  \u2705 Written to [cyan]{filename}[/cyan] ({total_lines} lines)")


def print_summary(results: dict[str, str], dry_run: bool = False) -> None:
    """Print the generation summary."""
    total_files = len(results)
    total_lines = sum(len(c.split("\n")) for c in results.values())

    console.print("\n" + "\u2500" * 78, style="dim")

    action = "previewed" if dry_run else "generated"
    summary = (
        f"[bold green]\u2705 {total_files} pipeline configs {action}[/bold green]\n"
        f"\U0001f4c4 {total_lines} total lines of CI/CD configuration\n"
    )

    filenames = "\n".join(f"  \u2022 [cyan]{f}[/cyan]" for f in results.keys())
    summary += f"\n{filenames}"

    console.print(
        Panel(
            summary,
            title="[bold]SUMMARY[/bold]",
            border_style="green",
            padding=(1, 2),
        )
    )
    console.print()


def print_detection(result: "DetectionResult") -> None:
    """Print auto-detection results."""
    if not result.language:
        console.print(
            Panel(
                "[yellow]Could not detect project type.[/yellow]\n\n"
                "Try running in a project directory, or use:\n"
                "  [cyan]pipe-gen init --preset python[/cyan]",
                title="\U0001f50d Detection",
                border_style="yellow",
            )
        )
        return

    lines: list[str] = []
    lines.append(f"[bold]Language:[/bold]     {result.language.title()} {result.version}")
    if result.framework:
        lines.append(f"[bold]Framework:[/bold]    {result.framework}")
    lines.append(f"[bold]Pkg Manager:[/bold]  {result.package_manager}")
    docker_status = "[green]\u2705 Found[/green]" if result.has_dockerfile else "[dim]\u2796 Not found[/dim]"
    lines.append(f"[bold]Dockerfile:[/bold]   {docker_status}")
    test_status = "[green]\u2705 Found[/green]" if result.has_tests else "[dim]\u2796 Not found[/dim]"
    lines.append(f"[bold]Tests:[/bold]        {test_status}")

    if result.existing_ci:
        lines.append("")
        lines.append("[bold]Existing CI:[/bold]")
        for ci in result.existing_ci:
            lines.append(f"  \u2022 {ci}")

    lines.append("")
    lines.append("[dim]Suggested command:[/dim]")
    lines.append(
        f"  [cyan]pipe-gen init --preset {result.language} --name my-project[/cyan]"
    )

    console.print(
        Panel(
            "\n".join(lines),
            title="\U0001f50d  Project Detection",
            border_style="blue",
            padding=(1, 2),
        )
    )


def print_init_success(output_path: str, preset: str) -> None:
    """Print success message after creating a spec file."""
    console.print(
        Panel(
            f"[green]\u2705 Created [bold]{output_path}[/bold][/green]\n\n"
            f"Preset: [cyan]{preset}[/cyan]\n\n"
            "Next steps:\n"
            f"  1. Edit [cyan]{output_path}[/cyan] to match your project\n"
            "  2. Run [cyan]pipe-gen generate --platform all[/cyan]\n"
            "  3. Commit the generated pipeline files",
            title="\U0001f389  Spec File Created",
            border_style="green",
            padding=(1, 2),
        )
    )


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"\n[bold red]\u274c Error:[/bold red] {message}\n")
