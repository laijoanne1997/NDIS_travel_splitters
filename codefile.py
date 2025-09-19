import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

def geocode_address(address, geolocator):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not geocode address: {address}")
            return None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None

def create_geomap(addresses, coordinates, filename="travel_map.html"):
    fmap = folium.Map(location=coordinates[0], zoom_start=13)
    for i, (address, coord) in enumerate(zip(addresses, coordinates)):
        folium.Marker(coord, popup=f"{address} ({i+1})").add_to(fmap)
        if i > 0:
            folium.PolyLine([coordinates[i-1], coord], color="blue").add_to(fmap)
    fmap.save(filename)
    print(f"Map saved as {filename}")

def calculate_total_distance(coordinates):
    total_distance = 0.0
    for i in range(1, len(coordinates)):
        total_distance += geodesic(coordinates[i-1], coordinates[i]).km
    return total_distance

def main():
    print("Enter the addresses travelled to, one per line. Enter a blank line to finish:")
    addresses = []
    while True:
        address = input("Address: ").strip()
        if not address:
            break
        addresses.append(address)

    num_clients = int(input("How many clients were seen during travel? "))
    travel_rate_per_hour = float(input("How much is charged for travel per hour (in dollars)? "))
    avg_speed_kmh = float(input("Enter average travel speed in km/h (e.g., 60): "))

    geolocator = Nominatim(user_agent="travel_cost_splitter")
    coordinates = []
    print("Geocoding addresses...")
    for address in addresses:
        coord = None
        while coord is None:
            coord = geocode_address(address, geolocator)
            if coord is None:
                print("Please try again or check the address.")
                address = input(f"Re-enter address for {address}: ").strip()
        coordinates.append(coord)
        time.sleep(1)  # avoid rate limiting

    create_geomap(addresses, coordinates)

    total_distance = calculate_total_distance(coordinates)
    print(f"Total travel distance: {total_distance:.2f} km")

    total_travel_time_hours = total_distance / avg_speed_kmh
    print(f"Estimated total travel time: {total_travel_time_hours:.2f} hours")

    total_cost = total_travel_time_hours * travel_rate_per_hour
    print(f"Total travel cost: ${total_cost:.2f}")

    cost_per_client = total_cost / num_clients if num_clients > 0 else 0
    print(f"Travel cost per client: ${cost_per_client:.2f}")

if __name__ == "__main__":
    main()