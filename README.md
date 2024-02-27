**This code is a Streamlit app that allows users to chat with a LLM(Gemini) about multiple PDFs. The app uses the following steps:**

 - The user uploads one or more PDFs to the app
 - The file is saved locally and is converted to text chunks 
 - The app creates a vectorstore DB from the text chunks
 - The user asks a question about the PDFs
 - The app uses the conversation chain to generate a response. 
 - The app displays the response to the user
