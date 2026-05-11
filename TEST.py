from src.agent.graph import graph

initial_state = {

    "dataset_path": r"C:\WOLF\Private\VS_CODE\self_improving_ai_agent\data\datasets\titanic.csv"
}


config = {

    "configurable": {

        "thread_id": "titanic_session"
    }
}


result = graph.invoke(

    initial_state,

    config=config
)


print("\nFINAL RESULT:\n")
print(result)