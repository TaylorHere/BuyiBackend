# coding: utf-8
import sys
sys.path.append('..')

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from model.init_data import init_data


engine = create_engine(
    'sqlite:///buyi.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db(test_data=False):
    import Association_specie_order
    import Association_market_pedlar
    import Association_specie_supplier
    import Association_supplier_market
    import Login
    import Market
    import Order
    import Pedlar
    import Permission
    import Specie
    import Supplier
    import User

    Base.metadata.create_all(bind=engine)
    if test_data:
        init_data(db_session)
