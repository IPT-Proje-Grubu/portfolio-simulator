"""Application entry point for the portfolio simulator."""

from src.app import main as run_application


def main() -> int:
    return run_application()


if __name__ == "__main__":
    raise SystemExit(main())
