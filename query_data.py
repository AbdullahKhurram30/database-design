from sqlalchemy import func
from datetime import datetime
from create import Office, Agent, House, Sale, Commission
from insert_data import session

# Get the current month and year
current_month = datetime.now().month
current_year = datetime.now().year
def top_offices(month=current_month, year=current_year):
    '''
    Function to run the query to get the top 5 offices with the most sales for the current month
    '''
    # Query to get the offices with the most sales for the current month
    top_offices = session.query(Office, func.count(Sale.id).label('total_sales')).\
        join(Sale, Sale.office_id == Office.id).\
        filter(func.extract('month', Sale.date_sold) == month).\
        filter(func.extract('year', Sale.date_sold) == year).\
        group_by(Office.id).\
        order_by(func.count(Sale.id).desc()).\
        limit(5).all()
    # Print the top 5 offices with the most sales for the current month
    print("Top 5 Offices with the Most Sales for the Current Month:")
    for i, (office, total_sales) in enumerate(top_offices):
        print(f"{i+1}. Office Name: {office.name}, Total Sales: {total_sales}")

def top_agents(month=current_month, year=current_year):
    '''
    Function to run the query to get the top 5 estate agents who have sold the most for the current month
    '''
    # Query to get the estate agents who have sold the most for the current month
    top_agents = session.query(Agent, func.count(Sale.id).label('total_sales')).\
        join(Sale, Sale.agent_id == Agent.id).\
        filter(func.extract('month', Sale.date_sold) == month).\
        filter(func.extract('year', Sale.date_sold) == year).\
        group_by(Agent.id).\
        order_by(func.count(Sale.id).desc()).\
        limit(5).all()

    # Print the top 5 estate agents who have sold the most for the current month
    print("Top 5 Estate Agents with the Most Sales for the Current Month:")
    for i, (agent, total_sales) in enumerate(top_agents):
        print(f"{i+1}. Agent Name: {agent.name}, Phone: {agent.phone}, Email: {agent.email}, Total Sales: {total_sales}")

def get_commissions():
    '''
    Function to run the query to get the commissions for each agent. We only display the first 10 results
    '''
    # Query to get the commissions for each agent
    commissions = session.query(Commission, Agent.name, func.sum(Commission.amount).label('total_commission')).\
        join(Agent, Agent.id == Commission.agent_id).\
        group_by(Commission.agent_id).\
        order_by(func.sum(Commission.amount).desc()).all()

    # Print the commissions for each agent
    print("Commissions for Each Agent (Only first 10):")
    commissions = commissions[:10]
    for i, (commission, agent_name, total_commission) in enumerate(commissions):
        print(f"{i+1}. Agent Name: {agent_name}, Total Commission: {total_commission:.2f}")

def get_avg_days_on_market(month=current_month, year=current_year):
    # Query to calculate average number of days on the market for all houses sold that month
    avg_days_on_market = session.query(func.avg((Sale.date_sold - House.date_listed)).label('avg_years')).\
        join(House, House.id == Sale.house_id).\
        filter(func.extract('month', Sale.date_sold) == current_month).\
        filter(func.extract('year', Sale.date_sold) == current_year).\
        scalar()
    # Print the average number of days on the market for
    print(f"Average Number of Days on the Market for Houses Sold in the Current Month: {int(avg_days_on_market * 365)} days")

def get_avg_selling_price(month=current_month, year=current_year):
    # Query to calculate the average selling price for houses sold in the current month
    avg_selling_price = session.query(func.avg(Sale.price).label('avg_price')).\
        filter(func.extract('month', Sale.date_sold) == current_month).\
        filter(func.extract('year', Sale.date_sold) == current_year).\
        scalar()

    # Print the average selling price for houses sold in the current month
    print(f"Average Selling Price for Houses Sold in the Current Month: ${avg_selling_price:.2f}")

if __name__ == '__main__':
    top_offices()
    top_agents()
    get_commissions()
    get_avg_days_on_market()
    get_avg_selling_price()