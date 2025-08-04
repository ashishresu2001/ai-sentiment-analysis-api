from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Enums for better type safety
class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class CategoryType(str, Enum):
    PRODUCT_REVIEW = "product_review"
    SOFTWARE_UPDATE = "software_update"
    GENERAL = "general"
    BRAND_REVIEW = "brand_review"
    SERVICE_REVIEW = "service_review"
    CUSTOMER_SUPPORT = "customer_support"
    PRICING = "pricing"
    FEATURE_REVIEW = "feature_review"
    QUALITY_REVIEW = "quality_review"
    NEGATIVE_REVIEW = "negative_review"

# Pydantic models for API requests and responses
class StatementRequest(BaseModel):
    statements: List[str]

class BulkStatementRequest(BaseModel):
    statements: List[str]
    include_metadata: Optional[bool] = False

class SentimentResult(BaseModel):
    statement: str
    sentiment: SentimentType
    score: float
    confidence: float
    keywords_found: Optional[List[str]] = None

class InsightSummary(BaseModel):
    summary: str
    sentiment_distribution: Dict[str, int]
    average_score: float
    total_statements: int
    recommendations: Optional[List[str]] = None

class InfluencerStatement(BaseModel):
    id: int
    influencer: str
    statement: str
    category: str
    timestamp: str

class InfluencerData(BaseModel):
    influencer_statements: List[InfluencerStatement]

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: str

# Data classes for internal use
@dataclass
class AnalysisResult:
    sentiment: SentimentType
    score: float
    confidence: float
    keywords_found: List[str]

@dataclass
class ProcessingMetrics:
    total_processed: int
    positive_count: int
    negative_count: int
    neutral_count: int
    average_confidence: float
    processing_time: float

# Configuration model
class AnalyzerConfig(BaseModel):
    positive_keywords: List[str] = [
        "love", "amazing", "impressed", "quality", "great", "excellent", 
        "wonderful", "outstanding", "fantastic", "awesome", "perfect"
    ]
    negative_keywords: List[str] = [
        "disappointing", "not happy", "hope they improve", "bad", "terrible", 
        "awful", "worst", "hate", "horrible", "disappointing"
    ]
    neutral_keywords: List[str] = [
        "neutral", "mixed feelings", "okay", "average", "uncertain", "unsure"
    ]
    confidence_threshold: float = 0.7
    minimum_score: float = 0.1
    maximum_score: float = 0.9
