import logging
import coloredlogs

# Create a shared logger instance
log = logging.getLogger("mlops-hypervisor")

# Avoid duplicate logs in multi-import situations
if not log.hasHandlers():
    coloredlogs.install(
        level="INFO",
        logger=log,
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

# Optional: customize per level colors
coloredlogs.DEFAULT_LEVEL_STYLES['info'] = {'color': 'green'}
coloredlogs.DEFAULT_LEVEL_STYLES['warning'] = {'color': 'yellow'}
coloredlogs.DEFAULT_LEVEL_STYLES['error'] = {'color': 'red'}
coloredlogs.DEFAULT_LEVEL_STYLES['critical'] = {'color': 'magenta'}