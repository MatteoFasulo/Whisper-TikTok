import subprocess
from dataclasses import dataclass
from logging import Logger
from pathlib import Path


class CommandExecutionError(Exception):
    """Custom exception for command execution errors."""

    pass


class CommandTimeoutError(Exception):
    """Custom exception for command timeouts."""

    pass


@dataclass
class ExecutionResult:
    """Result of command execution."""

    returncode: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        return self.returncode == 0


class CommandExecutor:
    """Executes external commands with error handling."""

    def __init__(self, logger: Logger):
        self.logger = logger

    def execute(self, command: str, cwd: Path | None = None, timeout: int | None = None) -> ExecutionResult:
        """Execute command and return result."""

        self.logger.debug(f"Executing: {command}")
        try:
            with subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as process:
                stdout, stderr = process.communicate(timeout=timeout)
                result = ExecutionResult(returncode=process.returncode, stdout=stdout, stderr=stderr)

            return ExecutionResult(returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        except subprocess.TimeoutExpired as exc:
            self.logger.error(f"Command timed out: {command}")
            raise CommandTimeoutError(f"Command timed out after {timeout}s") from exc
        except Exception as exc:
            self.logger.exception(f"Command execution failed: {command}")
            raise CommandExecutionError(str(exc)) from exc
