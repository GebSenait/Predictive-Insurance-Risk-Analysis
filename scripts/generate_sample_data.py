"""Generate a small synthetic dataset with the same schema as MachineLearningRating_v3.txt.

Use this for local development and CI when the full DVC-tracked dataset is unavailable
or causes out-of-memory errors. Output is pipe-delimited (|) to match production.

Schema (aligned with production and tests/fixtures/sample_insurance_data.csv):
  PolicyID, Province, PostalCode, Gender, Age, TotalPremium, TotalClaims, VehicleType

Output: data/raw/MachineLearningRating_sample.txt
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "MachineLearningRating_sample.txt"
SEED = 42
N_ROWS = 12_000  # Enough for train/test and severity subset (TotalClaims > 0)


def main() -> None:
    np.random.seed(SEED)
    rng = np.random.default_rng(SEED)

    provinces = ["Gauteng", "WesternCape", "KwaZuluNatal", "EasternCape", "Limpopo"]
    postal_codes = [2001, 2002, 2003, 7001, 7002, 4001, 4002, 5001, 5002, 6001]
    genders = ["Male", "Female"]
    vehicle_types = ["Sedan", "Hatchback", "SUV", "Truck"]

    n = N_ROWS
    df = pd.DataFrame(
        {
            "PolicyID": np.arange(1, n + 1),
            "Province": rng.choice(provinces, size=n),
            "PostalCode": rng.choice(postal_codes, size=n),
            "Gender": rng.choice(genders, size=n),
            "Age": np.clip(rng.integers(18, 70, size=n), 18, 69),
            "TotalPremium": np.round(
                np.clip(600 + rng.lognormal(0, 0.6, size=n) * 400, 400, 3500), 2
            ),
            "TotalClaims": np.round(
                np.where(
                    rng.random(size=n) < 0.35,  # ~35% with claims
                    np.clip(rng.lognormal(5, 1.2, size=n) * 20, 10, 2500),
                    0.0,
                ),
                2,
            ),
            "VehicleType": rng.choice(vehicle_types, size=n),
        }
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, sep="|", index=False)
    print(f"Wrote {OUTPUT_FILE} ({len(df)} rows, {len(df.columns)} columns)")
    n_with_claims = (df["TotalClaims"] > 0).sum()
    print(f"  Rows with claims (for severity): {n_with_claims}")
    return None


if __name__ == "__main__":
    main()
    sys.exit(0)
