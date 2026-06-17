import json
from pathlib import Path


LOG_FILE = Path("logs/agent_trail.jsonl")


class DebugLogger:

    @staticmethod
    def write_log(data):

        LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=None,
                    default=str
                )
            )

            f.write("\n")