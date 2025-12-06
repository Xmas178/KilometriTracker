"""
Google Maps integration service for KilometriTracker
Handles distance calculation between addresses using Google Maps Distance Matrix API

This service provides:
- Distance calculation between two addresses
- Route data extraction from Google Maps
- Error handling for API failures
"""

import googlemaps
from django.conf import settings
from decimal import Decimal
from apps.core.exceptions import GoogleMapsAPIError, InvalidAddressError
import logging

# Get logger for this module
logger = logging.getLogger(__name__)


class GoogleMapsService:
    """
    Service class for Google Maps Distance Matrix API

    Handles all Google Maps API interactions for distance calculation.

    Usage:
        service = GoogleMapsService()
        result = service.calculate_distance("Oulu, Finland", "Helsinki, Finland")
        # Returns: {'distance_km': 607.5, 'route_data': {...}}

    Attributes:
        client: Google Maps API client instance
    """

    def __init__(self):
        """
        Initialize Google Maps client

        Raises:
            GoogleMapsAPIError: If API key is not configured
        """

        # Get API key from Django settings
        api_key = settings.GOOGLE_MAPS_API_KEY

        if not api_key:
            # API key not configured - this is critical error
            logger.error("Google Maps API key not configured in settings")
            raise GoogleMapsAPIError(
                "Google Maps API is not configured. "
                "Please add GOOGLE_MAPS_API_KEY to environment variables."
            )

        # Initialize Google Maps client
        try:
            self.client = googlemaps.Client(key=api_key)
            logger.info("Google Maps client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Maps client: {str(e)}")
            raise GoogleMapsAPIError(f"Failed to initialize Google Maps: {str(e)}")

    def calculate_distance(self, start_address, end_address):
        """
        Calculate distance between two addresses using Google Maps

        Makes request to Google Maps Distance Matrix API to get
        distance and route information.

        Args:
            start_address (str): Starting location address
            end_address (str): Destination address

        Returns:
            dict: Dictionary containing:
                - distance_km (Decimal): Distance in kilometers
                - distance_meters (int): Distance in meters (from API)
                - duration_seconds (int): Estimated duration in seconds
                - route_data (dict): Full Google Maps API response
                - start_address (str): Geocoded start address
                - end_address (str): Geocoded end address

        Raises:
            InvalidAddressError: If addresses are empty or invalid
            GoogleMapsAPIError: If API call fails

        Example:
            result = service.calculate_distance(
                "Oulu, Finland",
                "Helsinki, Finland"
            )
            print(result['distance_km'])  # 607.5
        """

        # Validate addresses are not empty
        if not start_address or not start_address.strip():
            raise InvalidAddressError("Start address cannot be empty")

        if not end_address or not end_address.strip():
            raise InvalidAddressError("End address cannot be empty")

        # Strip whitespace
        start_address = start_address.strip()
        end_address = end_address.strip()

        logger.info(f"Calculating distance: '{start_address}' -> '{end_address}'")

        try:
            # Call Google Maps Distance Matrix API
            # This API returns distance and duration between locations
            result = self.client.distance_matrix(
                origins=[start_address],
                destinations=[end_address],
                mode="driving",  # Calculate driving distance
                units="metric",  # Use kilometers, not miles
            )

            # Log API response for debugging
            logger.debug(f"Google Maps API response: {result}")

            # Extract distance data from response
            # API response structure:
            # {
            #   'rows': [{
            #     'elements': [{
            #       'distance': {'value': 607500, 'text': '608 km'},
            #       'duration': {'value': 21600, 'text': '6 hours'},
            #       'status': 'OK'
            #     }]
            #   }],
            #   'origin_addresses': ['Oulu, Finland'],
            #   'destination_addresses': ['Helsinki, Finland']
            # }

            # Check if API returned valid response
            if result["status"] != "OK":
                logger.error(f"Google Maps API error: {result['status']}")
                raise GoogleMapsAPIError(
                    f"Google Maps API returned error: {result['status']}"
                )

            # Get first row (we only sent one origin)
            row = result["rows"][0]

            # Get first element (we only sent one destination)
            element = row["elements"][0]

            # Check element status
            if element["status"] != "OK":
                # Common statuses:
                # - NOT_FOUND: Address not found
                # - ZERO_RESULTS: No route found
                # - MAX_ROUTE_LENGTH_EXCEEDED: Route too long
                logger.warning(
                    f"Could not calculate route: {element['status']} "
                    f"({start_address} -> {end_address})"
                )

                if element["status"] == "NOT_FOUND":
                    raise InvalidAddressError(
                        "One or both addresses could not be found. "
                        "Please check spelling and try again."
                    )
                elif element["status"] == "ZERO_RESULTS":
                    raise GoogleMapsAPIError(
                        "No route found between these addresses. "
                        "They may be on different continents or islands."
                    )
                else:
                    raise GoogleMapsAPIError(
                        f"Could not calculate distance: {element['status']}"
                    )

            # Extract distance in meters (int)
            distance_meters = element["distance"]["value"]

            # Extract duration in seconds (int)
            duration_seconds = element["duration"]["value"]

            # Convert meters to kilometers (Decimal for precision)
            # Google Maps returns meters as integer
            # We convert to km with 2 decimal places
            distance_km = Decimal(distance_meters) / Decimal(1000)

            # Round to 2 decimal places
            distance_km = distance_km.quantize(Decimal("0.01"))

            # Get geocoded addresses (Google's standardized format)
            geocoded_start = result["origin_addresses"][0]
            geocoded_end = result["destination_addresses"][0]

            # Prepare response data
            response_data = {
                "distance_km": distance_km,
                "distance_meters": distance_meters,
                "duration_seconds": duration_seconds,
                "start_address": geocoded_start,
                "end_address": geocoded_end,
                "route_data": result,  # Store full API response
            }

            logger.info(
                f"Distance calculated: {distance_km} km "
                f"({geocoded_start} -> {geocoded_end})"
            )

            return response_data

        except googlemaps.exceptions.ApiError as e:
            # API-specific errors (invalid key, quota exceeded, etc.)
            logger.error(f"Google Maps API error: {str(e)}")
            raise GoogleMapsAPIError(f"Google Maps API error: {str(e)}")

        except googlemaps.exceptions.HTTPError as e:
            # Network/HTTP errors
            logger.error(f"Google Maps HTTP error: {str(e)}")
            raise GoogleMapsAPIError(
                "Failed to connect to Google Maps. Please try again later."
            )

        except googlemaps.exceptions.Timeout as e:
            # Request timeout
            logger.error(f"Google Maps timeout: {str(e)}")
            raise GoogleMapsAPIError("Google Maps request timed out. Please try again.")

        except Exception as e:
            # Catch-all for unexpected errors
            logger.exception(f"Unexpected error in calculate_distance: {str(e)}")
            raise GoogleMapsAPIError(f"An unexpected error occurred: {str(e)}")

    def validate_address(self, address):
        """
        Validate that an address can be geocoded by Google Maps

        This is useful for checking addresses before saving them.

        Args:
            address (str): Address to validate

        Returns:
            bool: True if address is valid, False otherwise

        Example:
            is_valid = service.validate_address("Oulu, Finland")
            if is_valid:
                print("Address is valid!")
        """

        if not address or not address.strip():
            return False

        try:
            # Try to geocode the address
            result = self.client.geocode(address)

            # If geocoding returns results, address is valid
            return len(result) > 0

        except Exception as e:
            logger.warning(f"Address validation failed: {str(e)}")
            return False
