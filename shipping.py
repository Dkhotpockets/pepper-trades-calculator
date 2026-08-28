import argparse
import random
import string

def generate_tracking_number(carrier):
    prefix = "1Z" if carrier.lower() == "ups" else "9400"
    suffix = ''.join(random.choices(string.digits, k=16))
    return f"{prefix}{suffix}"

def estimate_shipping(weight_oz, package_type, destination_zone):
    # Base rate calculation simulation for community trades
    base_rate = 4.50 if package_type == "seeds" else 8.50
    weight_surcharge = (weight_oz / 16.0) * 3.00
    zone_multiplier = 1.0 + (destination_zone * 0.1)
    
    total_cost = (base_rate + weight_surcharge) * zone_multiplier
    return round(total_cost, 2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pepper Trades Logistics & Shipping Calculator")
    parser.add_argument("--type", required=True, choices=["seeds", "sauce"], help="Type of item being shipped")
    parser.add_argument("--weight", type=float, required=True, help="Weight in ounces")
    parser.add_argument("--zone", type=int, default=1, help="Shipping zone distance (1-5)")
    parser.add_argument("--carrier", default="USPS", help="Carrier name (USPS, UPS)")

    args = parser.parse_args()

    cost = estimate_shipping(args.weight, args.type, args.zone)
    tracking = generate_tracking_number(args.carrier)

    print("\n--- SHIPPING ESTIMATE & TRACKING ---")
    print(f"Item Class:      {args.type.capitalize()}")
    print(f"Package Weight:  {args.weight} oz")
    print(f"Carrier Selected:{args.carrier}")
    print(f"Estimated Cost:  ${cost:.2f}")
    print(f"Mock Tracking ID:{tracking}")
    print("------------------------------------\n")
