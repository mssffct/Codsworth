from litestar import Litestar


async def run_periodic_cleanup(app: Litestar) -> None:
    """
    Runs periodic cleanups
    Args:
        app: application instance
    """
    async with app.state.db_session() as db_session:
        while True:
            app_state: AppState = app.state
