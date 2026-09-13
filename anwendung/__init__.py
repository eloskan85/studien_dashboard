from .dashboard_service import DashboardService

__all__ = ["DashboardService", "Starter"]


def __getattr__(name):
    if name == "Starter":
        from .starter import Starter
        return Starter
    raise AttributeError(name)
