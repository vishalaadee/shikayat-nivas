from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


engine=create_engine('postgres://qppuncsd:xMtzzO_o_e_PTcGCYekzFHzH4mPyfEOL@castor.db.elephantsql.com/qppuncsd', echo=True)
#engine=create_engine('postgresql://duztlwzobnbxfs:baf4b29105ef08142616f9850af5320feea80e04c175f30f7bb6bf9d8f5e3290@ec2-34-194-25-190.compute-1.amazonaws.com:5432/d7hrsrflefo7ok', echo=True)
Base=declarative_base()

Session=sessionmaker(bind=engine)
