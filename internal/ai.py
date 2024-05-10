import json
import uuid
from openai import AsyncOpenAI

from database.enums import IncentiveType
from database.models import Incentive, Product
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

    async def get_incentives(self, location: str, incentives: list[Incentive] = []):
        example_content = {}
        print(incentives[0].type)
        for incentive in incentives:
            action: str = ""
            audience: str = ""
            if incentive.type == IncentiveType.solar.name:
                action = "installation"
                audience = "homeowners"
            elif incentive.type == IncentiveType.wind.name:
                action = "installation"
                audience = "homeowners"
            elif incentive.type == IncentiveType.geothermal.name:
                action = "installation"
                audience = "homeowners"
            elif incentive.type == IncentiveType.ev.name:
                action = "purchase"
                audience = "individuals"
            elif incentive.type == IncentiveType.home.name:
                action = "upgrade"
                audience = "individuals"
            elif incentive.type == IncentiveType.water.name:
                action = "installation"
                audience = "individuals"

            example_core = {
                "description": f"The federal government offers a $1,000 rebate for {incentive.display_name} {action}s.",
                "eligibility": f"{audience.capitalize()} who purchase {incentive.display_name}s for their themselves",
                "requirements": "It must be completed prior to August 2024",
                "source": "https://www.energysage.com/solar/cost-benefit/solar-incentives-and-rebates/",
            }

            federal = {
                **example_core,
                "id": str(uuid.uuid4()),
                "name": f"Federal {incentive.display_name} incentive",
            }
            state = {
                **example_core,
                "id": str(uuid.uuid4()),
                "name": f"State {incentive.display_name} incentive",
            }
            other = {
                **example_core,
                "id": str(uuid.uuid4()),
                "name": f"Other {incentive.display_name} incentive",
            }

            example_content[incentive.type] = [federal, state, other]

        example_json = {
            "role": "assistant",
            "content": json.dumps(example_content),
        }

        incentive_names = [incentive.display_name for incentive in incentives]

        prompt = {
            "role": "user",
            "content": f"""Give me any state, federal, or other rebates/incentives that are available
                                now, during the year 2024, for the following categories: {" ".join(incentive_names)}. 
                                The results should be relavent for individuals or businesses located near 
                                {location} in a json format""",
        }

        messages = [ai_setup, example_json, prompt]

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=messages,
        )

        return response.choices[0].message.content
