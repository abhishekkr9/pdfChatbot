This code is a Streamlit app that allows users to chat with a LLM(Gemini) about multiple PDFs. The app uses the following steps:

The user uploads one or more PDFs to the app.
The app extracts the text from the PDFs.
The app splits the text into chunks.
The app creates a vectorstore from the text chunks.
The app creates a conversation chain from the vectorstore and an LLM.
The user asks a question about the PDFs.
The app uses the conversation chain to generate a response.
The app displays the response to the user.
The app also includes a chat history feature, so that users can see what they have asked and been told.
