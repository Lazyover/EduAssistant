
from app import create_app

app = create_app()


from werkzeug.security import generate_password_hash
from app.models.user import User, Role, UserRole
from app.models.base import db

def main():
    # 教师用户信息
    teacher_info = {
        "username": "MR. Cao",
        "email": "teacher@example.com", 
        "password": "123456",
        "name": "CaoLH"
    }

    # 连接数据库
    db.connect()

    try:
        # 1. 确保教师角色存在
        teacher_role = Role.get(Role.name=="teacher")
        
        
        # 2. 创建用户
        password_hash = generate_password_hash(teacher_info["password"])
        
        user, user_created = User.get_or_create(
            username=teacher_info["username"],
            defaults={
                "email": teacher_info["email"],
                "password_hash": password_hash,
                "name": teacher_info["name"],
                "is_active": True
            }
        )
        
        if user_created:
            print(f"已创建教师用户: {teacher_info['name']} ({teacher_info['username']})")
        else:
            print(f"教师用户 {teacher_info['username']} 已存在")
            
        # 3. 确保用户具有教师角色
        user_role, ur_created = UserRole.get_or_create(
            user=user,
            role=teacher_role
        )
        
        if ur_created:
            print(f"已为用户分配教师角色")
        else:
            print(f"用户已具有教师角色")
        
    except Exception as e:
        print(f"创建教师用户时出错: {str(e)}")

    finally:
        # 关闭数据库连接
        if not db.is_closed():
            db.close()

if __name__ == "__main__":
    main()