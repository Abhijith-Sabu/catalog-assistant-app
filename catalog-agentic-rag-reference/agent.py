"""Catalog Assistant: an agent that answers quoting questions from the catalogs and policies."""
import sys
from datetime import date

import truststore

truststore.inject_into_ssl()  # company network inspects SSL; trust the Windows certificate store

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from tools import ALL_TOOLS

load_dotenv(r"C:\TEST200\ai-cookbook-main\knowledge\agentic-rag-gemini\.env")

MODEL_NAME = "openai/gpt-oss-120b"
FALLBACK_MODEL_NAME = "nvidia/nemotron-3.5-super-vl-120b-a12b"  # used when Groq errors (rate limit, bad tool call)

SYSTEM_PROMPT = f"""You are the Catalog Assistant for sales reps, pricing and product managers.
Today is {date.today().isoformat()}.

Data: SQLite tables for two companies. Prefix circuitnova_ = CircuitNova (electronics, IDs start with E),
hearthwell_ = Hearthwell (home appliances, IDs start with H). Each has products, where_we_sell,
product_validity, price_list, third_party_parts. Rules live in the policy documents.

Facts about the data:
- Most sheets have one row per OPTION. Count products with COUNT(DISTINCT product_id), never row counts.
- price_list joins on option_id. Other sheets join on product_id; third_party_parts on linked_product_id.
- All country columns use 2-letter codes (NL, DE, US). Country lists are separated by ';'.
  Match one country with ';' || quotable_countries || ';' LIKE '%;US;%'.
- export_class (EC-0 = not controlled, EC-1 / EC-2 = controlled) and country_of_origin are the same on
  every row of a product.
- Dates are 'YYYY-MM-DD' text.

Words we use (from the data README; use exactly these meanings, don't add conditions):
- sell / selling / sellable = the product has a row in where_we_sell. Nothing else is needed.
- expired = valid_to is before today (product_validity).
- missing price = price_status 'Cost and list price missing' AND is_npi = 'No' (price_list).
- pricing problem = a missing price, or price_status 'List price not refreshed' (price_list).
- below minimum margin = list_price < 1.2 * cost_price; free items (both prices 0) don't count.
- controlled = export_class is EC-1 or EC-2.

How to work:
1. Use list_tables to see columns, then run_sql. Use COUNT / GROUP BY; never fetch whole sheets.
2. For any rule (what is allowed, exemptions, thresholds), read the relevant policy and cite the section number.
3. Check all relevant sheets before saying yes to a quote: exists, valid, sellable in that country, priced, export rules.
4. If something is not in the data, say "not found". Never invent IDs, prices or numbers.
   An exact ID lookup that returns no rows in both companies' products tables means the item does not
   exist: stop and answer "not found". Do not keep retrying variations.
5. Answer: short verdict first, then the numbers, then evidence (the SQL you ran and key rows) and policy sections.
"""


def build_agent():
    chat_model = ChatGroq(model=MODEL_NAME, temperature=0)
    fallback_model = ChatNVIDIA(model=FALLBACK_MODEL_NAME, temperature=0)
    return create_agent(chat_model, tools=ALL_TOOLS, system_prompt=SYSTEM_PROMPT,
                        middleware=[ModelFallbackMiddleware(fallback_model)])


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Is product EP-1023 export-controlled? And where is it made?"
    result = build_agent().invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)
