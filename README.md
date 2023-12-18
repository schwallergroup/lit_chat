# LitChat QA

## Setup and Activation

 1. SSH into the workstation using your workstation ID, for example: `yourname@liacpc1.epfl.ch`

 2. Go to the `lit_chat` directory. If it's your first time, set up a conda environment. **This is a one-time setup**. From the `lit_chat` root directory, run: `conda env create  -f environment.yml`. If you have already set up the environment, skip to step 3.

 3.  Activate your conda environment. This step is required every time you use the QA chatbot locally: `conda activate litchat`

 4.  **Important**: Ensure the path to the vectorstore in the `chat.py` module is correctly updated. Refer to this [line in the chat.py file](https://github.com/schwallergroup/lit_chat/blob/232b65adc68f7481d6e9f92e0fab488deb23319e/lit_chat/chat.py#L21) for guidance.

 5.  Start the LitChat QA interface by running: `streamlit run app.py` from the root directory. This command will generate a URL.

 6.  Copy and paste the provided URL into your browser, enter your OpenAI API key, and start using the chat!

## Converting literature (PDFs) to a vectorestore
To create or extend a vectorstore with your literature (list of PDF files), use the `vectorstore.py` module.

- To extend an existing vectorstore, execute:


  ```
  python vectorstore --openai_key <your_key> --file_dir <path_to_pdfs> --persist_dir <path_to_vectorstore> --create_new False
  ```

- To create a new vectorstore, set `--create_new` to `True`. More details can be found in the [vectorstore module documentation](https://github.com/schwallergroup/lit_chat/blob/main/lit_chat/vectorstore.py).

