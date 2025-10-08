from fastapi import APIRouter
from service.service import User,Portfolio,Resources

router = APIRouter()

@router.get("/user")
def get_user(id: int):
    user = User.fetch_by_id(id)
    if user:
        return {
            "id": user["id"],
            "name": user["name"],
            "age": user["age"],
            "gender": user["gender"]
        }
    return {"error": "User not found"}

@router.get("/portfolio")
def get_portfolio(id: int):
    portfolio = Portfolio.fetch_by_portfolio_id(id)
    if portfolio:
        return {
            "total_money": portfolio["total_money"],
            "invested": portfolio["invested"],
            "isa_life_time": portfolio["isa_life_time"],
            "pension": portfolio["pension"],
            "cash_isa": portfolio["cash_isa"],
            "stocks": portfolio["stocks"],
            "GIA": portfolio["GIA"],
            "balance": portfolio["balance"]
        }
    return {"error": "Portfolio not found for user"}

@router.get("/resource_categories")
def get_resource_categories():
    return Resources.fetch_categories()

@router.get("/resources")
def get_resources(category: str):
    return Resources.fetch_by_category(category)
