"""
┌──────────────────────────────────────────────────────────────────────────────┐
│ @author: Davidson Gomes                                                      │
│ @file: custom_tools.py                                                       │
│ Developed by: Davidson Gomes                                                 │
│ Creation date: May 13, 2025                                                  │
│ Contact: contato@evolution-api.com                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ @copyright © Evolution API 2025. All rights reserved.                        │
│ Licensed under the Apache License, Version 2.0                               │
│                                                                              │
│ You may not use this file except in compliance with the License.             │
│ You may obtain a copy of the License at                                      │
│                                                                              │
│    http://www.apache.org/licenses/LICENSE-2.0                                │
│                                                                              │
│ Unless required by applicable law or agreed to in writing, software          │
│ distributed under the License is distributed on an "AS IS" BASIS,            │
│ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.     │
│ See the License for the specific language governing permissions and          │
│ limitations under the License.                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ @important                                                                   │
│ For any future changes to the code in this file, it is recommended to        │
│ include, together with the modification, the information of the developer    │
│ who changed it and the date of modification.                                 │
└──────────────────────────────────────────────────────────────────────────────┘
"""

from typing import Any, Dict, List
from google.adk.tools import FunctionTool
import requests
import json
import urllib.parse
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CustomToolBuilder:
    def __init__(self):
        self.tools = []

    def _create_http_tool(self, tool_config: Dict[str, Any]) -> FunctionTool:
        """Create an HTTP tool based on the provided configuration."""
        name = tool_config["name"]
        description = tool_config["description"]
        endpoint = tool_config["endpoint"]
        method = tool_config["method"]
        headers = tool_config.get("headers", {})
        parameters = tool_config.get("parameters", {}) or {}
        values = tool_config.get("values", {})
        error_handling = tool_config.get("error_handling", {})

        path_params = parameters.get("path_params") or {}
        query_params = parameters.get("query_params") or {}
        body_params = parameters.get("body_params") or {}

        def http_tool(**kwargs):
            try:
                # Combines default values with provided values
                all_values = {**values, **kwargs}

                # Substitutes placeholders in headers
                processed_headers = {
                    k: v.format(**all_values) if isinstance(v, str) else v
                    for k, v in headers.items()
                }

                # Processes path parameters
                url = endpoint
                for param, value in path_params.items():
                    if param in all_values:
                        # URL encode the value for URL safe characters
                        replacement_value = urllib.parse.quote(str(all_values[param]), safe='')
                        url = url.replace(f"{{{param}}}", replacement_value)

                # Process query parameters
                query_params_dict = {}
                for param, value in query_params.items():
                    if isinstance(value, list):
                        # If the value is a list, join with comma
                        query_params_dict[param] = ",".join(value)
                    elif param in all_values:
                        # If the parameter is in the values, use the provided value
                        query_params_dict[param] = all_values[param]
                    else:
                        # Otherwise, use the default value from the configuration
                        query_params_dict[param] = value

                # Adds default values to query params if they are not present
                for param, value in values.items():
                    if param not in query_params_dict and param not in path_params:
                        query_params_dict[param] = value

                body_data = {}
                for param, param_config in body_params.items():
                    if param in all_values:
                        body_data[param] = all_values[param]

                # Adds default values to body if they are not present
                for param, value in values.items():
                    if (
                        param not in body_data
                        and param not in query_params_dict
                        and param not in path_params
                    ):
                        body_data[param] = value

                # Makes the HTTP request
                response = requests.request(
                    method=method,
                    url=url,
                    headers=processed_headers,
                    params=query_params_dict,
                    json=body_data if body_data else None,
                    timeout=error_handling.get("timeout", 30),
                )

                if response.status_code >= 400:
                    raise requests.exceptions.HTTPError(
                        f"Error in the request: {response.status_code} - {response.text}"
                    )

                # Try to parse the response as JSON, if it fails, return the text content
                try:
                    return json.dumps(response.json())
                except ValueError:
                    # Response is not JSON, return the text content
                    return json.dumps({"content": response.text})

            except Exception as e:
                logger.error(f"Error executing tool {name}: {str(e)}")
                return json.dumps(
                    error_handling.get(
                        "fallback_response",
                        {"error": "tool_execution_error", "message": str(e)},
                    )
                )

        # Adds dynamic docstring based on the configuration
        param_docs = []

        # Adds path parameters
        for param, value in path_params.items():
            param_docs.append(f"{param}: {value}")

        # Adds query parameters
        for param, value in query_params.items():
            if isinstance(value, list):
                param_docs.append(f"{param}: List[{', '.join(value)}]")
            else:
                param_docs.append(f"{param}: {value}")

        # Adds body parameters
        for param, param_config in body_params.items():
            required = "Required" if param_config.get("required", False) else "Optional"
            param_docs.append(
                f"{param} ({param_config['type']}, {required}): {param_config['description']}"
            )

        # Adds default values
        if values:
            param_docs.append("\nDefault values:")
            for param, value in values.items():
                param_docs.append(f"{param}: {value}")

        http_tool.__doc__ = f"""
        {description}

        Parameters:
        {chr(10).join(param_docs)}

        Returns:
        String containing the response in JSON format
        """

        # Defines the function name to be used by the ADK
        http_tool.__name__ = name

        return FunctionTool(func=http_tool)

    def build_tools(self, tools_config: Dict[str, Any]) -> List[FunctionTool]:
        """Builds a list of tools based on the provided configuration. Accepts both 'tools' and 'custom_tools' (with http_tools)."""
        self.tools = []

        http_tools = []
        if tools_config.get("http_tools"):
            http_tools = tools_config.get("http_tools", [])
        elif tools_config.get("custom_tools") and tools_config["custom_tools"].get(
            "http_tools"
        ):
            http_tools = tools_config["custom_tools"].get("http_tools", [])
        elif (
            tools_config.get("tools")
            and isinstance(tools_config["tools"], dict)
            and tools_config["tools"].get("http_tools")
        ):
            http_tools = tools_config["tools"].get("http_tools", [])

        for http_tool_config in http_tools:
            self.tools.append(self._create_http_tool(http_tool_config))

        return self.tools
