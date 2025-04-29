from pydantic import BaseModel
from typing import List, Optional


class JobSearchCriteria(BaseModel):
    """
    defines the criteria to search for jobs across multiple sources.
    includes keywords, location, and experience level.
    """
    keywords: List[str]
    location: Optional[str] = None
    experience_level: Optional[str] = None
