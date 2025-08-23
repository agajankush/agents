from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from typing import List, Optional
from openai import OpenAI

load_dotenv(override=True)

class Product(BaseModel):
    product_name: str = Field(
        description="The full, official name of the product."
    )
    brand: str = Field(
        description="The manufacturer or brand of the product (e.g., 'Bandai Spirits')."
    )
    series: Optional[str] = Field(
        default=None,
        description="The specific series or franchise the product belongs to (e.g., 'Mobile Suit Gundam')."
    )
    category: Optional[str] = Field(
        default=None,
        description="The general category of the product (e.g., 'Model Kit', 'Action Figure')."
    )
    scale: Optional[str] = Field(
        default=None,
        description="The scale ratio of the model, if applicable (e.g., '1/100', '1/144')."
    )
    release_date: Optional[str] = Field(
        default=None,
        description="The original or scheduled release date of the product in YYYY-MM-DD format."
    )
    availability: str = Field(
        description="The current stock status (e.g., 'In Stock', 'Pre-order', 'Out of Stock')."
    )
    price: float = Field(
        description="The standard retail price of the product in the specified currency."
    )
    discounted_price: Optional[float] = Field(
        default=None,
        description="The sale or discounted price, if available."
    )
    currency: str = Field(
        description="The ISO 4217 currency code for the price (e.g., 'USD', 'JPY')."
    )
    shipping_cost: Optional[float] = Field(
        default=None,
        description="The cost of shipping, if a flat rate is listed. Exclude if it needs calculation."
    )
    store_location: Optional[str] = Field(
        default=None,
        description="The physical city and state/country of the store, if available."
    )
    stock_quantity: Optional[int] = Field(
        default=None,
        description="The number of items available in stock, if specified."
    )
    store_name: str = Field(
        description="The name of the online or physical store selling the product."
    )
    store_url: str = Field(
        description="The base URL or homepage of the store's website."
    )
    url: str = Field(
        description="The direct URL of the specific product page being viewed."
    )
    store_region: Optional[str] = Field(
        default=None,
        description="The geographic region the store primarily serves (e.g., 'USA', 'EU')."
    )
    images: List[str] = Field(
        description="A list of direct URLs to the product images."
    )
    description: str = Field(
        description="A detailed paragraph describing the product, including its features and any included accessories."
    )
    product_id: str = Field(
        description="The unique product identifier, SKU, model number, or barcode."
    )
# Agent which will output the search terms to use
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

def web_scraper(html_page : str) -> Product:
    completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful web scraper. Given an html page, extract the data for the product. Be sure the data is in the JSON format. Use the extract_product_info tool to extract the data."},
                {
                "role": "user",
                "content": html_page,
                },
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "extract_product_info",
                        "description": "Extracts key details about a product.",
                        "parameters": Product.model_json_schema()
                    }
                }
            ],
            tool_choice={"type": "function", "function": {"name": "extract_product_info"}}
    )
    tool_call = completion.choices[0].message.tool_calls[0]
    json_output_string = tool_call.function.arguments

    product_data = Product.model_validate_json(json_output_string)

    return product_data