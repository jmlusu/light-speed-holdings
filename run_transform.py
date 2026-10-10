from ai_company.registry.public_transform import transform_public_registry

result = transform_public_registry()
print(f"Generated public registry: {result['meta']}")
