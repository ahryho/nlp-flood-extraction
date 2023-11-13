# content_extractor.py

import re
import os
import json
import pandas as pd
import requests
import newspaper
from newspaper import Article
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import multiprocessing
import openai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Timeout in seconds
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 120

# User agent for HTTP requests
USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Set OpenAI API key
openai.api_key = "sk-..."

# Override SSL verification settings
old_merge_environment_settings = requests.Session.merge_environment_settings
os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem' #'NRCAN-Root-2019-B64.cer'

class ContentExtractor:
    def __init__(self, openai_model="gpt-3.5-turbo", openai_temp=0.8, openai_max_tokens=100):
        self.openai_model = openai_model
        self.openai_temp = openai_temp
        self.openai_max_tokens = openai_max_tokens
        
        # Download stopwords and punkt if not already present
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        
        # Get the set of English stopwords
        self.stop_words = set(stopwords.words('english'))
        
    def read_data(self, fn, url_col_name="LinkURI"):
        """Reads data from a CSV file.

        Args:
            fn (str): File name.
            url_col_name (str, optional): Name of the column with URLs. Defaults to "LinkURI".

        Returns:
            pd.DataFrame: Dataframe with read data.
        """
        try:
            # Try reading the CSV file with UTF-8 encoding
            df = pd.read_csv(fn, sep='|', encoding='utf-8')
        except UnicodeDecodeError:
            # If UnicodeDecodeError occurs, try reading the file with cp1252 encoding (Windows encoding)
            df = pd.read_csv(fn, sep='|', encoding='cp1252')

        # Additional error handling for missing URL column
        if url_col_name not in df.columns:
            raise ValueError(f"Column '{url_col_name}' not found in the CSV file. Please check the column name or provide a valid column name.")

        # Rename the specified URL column to "URL"
        df.rename(columns={url_col_name: "URL"}, inplace=True)
        
        # Additional error handling for an empty dataframe
        if df.empty:
            raise ValueError("The CSV file is empty. Please provide a valid non-empty CSV file.")

        return df

    def clean_text(self, text):
        """Cleans text by removing HTML tags and special characters.

        Args:
            text (str): Input text.

        Returns:
            str: Cleaned text.
        """
        try:
            # Remove HTML tags from the text using regular expressions
            cleaned_text = re.sub(r'<[^>]+>', '', text)
            
            # Remove special characters, leaving only alphanumeric characters, commas, periods, and spaces
            cleaned_text = re.sub(r'[^a-zA-Z0-9.,\s]', '', cleaned_text)
            
            # Remove extra whitespaces by splitting and rejoining the text
            cleaned_text = ' '.join(cleaned_text.split())

            return cleaned_text
        except Exception as e:
            # Handle any unexpected errors and provide an error message
            raise ValueError(f"Error occurred while cleaning text: {str(e)}. Please check the input text and try again.")

    def remove_stopwords(self, text):
        """Removes stopwords from the text.

        Args:
            text (str): Input text.

        Returns:
            str: Text with stopwords removed.
        """
        try:
            # Tokenize the input text
            tokens = word_tokenize(text)

            # Remove stopwords from the list of tokens
            filtered_tokens = [word for word in tokens if word.lower() not in self.stop_words]

            # Join the filtered tokens to form the cleaned text
            filtered_text = " ".join(filtered_tokens)

            return filtered_text

        except Exception as e:
            # Handle any unexpected errors
            print(f"An error occurred while removing stopwords: {e}")
            return text  # Return the original text in case of an error

    def extract_url_content(self, url, language='en'):
        """Extracts content from a given URL.

        Args:
            url (str): URL to extract content from.
            language (str, optional): Language of the content. Defaults to 'en'.

        Returns:
            tuple: Summary, content, and validity flag (1 if valid body, 0 otherwise).
        """
        summary, content, is_valid = '', '', 0

        try:
            # Make a request to the URL with error handling for SSL, timeout, and connection errors
            response = self.make_request(url)
        except Exception as e:
            logging.error(f"An error occurred during the request: {str(e)}")
            return summary, content, is_valid

        try:
            # Use newspaper library to extract content from the HTML
            article = self.extract_article(url, response, language)

            # Process and clean the extracted content
            summary = self.clean_text(article.summary)
            content = self.clean_text(article.text)
            is_valid = 1 if article.is_valid_body() else 0
        except Exception as e:
            logging.error(f"An error occurred during content extraction: {str(e)}")

        return summary, content, is_valid

    def make_request(self, url):
        """Makes a request to the given URL with error handling.

        Args:
            url (str): URL to make a request to.

        Returns:
            requests.Response: Response object.
        """
        try:
            response = requests.post(url, verify=True, headers=USER_AGENT, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        except requests.exceptions.SSLError:
            response = requests.post(url, verify=False, headers=USER_AGENT, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        except requests.exceptions.ReadTimeout:
            logging.error(f"Access to {url} timed out")
            raise  # Re-raise the exception to be caught in the higher level
        except requests.exceptions.ConnectionError:
            logging.error(f"Access to {url} refused")
            raise  # Re-raise the exception to be caught in the higher level

        return response

    def extract_article(self, url, response, language):
        """Extracts article information using the newspaper library.

        Args:
            url (str): URL of the article.
            response (requests.Response): Response object from the request.
            language (str): Language of the article.

        Returns:
            newspaper.Article: Article object.
        """
        article = newspaper.Article(url='', language=language)
        article.download(input_html=response.content)
        article.parse()
        article.nlp()

        return article

    def extract_content(self, df, num_processes=None, out_fn=None):
        """Extracts content in parallel from URLs in the dataframe.

        Args:
            df (pd.DataFrame): Dataframe containing URLs.
            num_processes (int, optional): Number of processes for parallel extraction. Defaults to None.
            out_fn (str, optional): Output file name to save the results. Defaults to None.

        Returns:
            pd.DataFrame: Dataframe with extracted content.
        """
        try:
            if num_processes is None:
                num_processes = multiprocessing.cpu_count() - 1

            with multiprocessing.Pool(processes=num_processes) as pool:
                results = pool.starmap(self.extract_url_content, zip(df['URL'], df['Language']))

        except KeyboardInterrupt:
            logging.error('Got ^C while pool mapping, terminating the pool')
            pool.terminate()
            logging.error('Pool is terminated')
            logging.error('Joining pool processes')
            pool.join()
            logging.error('Join complete')

        df['Summary'], df['New_Content'], df['Is_Article'] = zip(*results)

        try:
            if out_fn is not None:
                logging.info("Saving results ...")
                df.to_csv(out_fn, index=False)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            logging.error("Data aren't saved but returned")
            pass

        return df

    def filter_scraped_data(self, df):
        """Filters the dataframe to include only valid articles.

        Args:
            df (pd.DataFrame): Dataframe with extracted content.

        Returns:
            pd.DataFrame: Filtered dataframe with valid articles.
        """
        try:
            # Check if 'Is_Article' column exists in the dataframe
            if 'Is_Article' not in df.columns:
                raise ValueError("Column 'Is_Article' not found in the dataframe. Please check the column name.")
            
            # Filter the dataframe to include only valid articles
            df_filtered = df[df["Is_Article"] == 1].reset_index(drop=True)
            
            return df_filtered

        except Exception as e:
            # Handle any unexpected errors and print a helpful message
            print(f"An error occurred during data filtering: {str(e)}")
            return pd.DataFrame()  # Return an empty DataFrame in case of an error

    def transform_openai_response_to_df(self, openai_content, openai_model="gpt-3.5-turbo"):
        """Transforms OpenAI response into a dataframe.

        Args:
            openai_content (str): OpenAI response content.
            openai_model (str, optional): OpenAI model name. Defaults to "gpt-3.5-turbo".

        Returns:
            pd.DataFrame: Dataframe with transformed OpenAI content.
        """
        try:
            if openai_model == "gpt-3.5-turbo":
                openai_content = re.sub(r'\n  ', '', openai_content)
            else:
                pattern = re.compile(r'Answers(\d+): (.+)')
                matches = pattern.findall(openai_content)
                data_dict = {f'Answers{index}': value for index, value in matches}
                openai_content = json.dumps(data_dict, indent=4)
                openai_content = re.sub("Answers", "Question", openai_content)
            
            openai_content_dict = json.loads(openai_content)
            openai_content_df = pd.DataFrame([openai_content_dict])
            
            column_mapping = {
                "Question1": "is_happened",
                "Question2": "event_name_en",
                "Question3": "date",
                "Question4": "location",
                "Question5": "death",
                "Question6": "evacuation"
            }
            
            openai_content_df.rename(columns=column_mapping, inplace=True)
            return openai_content_df

        except Exception as e:
            # Handle any unexpected errors and print a helpful message
            logger.error(f"An error occurred during transformation: {str(e)}")
            return pd.DataFrame()  # Return an empty DataFrame in case of an error

    def extract_single_event_chatopenai(self, url_content, url, openai_model="gpt-3.5-turbo", openai_temp=0.8, openai_max_tokens=100):
        """Extracts information for a single event using OpenAI API.

        Args:
            url_content (str): Content of the URL.
            url (str): URL of the event.
            openai_model (str, optional): OpenAI model name. Defaults to "gpt-3.5-turbo".
            openai_temp (float, optional): Temperature for OpenAI response. Defaults to 0.8.
            openai_max_tokens (int, optional): Maximum tokens for OpenAI response. Defaults to 100.

        Returns:
            pd.DataFrame: Dataframe with extracted information.
        """
        try:
            logger.info(f"Extracting information from {url}")

            system_msg = 'You are a helpful assistant. Your responses consist of valid JSON syntax, with no other comments, explanations, reasoning, or dialogue not consisting of valid JSON.'
            quest1 = "1. Did a flood event happen? (Yes or No only)"
            quest2 = "2. If a flood event happened, what is its name? (Name only or Unknown)"
            quest3 = "3. If a flood event happened, when did it happen? (YYYY-MM only or Unknown)"
            quest4 = "4. If a flood event happened, where did it happen? (Name of the place, city, state, country)"
            quest5 = "5. If a flood event happened, how many people died? (Number only or Unknown)"
            quest6 = "6. If a flood event happened, how many people were evacuated? (Number only or Unknown)"
            
            user_msg = f"Questions answering: \nContext: {url_content}\n" \
                    f"{quest1}\n {quest2}\n {quest3}\n {quest4}\n {quest5}\n {quest6}"

            if openai_model == "gpt-3.5-turbo":
                response = openai.ChatCompletion.create(
                    model=openai_model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    max_tokens=openai_max_tokens,
                    temperature=openai_temp
                )
                openai_content = response["choices"][0]["message"]["content"]
            else:
                prompt = system_msg + '\n' + user_msg
                response = openai.Completion.create(
                    model=openai_model,
                    prompt=prompt,
                    max_tokens=openai_max_tokens,
                    temperature=openai_temp
                )
                openai_content = response['choices'][0]['text']

            logger.info(f"Transforming information from {url}")
            content_df = self.transform_openai_response_to_df(openai_content, openai_model=openai_model)
            content_df["link"] = url

            return content_df

        except Exception as e:
            # Handle any unexpected errors
            logger.error(f"An error occurred during extraction: {str(e)}")
            return pd.DataFrame()  # Return an empty DataFrame in case of an error

    def extract_events_chatopenai(self, df, num_processes=None, openai_model="gpt-3.5-turbo", openai_temp=0.8, openai_max_tokens=100, out_fn=None):
        """Extracts information for multiple events using OpenAI API.

        Args:
            df (pd.DataFrame): Dataframe with content and URLs.
            num_processes (int, optional): Number of processes for parallel extraction. Defaults to None.
            openai_model (str, optional): OpenAI model name. Defaults to "gpt-3.5-turbo".
            openai_temp (float, optional): Temperature for OpenAI response. Defaults to 0.8.
            openai_max_tokens (int, optional): Maximum tokens for OpenAI response. Defaults to 100.
            out_fn (str, optional): Output file name to save the results. Defaults to None.

        Returns:
            pd.DataFrame: Dataframe with extracted information for multiple events.
        """
        try:
            # Set the default number of processes if not provided
            if num_processes is None:
                num_processes = multiprocessing.cpu_count() - 1

            # Prepare arguments for parallel processing
            model_args = [openai_model] * df.shape[0]
            temp_args = [openai_temp] * df.shape[0]
            tokens_args = [openai_max_tokens] * df.shape[0]

            # Use multiprocessing for parallel extraction
            with multiprocessing.Pool(processes=num_processes) as pool:
                results = pool.starmap(
                    self.extract_single_event_chatopenai,
                    zip(df['New_Content'], df['URL'], model_args, temp_args, tokens_args)
                )

            # Combine results into a single DataFrame
            results_df = pd.concat(results, axis=0)

        except KeyboardInterrupt:
            # Handle KeyboardInterrupt to terminate the pool gracefully
            logger.error('Got ^C while pool mapping, terminating the pool')
            pool.terminate()
            logger.error('Pool is terminated')
            logger.error('Joining pool processes')
            pool.join()
            logger.error('Join complete')

        try:
            # Save results to a CSV file if an output filename is provided
            if out_fn is not None:
                logger.info("Saving results ...")
                results_df.to_csv(out_fn, index=False)

        except Exception as e:
            # Handle exceptions during the saving process
            logger.error(f"An error occurred while saving results: {str(e)}")
            logger.info("Data aren't saved but returned.")

        # Return the DataFrame with extracted information
        return results_df