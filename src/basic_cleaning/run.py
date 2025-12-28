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


def go(args):

    # Initialize wandb once
    run = wandb.init(project="nyc_airbnb", group="cleaning", job_type="basic_cleaning", save_code=True)
    run.config.update(args)

    # Download input artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Filter longitude/latitude bounds
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save the cleaned file using the output artifact name
    output_file = args.output_artifact
    df.to_csv(output_file, index=False)

    # Log the new data
    artifact = wandb.Artifact(
        name=output_file,           # artifact name
        type=args.output_type,      # artifact type
        description=args.output_description,
    )
    artifact.add_file(output_file)
    run.log_artifact(artifact)
    logger.info(f"Logged cleaned data as {output_file} with type {args.output_type}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of artifact to be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of output artifact (will be saved as this filename)",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output artifact in W&B",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price to filter outliers",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price to filter outliers",
        required=True
    )

    args = parser.parse_args()

    go(args)
