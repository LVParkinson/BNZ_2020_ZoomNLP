# Zoom chat analytics
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
Examples of the histogram, network graph, and basic pdf report are in the examples folder **TODO: create examples folder** 

## How to use this Repo  
**TODO**

## Further reading
My goal is to create a tool that allows someone to glean more insights from their meetings. More about the goals of the program and how it works can be found in this Medium post: **TODO - INSERT POST**


## Citation
If you use this repo please consider citing it. 
```javascript
@misc{Zoom_chat_analysis,
  title={A terminal application for analytics of Zoom chat transcripts},
  author={Lindsey Viann Parkinson},
  year={2020},
  publisher={Github},
  journal={GitHub repository},
  howpublished={\url{https://github.com/LVParkinson/Zoom_chat_analytics}},
}
```
