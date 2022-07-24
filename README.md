# Piazza Archiver

This is a simple Python script to download all posts from a course on [Piazza](https://piazza.com) using the unofficial [Piazza API](https://github.com/hfaran/piazza-api).

## Installation

**Requirements:** Python >= 3.5

1. Clone this repository: `git clone https://github.com/64bitpandas/piazza-archiver` (or download as zip if you don't have git)
2. Install Piazza API: `pip install piazza-api`
3. Rename the SECRETS.template file to SECRETS, and fill in your email and password. (If you don't want to write down your password, skip this step and enter it in manually when running the script.)

## Usage

Run the script using `python3 archive.py`. 

If you didn't complete Step 3 in the installation, you will be prompted to enter your username and password.

After authentication is successful, you can choose which course(s) you wish to archive from the list of courses your account is enrolled in. Each course will be assigned a number, which will be printed in the console. Accepted inputs include:
 - Single numbers, like `5`
 - Ranges, like `10-15`
 - Lists of ranges and numbers, like `1-5, 6, 10-15`

The script will then create a new folder for each course it archives. Three files in JSON format are included in each folder:
 - `info.json`: basic course info
 - `stats.json`: publicly viewable course statistics such as top posters and number of posts by day
 - `posts.json`: list of all posts in the course

## Disclaimers

1. The Piazza API is unofficial, and there is no guarantee that it will be functional in the future if Piazza decides to change their architecture. If it breaks, this script will also break.
2. Fetching each post requires an individual API request, and Piazza has an undetermined rate limit (from testing, it seems awfully close to 60/min). As such, this script will take a minimum of 1 second to fetch each post which is pretty slow. A course with 1000 posts would probably take about 20 minutes to fully export.
3. I don't think this script as it is written violates any of Piazza's [terms of service](https://piazza.com/legal/terms), but make sure to read it before doing anything with the data it collects. I am not a lawyer and this is not legal advice.