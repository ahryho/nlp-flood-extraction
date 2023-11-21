# NLP Flood Extraction Tool

This tool provides functionality for extracting and processing content from URLs using the OpenAI API. The tool is designed to handle URL content processing in different modes, including:

* **Extractor Mode**: Extracts content from URLs using [Newspaper3k](https://newspaper.readthedocs.io/en/latest/) python library.
* **OpenAI Mode**: Filters valid articles and extracts flood event information using [OpenAI's GPT models](https://platform.openai.com/account/limits).
* **All Mode**: Combines the features of both Extractor and OpenAI modes, extracting content and filtering valid articles before extracting flood event information using OpenAI.

## Getting Started

These instructions will help you set up and run the tool in a Conda environment on the local machine.

### Requirements

- [Python 3.12](https://www.python.org/downloads/) 

- Conda:
  - [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) or 
  - [Anaconda](https://www.anaconda.com/)

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/ahryho/nlp-flood-extraction-tool.git
    ```

2. Navigate to the project directory:

    ```bash
    cd nlp-flood-extraction-tool
    ```

3. Create a Conda environment from the `environment.yml` file:

    ```bash
    conda env create -f environment.yml
    ```

4. Activate the Conda environment:

    ```bash
    conda activate nlp_flood_extract_env
    ```

5. Configure your OpenAI API key by setting the openai.api_key variable in `content_extractor.py`.

    ```python
    # Set OpenAI API key
    openai.api_key = "sk-..."
    ```
   
## Usage

Run the tool by executing the `nlp_flex.py` script with the path to the configuration file:

```bash
python nlp_flex.py --config config/all.ini
```

## Configuration

The tool uses a configuration file to specify various parameters such as input file, output file, mode, etc. The configuration file is structured as follows:

```ini
[General]
input_filename = path/to/input.csv
output_filename = path/to/output.csv  ; Set to "None" for no output file
mode = all  ; Options: extractor, openai, all
num_processes = 4  ; Number of processes for parallel extraction
url_col_name = LinkURI  ; Name of the column with URLs
openai_model = gpt-3.5-turbo
openai_temp = 0.8 
openai_max_tokens = 150
```

## Output
The tool generates output files based on the specified mode:

* In **Extractor** mode, it saves the extracted content to the specified output file. If no output file was specified, it creates a csv file with a timestamp in the `output` folder: `output/extracted_url_content_YYYY-MM-DD_HHMMSS.csv`.
* In **OpenAI** mode, it filters valid articles and extracts flood event information using OpenAI, saving the results to the specified output file. If no output file was specified, it creates a csv file with a timestamp in the `output` folder: `output/openai_results_YYYY-MM-DD_HHMMSS.csv`.
* In **All** mode, it combines the features of both modes, saving the final results to the specified output file. If no output file was specified, it creates a csv file with a timestamp in the `output` folder: `output/openai_results_YYYY-MM-DD_HHMMSS.csv`. The extracted URL content is saved to a csv file with a timestamp in the `output` folder: `output/extracted_url_content_YYYY-MM-DD_HHMMSS.csv`.

## Logging
The tool logs information, warnings, and errors to the console and a log file with a timestamp in the `logs` folder. The log file contains details about the execution, including the timestamp and any encountered errors (*Not working properly -> logs from multiprocessing are not saved to the file*).

## Limitations

1. Rate limit of OpenAI: 3 RPM and 200 RPD (free version).
2. SSL verification: 
   - NRCan certificate added to the default certificates, `cacert.pem`,
   - OpenAI requests verification, explcite assignment `verify` to `False` doesn’t work => might be the problem in the future.

3. KeyboardInterrupt termination. Issue with the temination of the child processes.

4. Redirecting of warnings and errors of child processes to a log file.