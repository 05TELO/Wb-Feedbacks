import datetime
import requests
from typing import List, Optional

from src.sku_reader import sku_reader


class NegativeFeedbacks:
    def __init__(self, sku: int) -> None:
        self.sku = sku
        self.name = None
        self.brand = None
        self.root = None
        self.card = self.get_card()
        self.feedbacks = self.get_feedbacks()

    def get_card(self) -> Optional[dict]:
        """
        Retrieves product card information using an API request.

        Returns:
        dict: Dictionary with information about the product card if successful, otherwise None.
        """

        url = f"https://card.wb.ru/cards/detail?nm={self.sku}"
        response = requests.get(url)
        if response.status_code == 200:
            card = response.json()
            self.name = card["data"]["products"][0]["name"]
            self.brand = card["data"]["products"][0]["brand"]
            self.root = card["data"]["products"][0]["root"]
            return card
        return None

    def get_feedbacks(self) -> Optional[dict]:
        """
        Retrieves product feedbacks using an API request.

        Returns:
        dict: Dictionary with product feedbacks if successful, otherwise None.
        """

        url = f"https://feedbacks1.wb.ru/feedbacks/v1/{self.root}"
        response = requests.get(url)
        if response.status_code == 200:
            feedbacks = response.json()
            return feedbacks["feedbacks"]
        return None

    def get_negative_feedback(self) -> List[dict]:
        """
        Gets negative feedback for the product within the last 24 hours.

        Returns:
        List[dict]: List of dictionaries with negative feedback information.
        """
        res = []
        if self.feedbacks:
            for feedback in self.feedbacks:
                feedback_date = datetime.datetime.strptime(
                    feedback["createdDate"], "%Y-%m-%dT%H:%M:%SZ"
                )

                if (datetime.datetime.now() - feedback_date).total_seconds() <= 864000:
                    if feedback["productValuation"] < 5:
                        res.append(
                            {
                                "brand": self.brand,
                                "product_name": self.name,
                                "feedback": feedback["text"],
                                "feedback_rating": feedback["productValuation"],
                            }
                        )

        return res


class SKUManager:
    def __init__(self, file_path: str) -> None:
        self.sku = sku_reader(file_path)

    def get_result(self) -> List[dict]:
        """
        Gets negative feedback for the product for list SKU within the last 24 hours.

        Returns:
        List[dict]: List of dictionaries with negative feedback information.
        """
        result = []
        for product in self.sku:
            feedbacks = NegativeFeedbacks(product)
            result.extend(feedbacks.get_negative_feedback())

        return result if result else [{"message": "No new feedbacks"}]
