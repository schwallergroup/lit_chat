# How to run LitChat QA locally

 1. ssh into the workstation using your workstation id.
 eg; ` yourname@liacpc1.epfl.ch`

 2. Once you have logged into the workstation go to the `litchat_QA` directory.

 3. Create a conda environment. DO THIS ONLY ONCE! From the litchat_QA directory run the command `conda env create  -f environment.yml`. Skip step 3 and do step 4 if you have setup an environment previously.

 4. Activate your conda environment: `conda activate litchat`. You run this command everytime you need to use the QA chatbot locally. 

 5. Next run the command `streamlit run app.py`. This will provide you with a URL to open the streamlit interface.

 6. Copy paste the URL in your browser, add your openai API key and use the chatbot! 

