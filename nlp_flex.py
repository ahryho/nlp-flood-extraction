# nlp_flex.py

from content_extractor import ContentExtractor

def nlp_flex():

    extractor = ContentExtractor()

    # Read data
    in_fn = 'data/collection_articles.csv'
    data_df = extractor.read_data(in_fn)

    # Extract content
    out_fn = "output/collection_articles_modified.csv"
    extracted_df = extractor.extract_content(data_df, num_processes=None, out_fn=out_fn)

    # Filter valid articles
    # filtered_df = extractor.filter_scraped_data(extracted_df)

if __name__ == "__main__":
    nlp_flex()
