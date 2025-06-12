from app.pipelines.qa_pipeline import ask_question

def main():
    print("\n🧠 Slack/JIRA/Confluence Q&A Chat\nType 'exit' to quit.\n")
    while True:
        query = input("You: ")
        if query.strip().lower() in ["exit", "quit"]:
            break
        try:
            answer = ask_question(query)
            print(f"Bot: {answer}\n")
        except Exception as e:
            print(f"[Error] {e}\n")

if __name__ == "__main__":
    main()
