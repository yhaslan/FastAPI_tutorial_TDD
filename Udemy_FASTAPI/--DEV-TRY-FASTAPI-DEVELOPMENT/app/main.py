import logging  # this is to access to basic logging functioanlity
import logging.config  # this is to specifically configure our logging system

from fastapi import FastAPI

from app.routers import category_routes

# using an external configuration file; in this case logging.conf


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
# setting the latter to false can be useful when you need to extend
# or modify or dynamically update an existing logging conf w/o disturbing the
# current logging hierarchy or conf

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(category_routes.router, prefix="/api/category", tags=["categories"])


"""# Define a test endpoint


@app.get("/test")
async def test_endpoint():
    try:
        # simulate an error by dividing to zero
        result = 1 / 0

    except Exception as e:
        # log the exception
        logger.error(f"An error occured: {e}")
        # Raise HTTP exception with status code 500 and detailed message
        raise HTTPException(status_code=500, detail="An error occured")


### ben denedim bu haliyle run edince bu hatayi alamadim
# adam i am just gonna refresh the page where it resides deyip sonra aliyodu hatayi
# bende olmadi
# ben anca gidip elimle /test endpoint i yazarsam bu hatayi almayi basardim

#neyse bunu basarinca dev.logda da hatayi kayitli gorebiliyoz
# """
