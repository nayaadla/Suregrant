# Suregrant
Hate Speech Analysis and Visualization Tool
Overview
This project analyzes hate speech in tweets from a dataset, categorizing the content based on region, offensiveness, and subcategories (Social, Religious, Politics). The results are visualized in an interactive 3D bar plot to provide insights into hate speech distribution and frequency.

Features
Preprocessing:

Removes emojis for cleaner text processing.
Identifies offensive words, regional keywords, and subcategories.
Categorization:

Classifies tweets based on regions (North Africa, Levant, Gulf).
Categorizes offensiveness into Most Offensive, Moderately Offensive, and Least Offensive.
Subdivides hate speech into Social, Religious, and Politics.
Visualization:

Displays results in a 3D bar plot.
Annotates frequencies and provides a color map for better interpretation.
Dataset
The dataset should be a CSV file with the following requirements:

Column name for the tweet text: Tweet
File path: /Users/nayaadla/Desktop/Suregrant FILES/arHateDataset.csv
Requirements
Python 3.x
Libraries: pandas, matplotlib, numpy, re
How It Works
Load Dataset: Reads the dataset from the specified file path.
Clean Text: Removes emojis and standardizes text for analysis.
Categorize Tweets:
Matches tweets with offensive keywords and regional identifiers.
Groups by Region, Offensiveness, and Subcategory to count occurrences.
Visualize Results:
Creates a 3D bar plot showing frequencies across categories.
How to Use
Ensure the dataset is available at the specified path.
Install the required Python libraries:
bash
Copy code
pip install pandas matplotlib numpy
Run the script:
bash
Copy code
python script_name.py
View the 3D bar plot for analysis and insights.
Example Output
3D Visualization:

X-Axis: Regions and Offensiveness levels.
Y-Axis: Subcategories (Social, Religious, Politics).
Z-Axis: Frequency of offensive words.
The plot includes:

Bars colored based on frequency (Viridis colormap).
Annotated heights for each bar.
Interactive rotation and zoom for better exploration.
Customization
Keywords: Modify offensiveness_categories or additional_categories for custom analysis.
Regions: Update region_keywords for other regions or keywords.
Plot Design: Adjust colormap or bar dimensions in plot_3d_bar().
Notes
Ensure the dataset contains sufficient data for meaningful analysis.
Handles tweets in Arabic; adapt keywords for other languages as needed.
License
This project is open-source and available under the MIT License. Contributions are welcome!












ChatGPT can make mistakes. Check important info.
