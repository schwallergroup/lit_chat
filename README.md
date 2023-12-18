# How to run LitChat QA locally

 1. ssh into the workstation using your workstation id.
 eg; ` yourname@liacpc1.epfl.ch`

 2. Once you have logged into the workstation go to the `litchat_QA` directory, create a conda environment. DO THIS ONLY ONCE! From the litchat_QA directory run the command `conda env create  -f environment.yml`. Skip step 3 and do step 4 if you have setup an environment previously.

 4. Activate your conda environment: `conda activate litchat`. You run this command everytime you need to use the QA chatbot locally.
 5. **IMPORTANT:** Update the correct path to the vectorstore in `chat.py` module. https://github.com/schwallergroup/lit_chat/blob/232b65adc68f7481d6e9f92e0fab488deb23319e/lit_chat/chat.py#L21

 6. Next run the command `streamlit run app.py`. This will provide you with a URL to open the streamlit interface.

 7. Copy paste the URL in your browser, add your openai API key and use the ChatBot!


# Converting literature (PDFs) to a vectorestore
To create a new vectorstore with your own literature (list of PDF files) or extend the existing one with more literature you can run the `lit_chat/vectorstore.py` module locally. 

To extend an existing vectorstore:

    python vectorstore --openai_key <your_key> --file_dir <path_to_pdfs> --persist_dir <path_to_vectorstore> --create_new False

Or else you can create a new vectorestore by setting `--create_new True`. See [vectorstore module](https://github.com/schwallergroup/lit_chat/blob/main/lit_chat/vectorstore.py)

