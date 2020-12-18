# Zoom chat analytics

## Author  
[Lindsey Viann Parkinson](https://linkedin.com/in/lindsey-viann)  
  
## Purpose
Recorded Zoom meetings include a transcript of the meeting chat box in the form of a .txt file. The Zoom_chat_analytics repository is the beginning of a tool to harness more information from those meetings. All the analytical functions can be run from the command line.

As of December 17, 2020 Zoom_chat_analytics.py can:  
- Create and export a csv of the chat with: time of comment, author, and comment
- Create and export a pdf that includes the following:
  - Ordered list of which participants commented the most
  - A histogram of comment volume of the course of the meeting
  - Any URLs shared
  - A network graph of commenters and responders
- Each of the analytical functions within the pdf report can also be run individually  

## Documents  
- requirements.txt - installs all required dependencies
- Zoom_chat_analytics.py - see above


## Example output  
Examples of the histogram, network graph, and basic pdf report are in the examples folder  

## How to use this Repo   
The command line application runs in the terminal using Google fire. In order to use it you will need to install the required dependencies listed in the [requirements file](requirements.txt).
```javascript
pip3 install -r requirements.txt
```

If you only want to make the csv:  
- **convert_to_csv**(filepath, csv_name) - Creates and exports three column csv: time, author, comment  

Analysis:  
- **start_to_finish**(filepath, csv_name, pdf_name) - Runs all the analytical functions and exports pdf, dataframe csv, and graphs as .png files      
- **one_analytic**(filepath, csv_name, function_name) - Runs one analytical function  
    * **find_urls** - Extract urls from comments  
    * **comments_by_author** - Count the number of comments made by each author  
    * **comments_over_time** - Returns histogram of comments over meeting time  
    * **comment_network** - Create a network graph of who responds to comments  

Variables:  
- **filepath**: path to .txt file   
- **csv_name**: name for exported csv (include .csv)  
- **pdf_name**: name for exported pdf (include .pdf)  
- **function_name**: which of the individual functions you'd like to run    

In the terminal:  
- Change directory to where Zoom_chat_analytics.py is stored  
- The three parts of the application call are $ {./Zoom_chat_analytics.py} {function name} {function variables}    

For example:  
```javascript
./Zoom_chat_analytics.py start_to_finish /home/folder/folder/Zoom.txt example.csv example.pdf
```

## Further reading  
My goal is to create a tool that allows someone to glean more insights from their meetings. More about the goals of the program and how it works can be found in this Medium post: **TODO - INSERT POST**


## Citation
If you use this repo please consider citing it. 
```javascript
@misc{Zoom_chat_analysis,
  title="A terminal application for analytics of Zoom chat transcripts",
  author="Lindsey Viann Parkinson",
  year="2020",
  publisher="Github",
  journal="GitHub repository",
  howpublished= "https://github.com/LVParkinson/Zoom_chat_analytics"
}
```
