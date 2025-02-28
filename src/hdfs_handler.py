import os

def upload_to_hdfs(local_path, hdfs_path):
    """Uploads a file from local storage to HDFS."""
    command = f"hdfs dfs -put -f {local_path} {hdfs_path}"
    exit_code = os.system(command)

    if exit_code == 0:
        print(f"✅ Successfully uploaded {local_path} to HDFS at {hdfs_path}")
    else:
        print(f"❌ Failed to upload {local_path} to HDFS. Check HDFS connection.")

# Example usage
if __name__ == "__main__":
    local_file = "tfl_data.json"
    hdfs_destination = "/data/tfl/raw/tfl_data.json"
    upload_to_hdfs(local_file, hdfs_destination)
