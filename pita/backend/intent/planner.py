import logging
from typing import Dict, Any, List

logger = logging.getLogger("Lucy-Planner")

class ActionPlanner:
    """
    Translates parsed intents into a deterministic execution plan.
    Provides execution isolation.
    """
    def __init__(self):
        logger.info("Action Planner initialized.")

    def plan(self, intent_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Creates a list of atomic actions to perform.
        """
        intent = intent_data.get("intent")
        target = intent_data.get("target")
        
        logger.info(f"Planning for intent: {intent}")
        
        # In a more complex system, this would break down multi-step tasks
        if intent == "unknown":
            return []

        return [{
            "action": intent,
            "params": {"target": target},
            "validation_required": intent in ["delete_file", "system_shutdown"]
        }]
