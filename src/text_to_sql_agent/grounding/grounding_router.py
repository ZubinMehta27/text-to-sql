from text_to_sql_agent.grounding.intent_rules import requires_sql

def routing_node():
    def _node(state):
        if requires_sql(state.user_query):
            state.execution_mode = "SQL_REQUIRED"
        else:
            state.execution_mode = "NON_SQL_RESPONSE"

        return state

    return _node
