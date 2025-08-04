# AI Sentiment Analysis & Insight Generation

A modern FastAPI application that uses AI components for sentiment analysis of influencer statements and generates actionable insights using Object-Oriented Programming principles.

## Project Structure

```
sentiment-analysis-app/
├── main.py                 # Main FastAPI application with OOP design
├── models.py              # Pydantic models and data classes
├── requirements.txt       # Python dependencies
└── data/
    └── dummy_statements.json  # Sample influencer data with metadata
```

## Features

- **Object-Oriented Design**: Uses abstract base classes, inheritance, and polymorphism
- **Advanced Sentiment Analysis**: Keyword-based analyzer with configurable parameters
- **Comprehensive Insights**: Detailed sentiment distribution and actionable recommendations
- **Rich Data Models**: Structured data with metadata and type safety
- **Multiple Endpoints**: Various API endpoints for different use cases
- **Error Handling**: Robust error handling with proper HTTP status codes
- **Logging**: Comprehensive logging for monitoring and debugging

## Installation

1. Navigate to the project directory:
   ```bash
   cd task-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### 1. Sentiment Analysis
**POST /sentiment**
```bash
curl -X POST http://localhost:8000/sentiment \
  -H "Content-Type: application/json" \
  -d '{"statements": ["I love this product!", "This is terrible."]}'
```

### 2. Insight Generation
**POST /insight**
```bash
curl -X POST http://localhost:8000/insight \
  -H "Content-Type: application/json" \
  -d '{"statements": ["I love this product!", "This is terrible.", "It is okay."]}'
```

### 3. Bulk Analysis
**POST /bulk-analysis**
```bash
curl -X POST http://localhost:8000/bulk-analysis \
  -H "Content-Type: application/json" \
  -d '{"statements": ["Great product!", "Not impressed."], "include_metadata": true}'
```

### 4. Get Sample Data
**GET /dummy-statements**
```bash
curl http://localhost:8000/dummy-statements
```

### 5. Get Full Influencer Data
**GET /influencer-data**
```bash
curl http://localhost:8000/influencer-data
```

### 6. Configuration
**GET /config**
```bash
curl http://localhost:8000/config
```

## Object-Oriented Design

### Abstract Base Classes
- `SentimentAnalyzer`: Abstract class for sentiment analysis implementations
- `InsightGenerator`: Abstract class for insight generation implementations  
- `DataRepository`: Abstract class for data access implementations

### Concrete Implementations
- `KeywordBasedSentimentAnalyzer`: Keyword-based sentiment analysis
- `AdvancedInsightGenerator`: Comprehensive insight generation with recommendations
- `JsonDataRepository`: JSON file-based data repository

### Main Service Class
- `SentimentAnalysisService`: Orchestrates all components using dependency injection

## Data Models

The application uses Pydantic models for type safety and validation:
- `StatementRequest`: API request model
- `SentimentResult`: Sentiment analysis result
- `InsightSummary`: Comprehensive insights with recommendations
- `InfluencerStatement`: Individual influencer statement with metadata

## Sample Response

### Sentiment Analysis Response
```json
[
  {
    "statement": "I love this product!",
    "sentiment": "positive",
    "score": 0.85,
    "confidence": 0.8,
    "keywords_found": ["love"]
  }
]
```

### Insight Summary Response
```json
{
  "summary": "Overwhelmingly positive sentiment detected (2/3, 66.7%). Influencers are expressing high satisfaction and enthusiasm. Analysis confidence: 100.0% of statements analyzed with high confidence.",
  "sentiment_distribution": {
    "positive": 2,
    "negative": 1,
    "neutral": 0
  },
  "average_score": 0.673,
  "total_statements": 3,
  "recommendations": [
    "Leverage positive sentiment for marketing campaigns",
    "Identify and amplify positive influencer voices",
    "Excellent: Maintain current strategies and expand successful initiatives"
  ]
}
```

## Customization

The sentiment analyzer can be customized by modifying the `AnalyzerConfig` class in `models.py`:
- Add new keywords for different sentiment categories
- Adjust confidence thresholds
- Modify scoring algorithms

## Error Handling

The application includes comprehensive error handling:
- Input validation using Pydantic models
- Proper HTTP status codes
- Detailed error messages
- Logging for debugging

## Testing

Test the API using the interactive documentation at `/docs` or use curl commands as shown above.

## Next Steps for Production

1. **Real AI Integration**: Replace keyword-based analysis with ML models (BERT, RoBERTa)
2. **Database Integration**: Add PostgreSQL or MongoDB for persistent storage
3. **Authentication**: Implement JWT-based authentication
4. **Rate Limiting**: Add rate limiting for API endpoints
5. **Caching**: Implement Redis caching for frequently accessed data
6. **Monitoring**: Add Prometheus metrics and Grafana dashboards
7. **Testing**: Add comprehensive unit and integration tests

---

Ready for deployment and review! 🚀
