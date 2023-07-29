# inteli_karoba

[**Inteli_karoba**](https://intelikaroba-oczygzn4vuqd2pqt8nwgbu.streamlit.app/) is an interactive Q&A chat interface designed to interact with PDF documents. It allows users to upload their documents and engage in a conversation about the contents of the documents leveraging conversational memory. The application is a combination of features from two different applications [ask-multiple-pdfs](https://github.com/alejandro-ao/ask-multiple-pdfs) and [Chatbot with ChatGPT API and Conversational Memory](https://medium.com/@avra42/how-to-build-a-chatbot-with-chatgpt-api-and-a-conversational-memory-in-python-8d856cda4542).

## Key Features

1. **PDF Upload:** Upload your PDF files directly to the chat interface for interaction. Input your OpenAI API key.

    ![Uploading PDFs for embedding](https://github.com/dbae1145/images/blob/main/embedding.JPG?raw=true)
    
2. **Show Page Content:** Display the contents of a specific page from a specific file.

    ![Showing page content](https://github.com/dbae1145/images/blob/main/show_page.JPG?raw=true)

3. **Conversational Q&A:** Ask questions and have a conversation about the contents of your uploaded documents.

    ![Conversation example](https://github.com/dbae1145/images/blob/main/conversation_example.JPG?raw=true)

## How to Use

1. **Upload your PDF documents:** Click on the upload button in the chat interface to upload your PDF documents.

2. **View Page Content:** To view the contents of a particular page, go to Show Page Content.

3. **Ask questions:** Once your PDF documents have been uploaded, simply type in the chat box to ask questions about the contents of the documents. The application's conversational memory feature allows it to maintain context, making interactions smooth and natural.

## Installation

To set up the app locally, you need to clone this repository and install the required packages. Follow these steps:

1. Clone the repository
```
git clone https://github.com/sbae1145/inteli_karoba.git
```

2. Change your directory
```
cd inteli_karoba
```

3. Install the required packages
```
pip install -r requirements.txt
```

4. Run the streamlit app
```
streamlit run app.py
```

For more advanced setup like deploying the app or dockerizing, please refer to Streamlit's official [deployment guide](https://docs.streamlit.io/en/stable/deploy_streamlit_app.html).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions to inteli_karoba!
## Acknowledgments

* [Alejandro AO](https://github.com/alejandro-ao) for the [ask-multiple-pdfs](https://github.com/alejandro-ao/ask-multiple-pdfs) application.
* Avra for the [Chatbot with ChatGPT API and Conversational Memory](https://medium.com/@avra42/how-to-build-a-chatbot-with-chatgpt-api-and-a-conversational-memory-in-python-8d856cda4542) tutorial.

For any issues, questions, or suggestions, please use the [Issues](https://github.com/dbae1145/inteli_karoba/issues) page on the Github repository.
