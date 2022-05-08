from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


engine=create_engine('postgresql://qppuncsd:xMtzzO_o_e_PTcGCYekzFHzH4mPyfEOL@castor.db.elephantsql.com/qppuncsd', echo=True)
Base=declarative_base()

Session=sessionmaker(bind=engine)
