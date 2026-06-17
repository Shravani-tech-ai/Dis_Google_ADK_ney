from fastapi import FastAPI
from google.genai.types import Content
from google.genai.types import Part
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from optimized_agent.agent import root_agent
from optimized_agent.schemas import (ChatRequest, ChatResponse, TranscriptEntry)
from optimized_agent.services.debug_logger import DebugLogger
from optimized_agent.services.transcript_service import TranscriptService
from optimized_agent.session_store import SESSIONS

app = FastAPI()

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="disney_app",
    session_service=session_service
)

@app.post("/disney_assistant", response_model=ChatResponse)

async def chat(req: ChatRequest):

    try:

        # ==================================================
        # SESSION HISTORY
        # ==================================================

        if req.session_id not in SESSIONS:
            SESSIONS[req.session_id] = []

        history = SESSIONS[req.session_id]

        transcript_entries = (
            TranscriptService.build_transcript(history)
        )

        # ==================================================
        # SESSION
        # ==================================================

        session = await session_service.get_session(
            app_name="disney_app",
            user_id=req.user_id,
            session_id=req.session_id
        )

        if session is None:

            session = await session_service.create_session(
                app_name="disney_app",
                user_id=req.user_id,
                session_id=req.session_id,
                state={
                    "question": req.message,
                    "transcript": [
                        item.model_dump()
                        for item in transcript_entries
                    ]
                }
            )

        else:

            session.state["question"] = req.message

            session.state["transcript"] = [
                item.model_dump()
                for item in transcript_entries
            ]

        # ==================================================
        # CAPTURED DATA
        # ==================================================

        context_input_json = {
            "question": req.message,
            "transcript": [
                item.model_dump()
                for item in transcript_entries
            ]
        }

        context_output_json = {}

        answer_input_json = {}

        answer_output_json = {}

        final_answer = ""

        generated_category = ""

        generated_summary = ""

        # ==================================================
        # RUN WORKFLOW
        # ==================================================

        async for event in runner.run_async(
            user_id=req.user_id,
            session_id=req.session_id,
            new_message=Content(
                role="user",
                parts=[
                    Part(text=req.message)
                ]
            )
        ):

            print("\nEVENT")
            print(event)

            if (
                hasattr(event, "actions")
                and event.actions
                and hasattr(event.actions, "state_delta")
                and event.actions.state_delta
            ):

                state_delta = event.actions.state_delta

                # ==========================================
                # CONTEXT AGENT OUTPUT
                # ==========================================

                context = state_delta.get("context")

                if context:

                    if hasattr(context, "model_dump"):
                        context_output_json = context.model_dump()

                    elif isinstance(context, dict):
                        context_output_json = context

                    generated_category = (
                        context_output_json.get(
                            "category",
                            ""
                        )
                    )

                    generated_summary = (
                        context_output_json.get(
                            "conversation_summary",
                            ""
                        )
                    )

                    answer_input_json = {
                        "context": context_output_json
                    }

                # ==========================================
                # ANSWER AGENT OUTPUT
                # ==========================================

                answer_result = state_delta.get(
                    "answer_result"
                )

                if answer_result:

                    if hasattr(answer_result, "model_dump"):

                        answer_output_json = (
                            answer_result.model_dump()
                        )

                    elif isinstance(
                        answer_result,
                        dict
                    ):

                        answer_output_json = answer_result

                    final_answer = (
                        answer_output_json.get(
                            "answer",
                            ""
                        )
                    )

        # ==================================================
        # SAVE HISTORY
        # ==================================================

        history.append(
            {
                "question": req.message,
                "answer": final_answer
            }
        )

        SESSIONS[req.session_id] = history[-5:]

        # ==================================================
        # DEBUG LOGGING
        # ==================================================

        # ==================================================
        # DEBUG LOGGING
        # ==================================================

        DebugLogger.write_log(
            {
                "session_id": req.session_id,
                "user_id": req.user_id,

                "request": {
                    "message": req.message
                },

                "context_agent": {
                    "input": context_input_json,
                    "output": context_output_json
                },

                "answer_agent": {
                    "input": answer_input_json,
                    "output": answer_output_json
                },

                "response": {
                    "answer": final_answer,
                    "category": generated_category,
                    "conversation_summary": generated_summary
                },

                "history": SESSIONS[req.session_id]
            }
        )

        # ==================================================
        # RESPONSE
        # ==================================================

        return ChatResponse(
            answer=final_answer,
            category=generated_category,
            conversation_summary=generated_summary
        )

    except Exception as e:

        print("ERROR:", str(e))

        raise