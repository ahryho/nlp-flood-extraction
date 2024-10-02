# NLP Flood Extraction Tool

This tool provides functionality for extracting and processing content from URLs using the OpenAI and AWS Bedrock APIs. The tool is designed to handle URL content processing in different modes, including:

* **Extractor Mode**: Extracts content from URLs using [Newspaper3k](https://newspaper.readthedocs.io/en/latest/) python library.
* **NLP Mode**: Filters valid articles and extracts flood event information using [OpenAI's GPT models](https://platform.openai.com/account/limits) and the following model available on the AWS Bedrock for NRCan:
        
        - amazon.titan-text-express-v1
        - amazon.titan-text-lite-v1
        - mistral.mixtral-8x7b-instruct-v0:1
        - mistral.mistral-7b-instruct-v0:2
        - mistral.mistral-large-2402-v1:0
        - meta.llama3-8b-instruct-v1:0
        - meta.llama3-70b-instruct-v1:0

* **All Mode**: Combines the features of both Extractor and NLP modes, extracting content and filtering valid articles before extracting flood event information using OpenAI or Bedrock.

## Getting Started

These instructions will help you set up and run the tool in a Conda environment on the local machine.

### Structure

The tool consists of the following files:

* `nlp_flex.py`: Main script for running the tool.
* `content_extraction.py`: Script for extracting content from URLs using Newspaper3k and processing the extracted content using OpenAI.
* `utils.py`: Logging configuration for the tool.
* `environment.yml`: Conda environment file for the tool.
* `config`: Folder containing configuration files for the tool.
* `data`: Folder containing input files for the tool.
* `output`: Folder containing results files for the tool.
* `logs`: Folder containing log files for the tool. Please, note that the log files are not included in the repository, but they are generated and stored locally on the user's machine.
* `tests`: Folder containing unit tests for the tool.

### Requirements

- [Python 3.12](https://www.python.org/downloads/) 

- Conda:
  - [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) or 
  - [Anaconda](https://www.anaconda.com/)

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://git.geoproc.geogc.ca/geoml/r_et_d/natural_language_processing/nlp-flood-extraction.git
    ```

2. Navigate to the project directory:

    ```bash
    cd nlp-flood-extraction
    ```

3. Create a Conda environment from the `environment.yml` file:

    ```bash
    conda env create -f environment.yml
    ```

4. Activate the Conda environment:

    ```bash
    conda activate nlp_flood_extract_env
    ```

## Setup your OpenAI API key

1. Create an account on the [OpenAI platform](https://platform.openai.com/).
2. Create an API key on the [OpenAI platform](https://platform.openai.com/api-keys).
3. In the project directory, create a file named `.env` and add your OpenAI API key to it:

    ```bash
    OPENAI_API_KEY=sk-...
    ```

## Add your credentials for AWS Bedrock

1. In the project directory, if not, create a file named `.env`.
2. Add your access and secret access keys, session token and AWS region to it:

    ```bash
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    AWS_SESSION_TOKEN=...
    AWS_REGION=...
    ```


You are now ready to use the tool.

**Note**: The `.env` file is included in the `.gitignore` file, so it will not be pushed to the repository.

## Usage

Run the tool by executing the `nlp_flex.py` script with the path to the configuration file:

```bash
python nlp_flex.py --config config/all.ini
```

## Configuration

The tool uses a configuration file to specify various parameters such as input file, output file, mode, etc. The configuration file is structured as follows:

```ini
[General]
input_filename = data/collection_articles.csv      ; Path to the file with th elist of URLs
output_filename = output/nlp_results.csv           ; Set to "None" or leave it empty for no output file
mode = all           ; Options: extractor, nlp, all
num_processes = 1    ; Number of processes for parallel extraction
url_col_name = URL   ; Name of the column with URLs
pub_date_col_name = PublishedDate  ; Name of the column with date when the article was  published


[NLP]
solution = bedrock                           ; bedrock or openai
model = mistral.mistral-7b-instruct-v0:26    ; NLP Model Name or Id
temp = 0.85                                  ; Temperature for the NLP model: a lower temperature means less randomness
max_tokens = 512                             ; Maximum tokens for the NLP model response
```

## Output
The tool generates output files based on the specified mode:

* In **Extractor** mode, it saves the extracted content to the specified output file. If no output file was specified, it creates a csv file with a timestamp in the `output` folder: `output/extracted_url_content_YYYY-MM-DD_HHMMSS.csv`.
* In **NLP** mode, it filters valid articles and extracts flood event information using Bedrock or OpenAI (as defined in the config file), saving the results to the specified output file. If no output file was specified, it creates a csv file with a timestamp in the `output` folder: `output/openai_results_YYYY-MM-DD_HHMMSS.csv`.
* In **All** mode, it combines the features of both modes, saving the final results to the specified output file. If no output file was specified, it creates a csv file with a timestamp in the `output` folder: `output/openai_results_YYYY-MM-DD_HHMMSS.csv`. The extracted URL content is saved to a csv file with a timestamp in the `output` folder: `output/extracted_url_content_YYYY-MM-DD_HHMMSS.csv`.

## Logging
The tool logs information, warnings, and errors to the console and a log file with a timestamp in the `logs` folder. The log file is named as follows: `logs/nlp_flex_YYYY-MM-DD_HH-MM.log`. The log file contains details about the tool's execution, including the start and end time, the number of URLs processed, the number of URLs that failed, and the number of URLs that were skipped. It also contains information about the number of URLs processed by each process in the case of parallel processing. The log file also contains warnings and errors of the main process.

## Limitations

1. The tool is limited to extracting content from URLs that are in English and French only.

2. The tool uses the free plan of the [OpenAI API](https://platform.openai.com/account/limits), which allows 3 requests per minute, RPM. To address this limitation, the tool uses a 'sleep' request of 60 seconds. This is not ideal, but it is the only way to avoid the error: "Too many requests. Please wait for a minute before making a new request." The tool can be modified to use a different plan to increase the number of requests per minute. While this mitigates RPM constraints, it does not address the daily API call limit. 

3. To terminate the tool, the user must press `Ctrl+C` in the console. Due to the use of multiprocessing, it takes some time to terminate all processes. The user can monitor the number of processes that are still running in the console. The tool will only terminate when all existing processes are completed. Sometimes, the tool does not terminate properly, and the user must press `Ctrl+C` multiple times to terminate the tool.

## Additional information

For additional information, questions, suggestions, please contact the owner of this repository.

## Authors

[Anastasiia Hryhorzhevska](https://www.linkedin.com/in/ahryhorzhevska)
