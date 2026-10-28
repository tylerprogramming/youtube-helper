# YouTube Helper

A small Streamlit app that drafts YouTube community content with AutoGen (v0.2 API):

- **Quizzes**: an AutoGen assistant writes one intermediate Python multiple-choice question with the answer and the reason.
- **Information Posts**: searches the web with [Tavily](https://tavily.com), then has the assistant shorten each result into a short post with a "Read More" link.

## Setup

Python 3.10 to 3.12 (pyautogen 0.2 does not support 3.13).

```bash
pip install -r requirements.txt
```

Set your keys as environment variables:

```bash
export OPENAI_API_KEY=sk-...
export TAVILY_API_KEY=tvly-...
```

The model is set in `OAI_CONFIG_LIST.json` (`gpt-5.4-mini`). The API key comes from `OPENAI_API_KEY`, so keep keys out of that file.

## Run

```bash
streamlit run main.py
```

`coding/mcq.json` holds example questions from earlier runs.
