# Interview_Task


A- Web Crawler:

    The code is a web crawler that scrapes company data from a website and saves it to an Excel file. Here’s a simple explanation of its architecture:
    
    1- Data Writing: WriteDataToExcel(company_data) converts a dictionary of company data into a pandas DataFrame and writes it to an Excel file using the openpyxl engine.
    
    2- Cloudflare Email Decoding: DecodeColudeFlareEmail(encoded_email) is used to decode email addresses protected by Cloudflare's encryption technique, by XOR decoding the characters.
    
    3- Data Extraction: ExtractCompanyData(url) takes a company URL, sends a request, and scrapes specific company attributes like name, phone, city, email, and activities using HTML tags. It decodes the Cloudflare-protected email and processes the activities into a readable format.
    
    4- Main Crawler Logic: RunWebCrawler() sends requests to a base URL for multiple pages (pagination handled via parameters). It extracts company URLs, scrapes each company’s data, stores it in a dictionary, and appends a delay between requests to avoid overwhelming the server.
    
    5- Asynchronous Execution: The main crawler is run asynchronously using asyncio.run() to avoid blocking and ensure tasks like delaying between requests are handled efficiently.
    
    6- Semantic Search: The commented-out sections at the bottom (ss.SetupDataForSearch(), etc.) is the semantic search functionality with a module called SemanticSearch.

B- Semantic Search:

    1- Data Fetching: The FetchActivtiesFromExcel() function reads activity data from an Excel file named "task_output.xlsx" using pandas and returns a list of activities.
    
    2- Embedding Creation: ConverDataToEmbeds(query) takes a query or list of activities and generates embeddings using OpenAI's text-embedding-ada-002 model. It returns the embeddings in a list format.
    
    3- Uploading to Qdrant: The UploadEmbedsToQdrant(embeds, big_data) function uploads the generated embeddings and the original activities to a Qdrant collection named "excel_search". This allows efficient searching based on the semantic similarity of the activities.
    
    4- Searching Functionality: The Search(query) function creates an embedding for the user’s query and performs a search in the Qdrant collection to find relevant activities. It returns a list of activities from the search results.
    
    5- Data Setup for Search: SetupDataForSearch() orchestrates the setup by fetching activities from Excel, converting them into embeddings, and uploading those embeddings to Qdrant. This prepares the system for searching.
    
    6- Displaying Results: The DrawSearchResult(search_result) function takes the results from a search query and displays them using Streamlit’s st.write(), rendering the results in the web interface.

C- Chanllanges:

    1- The cloudflare encryption over the email of the compan, took a bit of resarch to understand the strange formate and how to decode it
    
    2- The Semantic Search, with my very limited knowledge of the SS i was a bit hard to search and understand to provide the data for the search vector and how to call it and how to use open AI to search for the result, after finishing up the search logic i could not test it because of the rate limit on open ai token


HOW TO USE:

    run the main script file
