tools_todo = [
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "קבלת רשימת כל המשימות",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "הוספת משימה חדשה",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "כותרת המשימה"
                    },
                    "description": {
                        "type": "string",
                        "description": "תיאור המשימה"
                    }
                },
                "required": ["title"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "עדכון משימה קיימת",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "מזהה המשימה"
                    },
                    "title": {
                        "type": "string",
                        "description": "כותרת חדשה למשימה"
                    },
                    "description": {
                        "type": "string",
                        "description": "תיאור חדש למשימה"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "האם המשימה הושלמה"
                    }
                },
                "required": ["task_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "מחיקת משימה",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "מזהה המשימה למחיקה"
                    }
                },
                "required": ["task_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
