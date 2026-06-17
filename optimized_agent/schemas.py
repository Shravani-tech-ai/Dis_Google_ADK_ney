from pydantic import BaseModel
from typing import Literal, List, Optional


# =====================================================
# HTTP LAYER - API Contracts
# =====================================================

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    category: str
    conversation_summary: str


# =====================================================
# CONVERSATION HISTORY - Structured Transcript
# =====================================================

class TranscriptEntry(BaseModel):
    """Single conversation turn"""
    question: str
    answer: str


# =====================================================
# ROOT AGENT STATE - Input to workflow
# =====================================================

class RootAgentState(BaseModel):
    """State passed to the agent workflow"""
    question: str
    transcript: List[TranscriptEntry]


# =====================================================
# CONTEXT AGENT - Input/Output Contracts
# =====================================================

class ContextAgentInput(BaseModel):
    """Input to context_agent"""
    question: str
    transcript: List[TranscriptEntry]


class ContextAgentOutput(BaseModel):
    """Output from context_agent"""
    question: str
    category: Literal[
        "RESORT_INFO",
        "PARK_INFO",
        "RIDE_DISCOVERY",
        "DINING",
        "TRIP_PLANNING",
        "TICKETS_PRICING",
        "TRANSPORTATION",
        "WAIT_TIMES",
        "QUEUE_MGMT",
        "CHARACTER_EXP",
        "ENTERTAINMENT",
        "SHOPPING",
        "ACCESSIBILITY",
        "SEASONAL_EVENTS",
        "POLICIES"
    ]
    conversation_summary: str


# =====================================================
# ANSWER AGENT - Input/Output Contracts
# =====================================================

class AnswerAgentInput(BaseModel):
    context: ContextAgentOutput


class AnswerAgentOutput(BaseModel):
    """Output from answer_agent"""
    answer: str