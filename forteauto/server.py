import uvicorn
from forteauto.conf import config as base_config


def main():
    uvicorn.run(
        "forteauto.main:app",
        reload=base_config.settings.debug,
        workers=4,
        debug=base_config.settings.debug)


if __name__ == "__main__":
    main()
