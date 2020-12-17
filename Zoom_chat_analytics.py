#!/usr/bin/python3

"""
Script to convert raw text file from Zoom chat into usable dataframe and run basic analytics. 

Make csv:
    convert_to_csv() - Exports csv with three columns: time, author, and comment

Analysis:
    start_to_finish() - Runs all the analytical functions and exports pdf
    individual_function() - Runs one  analytical function
        find_urls() - Extract urls from comments
        comments_by_author() - Count the number of comments made by each author
        comments_over_time() - Returns histogram of comments over meeting time  
        comment_network() - Create a network graph of who responds to comments

Author: Lindsey Viann Parkinson
Last Updated: December 17, 2020

"""
# Import modules and packages
import fire
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import networkx as nx
from fpdf import FPDF, HTMLMixin



def convert_to_csv(filepath, csv_name):
    """
    Exports csv with three columns: time, author, and comment
    
    filepath: path to the .txt file downloaded from the Zoom recording
    csv_name: name for the exported csv file (include .csv !)
    """
    file = open(filepath, mode='r',encoding="utf8")

    time = []
    author =[]
    comment =[]

    regex_time = r'\d{2}:\d{2}:\d{2}'
    regex_author = r'\bFrom \s(.*?:)'
    regex_comment = r'(?:\: )(.*$)'

    for line in file:
    # Empty lines will be ignored
        if line.strip(): 
        # use .extend() instead of .append() to avoid making a list of single-item lists
            time.extend(re.findall(regex_time, line))
            author.extend(re.findall(regex_author, line))
            comment.extend(re.findall(regex_comment, line))
    
    s1=pd.Series(time,name='time')
    s2=pd.Series(author,name='author')
    s3=pd.Series(comment ,name='comment')
    
    df = pd.concat([s1,s2,s3], axis=1)
    
    #remove "  :" from each author
    df['author'] = df['author'].str[:-2]
    
    # remove private messages from dataframe
    df = df[~df['author'].str.contains("Privately")].reset_index(drop=True)
    
    df.to_csv(csv_name, index = False) 
    
    print("\n~~~~check source folder for Zoom chat csv~~~~\n")
    print(df.head())
    return df
    
    
def find_urls(df):
    """
    Extract urls from comments. 
    Only works with full urls containing "http(s)://"
    """
    #Bug: if 2+ links in one comment, the links are printed together. BUT both work.
    
    links=[]
    for comment in df['comment']:
        links.extend(re.findall(r'(https?://[^\s]+)', comment)) 
    return links
    

def comments_by_author(df):
    """
    Count the number of comments made by each author
    """
    authorcomments = df.groupby(df['author'])['author'].count().sort_values(ascending=False)
    return authorcomments


def comments_over_time(df):
    """
    Count the number of comments over time. Return histogram.
    """  
    #convert string to time
    df['time'] = pd.to_datetime(df['time'],format= '%H:%M:%S' ).dt.time

    # get a list of the times
    times = [t.hour + t.minute/60. for t in df['time']]

    # set the x-axis time interval required (in minutes)
    tinterval = 10

    # find the lower and upper bin edges (on an integer number of 10 mins past the hour)
    lowbin = np.min(times) - np.fmod(np.min(times)-np.floor(np.min(times)), tinterval/60.)
    highbin = np.max(times) - np.fmod(np.max(times)-np.ceil(np.max(times)), tinterval/60.)
    bins = np.arange(lowbin, highbin, tinterval/60.)  # set the bin edges    
     
    # create the histogram
    plt.hist(times, bins=bins)
    ax = plt.gca()  # get the current plot axes
    ax.set_xticks(bins)  # set the position of the ticks to the histogram bin edges

    # create new labels in hh:mm format (in twelve hour clock)
    newlabels = []
    for edge in bins:
        h, m = divmod(edge%12, 1)  # get hours and minutes (in 12 hour clock)
        newlabels.append('{0:01d}:{1:02d}'.format(int(h), int(m*60)))  # create the new label

    ax.set_xticklabels(newlabels, rotation = 60)  # set the new labels
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 2))
    ax.set_ylabel("Number of messages")
    ax.set_title("number of messages in 10-min intervals")
    plt.savefig("Zoom_histogram.png")
    
    print("\n~~~~check working directory for Zoom_histogram.png~~~~\n")
    
    
    
def comment_network(df):
    """
    Create a network graph of who responds to comments
    Lines are drawn between the author of a comment and the next person to comment
    """    
    dfchatters = df[['author']]
    dfchatters['responder'] = df['author'].shift(periods=-1)
    dfchatters = dfchatters.dropna()
    
    G = nx.DiGraph()

    G = nx.from_pandas_edgelist(dfchatters, 'author', 'responder')
    
    figure(figsize=(23, 15))
    nx.draw_shell(G, with_labels=True,font_weight='bold')

    plt.savefig("Zoom_network.png", bbox_inches="tight")
    
    print("\n~~~~check working directory for Zoom_network.png~~~~\n")

    
def individual_function(filepath, csv_name, function_name):
    """
    Call only one function of Zoom Chat Analytics
    
    filepath: path to .txt file 
    csv_name: what the output csv will be called (include .csv !)
    function_name: which individual function you'd like to run
    
    """
    df = convert_to_csv(filepath, csv_name)
    return eval(function_name + "(df)")
    
def start_to_finish(filepath, csv_name):    
    df = convert_to_csv(filepath, csv_name)

    #Create and Format pdf
    
    class MyFPDF(FPDF, HTMLMixin):
        pass
    
    pdf = MyFPDF()
    pdf.add_page()
        #Header
    pdf.set_font('Arial', 'B', size = 25)
    pdf.cell(200, 10, txt = "Zoom Chat - Basic Analytics",  
         ln = 1, align = 'C') 
    
    #Page 1 - Comments by author
    pdf.set_font('Arial', 'B', size = 15)
    pdf.cell(200, 10, txt = "Number of comments by each author", ln = 2) 
    
    author_list = comments_by_author(df)
    pdf.set_font('Arial', size = 15)
    for author, count in author_list.items():
        pdf.cell(200, 5, txt = f"{author} - {count}", ln = 1)

    #Page 2 - URLs
    pdf.add_page()
    pdf.set_font('Arial', 'B', size = 15)
    pdf.cell(200, 10, txt = "urls shared", ln=2) 
    
    url_list = find_urls(df)
    pdf.set_font('Arial', size = 12)
    for url in url_list: 
        pdf.write_html(text = f"<a href={url}>{url}</a></br>")
    
    #Page 3 - Histogram
    pdf.add_page(orientation = 'L')
    comments_over_time(df)    
    pdf.image("Zoom_histogram.png", w=250, h=160)
    
    #Page 4 - Network
    pdf.add_page()
    pdf.set_font('Arial', 'B', size = 15)
    pdf.cell(200, 10, txt = "Zoom Chat Network", ln = 1, align = 'C')
    comment_network(df)
    pdf.image("Zoom_network.png", w=200, h=200)
    
        #footer
    pdf.set_font('Arial', size = 10)
    pdf.multi_cell(180, 25, txt = "Document created with https://github.com/LVParkinson/BNZ_2020_ZoomNLP ", align = 'C')

    pdf.output("test.pdf")

    print("\n~~~~start-to-finish complete. Check working directory~~~~\n")        

    
if __name__ == '__main__':
    fire.Fire({
      'convert_to_csv': convert_to_csv,
      'find_urls': find_urls,
      'comments_by_author': comments_by_author,
      'comments_over_time': comments_over_time,
      'comment_network': comment_network,
      'individual_function': individual_function,
      'start_to_finish': start_to_finish
  })
