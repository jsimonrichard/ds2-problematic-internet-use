# Data Science 2 - Final Project: Children's Problematic Internet Use


## Getting Started
```
conda create -n DS2 python=3.12
conda activate DS2
pip install -r requirements.txt
```

### Downloading the data
Create an API key at https://www.kaggle.com/settings and put the downloaded `kaggle.json` file in `~/.kaggle`. Then download the data.
```bask
kaggle competitions download -c child-mind-institute-problematic-internet-use -p ./data
```