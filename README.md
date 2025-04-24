# Currency-Converter-using-GenAI

## Overview
This application provides real-time currency conversion rates and the latest news related to selected currency pairs. It combines financial data API integration with advanced language model capabilities to deliver both quantitative exchange rate information and qualitative market insights in one streamlined interface.

![Image](https://github.com/user-attachments/assets/f55700d6-59d4-49ce-824c-c4f025f6afcf)
![Image](https://github.com/user-attachments/assets/b561878b-9c19-4b7e-9d42-6ec6ee2e6c27)
![Image](https://github.com/user-attachments/assets/df283d16-e014-40e3-80ac-729d0b9017cb)
![Image](https://github.com/user-attachments/assets/f303158b-9cbf-47ec-b881-1fc7efe57c03)
![Image](https://github.com/user-attachments/assets/5805413e-7a69-4c36-9088-282d28cbb861)

## Features

### Currency Conversion
- Real-time exchange rates for multiple major currencies (USD, INR, EUR, GBP, JPY, CAD, AUD, CHF)
- Interactive conversion calculator
- Historical exchange rate data for the past 10 days with trend visualization
- Visual representation with country flags and animations

### Currency News
- AI-powered news aggregation for currency pairs
- Latest market insights and financial news
- News sourced from reputable financial publications
- Summarized article content with source attribution

## Technologies Used

### APIs and Services
- **Frankfurter API**: Provides real-time and historical exchange rate data
- **Google Serper API**: Used for web search capabilities
- **Google Gemini API**: Powers the language model for news processing

### Libraries and Frameworks
- **Streamlit**: Powers the web application interface and visualization
- **LangChain**: Orchestrates the AI-powered search and information retrieval
- **Pandas**: Handles data processing for historical rates
- **Streamlit Lottie**: Renders animated currency visualizations

## Technical Architecture

### Currency Data Flow
1. User selects base and target currencies
2. Application queries the Frankfurter API for exchange rates
3. Retrieved data is processed and displayed with appropriate formatting
4. Historical data is fetched and visualized as a time-series chart

### News Retrieval System
1. User selects currency pair for news
2. LangChain agent constructs a targeted search query
3. Google Serper API retrieves relevant web search results
4. Gemini language model processes and formats the search results
5. Structured news summaries are presented to the user

## Implementation Details

### User Interface
The application features a dark-themed, responsive interface with two main tabs:
- **Currency Converter**: For exchange rate calculations and historical data
- **Currency News**: For AI-powered currency news aggregation

Each currency is represented with:
- Country flag emoji
- Lottie animation
- Currency symbol
- Country information

### AI Integration
The application uses an LLM agent pattern combining:
- **Zero-shot agent framework**: The agent reasons through multi-step tasks
- **Web search tools**: For retrieving current information
- **Structured output formatting**: For consistent news presentation

### Error Handling
The application implements robust error handling for:
- API connection failures
- Data processing issues
- LLM agent response parsing
- Animation loading problems

## Setup and Installation

### Prerequisites
- Python 3.8+
- API keys for:
  - Google Serper API
  - Google AI (Gemini model)

### Environment Variables
Set up the following environment variables:
```
SERPER_API_KEY=your_serper_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Installation Steps
1. Clone the repository
2. Install dependencies:
   ```
   pip install streamlit langchain langchain-google-genai requests pandas streamlit-lottie
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## Usage Guide

### Currency Conversion
1. Select base and target currencies from the dropdown menus
2. Enter the amount to convert
3. Click "Get Conversion Rate"
4. View the conversion result and historical rate chart

### Currency News
1. Select base and target currencies for news
2. Click "Get Latest News"
3. Read through the AI-curated news summaries with source information

## Future Enhancements
- Additional currency options and cryptocurrency support
- Social media sentiment analysis for currencies
- Market prediction indicators based on historical patterns
- User accounts for saving favorite currency pairs
- Mobile application version
- Export functionality for historical data
- Alerts for significant rate changes

## Limitations
- News retrieval depends on search API availability and rate limits
- Historical data limited to 10 days
- Currency pairs limited to major currencies

## Contact
- [@itzz-keerthi](https://github.com/itzz-keerthi)
