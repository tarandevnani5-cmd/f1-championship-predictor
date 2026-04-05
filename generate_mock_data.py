import pandas as pd
import os

def generate_mock_data():
    """Create a robust mock CSV for testing the F1 MLOps pipeline."""
    os.makedirs('data', exist_ok=True)

    # 1. Races (5 years, 10 races each)
    races_data = []
    for y_off in range(5):
        year = 2023 - y_off
        for r in range(1, 11):
            r_id = 10 * y_off + r
            races_data.append({'raceId': r_id, 'year': year, 'round': r, 'name': f'Race{r_id}'})
    pd.DataFrame(races_data).to_csv('data/races.csv', index=False)

    # 2. Results & Standings 
    results_data = []
    standings_data = []
    
    for y_off in range(5):
        year = 2023 - y_off
        last_race_id = 10 * y_off + 10
        
        for driver_id in range(1, 11): # 10 drivers
            is_champ = (driver_id == (y_off % 10 + 1)) # One unique champion per year
            pos = 1 if is_champ else (driver_id + 1)
            
            # Results (10 races for this driver)
            for r in range(1, 11):
                r_id = 10 * y_off + r
                results_data.append({
                    'raceId': r_id, 
                    'driverId': driver_id, 
                    'position': str(pos), 
                    'statusId': 1
                })
            
            # Final Standing
            standings_data.append({
                'raceId':   last_race_id,
                'driverId': driver_id,
                'points':   250 if is_champ else (200 - driver_id * 10),
                'position': 1 if is_champ else (driver_id + 1),
                'wins':     8 if is_champ else 1
            })

    pd.DataFrame(results_data).to_csv('data/results.csv', index=False)
    pd.DataFrame(standings_data).to_csv('data/driver_standings.csv', index=False)

    # 3. Drivers
    drivers = pd.DataFrame({
        'driverId': range(1, 11),
        'forename': [f'Driver{i}' for i in range(1,11)],
        'surname':  [f'Lastname{i}' for i in range(1,11)]
    })
    drivers.to_csv('data/drivers.csv', index=False)

    print("✅ Robust mock data generated (50 rows, 5 champions)")

if __name__ == "__main__":
    generate_mock_data()
