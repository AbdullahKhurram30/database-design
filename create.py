from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create the database connection and connect to it
engine = create_engine('sqlite:///houses.db')

# Create the base class for the models
Base = declarative_base()

# Define the Office model
class Office(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(String(100))
    zipcode = Column(String(10))
    phone = Column(String(50))

# Define the Agent model
class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))

# Define the Agent-Office model
class AgentOffice(Base):
    __tablename__ = 'agent_office'
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    office_id = Column(Integer, ForeignKey('offices.id'))

# Define the Client model
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    address = Column(String(100))

# Define the House model
class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('clients.id'))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    listing_price = Column(Integer)
    zipcode = Column(Integer)
    date_listed = Column(DateTime)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    office_id = Column(Integer, ForeignKey('offices.id'))
    sold = Column(Boolean, default=False)

# Define the Buyer model
class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    address = Column(String(100))

# Define the Sales model
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    agent_id = Column(Integer, ForeignKey('agents.id'))
    office_id = Column(Integer, ForeignKey('offices.id'))
    price = Column(Integer)
    date_sold = Column(DateTime, index = True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'))

    @property
    # define the commission property for easy accessibility
    def commission(self):
        # if price below 100000, commission is 10%
        if self.price < 100000:
            return self.price * 0.1
        # if price is between 100000 and 200000, commission is 7.5%
        elif self.price >= 100000 and self.price < 200000:
            return self.price * 0.075
        # if price is between 200000 and 500000, commission is 6%
        elif self.price >= 200000 and self.price < 500000:
            return self.price * 0.06
        # if price is between 500000 and 1000000, commission is 5%
        elif self.price >= 500000 and self.price < 1000000:
            return self.price * 0.05
        # if price is above 1000000, commission is 4%
        else:
            return self.price * 0.04

class Commission(Base):
    __tablename__ = 'commissions'
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    sale_id = Column(Integer, ForeignKey('sales.id'))
    amount = Column(Float)
    sales = relationship(Sale)

# Create the tables in the database
Base.metadata.create_all(engine)