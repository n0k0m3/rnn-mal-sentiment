# rnn-mal-sentiment

## Requirements
- Python 3.8 for `pickle` protocol 5, else Python 3.6+
- Requirements for data collecting script `jikan.py`:
```
pip install -U requirements.txt
```

- Notebook (`main.ipynb`) can be run on Google Colab (Python 3.6) with the `tables` module updated (Run the first cell then restart the runtime).

## Notes
`jikan.py` was run on a self-hosted [Jikan REST API](https://github.com/jikan-me/jikan-rest). 

If you just want to test run the script:
- Change `API_URI` to the [public Jikan API](https://jikan.docs.apiary.io/#): `https://api.jikan.moe/v3`
- Uncomment the 4 rate limits lines in the script to avoid public API abuse.