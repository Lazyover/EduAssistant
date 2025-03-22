from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, Role, UserRole
from app.react.tools_register import register_as_tool

class UserService:
    """用户服务类，处理用户认证、注册和用户管理。
    
    该服务提供用户账户相关的所有功能，包括创建用户、验证用户凭证、
    用户角色分配和管理等操作。
    """
    
    def create_user(self, username, email, password, name, role_names=None):
        """创建新用户。
        
        Args:
            username (str): 用户名
            email (str): 电子邮件地址
            password (str): 用户密码
            name (str): 用户真实姓名
            role_names (list): 角色名称列表，默认为None
            
        Returns:
            User: 创建的用户对象
            
        Raises:
            ValueError: 如果用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        if User.select().where(User.username == username).exists():
            raise ValueError(f"用户名 '{username}' 已存在")
        
        # 检查邮箱是否已存在
        if User.select().where(User.email == email).exists():
            raise ValueError(f"邮箱 '{email}' 已被注册")
        
        # 创建用户
        user = User.create(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            name=name
        )
        
        # 分配角色
        if role_names:
            for role_name in role_names:
                role = Role.get_or_none(Role.name == role_name)
                if role:
                    UserRole.create(user=user, role=role)
        
        return user
    
    def authenticate_user(self, username, password):
        """验证用户凭证。
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            User or None: 如果验证成功返回用户对象，否则返回None
        """
        user = User.get_or_none(User.username == username, User.is_active == True)
        
        if user is not None and check_password_hash(user.password_hash, password):
            return user
            
        return None
    
    def get_user_roles(self, user):
        """获取用户角色列表。
        
        Args:
            user (User): 用户对象
            
        Returns:
            list: 用户角色对象列表
        """
        return [ur.role for ur in user.roles]
    
    def has_role(self, user, role_name):
        """检查用户是否拥有指定角色。
        
        Args:
            user (User): 用户对象
            role_name (str): 角色名称
            
        Returns:
            bool: 如果用户拥有指定角色则返回True，否则返回False
        """
        return UserRole.select().join(Role).where(
            (UserRole.user == user) & (Role.name == role_name)
        ).exists()

