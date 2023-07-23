from fastapi import FastAPI, Request, Depends, Form
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import models
from database import engine, sessionlocal

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", name="home")
async def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).order_by(models.Todo.id.desc())
    context = {
        "request": request,
        "todos": todos
    }
    return templates.TemplateResponse("index.html", context)


@app.post("/add")
async def add(request: Request, task: str = Form(...), db: Session = Depends(get_db)):
    todo = models.Todo(task=task)
    db.add(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{todo_id}")
async def add(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).one()
    context = {
        "request": request,
        "todo": todo
    }
    return templates.TemplateResponse("edit.html", context)


@app.post("/edit/{todo_id}")
async def add(request: Request, todo_id: int, task: str = Form(...), completed: bool = Form(False),
              db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).one()
    todo.task = task
    todo.completed = completed
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{todo_id}")
async def add(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).one()
    db.delete(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# from typing import Union, Optional
#
# from fastapi import FastAPI, Query, Path
# from pydantic import BaseModel
#
# app = FastAPI()
#
# products = []
#
#
# class Product(BaseModel):
#     id: int
#     name: str
#     description: str | None = None
#     price: float
#
#
# products.append(Product(id=1, name='Samsung Galaxy S2', description='Yangi tovar', price=250))
# products.append(Product(id=2, name='Iphone 6', description='Yangi tovar', price=350))
# products.append(Product(id=3, name='Iphone 6', description='Yangi tovar', price=450))
#
#
# @app.get("/items/{item_id}")
# async def read_items(
#         item_id: int = Path(title="The ID of the item to get"),
#         q: str | None = Query(default=None, alias="item-query"),
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# @app.get('/products')
# async def get_all_products(price: int | None = Query(default=None, lt=500)):
#     if price:
#         return list(filter(lambda x: x.price > price, products))
#     return products
#
#
# @app.post('/products')
# async def create_product(product: Product):
#     products.append(product)
#     return {'message': 'Product created successfully'}
#
#
# @app.put('/product/{pk}')
# async def update_product(pk: int, product: Product):
#     for i in products:
#         if i.id == pk:
#             i.name = product.name
#             i.description = product.description
#             i.price = product.price
#             return {'message': 'Product updated successfully'}
#
#     return {'message': 'Not Found'}
#
#
# @app.delete('/product/{pk}')
# async def delete_product(pk: int):
#     for i in products:
#         if i.id == pk:
#             products.remove(i)
#             return {'message': 'Product deleted successfully'}
#
#     return {'message': 'Not Found'}
