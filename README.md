# FitOver: Your AI Virtual Try-On (Prototype)
FitOver is a Streamlit application that utilizes the Replicate API to demonstrate a Virtual Try-On feature. Users can upload their photo and a photo of a piece of clothing, and the AI model generates an image of the user wearing the uploaded apparel.

![Example screenshot](https://github.com/Drayerr/fit-over-prototype/blob/c92d207bd26e4a11e016ac9ba5a15611c618f8e4/Picture%2001.png)

## 💡Features
* Virtual Try-On: Seamlessly generate images of a person wearing new clothes using AI.

* Simple Interface: Intuitive two-column layout for easy image uploads.

* API Integration: Connects directly to the Omnious/Vella-1.5 model on Replicate.

## 🛠️ Setup and Installation
Follow these steps to get your local copy of FitOver running.

1. Prerequisites

You need Python 3.8+ installed.

2. Clone the Repository

```Bash
git clone https://github.com/Drayerr/fit-over-prototype
cd fitover-virtual-try-on
```

4. Install Dependencies

It's recommended to use a virtual environment (venv).

```Bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate # On Windows, use: venv\Scripts\activate
```


 Install required Python packages
```Bash
pip install streamlit python-dotenv replicate streamlit-extras
```

5. Configure API Key

This project relies on the Replicate API to run the AI model.

Get your API Token from the [Replicate website](https://replicate.com).

Create a file named .env in the root directory of the project with the following:
```py
REPLICATE_API_TOKEN=your_key_here
```

## 💻 How to Run
Ensure your virtual environment is active and dependencies are installed.

Run the Streamlit application from your terminal:

```Bash
streamlit run app.py
```
The application will open in your default web browser (usually at http://localhost:8501).

## ⚙️ Key Technologies
* Streamlit: An open-source Python library that allows data scientists and machine learning engineers to create interactive web applications for data projects with minimal code. 
* Replicate (AI): Replicate API (using the omnious/vella-1.5 model), used for editing the user submitted photo with the new content uploaded.
