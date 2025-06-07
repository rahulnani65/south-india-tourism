from composio_utils import get_place_details, get_route_planning

def test_place_details():
    # Test getting details for a place in South India
    place_name = "Mysore Palace"
    result = get_place_details(place_name)
    print("\nTesting Place Details:")
    print(f"Result for {place_name}:")
    print(result)

def test_route_planning():
    # Test route planning between two places in South India
    origin = "Bangalore"
    destination = "Mysore"
    result = get_route_planning(origin, destination)
    print("\nTesting Route Planning:")
    print(f"Route from {origin} to {destination}:")
    print(result)

if __name__ == "__main__":
    test_place_details()
    test_route_planning() 