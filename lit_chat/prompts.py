QA_PROMPT = """Your goal is to find the answer to the following question using the text provided below. \n \n
    The text may contain multiple answers, provide them all\n. 
    
    Question: {}

    \ntext: {}

    Also provide the text which was used to generate the answer. Add citations to each.\n

    If you couldn't find an answer, reply with 'could not find an answer'

    You can follow the following format for your answer: \n

    - First provide your answers here. answer: \n

    - Second, provide parts of the texts used to generate the answers. literature evidence: ``evidence `` \n

    - Finally, provide the list of references used to answer from the text. Use APA citation style for referencing.
        Example: \n
        References: \n
        1. reference 1 \n
        2. reference 2 \n    
    """

META_PROMPT = """You are given the fist two pages of an academic publication.
                Your goal is to extract list of author names, title, and year of publication from the following text. 
                
                /n text:  {text}.
                
                Output should have following format:
                
                "Authors": "author1, author2 ...",
                
                "Year": "year of publication", 
                
                "Title": "title of the paper"
                 
                Format instructions: \n{format_instructions}
                """
