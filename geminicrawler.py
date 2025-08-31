import streamlit as st
import pandas as pd
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyA5NCVPIlElx7VJurIv0M0m1kl66jflgl0")  # replace with your valid Gemini API key

def scrape_youtube_comments(url, max_scrolls=5):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(executable_path="./chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    items = []
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Scroll to load comments
        for _ in range(max_scrolls):
            driver.execute_script("window.scrollBy(0, 3000);")
            time.sleep(2)

        # Wait until at least one comment is visible
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content-text")))
        except TimeoutException:
            st.warning("Could not load comments. YouTube may have blocked Selenium or comments not loaded.")
            return "sample.csv"

        # Updated selectors
        username_elems = driver.find_elements(By.CSS_SELECTOR, "#author-text span")
        comment_elems = driver.find_elements(By.CSS_SELECTOR, "#content-text")

        for username, comment in zip(username_elems, comment_elems):
            items.append({
                "Author": username.text.strip(),
                "Comment": comment.text.strip()
            })

        print("Scraped comments (first 5):", items[:5])

        filename = "sample.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Author", "Comment"])
            writer.writeheader()
            writer.writerows(items)

        print(f"✅ Extracted {len(items)} comments.")
    finally:
        driver.quit()
    
    return "sample.csv"

def classify_comment_with_gemini(comment):
    # Very strict prompt to force "Good" or "Bad" only
    prompt = f"""
You are a sentiment classification AI. Classify the following YouTube comment into only ONE of these categories: Good or Bad.
- "Good" = positive or neutral comment
- "Bad" = negative, abusive, offensive, or harsh comment

Comment:
\"\"\"{comment}\"\"\"

Return exactly one word: Good or Bad. No explanations, no quotes.
"""
    try:
        response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
        # Use candidates[0].content if available
        text = getattr(response, "text", None) or getattr(response, "candidates", [{}])[0].get("content", "")
        text = text.strip().lower()

        if text == "good":
            return "Good"
        elif text == "bad":
            return "Bad"
        else:
            # fallback if model returns something unexpected
            return "Unknown"
    except Exception as e:
        print(f"Error processing comment with Gemini: {e}")
        return "Unknown"

def process_comments():
    df = pd.read_csv("sample.csv")
    df["Sentiment"] = df["Comment"].apply(classify_comment_with_gemini)
    df.to_csv("labeled_comments.csv", index=False, encoding="utf-8")
    return df

def main():
    st.title("YouTube Comment Scraper and Sentiment Analysis")
    st.subheader("Scrape YouTube Comments and Classify Them as Good or Bad")
    
    youtube_url = st.text_input("Enter YouTube Video URL", "")

    if st.button("Scrape Comments"):
        if youtube_url.strip():
            st.text("Scraping YouTube comments...")
            filename = scrape_youtube_comments(youtube_url)
            st.success(f"Comments have been scraped and saved to {filename}")
            df_preview = pd.read_csv(filename)
            st.subheader("Scraped Comments Preview")
            st.write(df_preview.head())
        else:
            st.warning("Please enter a valid YouTube video URL.")

    if st.button("Classify Comments"):
        try:
            st.text("Classifying comments with Gemini...")
            df = process_comments()
            st.success("Classification completed!")
            st.subheader("Classified Comments")
            st.write(df)
            st.download_button(
                label="Download Classified Comments",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="labeled_comments.csv",
                mime="text/csv"
            )
        except FileNotFoundError:
            st.warning("No scraped comments found. Please scrape comments first.")

if __name__ == "__main__":
    main()
