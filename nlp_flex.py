# nlp_flex.py

from content_extractor import ContentExtractor

def nlp_flex():

    extractor = ContentExtractor()

    # Read data
    data_df = extractor.read_data("your_data.csv")

    # Extract content
    extracted_df = extractor.extract_content(data_df, num_processes=None, out_fn="output.csv")

    # Filter valid articles
    # filtered_df = extractor.filter_scraped_data(extracted_df)

if __name__ == "__main__":
    nlp_flex()
