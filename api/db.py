from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, DateTime, func
from config import Config
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()  # 建立 sql rom基类
Session = sessionmaker(bind=engine)

class SecondDomain(Base):  # 二级域名
    # 指定映射表名
    __tablename__ = 'SecondDomain'
    
    # ID设置为主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    second_domain = Column(String(100), unique=True)
    sub_domain_num = Column(Integer)
    ctime = Column(DateTime, server_default=func.now())
    
    def insert_domain(self, domain_nm):
        pass
    
    def query_domain(self, domain_nm):
        DBSession = Session()
        result = DBSession.query(self).filter_by(second_domain=domain_nm).one()
        return result
        
class ThirdDomain(Base):  # 三级域名
    # 指定映射表名
    __tablename__ = 'ThirdDomain'
    
    # ID设置为主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    third_domain = Column(String(200), unique=True)
    sub_domain_num = Column(String(200))
    ctime = Column(DateTime, server_default=func.now())
    
class secondDomainScheme:
    def __init__(self) -> None:
        pass
    
    # 添加记录
    def insert_domain(self, second_domain, sub_domain_num=1):
        DBSession = Session()
        try:
            result = DBSession.add(SecondDomain(
                second_domain=second_domain,
                sub_domain_num=sub_domain_num
            ))
            print(f'添加二级域名 <{second_domain}> SUCCESS!')
        except:
            DBSession.close()
            print(f'添加二级域名 <{second_domain}> Fail!')
        DBSession.commit()
        DBSession.close()
        return result
    
    # 删除记录
    def delete_domain(self, second_domain):
        DBSession = Session()
        try:
            result = DBSession.query(SecondDomain).filter(SecondDomain.second_domain==second_domain).delete()
            print(f'删除二级域名 <{second_domain}> SUCCESS!')
        except:
            DBSession.close()
            print(f'删除二级域名 <{second_domain}> Fail!')
        DBSession.commit()
        DBSession.close()
        return result
    
    # 更新记录
    def update_subdomain_num(self, second_domain, sub_domain_num):
        DBSession = Session()
        try:
            rows_changed = DBSession.query(SecondDomain).filter_by(second_domain=second_domain).update(
                dict(sub_domain_num = sub_domain_num)
            )
            if rows_changed:
                print(f'更改二级域名 <{second_domain}> 数量为 [{sub_domain_num}]!')
            else:
                print(f'未发现二级域名 <{second_domain}> !')
        except:
            DBSession.close()
            print(f'更改二级域名 <{second_domain}> 数量 Fail!')
        DBSession.commit()
        DBSession.close()
        return rows_changed
            
    # 查询记录
    def query_record(self, second_domain):
        DBSession = Session()
        try:
            result = DBSession.query(SecondDomain).filter_by(second_domain=second_domain).one()
            print(f'查询到二级域名 <{second_domain}> [{result}]!')
        except:
            DBSession.close()
            result = None
            print(f'未查询到二级域名 <{second_domain}> !')
        DBSession.commit()
        DBSession.close()
        return result
    
if __name__ == '__main__':
    # 清空表
    # 创建表
    Base.metadata.create_all(engine)
    # result = DBSession.query(SecondDomain).filter_by(second_domain='www.baidu.com').one()
    sec_op = secondDomainScheme()
    # TEST
    # Add
    # result = sec_op.insert_domain(second_domain='google.com')
    # Delete
    # result = sec_op.delete_domain(second_domain='google.com')
    # Update
    # result = sec_op.update_subdomain_num(second_domain='baidu.com', sub_domain_num=1)
    # Query
    result = sec_op.query_record(second_domain='baidu.com')
    print(result)
    