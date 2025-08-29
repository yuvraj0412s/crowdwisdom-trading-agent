<div align="center">
  <h1>🎲 CrowdWisdomTrading AI Agent 🚀</h1>
  <h3>Unified, Intelligent Prediction Market Data Aggregator<br>Powered by CrewAI + Mistral + Selenium</h3>
</div>

---

### **Badges**

<p align="center">
  <img src="https://img.shields.io/github/repo-size/yuvraj0412s/CrowdWisdomTrading-AI-Agent?style=for-the-badge" alt="Repo Size">
  <img src="https://img.shields.io/github/license/yuvraj0412s/CrowdWisdomTrading-AI-Agent?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CrewAI-2025-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB..." alt="CrewAI">
  <a href="https://mistral.ai/"><img src="https://img.shields.io/badge/Mistral-FF7E00?style=for-the-badge&logo=mistralai&logoColor=white" alt="Mistral API"></a>
  <img src="https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium WebDriver">
  <a href="https://github.com/yuvraj0412s/CrowdWisdomTrading-AI-Agent/stargazers"><img src="https://img.shields.io/github/stars/yuvraj0412s/CrowdWisdomTrading-AI-Agent?style=for-the-badge&color=ffd700" alt="Repo Stars"></a>
</p>

---

### **About The Project** 💡

*Modern trading and forecasting deserves more than scattered, siloed data.*  
**CrowdWisdomTrading AI Agent** is a cutting-edge backend system that unifies prediction market insights from top platforms (Polymarket, Kalshi, and more) into actionable, business-ready intelligence.  
It’s more than a scraper—it’s an orchestrated, multi-agent *AI pipeline* that collects, analyzes, matches, and delivers unified market opportunities right to you.

---

### **Features** ✨

- **♻️ Multi-Site Scraping:** Aggregates prediction data from Polymarket, Kalshi, and other major platforms.
- **🤖 Multi-Agent Intelligence:** CrewAI agents divide tasks: data gathering, product matching, and CSV organization.
- **💡 Product Unification:** Detects identical markets across sites—even if the naming and odds differ.
- **📈 Unified CSV Output:** Exports a comparative board with prices, volumes, product confidence, and more.
- **🕵️ Robust Guardrails:** Built-in data validation for reliability and accuracy at each workflow stage.
- **🛡️ Error Recovery:** Handles inaccessible sites and unexpected formats gracefully.
- **🔎 Powerful Logging:** Every step traceable for audits and debugging.

---

### **Tech Stack** 🛠️

| **Category**      | **Technology**                                         |
|-------------------|-------------------------------------------------------|
| **Framework**     | [CrewAI](https://github.com/crewAIInc/crewAI), [Pydantic](https://docs.pydantic.dev/) |
| **AI & APIs**     | [Mistral AI](https://mistral.ai/), [LiteLLM](https://litellm.ai/)      |
| **Scraping**      | [Selenium](https://www.selenium.dev/), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), Requests |
| **Data Science**  | [Pandas](https://pandas.pydata.org/), Numpy           |
| **Config**        | [python-dotenv](https://github.com/theskumar/python-dotenv) |
| **Logging**       | [Loguru](https://github.com/Delgan/loguru)            |

---

### **Installation & Usage** 🚀

**Prerequisites**
- Python 3.9+
- Google Chrome browser (for Selenium)
- Mistral API Token

**Local Setup**

1. **Clone the repository:**
    ```
    git clone https://github.com/yuvraj0412s/CrowdWisdomTrading-AI-Agent.git
    cd CrowdWisdomTrading-AI-Agent
    ```
2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
3. **Set up your environment variables:**
    - Copy the example env file and add your API key.
    ```
    cp .env.example .env
    ```
    Edit `.env` to include:
    ```
    MISTRAL_API_KEY="your_mistral_api_key_here"
    ```

4. **Run system test (recommended):**
    ```
    python test_system.py
    ```

5. **Run the main pipeline:**
    ```
    python run.py
    ```

---

### **Contributing** 🤝

Want to help make trading intelligence smarter for everyone?  
Any contributions—bug fixes, feature suggestions, or optimizations—are **warmly welcome**!

1. **Fork** the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'add AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. **Open a pull request**!

Have a bug, question, or suggestion? Open an **issue** or reach out.

---

### **Roadmap** 🗺️

- [ ] Add more sites and dynamic onboarding of providers.
- [ ] Realtime data refresh and dashboard visualization.
- [ ] Advanced product matching using embeddings.
- [ ] Alerts for market anomalies or arbitrage.
- [ ] Export to JSON/Excel and cloud storage options.

---

### **License** 📄

This project is open-sourced under the **MIT License**.  
See the [LICENSE](LICENSE) file for more information.

---

### **Contact & Links** 🔗

**Yuvraj Singh** – Algorithmic Software Developer  
Let's connect!

<div align="center">
  <a href="https://www.yuvraj.bio"><img src="https://img.shields.io/badge/Live_Demo-yuvraj.bio-2ea44f?style=for-the-badge&logo=vercel"></a>
  &nbsp;
  <a href="https://www.linkedin.com/in/yuvraj-singh-77601827a/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"></a>
</div>

---

### **Tags**
`#CrewAI` `#PredictionMarkets` `#MistralAI` `#Selenium` `#WebScraping` `#AIProductMatching` `#TradingIntelligence` `#AlgorithmicTrading` `#PythonBackend` `#Automation`
