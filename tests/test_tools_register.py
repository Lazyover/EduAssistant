from app.react.tools_register import initialize_services, tools
from app import create_app
app = create_app()

print(tools)
print(tools['get_student_knowledge_mastery']['function'](
    {
        "student_id": 7,
    }
))