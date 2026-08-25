import shutil
import subprocess


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None

def run_command(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""