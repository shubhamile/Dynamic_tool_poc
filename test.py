

import os
from typing import List, Optional, Union

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class RangeInt(BaseModel):
    min: Optional[int] = Field(
        default=None,
        description="Minimum value. Used with max to define a range."
    )
    max: Optional[int] = Field(
        default=None,
        description="Maximum value. Used with min to define a range."
    )
    strict: Optional[bool] = Field(
        default=False,
        description="If true, min and max must be the same to match exact value."
    )

class PropertyDetails(BaseModel):
    purchasetype: Optional[str] = Field(default=None, description="Type of purchase (e.g., rent, buy, lease)")
    condition: Optional[str] = Field(default=None, description="Condition of the property (e.g., new, good, needs repair)")
    
    price: Optional[Union[float, RangeInt]] = Field(
        default=None,
        description="Sale price of the property. Can be a float or a range with strict option."
    )
    
    rentalprice: Optional[Union[float, RangeInt]] = Field(
        default=None,
        description="Rental price of the property. Can be a float or a range with strict option."
    )
    
    bedrooms: Optional[Union[int, RangeInt]] = Field(
        default=None,
        description="Number of bedrooms. Can be a number or a range with strict option."
    )
    
    bathrooms: Optional[Union[int, RangeInt]] = Field(
        default=None,
        description="Number of bathrooms. Can be a number or a range with strict option."
    )
    
    squarefeet: Optional[Union[int, RangeInt]] = Field(
        default=None,
        description="Total area in square feet. Can be a number or a range with strict option."
    )

    make: Optional[str] = Field(default=None, description="Make or builder of the property (if applicable)")
    year: Optional[int] = Field(default=None, description="Year the property was built")
    featureflags: Optional[List[str]] = Field(default_factory=list, description="Flags for special features (e.g., sea_view, penthouse)")
    features: Optional[List[str]] = Field(default_factory=list, description="Descriptive features (e.g., balcony, modular kitchen)")
    community_name: Optional[str] = Field(default=None, description="Name of the community or society")
    address: Optional[str] = Field(default=None, description="Full address or location of the property")
    communityType: Optional[str] = Field(default=None, description="Type of community (e.g., gated, open, retirement)")
    exploreSection: Optional[str] = Field(default=None, description="Section or category to highlight (e.g., featured, hot deals)")
    amenities: Optional[List[str]] = Field(default_factory=list, description="List of main amenities (e.g., gym, pool)")
    moreAmenities: Optional[List[str]] = Field(default_factory=list, description="Additional amenities beyond the main list")

os.environ["GOOGLE_API_KEY"] = "AIzaSyC4caXCogyYT2FQ00NLLx5ttd0n8hnq-fQ"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
structured_llm = llm.with_structured_output(PropertyDetails)

query = "I want a 3 to 5 bedroom apartment with 2 bathrooms in New York, preferably with a gym and pool."

import time

start_time = time.time()

result = structured_llm.invoke(query)
end_time = time.time()
print(result)
print(f"Execution time: {end_time - start_time:.2f} seconds")

