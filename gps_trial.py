import random
from math import radians, sin, cos, sqrt, atan2


# Define the bounding box for Bến Cát
BEN_CAT_REGION = {
    'min_lat': 11.072128,  # Minimum latitude (approximate latitude of Thị Tính river)
    'max_lat': 11.134877,  # Maximum latitude (approximate latitude of Vitadairy Binh Duong factory)
    'min_lon': 106.580999,  # Minimum longitude (approximate longitude of Café Tiến Anh)
    'max_lon': 106.658452   # Maximum longitude (approximate longitude of Miếu Bà)
}

# Number of GPS coordinates to generate
num_coordinates = 1000

# Generate random GPS coordinates within Bến Cát
gps_coordinates = []
for _ in range(num_coordinates):
    lat = round(random.uniform(BEN_CAT_REGION['min_lat'], BEN_CAT_REGION['max_lat']), 6)
    lon = round(random.uniform(BEN_CAT_REGION['min_lon'], BEN_CAT_REGION['max_lon']), 6)
    gps_coordinates.append((lat, lon))

# Export coordinates to a text file
output_file = 'gps_coordinates.txt'
with open(output_file, 'w') as file:
    for lat, lon in gps_coordinates:
        file.write(f'{lat},{lon}\n')

print(f'{num_coordinates} GPS coordinates generated and saved in "{output_file}" file.')



def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    d_lon = lon2_rad - lon1_rad
    d_lat = lat2_rad - lat1_rad

    a = sin(d_lat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Load GPS coordinates from the text file
input_file = 'gps_coordinates.txt'
gps_coordinates = []
with open(input_file, 'r') as file:
    for line in file:
        lat, lon = map(float, line.strip().split(','))
        gps_coordinates.append((lat, lon))

# Home location (VGU)
location_to_check = (11.106550, 106.613027)  



# Check if the GPS tracker is within 1 kilometer range of any point in the region
for lat, lon in gps_coordinates:
    distance = calculate_distance(location_to_check[0], location_to_check[1], lat, lon)
    if distance <= 0.5:
        print(1)
    else:
        print(0)

