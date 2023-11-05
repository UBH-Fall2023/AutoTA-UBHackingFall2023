import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import markdown
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import json
import numpy as np
from IPython.display import display, HTML


class TextPreprocessor():
    def __init__(self, corpus_folders_path: str='./openai-api-testing/data/'):
        # Download NLTK Data (if not already downloaded)
        nltk.download('stopwords')
        nltk.download('punkt')

        # Get all filepaths in corpus
        self.all_files_paths = []
        for folder in os.listdir(corpus_folders_path):
            for filepath in os.listdir(os.path.join(corpus_folders_path, folder)):
                self.all_files_paths.append(os.path.join(corpus_folders_path, folder, filepath))

        # Load and preprocess text files
        self.preprocessed_texts = []
        for filepath in self.all_files_paths:
            with open(filepath, 'r', encoding='utf-8') as f:
                corpus_text = f.read()
                corpus_tokens = word_tokenize(corpus_text)
                self.stop_words = set(stopwords.words('english'))
                filtered_corpus_tokens = [w for w in corpus_tokens if w not in self.stop_words]
                self.ps = PorterStemmer()
                stemmed_corpus_tokens = [self.ps.stem(w) for w in filtered_corpus_tokens]
                self.preprocessed_texts.append(' '.join(stemmed_corpus_tokens))

        self.vectorizer = TfidfVectorizer()
        self.corpus_tfidf_matrixes = self.vectorizer.fit_transform(self.preprocessed_texts)

        print("\nLoaded and preprocessed all text files in corpus.\n")

    def get_all_similarities(self, user_input: str):
        # Preprocess user input
        tokens = word_tokenize(user_input)
        filtered_tokens = [w for w in tokens if w not in self.stop_words]
        stemmed_tokens = [self.ps.stem(w) for w in filtered_tokens]
        preprocessed_input = ' '.join(stemmed_tokens)
        user_vector = self.vectorizer.transform([preprocessed_input])

        # Compute cosine similarity between user input and each document in corpus
        similarities = cosine_similarity(user_vector, self.corpus_tfidf_matrixes)
        return similarities
    
    def get_top_similarities(self, user_input: str, percentage_of_similarity_represented=0.10):
        similarities = self.get_all_similarities(user_input)
        most_similar_docs_indexes = similarities.argsort()[0][-int(len(similarities[0]) * percentage_of_similarity_represented):][::-1]
        return most_similar_docs_indexes
    
    def get_filepaths_of_relevent_docs(self, user_input: str, percentage_of_similarity_represented=0.10):
        top_similarities = self.get_top_similarities(user_input, percentage_of_similarity_represented)
        filepaths_of_relevent_docs = [self.all_files_paths[i] for i in top_similarities]
        return filepaths_of_relevent_docs
    

class AutoTA():
    def __init__(self, api_key_path: str, corpus_folders_path: str):
        # Set OpenAI API Key
        print(os.getcwd())
        openai.api_key = open(api_key_path, "r").readline().strip()

        # Load and preprocess text files
        self.text_preprocessor = TextPreprocessor(corpus_folders_path)
        self.all_files_paths = self.text_preprocessor.all_files_paths

        self.start_system_msg = """You are a Socratic teaching assistant in a large university for freshman computer science courses. You are passionate about academic integrity and want students to do their own work. Use the following principles in responding to students:
            - Never think on behalf of the student. Do not be too helpful. 
            - NEVER generate code for the student. 
            - NEVER help the student debug their code. You should not explain to the student how a block of code that they have gave you works. 
            - NEVER discuss explicit implementation details with the student. Instead explain concepts and expectations. 
            - NEVER fix a student's code for them. Instead ask them thought provoking questions to point them to where their errors might be. 
            - Ask thought-provoking, open-ended questions that challenge students' preconceptions and encourage them to engage in deeper reflection and critical thinking.
            - Actively listen to students' responses, paying careful attention to their underlying thought processes and making a genuine effort to understand their thinking process.
            - Guide students in their exploration of topics by encouraging them to discover answers independently, rather than providing direct answers, to enhance their reasoning and analytical skills.
            - Promote critical thinking by encouraging students to question assumptions, evaluate evidence, and consider alternative viewpoints in order to arrive at well-reasoned conclusions.
            - Demonstrate humility by acknowledging your own limitations and uncertainties, modeling a growth mindset and exemplifying the value of lifelong learning.
            - Keep you answers short and terse. Do not provide answers longer than two paragraphs. Whenever possible it is better to give a student a reference for where they should look to find an answer rather than giving them the answer directly. 
            - Your answers should be very simple and rudimentary as you will be conversing with students with little to no domain knowledge of the material they are learning. 
            - You may only include code snippets without modification if that code is directly given to you in this prompt.
            If you believe that the student is trying to get too much help from you, decline to respond so that the student does not receive an academic integrity violation. If you are unsure of whether a student's question is appropriate or not, decline to respond to stay safe and ask them to re-word their question.
            
            Remember that we are trying to help the student as a good teaching assistant would without giving them the answer to their question. Instead ask questions and lead them to information that will help them answer their own question. If you answered the users question, please regenerate your response to instead lead them to answer the question on their own."""
        
        self.previous_messages = []
        
    def get_filepaths_of_relevent_docs(self, user_input: str, percentage_of_similarity_represented=0.10):
        filepaths_of_relevent_docs = self.text_preprocessor.get_filepaths_of_relevent_docs(user_input, percentage_of_similarity_represented)
        return filepaths_of_relevent_docs

    # Define a function to generate the answer to the user's question
    def get_chatgpt_responce(self, user_input: str):
        final_system_content = self.start_system_msg + "\n\n"

        # Add relevent docs to system response
        filepaths_of_relevent_docs = self.get_filepaths_of_relevent_docs(user_input=user_input)

        for filepath in filepaths_of_relevent_docs:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                final_system_content += f"{filepath}:\n{text}\n\n\n"

        final_user_content = user_input

        # Remove Excess Whitespace and Newlines
        final_system_content = ' '.join(final_system_content.split())
        final_user_content = ' '.join(final_user_content.split())

        # Add previous messages to system response if they exist
        messages=[
                {"role": "system", "content": final_system_content},
        ]
        
        if len(self.previous_messages) != 0:
            for message in self.previous_messages:
                messages.append(message)

        messages.append({"role": "user", "content": final_user_content})


        completion = openai.ChatCompletion.create(model="gpt-4", messages=messages)

        self.previous_messages = messages[1:]
        self.previous_messages.append(dict(completion["choices"][0]["message"]))

        return completion, filepaths_of_relevent_docs

    def ask(self, user_input: str):
        self.previous_messages = []
        completion, filepaths_of_relevent_docs = self.get_chatgpt_responce(user_input=user_input)

        # Convert Markdown to HTML
        markdown_text = completion["choices"][0]["message"]["content"]
        html = markdown.markdown(markdown_text)
        
        return html, user_input, filepaths_of_relevent_docs, completion["usage"]["total_tokens"]

    def follow_up(self, user_input: str):
        completion, filepaths_of_relevent_docs = self.get_chatgpt_responce(user_input=user_input)

        # Convert Markdown to HTML
        markdown_text = completion["choices"][0]["message"]["content"]

        return markdown_text, user_input, filepaths_of_relevent_docs, completion["usage"]["total_tokens"]
        


if __name__ == "__main__":
    AutoTA = AutoTA(api_key_path="./openai-api-testing/OPENAI_API_KEY.txt")

    AutoTA.ask("What are pointers in C?")
    AutoTA.follow_up("How do i create a two dimensional array?")
