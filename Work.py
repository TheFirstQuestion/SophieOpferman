from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Work(Base):
    __tablename__ = 'Work'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    description = Column(String)
    category = Column(String)
    subcategory = Column(String)
    status = Column(String)
    updated = Column(DateTime)
    demoLink = Column(String)


    # For nice printing
    def __repr__(self):
        return "Test()"
    def __str__(self):
        return ("===============\n" + self.name + "\n" + self.link + "\n" + self.desc + "\n" + self.cat + "\n" +self.subcat + "\n===============")


# Testing
if __name__ == "__main__":
    engine = create_engine('sqlite:///test.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    s=session()

    s.add(InfoBox(name="Test Entry", desc="Description goes here", link="linklinklink", cat="testCat", subcat="sub cat"))
    s.commit()
    s.close()
