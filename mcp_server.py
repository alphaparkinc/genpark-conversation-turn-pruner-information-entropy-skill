"""
MCP Server for genpark-conversation-turn-pruner-information-entropy-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import TurnInformationEntropyPrunerClient

pruner = TurnInformationEntropyPrunerClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "prune_noise_turns",
                        "description": "Strip low-entropy pleasantries from multi-turn dialog context.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "turns": {"type": "array", "items": {"type": "object"}}
                            },
                            "required": ["turns"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "prune_noise_turns":
            res = pruner.prune_conversation(args["turns"])
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(res)}]
                }
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
