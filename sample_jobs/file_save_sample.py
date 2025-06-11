import json
import os
import sys

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 0)
FAIL_RATE = os.getenv("FAIL_RATE", 0)


# Define main script
def main():
    print(f"Starting File Save Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")
    file_name = "test_file.txt"
    text = "test"
    path = "/result"

    print(f"Writing to file , path={path}, filename={file_name} ...")
    with open(os.path.join(path,file_name),"w") as o:
        print(text, file=o) 

    print(f"Completed Task #{TASK_INDEX}.")

# Start script
if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process