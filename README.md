
# YouTube Comments Sentimental Analysis

A Python project that scrapes YouTube comments from any video and classifies them as Good (positive/neutral) or Bad (negative/offensive) using Google Gemini API (gemini-1.5-pro). As this is a basic project on python done for experience to see how API calling could work and got to try different approches while working on this project



## Features

* Scrapes comments from any public YouTube video.
* Classifies comments as **Good** or **Bad** using Gemini AI.
* Preview scraped comments in the app.
* Download classified comments as a CSV file.



## Tech Used

* **Python 3.10+**
* **Streamlit** – interactive web UI
* **Selenium** – scraping YouTube comments
* **Pandas** – data handling and CSV
* **Google Gemini API (gemini-1.5-pro)** – sentiment classification
* **Chrome & ChromeDriver** – browser automation



## How It Works

1. Enter a YouTube video URL in the app.
2. **Scrape Comments**: The app uses Selenium to scroll and collect comments.
3. **Classify Comments**: Each comment is sent to Google Gemini API to classify as Good or Bad.
4. Preview the classified comments and download them as CSV.

> Note: Make sure your Gemini API key is valid and ChromeDriver version matches your Chrome browser.



## How to Run

1. Clone the repository:

```bash
git clone https://github.com/saisindhu218/Basic-YouTube-Comments-Sentimental-Analysis.git
cd YTCommentsSentimentAnalysis
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Place **chromedriver.exe** in the project folder.
4. Replace **YOUR_GEMINI_KEY** in **geminicrawler.py** with your Gemini API key.
5. Run the app:

```bash
streamlit run geminicrawler.py
```

6. Enter the YouTube video URL → Click **Scrape Comments** → Click **Classify Comments** → Download results.



## Folder Structure

```
YTCommentsSentimentAnalysis/
│
├─ geminicrawler.py        # Main Streamlit app
├─ chromedriver.exe        # ChromeDriver for Selenium
├─ requirements.txt       # Python dependencies
├─ sample.csv              # Scraped comments (generated)
├─ labeled_comments.csv    # Classified comments (generated)
└─ README.md               # Project documentation
```



## 

Rachabattuni Sai Sindhu
