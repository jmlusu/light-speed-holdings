from ai_company.registry import load_registry
reg = load_registry()
print("Company dir:", [k for k in dir(reg.company) if not k.startswith("_")])
print("Company executives:", len(reg.company.executives) if hasattr(reg.company, 'executives') else 'N/A')
print("Company specialists:", len(reg.company.specialists) if hasattr(reg.company, 'specialists') else 'N/A')
if hasattr(reg.company, 'executives'):
    print("Executive names:", [e.name for e in reg.company.executives])
if hasattr(reg.company, 'specialists'):
    print("Specialist names:", [s.name for s in reg.company.specialists])