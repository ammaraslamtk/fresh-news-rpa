# Python nytimes scrapper

A simple web scraper robot implemented in Python using the `rpaframework` set of libraries.

Searches for a specific search term provided in config.json, gets the meta data of the result, downloads the image and stores it all in excel

Each excel row will also contain the number of occurrences of the searched item in title and description, and if any references to currencies are present.

## Dependencies

Requires [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html)

dependencies can be installed using conda.yaml file. Uses `Python=3.9.6` and `rpaframework==13.0.3`.

```bash
conda init
conda create --name env
conda activate env
conda env update -f conda.yaml
```

Note: While using miniconda, `conda install pywin32` may be needed for win32api

## Configuration

`config.json` contains the following modifiable configurations, the item to search, the section to search from and the range (in months) to search in (from current date)

```json
{
  "search_phrase": "$15",
  "section": "Business",
  "months": 48
}
```

## Usage

```bash
python tasks.py
```
