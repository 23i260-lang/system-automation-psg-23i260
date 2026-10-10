
import os
import random
from datetime import datetime

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "sentinel_log.txt")

MACHINES = {
    "M1": "Hydraulic Press",
    "M2": "Cooling Unit",
    "M3": "Assembly Robot",
    "M4": "Packaging Line",
    "M5": "Power Generator"
}

FAULTS = {
    "fire": (100, "CRITICAL", "Activate emergency procedures"),
    "smoke": (98, "CRITICAL", "Stop safely and investigate smoke"),
    "electrical": (95, "CRITICAL", "Isolate power safely; call a technician"),
    "overheating": (90, "CRITICAL", "Stop safely and inspect cooling"),
    "pressure leak": (85, "HIGH", "Safely isolate the affected system"),
    "motor failure": (80, "HIGH", "Inspect motor and power supply"),
    "vibration": (70, "HIGH", "Inspect bearings and alignment"),
    "coolant leak": (65, "HIGH", "Inspect and contain the leak"),
    "sensor failure": (45, "MEDIUM", "Check sensor and connections"),
    "slow operation": (35, "MEDIUM", "Inspect load and operating speed"),
    "maintenance": (15, "LOW", "Schedule preventive maintenance"),
    "none": (0, "NORMAL", "No action needed")
}


def record(message):
    with open(LOG, "a", encoding="utf-8") as file:
        file.write(f"[{datetime.now()}] {message}\n")


def analyze(description):
    description = description.lower()

    matches = [
        (name, data) for name, data in FAULTS.items()
        if name != "none" and name in description
    ]

    if not description or description == "none":
        return 0, "NORMAL", "No action needed"

    if not matches:
        return 50, "MEDIUM", "Unknown fault: request technician diagnosis"

    name, (score, level, action) = max(
        matches, key=lambda item: item[1][0]
    )
    return score, level, action


def main():
    incidents = []

    print("\n" + "=" * 55)
    print("       SENTINEL X - FACTORY COMMAND CENTER")
    print("=" * 55)
    print("Enter a fault for each machine.")
    print("Examples: overheating, vibration, sensor failure, none")

    record("\n========== NEW SESSION ==========")

    for machine_id, name in MACHINES.items():
        print(f"\n[{machine_id}] {name}")
        fault = input("Describe fault: ").strip() or "unknown"

        score, level, action = analyze(fault)

        incident = {
            "id": machine_id,
            "machine": name,
            "fault": fault,
            "score": score,
            "level": level,
            "action": action
        }

        incidents.append(incident)
        record(f"INPUT | {machine_id} | {name} | {fault}")

    while True:
        incidents.sort(key=lambda item: item["score"], reverse=True)

        print("\n\n" + "=" * 65)
        print("             LIVE PRIORITY DASHBOARD")
        print("=" * 65)

        for rank, item in enumerate(incidents, 1):
            print(f"\n#{rank} {item['id']} - {item['machine']}")
            print(f"   Fault: {item['fault']}")
            print(f"   Severity: {item['level']} | Risk: {item['score']}/100")
            print(f"   Action: {item['action']}")

        active = [item for item in incidents if item["score"] > 0]

        if active:
            first = active[0]
            print("\n>>> FIRST RESPONSE TARGET <<<")
            print(first["machine"], "-", first["fault"])
            print("Recommended:", first["action"])
            record(
                f"TOP PRIORITY | {first['machine']} | "
                f"{first['fault']} | Risk {first['score']} | "
                f"{first['action']}"
            )
        else:
            print("\nAll machines are reporting normal operation.")

        print(f"\nLOG FILE: {LOG}")
        print("\n1. Update a machine fault")
        print("2. Exit")

        choice = input("\nChoose 1 or 2: ").strip()

        if choice == "2":
            record("SESSION ENDED")
            print("\nSENTINEL X stopped. Log saved successfully.")
            break

        if choice == "1":
            machine_id = input("Machine ID (M1-M5): ").strip().upper()

            if machine_id not in MACHINES:
                print("Invalid machine ID.")
                continue

            fault = input("New fault: ").strip() or "unknown"
            score, level, action = analyze(fault)

            for item in incidents:
                if item["id"] == machine_id:
                    item.update({
                        "fault": fault,
                        "score": score,
                        "level": level,
                        "action": action
                    })
                    break

            record(f"UPDATE | {machine_id} | {fault}")
        else:
            print("Please enter 1 or 2.")


if __name__ == "__main__":
    main()
