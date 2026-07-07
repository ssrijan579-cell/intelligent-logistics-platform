"""
Configuration settings for synthetic logistics data generation.
"""

# Number of records to be generate
NUM_RECORDS = 1_000  # scale to 200000 later

# Random seed for reproducibility
RANDOM_SEED = 42

# Train/Validation/Test split
TRAIN_SPLIT = 0.80
VALIDATION_SPLIT = 0.10
TEST_SPLIT = 0.10