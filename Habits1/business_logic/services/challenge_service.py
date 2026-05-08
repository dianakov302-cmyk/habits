from Habits1.repositories.challenge_repository import PostRepository
from .interfaces import IChallengeService


class ChallengeService(IChallengeService):
    def __init__(self, challenge_repository: PostRepository):
        self.challenge_repository = challenge_repository

    def get_challenges(self):
        try:
            challenges = list(self.challenge_repository.collection.find())
            for challenge in challenges:
                challenge["_id"] = str(challenge["_id"])
            return challenges
        except Exception as e:
            print(f"Error fetching challenges: {e}")
            return []

    def create_challenge(self, title: str):
        try:
            result = self.challenge_repository.create({"title": title})
            return {"message": "Challenge created", "id": str(result.inserted_id)}
        except Exception as e:
            return {"error": f"Failed to create challenge: {str(e)}"}
