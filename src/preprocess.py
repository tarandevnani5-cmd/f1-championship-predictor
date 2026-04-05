import pandas as pd
import os


def load_and_preprocess(data_dir="data/"):
    """
    Load real Kaggle F1 CSVs and build a feature set per driver per season.
    Target: is_champion (1 if driver won the championship that year)
    """

    # ── Load CSVs ────────────────────────────────────────────────────────────
    standings = pd.read_csv(os.path.join(data_dir, "driver_standings.csv"))
    results   = pd.read_csv(os.path.join(data_dir, "results.csv"))
    races     = pd.read_csv(os.path.join(data_dir, "races.csv"))

    # ── Get last round of each season ────────────────────────────────────────
    race_info  = races[["raceId", "year", "round"]]
    last_round = races.groupby("year")["round"].max().reset_index()
    last_round.columns = ["year", "last_round"]

    # ── Merge standings with year & round ────────────────────────────────────
    standings = standings.merge(race_info, on="raceId")
    standings = standings.merge(last_round, on="year")

    # ── Keep only final standings of each season ─────────────────────────────
    final = standings[standings["round"] == standings["last_round"]].copy()
    final["is_champion"] = (final["position"] == 1).astype(int)

    # ── Merge results with year ───────────────────────────────────────────────
    results = results.merge(race_info, on="raceId")

    # ── Feature: podiums (top 3 finishes) ────────────────────────────────────
    podiums = (
        results[results["position"].isin(["1", "2", "3"])]
        .groupby(["driverId", "year"])
        .size()
        .reset_index(name="podiums")
    )

    # ── Feature: DNFs (statusId != 1 means did not finish) ───────────────────
    dnfs = (
        results[results["statusId"] != 1]
        .groupby(["driverId", "year"])
        .size()
        .reset_index(name="dnfs")
    )

    # ── Feature: total races entered per driver per season ───────────────────
    races_entered = (
        results.groupby(["driverId", "year"])
        .size()
        .reset_index(name="races_entered")
    )

    # ── Build final feature table ─────────────────────────────────────────────
    # Note: 'wins' column already exists in driver_standings!
    features = final[["driverId", "year", "points", "wins", "is_champion"]].copy()
    features = features.merge(podiums,      on=["driverId", "year"], how="left")
    features = features.merge(dnfs,         on=["driverId", "year"], how="left")
    features = features.merge(races_entered,on=["driverId", "year"], how="left")

    features.fillna(0, inplace=True)

    print(f"✅ Dataset ready: {len(features)} rows | "
          f"{features['year'].nunique()} seasons | "
          f"{int(features['is_champion'].sum())} champions")

    return features


if __name__ == "__main__":
    df = load_and_preprocess()
    print(df[df["is_champion"] == 1][["year", "driverId", "points", "wins", "podiums"]].tail(10))