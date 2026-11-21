
import math


def parse_walk_schedule(schedule_spec):
    if not isinstance(schedule_spec, str):
        raise ValueError("Schedule must be a string.")

    parts = schedule_spec.strip().split("-")

    if len(parts) != 3 or any(not part.strip() for part in parts):
        raise ValueError("Enter schedule in pets-minutes-weekend format.")

    pets_str, mins_str, weekend_str = parts

    try:
        pets = int(pets_str.strip())
        mins = int(mins_str.strip())
    except ValueError:
        raise ValueError("Pets and minutes must be valid integers.")

    if pets <= 0 or mins <= 0:
        raise ValueError("Pets and minutes must be positive.")

    weekend_map = {"YES": 15.0, "NO": 0.0}
    weekend = weekend_str.strip().upper()

    if weekend not in weekend_map:
        raise ValueError("Weekend value must be YES or NO.")

    weekend_fee = weekend_map[weekend]
    base_fee = 20.0 if mins <= 30 else 35.0
    total = base_fee + (pets * 5.0) + weekend_fee

    return f"Walk: {pets} pets, {mins} mins - Total ${total:.2f}"


def compute_pace_per_pet(walk_metrics_str):
    if not isinstance(walk_metrics_str, str):
        raise ValueError("Input must be a string.")

    parts = walk_metrics_str.split("/")

    if len(parts) != 2:
        raise ValueError("Enter minutes/pets format.")

    try:
        mins = float(parts[0].strip())
        pets = float(parts[1].strip())
    except ValueError:
        raise ValueError("Minutes and pets must be numbers.")

    if not math.isfinite(mins) or not math.isfinite(pets):
        raise ValueError("Values must be finite numbers.")

    if mins < 0 or pets <= 0:
        raise ValueError("Minutes must be non-negative and pets positive.")

    pace = mins / pets
    return round(pace, 2)


def lookup_temperament_surcharge(temperament_code):
    if not isinstance(temperament_code, str):
        raise ValueError("Temperament must be a string.")

    prefix = temperament_code.strip().upper()[:3]

    surcharges = {
        "CAL": 0.0,
        "PLY": 5.0,
        "REA": 12.0,
        "AGG": 20.0
    }

    if prefix not in surcharges:
        raise ValueError("Unknown temperament code.")

    return surcharges[prefix]


def main():
    print("==== Running parse_walk_schedule ====")
    s_input = input("Enter schedule (e.g. 2-30-YES): ")
    print(parse_walk_schedule(s_input))

    print("\n==== Running compute_pace_per_pet ====")
    p_input = input("Enter minutes/pets (e.g. 45/3): ")
    print("Pace (min/pet):", compute_pace_per_pet(p_input))

    print("\n==== Running lookup_temperament_surcharge ====")
    t_input = input("Enter temperament code (e.g. CALM, PLAYFUL, AGGRESSIVE): ")
    print("Surcharge: $", lookup_temperament_surcharge(t_input))


if __name__ == "__main__":
    main()
