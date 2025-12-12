import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_dog_by_name(dog_name: str) -> Optional[Dict[str, str]]:
    """
    Find a specific dog by name on the Nakarm Psa website

    Args:
        dog_name: Name of the dog to search for (case-insensitive)

    Returns:
        Dictionary with dog information or None if not found
    """
    url = "https://nakarmpsa.olx.pl/"

    try:
        logger.info(f"Searching for dog: {dog_name}")

        # Fetch the webpage with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all dog containers
        dogs = soup.find_all('div', class_='single-pet')

        if not dogs:
            logger.warning("No dogs found on the page")
            return None

        # Search for the specific dog
        for dog in dogs:
            name_element = dog.find('div', class_='single-pet-name-inner')
            if name_element:
                name = name_element.get_text().strip()

                if name.lower() == dog_name.lower():
                    # Extract dog information
                    dog_info = {
                        'name': name,
                        'id': dog.get('data-pet-id'),
                        'votes': dog.get('data-pet-votes'),
                        'type': dog.get('data-pet-type'),
                        'html_id': dog.get('id'),
                    }

                    # Get image URL
                    img_div = dog.find('div', class_='single-pet-image-inner')
                    if img_div:
                        dog_info['image_url'] = img_div.get('data-lazy-background')

                    # Get profile URL
                    link = dog.find('a', href=True)
                    if link:
                        dog_info['profile_url'] = link['href']

                    # Get vote percentage
                    bone_label = dog.find('div', class_='bone-label')
                    if bone_label:
                        dog_info['percentage'] = bone_label.get_text().strip()

                    logger.info(f"Found dog: {name} with {dog_info.get('votes', 'unknown')} votes")
                    return dog_info

        logger.warning(f"Dog '{dog_name}' not found on the page")
        return None

    except requests.Timeout:
        logger.error("Request timed out while fetching website")
        return None
    except requests.RequestException as e:
        logger.error(f"Error fetching website: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


if __name__ == "__main__":
    # Test the function
    dog_names = ["Piorun", "Azorek", "Feniks"]

    for name in dog_names:
        dog = find_dog_by_name(name)
        if dog:
            print(f"\n{'=' * 50}")
            print(f"Found dog: {dog['name']}")
            print(f"ID: {dog['id']}")
            print(f"Votes: {dog['votes']}")
            print(f"Percentage: {dog.get('percentage', 'N/A')}")
            print(f"Profile URL: {dog.get('profile_url', 'N/A')}")
            print(f"Image URL: {dog.get('image_url', 'N/A')}")
        else:
            print(f"Dog '{name}' not found")

