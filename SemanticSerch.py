import openai
import pandas as pd
import streamlit as st
from qdrant_client import QdrantClient

openai.api_key = "open-api-key"
client = QdrantClient(host="localhost", port=6333)

# convert data to small segmants
def FetchActivtiesFromExcel():
	# read data from task excel file
	df = pd.read_excel("task_output.xlsx")
	big_data = df['activities'].tolist()

	return big_data

# convert data to small segmants
def ConverDataToEmbeds(query):
	# run open ai to create small segmants of data
	response = openai.embeddings.create(model="text-embedding-ada-002", input=query)
	
	return [embedding['embedding'] for embedding in response['data']]

def UploadEmbedsToQdrant(embeds, big_data):
	client.upload_collection(
		collection_name="excel_search",
		vectors=embeds,
		payload=[{'activities': segmant} for segmant in big_data]
	)

def Search(query):
	# gen new embeds but with query this time
	query_embedding = ConverDataToEmbeds([query])
	
	# run search on Qdrant
	search_results = client.search(collection_name="excel_search", query_vector=query_embedding)
	
	return [res.payload['activities'] for res in search_results]

# setup the data for the later search
def SetupDataForSearch():
	big_data = FetchActivtiesFromExcel()
	embeds = ConverDataToEmbeds(big_data)
	UploadEmbedsToQdrant(embeds, big_data)

# write data to console
def DrawSearchResult(search_result):
	for res in search_result:
		st.write(res)