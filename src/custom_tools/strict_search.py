from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

import os


class SearchInput(BaseModel):
    search_query: str = Field(description="The search query to be used for the search.")
    doc_text: str = Field(description="The text to be searched.")


class StrictSearchTool(BaseTool):
    name: str = "Strict Search"
    description: str = "Performs a strict search using the provided search query."
    args_schema: Type[BaseModel] = SearchInput
    return_direct: bool = True
    handle_tool_error: bool = True

    def _run(
            self,
            search_query: str,
            doc_text: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Run the function"""


    def split_query(self, search_query: str) -> list:
        """Split the search query"""
        return [split for split in search_query.split(" ")]
    

    def find_sentence(self, term: str, doc_text: str) -> list:
        """Find sentences where the term is present"""
        return [sentence for sentence in doc_text.split(".") if term in sentence]





if __name__ == "__main__":
    search_query = "AI ethics that enable inovation"
    text_path = os.path.join(os.path.dirname(__file__), "example.txt")
    print(text_path)
    with open(text_path, "r") as f:
        doc_text = f.read()


    search_tool = StrictSearchTool() 
    res = search_tool.split_query(search_query)
    print(res)
    term = res[0]
    match = search_tool.find_sentence(term, doc_text)
    print(match)