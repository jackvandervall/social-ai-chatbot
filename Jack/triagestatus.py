# # DEFINE STRUCTURED TRIAGE (classify topics/language/urgency as structured data for log/analysis)
# class TriageStatus(BaseModel):
#     """
#     Represents the urgency and categorization of a user's input.
#     Attributes:
#         is_emergency (bool): Indicates if the situation is life-threatening.
#         topic (str): The specific category of help needed.
#         language_detected (str): The ISO code of the detected language.
#     """
#     is_emergency: bool = Field(
#         False, description="Is this a life-threatening situation (911/112)?"
#     )
#     topic: str = Field(
#         ..., description="Category: 'shelter', 'medical', 'legal', 'food', 'other'"
#     )
#     language_detected: str = Field(
#         ..., description="Language code: nl, en, pl, ar"
#     )