from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
    
class RangeFloat(BaseModel):
    min: Optional[float] = Field(
        default=None,
        description="Minimum value for the field. Used with max to define a numeric range."
    )
    max: Optional[float] = Field(
        default=None,
        description="Maximum value for the field. Used with min to define a numeric range."
    )
    strict: Optional[bool] = Field(
        default=False,
        description="If true, min and max must be the same to match an exact value."
    )
 
class AddressModel(BaseModel):
    city: Optional[str] = Field(
        default=None,
        description="City where the property is located. Only include if the user specifies it."
    )
    state: Optional[str] = Field(
        default=None,
        description="State where the property is located. Only include if the user specifies it."
    )
 
class CommunityModel(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Name of the community. Only include if the user mentions a community name."
    )
    address: Optional[List[str]] = Field(
        default=None,
        description=(
            "List of location components exactly as provided by the user. "
            "Each city, state, or abbreviation (e.g., 'Miami', 'FL') must be a separate string in the list. "
            "Do not combine them into a single string like 'Miami, FL'. "
            "Do not infer or expand values (e.g., 'FL' should not become 'Florida')."
        )
    )
    communityType: Optional[str] = Field(
        default=None,
        description="Type of the community (e.g., villa, apartment). Only include if mentioned by the user."
    )
    amenities: Optional[List[str]] = Field(
        default=None,
        description="Amenities in the community (e.g., gym, pool). Include only if the user specifies any."
    )
 
class CommunityFilter(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Community name. Include only if the user specifies a community."
    )
    code: Optional[str] = Field(
        default=None,
        description="Community code or identifier. Include only if provided or required."
    )
    type: Optional[str] = Field(
        default=None,
        description="Community type (e.g., gated, apartment). Only include if the user mentions it."
    )
 
class HomeModel(BaseModel):
    purchasetype: Optional[str] = Field(
        default=None,
        description="Purchase type such as 'sale' or 'rent'. Include only if the user specifies."
    )
    condition: Optional[str] = Field(
        default=None,
        description="Condition of the home (e.g., new, good, needs renovation). Include only if mentioned."
    )
    price: Optional[RangeFloat] = Field(
        default=None,
        description="Price range for purchase. Include only if the user provides price expectations."
    )
    rentalprice: Optional[RangeFloat] = Field(
        default=None,
        description="Rental price range. Include only if the user provides rental price expectations."
    )
    bedrooms: Optional[RangeFloat] = Field(
        default=None,
        description="Number of bedrooms. Include only if the user specifies bedroom preferences."
    )
    bathrooms: Optional[RangeFloat] = Field(
        default=None,
        description="Number of bathrooms. Include only if the user specifies bathroom preferences."
    )
    squarefeet: Optional[RangeFloat] = Field(
        default=None,
        description="Square footage range. Include only if the user mentions area or size."
    )
    make: Optional[str] = Field(
        default=None,
        description="Builder or brand name. Only include if the user requests a specific builder."
    )
    year: Optional[int] = Field(
        default=None,
        description="Year the property was built. Include only if mentioned."
    )
    features: Optional[List[str]] = Field(
        default=None,
        description="List of amenities or features in the home (e.g., AC, garden). Include only if specified."
    )
    community: Optional[CommunityFilter] = Field(
        default=None,
        description="Community information (name, type, code). Include only if the user mentions it."
    )
    address: Optional[AddressModel] = Field(
        default=None,
        description="Exact city and state provided by the user. **Do not infer, guess, or add anything not explicitly mentioned.**"
    )
 
# Final wrapping structures
class Community(BaseModel):
    additionalData: CommunityModel = Field(
        ...,
        description="Contains the detailed fields related to the community. Only populate based on user-provided information."
    )
    entityType: str = Field(
        default="community",
        description="Should always be 'community'. Do not change."
    )
 
class HomeFilters(BaseModel):
    Fields: HomeModel = Field(
        ...,
        description="Contains filter fields related to homes. Only fill values based on specific details provided in the user query."
    )
 
class Home(BaseModel):
    additionalData: HomeFilters = Field(
        ...,
        description="Contains the structured filters for home-related queries. Only populate based on user-provided input."
    )
    entityType: str = Field(
        default="home",
        description="Should always be 'home'. Do not change."
    )