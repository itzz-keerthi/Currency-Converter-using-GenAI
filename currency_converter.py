import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
import json
import os
import streamlit_lottie
import pandas as pd
from datetime import datetime, timedelta

os.environ["SERPER_API_KEY"] = ""
os.environ["GOOGLE_API_KEY"] = ""

# Initialize the Gemini language model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)

# Initialize the Serper API wrapper for web searches
search = GoogleSerperAPIWrapper()

# Create a Langchain tool using the Serper API
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. The input to this should be a single search query.",
    )
]

# Initialize the LLM agent
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

# Set page configuration
st.set_page_config(
    page_title="Currency Converter & News",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS
dark_theme = """
<style>
    .main {
        background-color: #212529;
        color: #f8f9fa;
    }
    .stApp {
        background-color: #212529;
    }
    h1, h2, h3 {
        color: #0dcaf0;
    }
    .rate-display {
        background-color: #343a40;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 15px 0;
        text-align: center;
    }
    .rate-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #0dcaf0;
    }
    .country-info {
        border: 1px solid #495057;
        border-radius: 10px;
        padding: 15px;
        background-color: #343a40;
        margin-top: 10px;
    }
    .news-item {
        background-color: #343a40;
        border-left: 4px solid #0dcaf0;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .news-source {
        font-size: 0.85rem;
        color: #adb5bd;
        margin-top: 5px;
    }
    .news-title {
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
</style>
"""

# Dictionary of currency information including country code and lottie animation URLs
currency_info = {
    "USD": {
        "country": "United States",
        "flag_emoji": "🇺🇸",
        # "animation": "https://assets10.lottiefiles.com/private_files/lf30_bb9bkg1h.json",
        "icon": "$"
    },
    "INR": {
        "country": "India",
        "flag_emoji": "🇮🇳",
        # "animation": "https://assets3.lottiefiles.com/packages/lf20_rgtxujvt.json",
        "icon": "₹"
    },
    "EUR": {
        "country": "European Union",
        "flag_emoji": "🇪🇺",
        # "animation": "https://assets3.lottiefiles.com/packages/lf20_xRmNN8.json",
        "icon": "€"
    },
    "GBP": {
        "country": "United Kingdom",
        "flag_emoji": "🇬🇧",
        # "animation": "https://assets9.lottiefiles.com/packages/lf20_gnur27ia.json",
        "icon": "£"
    },
    "JPY": {
        "country": "Japan",
        "flag_emoji": "🇯🇵",
        # "animation": "https://assets2.lottiefiles.com/packages/lf20_xlkwtmrk.json",
        "icon": "¥"
    },
    "CAD": {
        "country": "Canada",
        "flag_emoji": "🇨🇦",
        # "animation": "https://assets10.lottiefiles.com/packages/lf20_abqjj2m3.json",
        "icon": "C$"
    },
    "AUD": {
        "country": "Australia",
        "flag_emoji": "🇦🇺",
        # "animation": "https://assets9.lottiefiles.com/packages/lf20_v7gj8hk1.json",
        "icon": "A$"
    },
    "CHF": {
        "country": "Switzerland",
        "flag_emoji": "🇨🇭",
        # "animation": "https://assets2.lottiefiles.com/packages/lf20_vxpjg3mt.json",
        "icon": "Fr"
    }
}

# Function to fetch currency conversion rate
def get_currency_conversion(currency_pair):
    """Fetches the latest currency conversion rate from frankfurter API."""
    base_currency, target_currency = currency_pair.split('-')
    url = f"https://api.frankfurter.dev/v1/latest?base={base_currency}&symbols={target_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["rates"][target_currency]
    except Exception as e:
        st.error(f"Error fetching currency data: {e}")
        return None

# Function to get historical currency data for the last 10 days
def get_historical_rates(base_currency, target_currency):
    """Fetches historical currency rates for the last 10 days from frankfurter API."""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    
    url = f"https://api.frankfurter.dev/v1/{start_date}..{end_date}?base={base_currency}&symbols={target_currency}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Convert to DataFrame for charting
        rates_data = []
        for date, rates in data["rates"].items():
            rates_data.append({
                'Date': date,
                'Rate': rates[target_currency]
            })
        
        return pd.DataFrame(rates_data)
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
        return None

# Function to get currency news using LLM agent
def get_currency_news_with_agent(base_currency, target_currency):
    """
    Uses LLM agent to find the latest news articles related to the currency pair.
    Returns processed news with sources.
    """
    try:
        # Create a specific prompt for the LLM agent
        prompt = f"""
        Find the latest news articles about the {base_currency} and {target_currency}  
        For each article, include:
        1. The title of the article
        2. A brief summary (1-2 sentences)
        3. The source publication name
        4. The URL link to the article if available (if not available, just indicate "Source: [Publication Name]")

        Format the results as a numbered list with 3-5 recent articles from reputable financial news sources.
        Include only articles that discuss the {base_currency} or {target_currency}.
        """
        
        # Run the agent with the prompt
        news_results = agent.run(prompt)
        return news_results
    except Exception as e:
        st.error(f"Error fetching news with agent: {e}")
        return None

def display_lottie_animation(currency_code, container):
    """Display lottie animation for the selected currency."""
    animation_url = currency_info.get(currency_code, {}).get("animation")
    if animation_url:
        try:
            with container:
                streamlit_lottie.st_lottie(
                    url=animation_url,
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="medium",
                    height=180,
                    key=f"lottie_{currency_code}"
                )
        except Exception as e:
            st.warning(f"Could not load animation for {currency_code}")

def main():
    # Apply the dark theme
    st.markdown(dark_theme, unsafe_allow_html=True)
    
    # App header
    st.title("Currency Converter and News")
    st.markdown("Get real-time exchange rates and the latest currency news")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This application uses:
        - Frankfurter API for real-time exchange rates
        - Historical data for the last 10 days
        - LLM agent for finding relevant currency news
        """)
    
    
    # Main content area using tabs
    tab1, tab2 = st.tabs(["Currency Converter", "Currency News"])
    
    with tab1:
        currencies = ["USD", "INR", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF"]
        
        # Currency selection with better layout
        col1, col2 = st.columns(2)
        
        with col1:
            base_currency = st.selectbox("Base Currency", currencies, index=0, key="base_currency")
            # Display country animation for base currency
            display_lottie_animation(base_currency, col1)
            # Show country info
            st.markdown(f"""
            <div class="country-info">
                <h3>{currency_info[base_currency]['flag_emoji']} {currency_info[base_currency]['country']}</h3>
                <p>Currency Symbol: {currency_info[base_currency]['icon']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            target_currency = st.selectbox("Target Currency", currencies, index=1, key="target_currency")
            # Display country animation for target currency
            display_lottie_animation(target_currency, col2)
            # Show country info
            st.markdown(f"""
            <div class="country-info">
                <h3>{currency_info[target_currency]['flag_emoji']} {currency_info[target_currency]['country']}</h3>
                <p>Currency Symbol: {currency_info[target_currency]['icon']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Amount input
        amount = st.number_input("Amount to Convert", min_value=0.01, value=1.0, step=0.01)
        
        if st.button("Get Conversion Rate"):
            if base_currency and target_currency and base_currency != target_currency:
                currency_pair = f"{base_currency}-{target_currency}"
                with st.spinner("Fetching latest exchange rates..."):
                    # Get the conversion rate
                    conversion_rate = get_currency_conversion(currency_pair)
                    
                    if conversion_rate:
                        converted_amount = amount * conversion_rate
                        
                        # Display results with styling
                        st.markdown(f"""
                        <div class="rate-display">
                            <div>
                                <span style="font-size: 1.2rem;">{amount} {base_currency} = </span>
                                <span class="rate-value">{converted_amount:.4f} {target_currency}</span>
                            </div>
                            <div style="margin-top: 10px; font-size: 1.1rem;">
                                Exchange Rate: 1 {base_currency} = {conversion_rate:.4f} {target_currency}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Get and display historical data
                        st.subheader("Historical Exchange Rates (Last 10 Days)")
                        with st.spinner("Fetching historical data..."):
                            historical_data = get_historical_rates(base_currency, target_currency)
                            
                            if historical_data is not None and not historical_data.empty:
                                # Convert to datetime for better x-axis display
                                historical_data['Date'] = pd.to_datetime(historical_data['Date'])
                                
                                # Sort by date
                                historical_data = historical_data.sort_values('Date')
                                
                                # Plot the chart
                                st.line_chart(historical_data.set_index('Date'))
                            else:
                                st.error("Could not fetch historical data.")
                    else:
                        st.error("Failed to fetch conversion rate. Please try again later.")
            elif base_currency == target_currency:
                st.warning("Please select two different currencies.")
    
    with tab2:
        st.header("Latest Currency News")
        
        # Currency selection for news
        col1, col2 = st.columns(2)
        with col1:
            news_base_currency = st.selectbox("Select Base Currency", currencies, index=0, key="news_base")
        with col2:
            news_target_currency = st.selectbox("Select Target Currency", currencies, index=1, key="news_target")
        
        if st.button("Get Latest News"):
            if news_base_currency != news_target_currency:
                with st.spinner("Searching for the latest currency news with AI agent..."):
                    # Use LLM agent to get news
                    news_results = get_currency_news_with_agent(news_base_currency, news_target_currency)
                    
                    if news_results:
                        # Display the news results
                        st.markdown("## Latest News Articles")
                        st.markdown(news_results)
                    else:
                        st.warning(f"No recent news found for {news_base_currency}-{news_target_currency}. Try a different currency pair.")
            else:
                st.warning("Please select two different currencies for news.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; opacity: 0.7;">
            <p>Currency Converter & News | Powered by Real-Time Data & AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
