import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import base64

# Function to scrape tweets
def scrape_twitter(keyword, start_date, end_date, tweet_limit):
    # Creating list to append tweet data to
    tweets_list = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{start_date} until:{end_date}').get_items()):
        if i >= tweet_limit:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

    return tweets_df

# Page title
st.title('Twitter Scraper')

# Keyword input
keyword = st.text_input('Enter a keyword or hashtag to search for:')

# Date range input
start_date = st.date_input('Start date:')
end_date = st.date_input('End date:')

# Tweet limit input
tweet_limit = st.number_input('Enter the maximum number of tweets to scrape:', value=50, min_value=1, max_value=500)

# Scrape tweets
if st.button('Scrape tweets'):
    if keyword:
        st.write('Scraping tweets...')
        tweets_df = scrape_twitter(keyword, start_date, end_date, tweet_limit)
        st.write(f'Scraped {len(tweets_df)} tweets:')
        st.write(tweets_df)
    else:
        st.write('Please enter a keyword to search for.')

# Download links
if 'tweets_df' in locals():
    csv = tweets_df.to_csv(index=False)
    b64_csv = base64.b64encode(csv.encode()).decode()
    json = tweets_df.to_json(indent=4)
    b64_json = base64.b64encode(json.encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{b64_csv}" download="{keyword}_tweets.csv">Download CSV</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="data:file/json;base64,{b64_json}" download="{keyword}_tweets.json">Download JSON</a>', unsafe_allow_html=True)


