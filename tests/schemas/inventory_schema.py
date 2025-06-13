INVENTORY_SCHEMA = {
  "type": "object",
  "properties": {
    "approved": { "type": "integer" },
    "placed": { "type": "integer" },
    "delivered": { "type": "integer" }
  },
  "required": ["approved", "placed", "delivered"]
}