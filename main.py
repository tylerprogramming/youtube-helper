import streamlit as st
import autogen
import json
import random
from tavily import TavilyClient
tavily = TavilyClient(api_key="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")

st.title("YouTube")

tab1, tab2 = st.tabs(["Quizzes", "Information Posts"])


def main():
    with tab1:
        cache = st.checkbox("Different Questions?")
        if st.button("Generate MCQ"):
            # If you have created an OAI_CONFIG_LIST.json file in the current working directory, that file will be used.
            config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

            # Create the agent that uses the LLM.
            assistant = autogen.AssistantAgent(
                "assistant",
                system_message="You are a helpful assistant.  Return 'TERMINATE' when the task is done.",
                llm_config={
                    "config_list": config_list,
                    "cache_seed": None if cache else 41
                }
            )

            # Create the agent that represents the user in the conversation.
            user_proxy = autogen.UserProxyAgent(
                "user_proxy",
                human_input_mode="NEVER",
                is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
                code_execution_config={
                    "work_dir": "coding",
                    "use_docker": False
                }
            )

            chat_result = user_proxy.initiate_chat(
                assistant,
                message="""
                    I want you to create an MCQ about Python.  It is for intermediate level developers.  The topics can include
                    data structures, syntax with Python, best code practices, dictionaries, lists, and other various topics
                    that are Python specific.  If the question contains code, put it in the correct json property 
                    below, but if not, then leave the code property blank.
                    
                    Only give me 1 MCQ, and do not code anything.  Along with that, please give me a very detailed reason
                    for the correct answer.  Make sure the reason is under 450 characters in length.  The response should 
                    be in JSON format like the example below:
                    
                    The MCQ should be formatted in JSON in the following format:
                    {
                        "question": The question,
                        "code": code,
                        "correct_answer": correct answer,
                        "first_incorrect_answer": first incorrect answer,
                        "second_incorrect_answer": second incorrect answer,
                        "third_incorrect_answer": third incorrect answer
                        "reason": reason
                    }
                """,
                max_turns=1
            )

            my_dict = json.loads(chat_result.summary)
            question = my_dict.get('question')
            code = my_dict.get('code')
            correct_answer = my_dict.get('correct_answer')
            first_incorrect_answer = my_dict.get('first_incorrect_answer')
            second_incorrect_answer = my_dict.get('second_incorrect_answer')
            third_incorrect_answer = my_dict.get('third_incorrect_answer')
            reason = my_dict.get('reason')

            answers = [correct_answer, first_incorrect_answer, second_incorrect_answer, third_incorrect_answer]
            random.shuffle(answers)

            st.write("The question:")
            with st.container(border=True):
                st.subheader(question)
                if code:
                    st.code(code)

            st.divider()

            # Create two columns for displaying the answer choices
            col1, col2 = st.columns(2)

            # Display answers in two columns
            with col1:
                st.info(f"1. {answers[0]}")
                st.info(f"3. {answers[2]}")
            with col2:
                st.info(f"2. {answers[1]}")
                st.info(f"4. {answers[3]}")

            st.subheader("The correct answer and reason:")
            st.success(correct_answer)
            st.error(reason)

    with tab2:
        if st.button("Find content"):

            # You can easily get search result context based on any max tokens straight into your RAG.
            # The response is a string of the context within the max_token limit.
            # tavily.get_search_context(query="What happened in the burning man floods?", search_depth="advanced",
            #                           max_tokens=1500)

            response = tavily.search(query="Should I invest in Apple in 2024?", search_depth="advanced")

            # Get the search results as context to pass an LLM:
            context = [{"url": obj["url"], "content": obj["content"]} for obj in response.get('results')]

            config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

            # Create the agent that uses the LLM.
            assistant = autogen.AssistantAgent(
                "assistant",
                system_message="You are a helpful assistant.  Return 'TERMINATE' when the task is done.",
                llm_config={
                    "config_list": config_list,
                    "cache_seed": None if cache else 41
                }
            )

            # Create the agent that represents the user in the conversation.
            user_proxy = autogen.UserProxyAgent(
                "user_proxy",
                human_input_mode="NEVER",
                is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
                code_execution_config=False
            )

            chat_resultz = user_proxy.initiate_chat(
                assistant,
                message=f"""
                                Take the urls and content from this context: {context}.  I want you to make each content 
                                shortened to less than 300 characters and at the end of each shortened content add the 
                                Read More with hyperlink from the url with the content.  
                                
                                Please put it in json array format:
                                {{
                                    
                                        "url": the url
                                        "content": the content for the url above
                                    
                                }}
                                
                                Wrap all the json in this format in an array and return the response.  Don't put it
                            """,
                max_turns=1
            )

            print(chat_resultz)
            my_dict = json.loads(chat_resultz.summary)

            st.write(my_dict)

            # summary = json.loads(chat_resultz.summary)
            # st.write(summary)


if __name__ == "__main__":
    main()
