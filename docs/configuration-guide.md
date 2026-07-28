# Configuration Guide

Aurora uses explicit configuration files so behavior can be adjusted without changing the source code.

## Principles

- Keep defaults explicit.
- Group settings by feature.
- Use descriptive, consistent names.
- Prefer safe defaults for optional values.

## Example

```json
{
  "features": {
    "panel": {
      "enabled": true,
      "position": "top"
    }
  }
}
```

## Expectations

- Invalid values should fail clearly.
- Missing optional values should fall back to defaults.
- User-visible configuration changes should be documented.
