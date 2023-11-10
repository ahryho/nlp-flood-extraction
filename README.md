# Content Extractor

This tool provides functionality for extracting and processing content from URLs using the OpenAI API, along with other utility functions for data manipulation.

## Getting Started

These instructions will help you set up and run the Content Extractor tool in a Conda environment on your local machine.

### Prerequisites

- Conda (Miniconda or Anaconda)
- Git

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/content-extractor.git
    ```

2. Navigate to the project directory:

    ```bash
    cd content-extractor
    ```

3. Create a Conda environment from the `environment.yml` file:

    ```bash
    conda env create -f environment.yml
    ```

4. Activate the Conda environment:

    ```bash
    conda activate nlp_flood_extract_env
    ```

### Usage

1. Open `nlp_flex.py` to see an example of how to use the `ContentExtractor` class.

2. Customize the OpenAI API key in `content_extractor.py`:

    ```python
    # Set OpenAI API key
    openai.api_key = "sk-..."
    ```

3. Run the `nlp_flex.py` script:

    ```bash
    python nlp_flex.py
    ```

## Running Tests

To run the unit tests for the Content Extractor functions, use the following command:

```bash
python test_content_extractor.py
