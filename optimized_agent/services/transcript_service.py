from ..schemas import TranscriptEntry

class TranscriptService:

    @staticmethod
    def build_transcript(history):

        return [
            TranscriptEntry(
                question=item["question"],
                answer=item["answer"]
            )
            for item in history
        ]

    @staticmethod
    def keep_last_five(history):

        return history[-5:]