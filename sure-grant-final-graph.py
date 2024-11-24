import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import re
from matplotlib import cm  # Colormap for better visuals

# File paths
arHateDataset_path = "/Users/nayaadla/Desktop/Suregrant FILES/arHateDataset.csv"

# Load the file into a DataFrame
arHateDataset_df = pd.read_csv(arHateDataset_path)

# Use 'Tweet' as the tweet column based on your dataset
tweet_column = 'Tweet'

# Function to remove emojis
def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Define the categories
offensiveness_categories = {
    "Most Offensive": ['يلعن', 'كلب', 'كلاب', 'واطي', 'خنزير', 'حقير', 'حمار', 'عرص', 'قذر', 'مجرم', 'لعنة', 'زاني', 'زانية'],
    "Moderately Offensive": ['حيوان', 'ولاك', 'غبي', 'عميل', 'تفو', 'جحش', 'لقيط', 'نجس', 'العما', 'خرا', 'طرطور', 'بوط', 'شرف'],
    "Least Offensive": ['سوري', 'شعب', 'اللاجئين', 'لاجئ', 'امريكا', 'اوربا', 'عرب', 'بطران', 'تشبيح', 'تيس', 'جبان', 'حقود', 'زبالة', 'شحاد', 'شرف', 'مقمل', 'ندل', 'نذل', 'نعل', 'فاشل', 'كره']
}

additional_categories = {
    "Social": ['كلب', 'كلاب', 'واطي', 'يلعن', 'قذر', 'نجس', 'تفو', 'حقير', 'حمار', 'حيوان', 'ولاك', 'غبي', 'جحش', 'لقيط', 'العما', 'خرا', 'بوط', 'شرف', 'تيس', 'جبان', 'حقود', 'زبالة', 'شحاد', 'مقمل', 'ندل', 'نذل', 'نعل', 'فاشل', 'كره'],
    "Religious": ['زاني', 'زانية', 'سنة', 'شيعة'],
    "Politics": ['مجرم', 'عميل', 'طرطور', 'خنزير', 'سوري', 'عرب', 'اللاجئين', 'لاجئ', 'امريكا', 'اوربا', 'السعودية', 'قطر', 'مصر', 'لبنان', 'سوريا', 'فلسطين', 'الأردن', 'العراق', 'الإمارات', 'الكويت', 'البحرين', 'اليمن', 'عمان', 'ليبيا', 'الجزائر', 'المغرب', 'تونس', 'السودان']
}

region_keywords = {
    "North Africa": ['الجزائر', 'مصر', 'ليبيا', 'موريتانيا', 'المغرب', 'السودان', 'تونس'],
    "Levant": ['الأردن', 'لبنان', 'فلسطين', 'سوريا'],
    "Gulf": ['البحرين', 'العراق', 'الكويت', 'عمان', 'قطر', 'السعودية', 'الإمارات', 'اليمن']
}

# Function to categorize a tweet based on its content
def categorize_tweet(tweet):
    regions = []
    categories = []
    
    # First, check for region keywords
    for region, keywords in region_keywords.items():
        if any(keyword in tweet for keyword in keywords):
            regions.append(region)
    
    # Then, check for offensiveness and subcategories
    for offensiveness, words in offensiveness_categories.items():
        if any(word in tweet for word in words):
            for subcategory, subwords in additional_categories.items():
                if any(subword in tweet for subword in subwords):
                    for region in regions:  # Combine region with offense and subcategory
                        categories.append((region, offensiveness, subcategory))
    
    return categories

# Remove emojis from the tweets
tweets = arHateDataset_df[tweet_column].apply(remove_emoji)

# Categorize each tweet
categorized_tweets = [categorize_tweet(tweet) for tweet in tweets]
flat_categorized_tweets = [item for sublist in categorized_tweets for item in sublist]

# Create a DataFrame from the categorized data
df = pd.DataFrame(flat_categorized_tweets, columns=['Region', 'Offensiveness', 'Subcategory'])

# Group by Region, Offensiveness, and Subcategory to count occurrences
grouped_counts = df.groupby(['Region', 'Offensiveness', 'Subcategory']).size().unstack(fill_value=0)

# Filter out rows and columns with all zeroes to improve the graph
grouped_counts = grouped_counts.loc[(grouped_counts.T != 0).any(), (grouped_counts != 0).any()]

# Function to create a 3D bar plot with annotations and color explanation
def plot_3d_bar(grouped_data, title):
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Prepare positions for bars
    x = np.arange(len(grouped_data.index))  # Regions
    y = np.arange(len(grouped_data.columns))  # Subcategories
    xpos, ypos = np.meshgrid(x, y)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros_like(xpos)

    # Bar heights
    heights = grouped_data.values.T.flatten()

    # Color mapping based on heights (using a colormap)
    colors = cm.viridis(heights / max(heights))

    # Bar width and depth
    dx = dy = 0.4

    # Plot 3D bars
    ax.bar3d(xpos, ypos, zpos, dx, dy, heights, color=colors, shade=True)

    # Annotate bars with their heights (frequencies)
    for i in range(len(heights)):
        if heights[i] > 0:  # Only annotate non-zero heights
            ax.text(xpos[i], ypos[i], heights[i], '%d' % int(heights[i]), ha='center', va='bottom')

    # Set labels
    ax.set_xlabel('Region and Offensiveness')
    ax.set_ylabel('Subcategory')
    ax.set_zlabel('Frequency')

    # Set tick positions and labels
    ax.set_xticks(np.arange(len(grouped_data.index)))
    ax.set_xticklabels(grouped_data.index, rotation=45, ha='right')
    ax.set_yticks(np.arange(len(grouped_data.columns)))
    ax.set_yticklabels(grouped_data.columns)

    # Add color bar for explanation
    mappable = cm.ScalarMappable(cmap='viridis')
    mappable.set_array(heights)
    fig.colorbar(mappable, ax=ax, shrink=0.6, aspect=5)

    # Add title
    plt.title(title, pad=20)
    plt.tight_layout()
    plt.show()

# Plot 3D bar plot with correct frequencies and annotations
plot_3d_bar(grouped_counts, '3D Visualization of Offensive Words by Region, Offensiveness, and Subcategory')
