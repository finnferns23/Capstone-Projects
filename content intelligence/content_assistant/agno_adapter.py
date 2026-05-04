class AgnoAdapter:
    def __init__(self) -> None:
        self.available = self._check_available()

    def _check_available(self) -> bool:
        try:
            import agno  # noqa: F401
            return True
        except Exception:
            return False

    def status(self) -> str:
        return "Agno available" if self.available else "Agno optional adapter ready; install agno to enable."
