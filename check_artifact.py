import os
import wandb

# Replace with your artifact name as shown in WandB
ARTIFACT_NAME = "trainval_data.csv:v1"

def main():
    print(f"Checking artifact: {ARTIFACT_NAME}")
    api = wandb.Api()
    
    try:
        artifact = api.artifact(ARTIFACT_NAME)
        artifact_dir = artifact.download()
        print(f"Artifact downloaded to: {artifact_dir}")
        
        # Check CSV files inside
        csv_files = [f for f in os.listdir(artifact_dir) if f.endswith(".csv")]
        if len(csv_files) != 1:
            print(f"Expected exactly one CSV file, found: {csv_files}")
        else:
            print(f"CSV file found: {csv_files[0]}")
            csv_path = os.path.join(artifact_dir, csv_files[0])
            print(f"Full path: {csv_path}")
    
    except Exception as e:
        print(f"Error accessing artifact: {e}")

if __name__ == "__main__":
    main()

