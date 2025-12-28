#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

# DO NOT MODIFY
def go(args):
    # Start W&B run with job_type basic_cleaning
    run = wandb.init(project=args.wandb_project, entity=args.wandb_entity, job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop outliers based on min_price and max_price
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Filter by longitude and latitude for NYC bounds
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save cleaned CSV
    os.makedirs("data", exist_ok=True)
    cleaned_file_path = "data/clean_sample.csv"
    df.to_csv(cleaned_file_path, index=False)

    # Log cleaned artifact to W&B
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(cleaned_file_path)
    run.log_artifact(artifact)
    logger.info(f"Cleaned data artifact {args.output_artifact} logged to W&B.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="The input dataset artifact name to clean (e.g., 'sample.csv:latest')",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="The name of the artifact where cleaned data will be saved",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="The type of artifact to log (e.g., 'cleaned_data')",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact for W&B logging",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price threshold for listings",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price threshold for listings",
        required=True
    )

    parser.add_argument(
        "--wandb_project",
        type=str,
        help="W&B project name",
        default="nyc_airbnb"
    )

    parser.add_argument(
        "--wandb_entity",
        type=str,
        help="W&B entity/user",
        default="madisoncbayne-western-governors-university"
    )

    args = parser.parse_args()
    go(args)
