from fastapi import FastAPI, HTTPException
from typing import List
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
import random
import time
import os

# Import models from models.py
from models import (
    StatementRequest, BulkStatementRequest, SentimentResult, InsightSummary,
    InfluencerStatement, InfluencerData, HealthResponse, ErrorResponse,
    AnalysisResult, ProcessingMetrics, AnalyzerConfig, SentimentType
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Abstract base classes
class SentimentAnalyzer(ABC):
    """Abstract base class for sentiment analyzers."""
    
    @abstractmethod
    def analyze(self, statement: str) -> AnalysisResult:
        """Analyze sentiment of a single statement."""
        pass
    
    @abstractmethod
    def analyze_batch(self, statements: List[str]) -> List[AnalysisResult]:
        """Analyze sentiment of multiple statements."""
        pass

class InsightGenerator(ABC):
    """Abstract base class for insight generators."""
    
    @abstractmethod
    def generate(self, sentiments: List[SentimentResult]) -> InsightSummary:
        """Generate insights from sentiment results."""
        pass

class DataRepository(ABC):
    """Abstract base class for data repositories."""
    
    @abstractmethod
    def load_statements(self) -> List[str]:
        """Load influencer statements."""
        pass

# Concrete implementations
class KeywordBasedSentimentAnalyzer(SentimentAnalyzer):
    """Keyword-based sentiment analyzer using configurable keywords."""
    
    def __init__(self, config: AnalyzerConfig = None):
        self.config = config or AnalyzerConfig()
        logger.info("KeywordBasedSentimentAnalyzer initialized with %d positive and %d negative keywords", 
                   len(self.config.positive_keywords), len(self.config.negative_keywords))

    def analyze(self, statement: str) -> AnalysisResult:
        """Analyze sentiment of a single statement."""
        statement_lower = statement.lower()
        
        # Count keyword matches
        positive_matches = [word for word in self.config.positive_keywords if word in statement_lower]
        negative_matches = [word for word in self.config.negative_keywords if word in statement_lower]
        neutral_matches = [word for word in self.config.neutral_keywords if word in statement_lower]
        
        positive_count = len(positive_matches)
        negative_count = len(negative_matches)
        neutral_count = len(neutral_matches)
        
        # Determine sentiment
        if positive_count > negative_count and positive_count > neutral_count:
            sentiment = SentimentType.POSITIVE
            score = min(self.config.maximum_score, 0.6 + (positive_count * 0.1))
            confidence = min(0.95, 0.5 + (positive_count * 0.15))
            keywords_found = positive_matches
        elif negative_count > positive_count and negative_count > neutral_count:
            sentiment = SentimentType.NEGATIVE
            score = max(self.config.minimum_score, 0.4 - (negative_count * 0.1))
            confidence = min(0.95, 0.5 + (negative_count * 0.15))
            keywords_found = negative_matches
        else:
            sentiment = SentimentType.NEUTRAL
            score = random.uniform(0.4, 0.6)
            confidence = 0.5 + (neutral_count * 0.1)
            keywords_found = neutral_matches or []
        
        return AnalysisResult(
            sentiment=sentiment, 
            score=score, 
            confidence=confidence,
            keywords_found=keywords_found
        )

    def analyze_batch(self, statements: List[str]) -> List[AnalysisResult]:
        """Analyze sentiment of multiple statements."""
        return [self.analyze(stmt) for stmt in statements]

class AdvancedInsightGenerator(InsightGenerator):
    """Advanced insight generator with detailed analysis and recommendations."""
    
    def __init__(self):
        logger.info("AdvancedInsightGenerator initialized")

    def generate(self, sentiments: List[SentimentResult]) -> InsightSummary:
        """Generate comprehensive insights from sentiment results."""
        if not sentiments:
            return InsightSummary(
                summary="No statements to analyze.",
                sentiment_distribution={},
                average_score=0.0,
                total_statements=0,
                recommendations=[]
            )

        # Calculate distribution and metrics
        distribution = {sentiment_type.value: 0 for sentiment_type in SentimentType}
        total_score = 0
        high_confidence_count = 0
        
        for result in sentiments:
            distribution[result.sentiment.value] += 1
            total_score += result.score
            if result.confidence > 0.7:
                high_confidence_count += 1
        
        average_score = total_score / len(sentiments)
        total = len(sentiments)
        confidence_ratio = high_confidence_count / total
        
        # Generate detailed summary
        pos = distribution[SentimentType.POSITIVE.value]
        neg = distribution[SentimentType.NEGATIVE.value]
        neu = distribution[SentimentType.NEUTRAL.value]
        
        if pos > neg and pos > neu:
            summary = f"Overwhelmingly positive sentiment detected ({pos}/{total}, {pos/total:.1%}). Influencers are expressing high satisfaction and enthusiasm."
        elif neg > pos and neg > neu:
            summary = f"Concerning negative sentiment trend ({neg}/{total}, {neg/total:.1%}). Significant issues require immediate attention."
        elif neu > pos and neu > neg:
            summary = f"Neutral sentiment dominates ({neu}/{total}, {neu/total:.1%}). Influencers are taking a wait-and-see approach."
        else:
            summary = f"Mixed sentiments observed. Opinions are evenly divided among influencers with no clear majority."
        
        # Add confidence information
        summary += f" Analysis confidence: {confidence_ratio:.1%} of statements analyzed with high confidence."
        
        # Generate recommendations
        recommendations = self._generate_recommendations(pos, neg, neu, total, average_score, confidence_ratio)
        
        return InsightSummary(
            summary=summary,
            sentiment_distribution=distribution,
            average_score=round(average_score, 3),
            total_statements=total,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, pos: int, neg: int, neu: int, total: int, avg_score: float, confidence: float) -> List[str]:
        """Generate actionable recommendations based on sentiment analysis."""
        recommendations = []
        
        if neg > pos:
            recommendations.append("Address negative feedback urgently to prevent reputation damage")
            recommendations.append("Implement customer satisfaction improvement initiatives")
        
        if pos > total * 0.6:
            recommendations.append("Leverage positive sentiment for marketing campaigns")
            recommendations.append("Identify and amplify positive influencer voices")
        
        if neu > total * 0.4:
            recommendations.append("Engage neutral influencers with targeted content")
            recommendations.append("Provide more compelling value propositions")
        
        if avg_score < 0.4:
            recommendations.append("Critical: Overall sentiment is very low - immediate action required")
        elif avg_score > 0.7:
            recommendations.append("Excellent: Maintain current strategies and expand successful initiatives")
        
        if confidence < 0.5:
            recommendations.append("Consider gathering more data for better analysis confidence")
        
        return recommendations

class JsonDataRepository(DataRepository):
    """JSON file-based data repository for influencer statements."""
    
    def __init__(self, data_path: str = "data/dummy_statements.json"):
        self.data_path = data_path
        logger.info(f"JsonDataRepository initialized with path: {data_path}")

    def load_statements(self) -> List[str]:
        """Load influencer statements from JSON file."""
        try:
            if not os.path.exists(self.data_path):
                logger.warning(f"Data file not found: {self.data_path}")
                return self._get_fallback_statements()
            
            with open(self.data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                statements = [item['statement'] for item in data.get('influencer_statements', [])]
                logger.info(f"Loaded {len(statements)} statements from {self.data_path}")
                return statements
        except Exception as e:
            logger.error(f"Error loading data from {self.data_path}: {e}")
            return self._get_fallback_statements()
    
    def load_full_data(self) -> InfluencerData:
        """Load complete influencer data with metadata."""
        try:
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            
            with open(self.data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return InfluencerData(**data)
        except Exception as e:
            logger.error(f"Error loading full data: {e}")
            raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")
    
    def _get_fallback_statements(self) -> List[str]:
        """Return fallback statements if JSON file is not available."""
        return [
            "I love the new product launch! It's amazing and everyone should try it.",
            "The recent update was disappointing and didn't meet expectations.",
            "I'm neutral about the changes, let's see how it goes.",
            "This brand always delivers quality, I'm impressed again.",
            "Not happy with the service lately, hope they improve soon."
        ]

# Main service class
class SentimentAnalysisService:
    """Main service orchestrating sentiment analysis and insight generation."""
    
    def __init__(self):
        self.config = AnalyzerConfig()
        self.analyzer = KeywordBasedSentimentAnalyzer(self.config)
        self.insight_generator = AdvancedInsightGenerator()
        self.data_repository = JsonDataRepository()
        logger.info("SentimentAnalysisService initialized successfully")

    def analyze_statements(self, statements: List[str]) -> List[SentimentResult]:
        """Analyze sentiment of multiple statements."""
        start_time = time.time()
        results = []
        
        try:
            for stmt in statements:
                analysis = self.analyzer.analyze(stmt)
                result = SentimentResult(
                    statement=stmt,
                    sentiment=analysis.sentiment,
                    score=analysis.score,
                    confidence=analysis.confidence,
                    keywords_found=analysis.keywords_found
                )
                results.append(result)
            
            processing_time = time.time() - start_time
            logger.info(f"Analyzed {len(statements)} statements in {processing_time:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing statements: {e}")
            raise HTTPException(status_code=500, detail=f"Error analyzing statements: {str(e)}")

    def generate_insights(self, statements: List[str]) -> InsightSummary:
        """Generate insights from statements."""
        try:
            sentiments = self.analyze_statements(statements)
            insights = self.insight_generator.generate(sentiments)
            logger.info("Generated insights successfully")
            return insights
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

    def get_dummy_data(self) -> List[str]:
        """Get dummy statements for testing."""
        return self.data_repository.load_statements()
    
    def get_full_data(self) -> InfluencerData:
        """Get complete influencer data with metadata."""
        return self.data_repository.load_full_data()

# Initialize FastAPI app
app = FastAPI(
    title="AI Sentiment Analysis & Insight Generation",
    description="FastAPI application for analyzing influencer sentiment and generating actionable insights ",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize service
sentiment_service = SentimentAnalysisService()

# API Endpoints
@app.post("/sentiment", response_model=List[SentimentResult])
async def sentiment_analysis(request: StatementRequest):
    """Analyze sentiment of influencer statements with detailed metrics."""
    if not request.statements:
        raise HTTPException(status_code=400, detail="No statements provided")
    
    return sentiment_service.analyze_statements(request.statements)

@app.post("/insight", response_model=InsightSummary)
async def insight_summary(request: StatementRequest):
    """Generate comprehensive insight summary with actionable recommendations."""
    if not request.statements:
        raise HTTPException(status_code=400, detail="No statements provided")
    
    return sentiment_service.generate_insights(request.statements)

@app.post("/bulk-analysis", response_model=InsightSummary)
async def bulk_analysis(request: BulkStatementRequest):
    """Perform bulk sentiment analysis with optional metadata inclusion."""
    if not request.statements:
        raise HTTPException(status_code=400, detail="No statements provided")
    
    insights = sentiment_service.generate_insights(request.statements)
    
    if request.include_metadata:
        # Add processing metadata
        sentiments = sentiment_service.analyze_statements(request.statements)
        high_conf_count = sum(1 for s in sentiments if s.confidence > 0.7)
        insights.recommendations.append(f"Processing metadata: {high_conf_count}/{len(sentiments)} high-confidence results")
    
    return insights

@app.get("/dummy-statements", response_model=List[str])
async def get_dummy_statements():
    """Get example influencer statements for testing."""
    return sentiment_service.get_dummy_data()

@app.get("/influencer-data", response_model=InfluencerData)
async def get_influencer_data():
    """Get complete influencer data with metadata."""
    return sentiment_service.get_full_data()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="sentiment-analysis-api",
        timestamp=datetime.now().isoformat()
    )

@app.get("/config")
async def get_config():
    """Get current analyzer configuration."""
    return {
        "positive_keywords": sentiment_service.config.positive_keywords,
        "negative_keywords": sentiment_service.config.negative_keywords,
        "neutral_keywords": sentiment_service.config.neutral_keywords,
        "confidence_threshold": sentiment_service.config.confidence_threshold
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
