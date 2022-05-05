
# Python nytimes scrapper

A simple web scraper robot implemented in Python using the `rpaframework` set of libraries.

Searches for a specific search term provided in config.json, gets the meta data of the result, downloads the image and stores it all in excel

Each excel row will also contain the number of occurrences of the searched item in title and description, and if any references to currencies are present.

## Dependencies

On VS Code, The extension Robocorp Code needs to be installed, after which a terminal with Robot Environment can be opened. In the terminal, the following command needs to be run.

```bash
rcc run
```

## Configuration

`devdata/work-items-in/fresh-news-test-input/work-items.json` contains the following test payload:
 - **search_phrase:** the phrase to search
 - **section:** the section to search in - if the provided section isn't available, it is ignored
 - **months:** the range (in months) to search (till the end of current month)

```json
{
  "search_phrase": "$15",
  "section": "Business",
  "months": 48
}
```

These should be configured as cloud work items when running the robot in a cloud environment like Control Room.

## Usage

```bash
python tasks.py
```
