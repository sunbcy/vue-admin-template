from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, DateTime, func
from config import Config
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()  # 建立 sql rom基类

class SecondDomain(Base):  # 二级域名
    # 指定映射表名
    __tablename__ = 'SecondDomain'
    
    # ID设置为主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    second_domain = Column(String(100))
    sub_domain_num = Column(String(100))
    ctime = Column(DateTime, server_default=func.now())
    
class ThirdDomain(Base):  # 三级域名
    # 指定映射表名
    __tablename__ = 'ThirdDomain'
    
    # ID设置为主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    third_domain = Column(String(200))
    sub_domain_num = Column(String(200))
    ctime = Column(DateTime, server_default=func.now())
    

    
if __name__ == '__main__':
    # 创建表
    Base.metadata.create_all(engine)