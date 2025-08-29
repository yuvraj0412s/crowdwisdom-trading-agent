# CrowdWisdomTrading AI Agent - Quick Setup Guide

## 📁 Project Structure

Your project directory should contain these files:

```
crowdwisdom-trading-agent/
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template  
├── config.py              # Configuration settings
├── llm_integration.py     # Mistral AI integration
├── tools.py               # Web scraping tools
├── agents.py              # CrewAI agents definitions
├── guardrails.py          # Validation functions
├── main_flow.py           # CrewAI Flow implementation
├── run.py                 # Main execution script
├── test_system.py         # System testing script
├── README.md              # Full documentation
├── output/                # Generated output folder
│   ├── unified_products.csv      # Final CSV output
│   └── crowdwisdom_trading.log   # Execution logs
└── .env                   # Your environment variables (create this)
```

## 🚀 Quick Installation & Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Mistral API key
# Replace 'your_mistral_api_key_here' with your actual API key
```

### Step 3: Get Your Mistral API Key

1. Go to [https://console.mistral.ai](https://console.mistral.ai)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file:

```env
MISTRAL_API_KEY=your_actual_api_key_here
```

### Step 4: Test System

```bash
python test_system.py
```

This will verify that:
- All modules can be imported
- Configuration is correct
- Mistral API connection works
- Agents can be created
- Guardrails are functional

### Step 5: Run the Full Pipeline

```bash
python run.py
```

## 🎯 What the System Does

1. **Data Collection**: Scrapes prediction market data from:
   - Polymarket.com
   - Kalshi.com  
   - Other prediction market sites

2. **Product Matching**: AI analyzes markets to find similar/identical predictions across sites

3. **CSV Generation**: Creates unified report with:
   - Market titles
   - Prices from different sites
   - Confidence scores
   - Price differences

## 📊 Expected Output

The system generates:
- `./output/unified_products.csv` - Main CSV report
- `./output/crowdwisdom_trading.log` - Detailed execution logs

Sample CSV content:
```csv
unified_title,category,polymarket_price,kalshi_price,other_site_price,price_difference,sites_available,confidence_level,volume_info,last_updated
"2024 Presidential Election Winner","Politics","$0.67","¢68","N/A","¢1","polymarket,kalshi","0.85","$2.3M","2024-01-15T10:30:00"
```

## ⚡ Quick Troubleshooting

### Issue: Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt
```

### Issue: Mistral API Key Not Found
```bash
# Make sure .env file exists and has your API key
cat .env
# Should show: MISTRAL_API_KEY=your_key_here
```

### Issue: Chrome Driver Problems
```bash
# Make sure Chrome browser is installed
# Driver is auto-managed via webdriver-manager
```

### Issue: Web Scraping Fails
- Check internet connection
- Some sites may block automated scraping
- System will continue with available data

## 🔍 Monitoring Execution

During execution, watch for:
- ✅ Green checkmarks = Success
- ⚠️ Yellow warnings = Non-critical issues  
- ❌ Red errors = Problems that need attention

Check `./output/crowdwisdom_trading.log` for detailed information.

## 💡 Key Features Implemented

✅ **CrewAI Flow with Guardrails**
- Sequential task execution with validation
- Error handling and recovery
- Structured workflow management

✅ **Three Specialized Agents**
- Data Collector: Web scraping specialist
- Product Matcher: AI market analysis
- Data Organizer: CSV report generator

✅ **Mistral AI Integration** 
- Via LiteLLM for standardized API access
- Configurable models and parameters
- Connection testing and error handling

✅ **Robust Web Scraping**
- Selenium WebDriver for dynamic content
- BeautifulSoup for HTML parsing
- Multiple fallback strategies

✅ **Comprehensive Validation**
- Input validation guardrails
- Output format verification
- Data quality assurance

✅ **Production-Ready Features**
- Detailed logging and monitoring
- Error recovery mechanisms
- Configurable parameters
- Clean CSV output format

## 📝 Assessment Requirements Met

- ✅ **Language**: Python
- ✅ **Framework**: CrewAI (latest version)
- ✅ **LLM Provider**: litellm + Mistral AI
- ✅ **3+ Websites**: Polymarket, Kalshi, prediction-market.com
- ✅ **3 Agents**: Data Collector, Product Matcher, Data Organizer
- ✅ **CrewAI Flow**: With guardrails implementation
- ✅ **CSV Output**: Unified product list with prices and confidence
- ✅ **Runnable Code**: Single command execution
- ✅ **Documentation**: Comprehensive setup guide

## 🎉 You're Ready!

Run `python run.py` to start the CrowdWisdomTrading AI Agent and generate your unified prediction market analysis!

---

**Built with CrewAI, Mistral AI, and modern web scraping techniques for intelligent prediction market data aggregation.**
