from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, DateTime, func
from config import Config
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from traceback import print_exc


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
        
class ThirdDomain(Base):  # 三级域名
    # 指定映射表名
    __tablename__ = 'ThirdDomain'
    
    # ID设置为主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    third_domain = Column(String(200), unique=True)
    sub_domain_num = Column(String(200))
    second_domain_id = Column(Integer, ForeignKey('SecondDomain.id'))
    second_domain = relationship('SecondDomain') # 声明与SecondDomain表的关系，可选，用于方便查询时的联结操作
    ctime = Column(DateTime, server_default=func.now())
    
class secondDomainScheme:  # 二级域名方法
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
    
    def query_three_level_dn_num(self, query_id):
        DBSession = Session()
        try:
            result = DBSession.query(ThirdDomain).filter_by(second_domain_id=query_id).all()
            print(len(result))
            print(f'查询到三级域名数量[{len(result)}]!')
        except:
            DBSession.close()
            result = None
            print(f'未查询到二级域名子域名!')
        DBSession.commit()
        DBSession.close()
        return len(result)
    
    def get_id_by_sec_dname(self, second_domain):
        DBSession = Session()
        try:
            result = DBSession.query(SecondDomain).filter_by(second_domain=second_domain).one()
            result_id = result.id
            print(f'查询到二级域名 <{second_domain}> id:[{result_id}]!')
        except:
            DBSession.close()
            result_id = None
            print(f'未查询到二级域名 <{second_domain}> !')
        DBSession.commit()
        DBSession.close()
        return result_id
        
class thirdDomainScheme:  # 二级域名方法
    def __init__(self) -> None:
        pass
    
    # 添加记录
    def insert_domain(self, third_domain, sub_domain_num=1):
        DBSession = Session()
        second_domain = '.'.join([third_domain.split('.')[-2], third_domain.split('.')[-1]])
        # 查询三级域名的ID
        second_domain = DBSession.query(SecondDomain).filter_by(second_domain=second_domain).one()
        second_domain_id = second_domain.id
        try:
            result = DBSession.add(ThirdDomain(
                third_domain=third_domain,
                sub_domain_num=sub_domain_num,
                second_domain_id=second_domain_id
            ))
            print(f'添加三级域名 <{third_domain}> SUCCESS!')
        except:
            DBSession.close()
            print(f'添加三级域名 <{third_domain}> Fail!')
            print_exc()
            result = None
        DBSession.commit()
        DBSession.close()
        return result
    
    # 删除记录
    def delete_domain(self, third_domain):
        DBSession = Session()
        try:
            result = DBSession.query(ThirdDomain).filter(ThirdDomain.third_domain==third_domain).delete()
            print(f'删除三级域名 <{third_domain}> SUCCESS!')
        except:
            DBSession.close()
            print(f'删除三级域名 <{third_domain}> Fail!')
        DBSession.commit()
        DBSession.close()
        return result
    
    # 更新记录
    def update_subdomain_num(self, third_domain, sub_domain_num):
        DBSession = Session()
        try:
            rows_changed = DBSession.query(ThirdDomain).filter_by(third_domain=third_domain).update(
                dict(sub_domain_num = sub_domain_num)
            )
            if rows_changed:
                print(f'更改三级域名 <{third_domain}> 数量为 [{sub_domain_num}]!')
            else:
                print(f'未发现三级域名 <{third_domain}> !')
        except:
            DBSession.close()
            print(f'更改三级域名 <{third_domain}> 数量 Fail!')
        DBSession.commit()
        DBSession.close()
        return rows_changed
            
    # 查询记录
    def query_record(self, third_domain):
        DBSession = Session()
        try:
            result = DBSession.query(ThirdDomain).filter_by(third_domain=third_domain).one()
            print(f'查询到三级域名 <{third_domain}> [{result}]!')
        except:
            DBSession.close()
            result = None
            print(f'未查询到三级域名 <{third_domain}> !')
        DBSession.commit()
        DBSession.close()
        return result
    
    
if __name__ == '__main__':
    # 清空表
    # 创建表
    Base.metadata.create_all(engine)
    # result = DBSession.query(SecondDomain).filter_by(second_domain='www.baidu.com').one()
    
    # 测试二级域名 func
    sec_op = secondDomainScheme()
    
    # 测试三级域名 func 
    # sec_op = thirdDomainScheme()
    
    # TEST
    # Add
    # result = sec_op.insert_domain(second_domain='google.com')
    # result = sec_op.insert_domain(third_domain='tieba.baidu.com')
    
    # Delete
    # result = sec_op.delete_domain(second_domain='google.com')
    # Update
    # result = sec_op.update_subdomain_num(second_domain='baidu.com', sub_domain_num=1)
    # Query
    # result = sec_op.query_record(second_domain='baidu.com')
    # result = sec_op.query_record(third_domain='tiebabaidu.com')
    result = sec_op.get_id_by_sec_dname(second_domain='baidu.com')
    
    # 查询三级域名数量
    # result = sec_op.query_three_level_dn_num(query_id=1)
    print(result)
