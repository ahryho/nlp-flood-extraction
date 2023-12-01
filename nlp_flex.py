# nlp_flex.py

import configparser
import argparse
import logging

from content_extractor import ContentExtractor
from utils import configure_logging

def nlp_flex(config_file_path):
    """
    Perform URL ontent extraction based on the specified mode in the configuration file.

    Parameters:
        config_file_path (str): The path to the configuration file.

    Returns:
        None
    """
    # Configure logging and get the log file path
    log_file = configure_logging()
    
    # Read configuration from the file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Get configuration options
    input_filename = config.get('General', 'input_filename')
    output_filename = config.get('General', 'output_filename')
    output_filename = None if output_filename == "None" else output_filename
    mode = config.get('General', 'mode')
    num_processes = config.getint('General', 'num_processes')
    url_col_name = config.get('General', 'url_col_name')
    pub_date_col_name = config.get('General', 'pub_date_col_name')
    
    if mode in {'openai', 'all'}:
        openai_api_key = config.get('OpenAI', 'openai_api_key')
        openai_model = config.get('OpenAI', 'openai_model')
        openai_temp = config.getfloat('OpenAI', 'openai_temp')
        openai_max_tokens = config.getint('OpenAI', 'openai_max_tokens') 
        
        # Initialize ContentExtractor
        extractor = ContentExtractor(openai_api_key, openai_model, openai_temp, openai_max_tokens)
    
    elif mode == 'extractor': extractor = ContentExtractor()
    
    else:
        logging.error("The provided mode is not recognized.")
        exit(0)
    
    # Read data
    data_df = extractor.read_data(input_filename, url_col_name=url_col_name, pub_date_col_name=pub_date_col_name)
    
    if mode == 'extractor':
        # Mode: Extractor
        # Extract content using ContentExtractor
        extractor.extract_content(data_df, num_processes=num_processes, out_fn=output_filename)

    elif mode == 'openai':
        # Mode: OpenAI
        # Filter valid articles from the data
        filtered_df = extractor.filter_scraped_data(data_df)

        # Extract flood events using OpenAI
        extractor.extract_events_chatopenai(filtered_df,  num_processes=num_processes, out_fn=output_filename)

    elif mode == 'all':
        # Mode: All
        # Extract content, filter valid articles, and extract events
        extracted_df = extractor.extract_content(data_df, num_processes=num_processes)
        filtered_df = extractor.filter_scraped_data(extracted_df)

        # Extract flood events using OpenAI
        extractor.extract_events_chatopenai(filtered_df,  num_processes=num_processes, out_fn=output_filename)
    
    # Log the location of the log file
    logging.info(f"Log file created at: {log_file}")
         
if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="NLP FLood EXtraction Tool")
    parser.add_argument("--config", required=True, help="the path to the configuration file")
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    nlp_flex(args.config)