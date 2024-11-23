# Interactive AI-Based Travel Planner
| An Interactive Traveling Ticket Planner Using Streamlit, Djikstra's Algorithm and Map Box 

## Description
> This simple project **Interactive AI-Based Traveling Ticket Planner** is web-based tool designed to simplify route decisions based on user prefences. This tool utilizes **Djikstra's** algorithm in the back-end to determine the shortest path either by duration or cost. It works by selecting a departure and a Destination city using a dropdown list from a sidebar and a choice to sort either by cost or duration. 

## Features:
- <span style="font-size: 16px; font-weight: bold;">Interactive User Interface:</span> An interactive user interface experience simplifying the interaction between the user and the backend.
- <span style="font-size: 16px; font-weight: bold;">Best Route: </span> Calculate the best route using Djikstra's Algorithm on two types of weights: Duration/Cost
- <span style="font-size: 16px; font-weight: bold;">Interactive Maps:</span> A visualization of the traveling route with a 3D effect on satellite maps.
- <span style="font-size: 16px; font-weight: bold;">Dynamic UI:</span> A super simple UI that includes drop-downs


## Requirements
> Python, Miniconda, pip OR python module: pip

## How to Run
```
conda create -n interactive-travel-planner python==3.8
conda activate interactive-travel-planner
pip install -r requirements.txt
streamlit run main.py
```

