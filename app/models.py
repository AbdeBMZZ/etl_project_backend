from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()

engine = create_engine('sqlite:///db.sqlite3', echo=True)
session = sessionmaker()


class CSVFile(Base):
    __tablename__ = 'csv_files'
    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    upload_date = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<CSVFile(name={self.name}, path={self.file_path})>"


class TransformationRule(Base):
    __tablename__ = 'transformation_rules'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    operation = Column(String(255))
    column = Column(String(255))
    operator = Column(String(255))
    value = Column(String(255))

    def __repr__(self):
        return f"<TransformationRule(name={self.rule_name}, rule={self.name})>"


class TransformedData(Base):
    __tablename__ = 'transformed_data'

    id = Column(Integer, primary_key=True)
    csv_file_id = Column(Integer, ForeignKey('csv_files.id'), nullable=False)
    rule_id = Column(Integer, ForeignKey('transformation_rules.id'), nullable=False)
    transformation_date = Column(DateTime, nullable=False, server_default=func.now())

    csv_file = relationship("CSVFile", backref="transformed_data")
    rule = relationship("TransformationRule", backref="transformed_data")

    def __repr__(self):
        return f"<TransformedData(csv_file={self.csv_file}, rule={self.rule})>"



Base.metadata.create_all(engine)