import json
from openai import AsyncOpenAI

from database.models import Product
from env import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

ai_setup = {
    "role": "system",
    "content": """Your job is to help customers find the most cost effective methods 
                for installing renewable energy on their home or business.""",
}


class RenewableAI:
    thread = None
    messages = list()

    async def create(self):
        self.thread = await client.chat.conversations.create()
        return self

    async def get_estimates(
        self,
        solar_panel_area: float,
        solar_product: Product,
        solar_radiation: float,
        wind_product: Product,
        wind_speed_average: float,
        wind_turbine_count: int,
    ):
        example_response = {
            "role": "assistant",
            "content": json.dumps(
                {
                    "power_out": {
                        "solar": 800,
                        "wind": 200,
                        "total": 1000,
                    },
                    "units": "kWh",
                }
            ),
        }

        user_prompt_solar = {
            "role": "user",
            "content": f"""Given an area of {solar_panel_area} square meters, with an average solar radiation of 
                        {solar_radiation}, and solar panels with a maxefficiency rating of {solar_product.efficiency_max}%,
                        estimate the power out in a json format.""",
        }

        user_prompt_wind = {
            "role": "user",
            "content": f"""Given {wind_turbine_count} wind turbines with an average wind speed of {wind_speed_average},
                        and wind turbines with a max efficiency rating of {wind_product.efficiency_max}%,
                        estimate the power out in a json format.""",
        }

        messages = [ai_setup, example_response, user_prompt_solar, user_prompt_wind]

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=messages,
        )

        return response.choices[0].message.content

    async def get_incentives(self, location: str, categories: list[str] = []):
        example_content = {}
        for category in categories:
            item: str
            action: str
            audience: str
            if category == "solar":
                item = "solar panel"
                action = "installation"
                audience = "homeowners"
            elif category == "wind":
                item = "wind turbine"
                action = "installation"
                audience = "homeowners"
            elif category == "geothermal":
                item = "geothermal"
                action = "installation"
                audience = "homeowners"
            elif category == "electric vehicles":
                item = "electric vehicle"
                action = "purchase"
                audience = "individuals"
            elif category == "energy efficiency":
                item = "energy efficiency"
                action = "upgrade"
                audience = "individuals"

            example_core = {
                "id": "dkd21SSa22sd2dia9dkasmda",
                "description": f"The federal government offers a $1,000 rebate for {item} {action}s.",
                "eligibility": f"{audience.capitalize()} who purchase {item}s for their themselves",
                "requirements": "It must be completed prior to August 2024",
                "source": "https://www.energysage.com/solar/cost-benefit/solar-incentives-and-rebates/",
            }

            federal = {**example_core, "name": f"Federal {category} incentive"}
            state = {**example_core, "name": f"State {category} incentive"}
            other = {**example_core, "name": f"Other {category} incentive"}

            example_content[category] = [federal, state, other]

        example_json = {
            "role": "assistant",
            "content": json.dumps(example_content),
        }

        messages = [
            ai_setup,
            example_json,
        ]

        messages.append(
            {
                "role": "user",
                "content": f"""Give me any state, federal, or other rebates/incentives that are available
                                now, during the year 2024, for the following categories: {"".join(categories)}. 
                                The results should be relavent for individuals or businesses located near 
                                {location} in a json format""",
            }
        )

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=messages,
        )
        # return """{
        #             "wind": [
        #                     {
        #                         "id": "dkd21SSa22sd2dia9dkasmda",
        #                         "name": "Federal Solar Tax Credit",
        #                         "description": "The federal government offers a $1,000 rebate for certified installations.",
        #                         "eligibility": "Homeowners who purchase solar panels for their primary residence",
        #                         "requirements": "The system must be installed by December 31, 2022",
        #                         "source": "https://www.energysage.com/solar/cost-benefit/solar-incentives-and-rebates/"
        #                     },
        #                     {
        #                         "id": "d2daScAD2DAsdsadS2",
        #                         "name": "State tax credit",
        #                         "description": "The state government offers a $2,000 rebate for certified installations.",
        #                         "eligibility": "Homeowners who purchase solar panels for their primary residence",
        #                         "requirements": "The system must be installed by December 31, 2024",
        #                         "source": "https://www.energysage.com/solar/cost-benefit/solar-incentives-and-rebates/"
        #                     }
        #                 ],
        #             "solar": [
        #                     {
        #                         "id": "dkd21SSa22sd2dia9dkasmda",
        #                         "name": "Federal Solar Tax Credit",
        #                         "description": "The federal government offers a $1,000 rebate for certified installations.",
        #                         "eligibility": "Homeowners who purchase solar panels for their primary residence",
        #                         "requirements": "The system must be installed by December 31, 2022",
        #                         "source": "https://www.energysage.com/solar/cost-benefit/solar-incentives-and-rebates/"
        #                     },
        #                     {
        #                         "id": "d2daScAD2DAsdsadS2",
        #                         "name": "State tax credit",
        #                         "description": "The state government offers a $2,000 rebate for certified installations.",
        #                         "eligibility": "Homeowners who purchase solar panels for their primary residence",
        #                         "requirements": "The system must be installed by December 31, 2024",
        #                         "source": "https://www.energysage.com/solar/cost-benefit/solar-incentives-and-rebates/"
        #                     }
        #                 ],
        #                 "electric vehicles": []
        #             }"""
        return response.choices[0].message.content
