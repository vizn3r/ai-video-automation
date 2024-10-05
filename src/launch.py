from os import environ, path
from scripts.utils import Error, Info

# Check validity of environment variables
if not path.exists(environ["IMAGEMAGICK_BINARY"]):
    Error("Invalid 'IMAGEMAGICK_BINARY' path")
    exit(0)

if not path.exists(environ["OUTPUT_DIR"]):
    Error("Invalid 'OUTPUT_DIR' path")
    exit(0)

if not path.exists(environ["VIDEO_INPUT_DIR"]):
    Error("Invalid 'VIDEO_INPUT_DIR' path")
    exit(0)

if not path.exists(environ["POST_LIST"]):
    Info("Creating new 'POST_LIST' file: '" + environ["POST_LIST"] + "'")
    f = open(environ["POST_LIST"], "w")
    f.close()
    exit(0)

if not path.exists(environ["LLM_PATH"]):
    Error("Invalid 'LLM_PATH' path")
    exit(0)

if not path.exists(environ["YT_SECRET"]):
    Error("Invalid 'YT_SECRET' path")
    exit(0)

if not path.exists(environ["IG_SECRET"]):
    Error("Invalid 'IG_SECRET' path")
    exit(0)

if not path.exists(environ["CONFIG_PATH"]):
    Error("Invalid 'CONFIG_PATH' path")
    exit(0)

if environ["MODE"] == "TESTING":
    Info("TESTING mode enabled")
    exit(0)

else:
    Info("Launching 'short.py'")
    from scripts.video import main
    main()
